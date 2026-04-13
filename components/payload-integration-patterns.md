# Payload Integration Patterns

> The companion computer is the integration hub. Everything else —
> cameras, LiDAR, multispectral, droppers — connects through it or
> through the FC's peripheral ports.

---

## Integration Topology

```
FC (Pixhawk/H743)
  ├── UART 1: RC receiver (ELRS/CRSF)
  ├── UART 2: GPS + compass
  ├── UART 3: Telemetry (MAVLink to GCS)
  ├── UART 4: Companion computer (MAVLink)
  ├── I2C:    Airspeed, optical flow, external compass
  ├── CAN:    GPS (DroneCAN), ESCs (Zubax/Vertiq)
  └── GPIO/PWM: Servo outputs → gimbal, dropper, parachute

Companion Computer (RPi CM4 / Jetson Orin / SkyNode)
  ├── USB:    FC (MAVLink), cameras, LiDAR
  ├── CSI:    High-speed camera (RPi camera v3, IMX477)
  ├── MIPI:   Sony IMX585 (via adapter)
  ├── Ethernet: Zenmuse (via DJI SDK), mapping cameras
  ├── UART:   Secondary FC comms, GNSS RTK
  └── GPIO:   Trigger signals, payload power control
```

---

## Camera Payloads

### Visible Light / RGB

**Mapping cameras** (Sony ILX-LR1, Phase One iXM, Micasense Altum):
- Connect via USB 3.0 or Ethernet to companion
- Trigger via GPIO or MAVLink `DO_DIGICAM_CONTROL`
- Geotag via MAVLink position injection into EXIF or sidecar files
- High data rate — plan 128GB+ per flight for full-res mapping

**FPV/ISR cameras:**
- Analog: direct to VTX, no companion needed
- Digital (DJI O3/O4, HDZero): dedicated link, not companion-routed
- Gimbal cameras: HDMI/SDI to encoder, H.264 stream to companion

### Thermal

**FLIR Boson/Lepton, Teledyne Tau:**
- USB or CSI interface to companion
- FLIR SDK for streaming and radiometric data
- Radiometric TIFF capture requires SDK license on some models
- Sync RGB+thermal via GPIO trigger for data fusion

**Seek Thermal, FLIR Hadron (RGB+thermal combo):**
- Single USB connection, dual stream
- Growing standard for DFR — one sensor, two data streams

### Multispectral

**Micasense RedEdge-P / Altum-PT, Sentera 6X:**
- USB or Ethernet
- Require calibration panel image at takeoff and landing
- Trigger via MAVLink `DO_DIGICAM_CONTROL` or standalone timer
- Output: per-band TIFFs, combine in Agisoft Metashape or Pix4D

---

## LiDAR Payloads

### Mapping LiDAR (Velodyne, Ouster, RESEPI)

High-bandwidth, typically Ethernet. Requires companion.

```
LiDAR → Ethernet → Companion → point cloud recording
                             → real-time obstacle avoidance
                             → SLAM (Cartographer, LIO-SAM)
```

Key integration concern: **time synchronization**. LiDAR timestamps
must align with IMU timestamps for accurate point cloud georeferencing.
Use PPS (pulse per second) from GPS for sub-microsecond sync.

### Rangefinder LiDAR (LightWare SF000, Benewake TF-Luna)

Single-point distance sensors for altitude hold and terrain following.
Connect directly to FC via UART or I2C — no companion needed.

ArduCopter config:
```
RNGFND1_TYPE = 8 (LightWare serial)
RNGFND1_PORT = UART2
RNGFND1_MAX_CM = 4000
RNGFND1_MIN_CM = 10
TERRAIN_ENABLE = 1  (if using terrain following)
```

---

## Delivery & Dropper Payloads

### Servo-Based Droppers

Simplest integration — standard servo output from FC.

```
ArduCopter:
SERVO8_FUNCTION = 28  (Gripper)
SERVO8_MIN = 1000     (closed)
SERVO8_MAX = 2000     (open)
GRIP_ENABLE = 1

Command: MAV_CMD_DO_GRIPPER (211)
  param1 = 1 (instance)
  param2 = 0 (release) or 1 (grab)
```

### Magnet Droppers

Electromagnet on servo output or direct GPIO.
Wire through a MOSFET if magnet draws >500mA (most do).
Cut power = release payload. Simpler and more reliable than servo mechanisms.

### Winch Systems

More complex — typically requires dedicated controller.
Interface via UART to FC (custom MAVLink messages) or
via companion computer with direct motor control.

---

## Gimbal Integration

### Pixhawk Gimbal Protocol

Standard two-axis brushless gimbal (Gremsy, Siyi, Viewpro):

```
FC UART → SBus/PWM → gimbal
or
FC UART → MAVLink (GIMBAL_DEVICE_ATTITUDE_STATUS)
```

Config:
```
MNT1_TYPE = 2 (SBus) or 4 (MAVLink)
MNT1_PITCH_MIN = -90
MNT1_PITCH_MAX = 0
MNT1_YAW_MIN = -180
MNT1_YAW_MAX = 180
```

### Targeting and ROI

```python
# MAVLink: point gimbal at GPS coordinate
DO_SET_ROI_LOCATION (195)
  lat = target_lat
  lon = target_lon
  alt = target_alt
```

---

## Power Architecture for Payloads

### Budgeting

| Payload | Typical Draw |
|---------|-------------|
| FLIR Boson 640 | 1.5W |
| Micasense Altum-PT | 6W |
| Jetson Orin NX | 10–25W |
| RPi CM4 | 5–8W |
| Velodyne VLP-16 | 8W |
| 2-axis gimbal | 5–15W |
| LTE modem | 2–5W |

Total typical ISR payload: 30–60W. Budget generously.

### Power Distribution

```
Battery → PDB
  ├── ESCs (raw voltage)
  ├── FC BEC → 5V regulated → FC, GPS, RC RX
  ├── Payload BEC → 5V or 12V → cameras, companion
  └── High-power BEC → 12V/19V → Jetson, LiDAR
```

Use **separate BECs** for payload vs FC. Payload power draw spikes
(motor startup, disk write) should not sag the FC's supply.

### Payload Power Control

Control payload power via FC relay output:
```
RELAY_PIN = 49  (AUX6 on many FCs)
RELAY_DEFAULT = 0  (off at boot)

# Turn on via MAVLink
MAV_CMD_DO_SET_RELAY (181)
  param1 = 0 (relay instance)
  param2 = 1 (on)
```

Use a MOSFET or relay module for any payload drawing >1A.

---

## Data Flow & Recording

### Onboard Recording

Record raw sensor data to companion computer SSD/NVMe.
Use ROS2 bags or a simple timestamped file logger.

Minimum recording:
- IMU data (100Hz)
- GPS position + GNSS raw (10Hz)
- Camera triggers with timestamps
- MAVLink telemetry stream

### Geofencing Data

For mapping payloads, ensure camera trigger events are logged with
GPS coordinates. Most mapping software (Pix4D, Metashape) ingests
either EXIF-embedded GPS or sidecar GeoJSON.

---

## Related

- [Companion Computer Integration](../integration/companion.md)
- [LiDAR Mapping Payloads](lidar-mapping-payloads.md)
- [Thermal Cameras](thermal-cameras.md)
- [Payload Droppers](payload-droppers.md)
- [Power Architecture & EMI](power-architecture-emi.md)
