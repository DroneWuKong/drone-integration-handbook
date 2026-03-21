# Sensor Payload Integration

Hanging a sensor off your drone is not plug-and-play. The mechanical interface, the electrical interface, the firmware configuration, and the data pipeline are four separate problems that all interact. Get any one wrong and you either damage the aircraft (CG shift causing attitude instability), damage the payload (vibration destroying a LiDAR scan), or just get useless data (GPS-triggered shutter not synced to IMU). This guide covers all four.

---

## Mechanical Integration

### Center of Gravity

Every payload changes your center of gravity. The flight controller compensates for CG offsets automatically — but only up to a point, and with a cost.

**What CG offset costs:**
A 200g LiDAR mounted 80mm forward of the CG forces the rear motors to work harder than the front motors to maintain level flight. The FC compensates via differential throttle, but that asymmetric loading means:
- Lower effective thrust margin (the rear motors are near their limit before the front motors are)
- Higher average current draw (compensating for the imbalance)
- Asymmetric PID response (the aircraft responds differently to forward vs rearward pitch corrections)
- Shortened flight time

**Rule of thumb:** Keep the payload CG within ±15% of the frame's geometric center in both fore-aft and lateral axes. Beyond that, consider ballast or repositioning the battery to compensate.

**Measuring CG shift:** Balance the complete flying system (with payload, without battery) on a fulcrum under the motor mounting pattern center. Note the direction of lean. Move the battery to counter it, or add ballast as a last resort.

### Vibration Isolation

This is the most commonly skipped and most consequential step. Two separate isolation problems exist on any camera/sensor drone:

**Problem 1: FC gyroscope noise from propulsion**
The flight controller's IMU is sensitive to vibration from motors, propellers, and frame flex. Motor and prop imbalance generates vibration at the motor electrical frequency (motor RPM / pole pairs), which couples into the gyro as high-frequency noise. This is the primary driver of PID tuning difficulty on poorly-built platforms.

Fix: Soft-mount the FC stack on rubber or silicone standoffs. Most modern FC stacks include mounting holes for M3 anti-vibration standoffs. This has nothing to do with the payload.

**Problem 2: Payload sensor noise from the same propulsion**
A camera or LiDAR mounted rigidly to the frame receives the same propulsion vibration as the frame. For cameras, this causes rolling shutter artifacts and blurry frames. For LiDAR, it introduces scan line discontinuities. For IMU-based payloads (survey-grade GNSS/INS), it overwhelms the sensor.

Fix: Isolate the payload from the frame with a vibration-damping mount. Options:
- **Foam/silicone tape:** Cheap, effective for light cameras under 200g. Adds 2–5mm compliance.
- **Rubber ball mounts:** Standardized vibration isolators (M3 or M5, various Shore hardness). Match Shore hardness to payload weight — too soft causes pendulum oscillation, too hard transmits vibration.
- **Gimbal:** Active stabilization for cameras. Gyro-stabilized gimbals eliminate both vibration noise and attitude coupling simultaneously for camera payloads.

**Don't double-isolate.** If the payload has its own vibration isolation, don't also soft-mount the payload bracket. The compliance of two soft mounts in series creates a resonant system that can amplify certain frequencies rather than damping them.

### Payload Weight and Arm Loading

On a quadrotor, payload weight is distributed across all four motors equally if mounted at the CG, and unequally if not. Check your motor's rated continuous thrust against the hover throttle with payload loaded — you want to be at 50–60% throttle in hover with the heaviest expected payload.

For hexarotors and octorotors carrying heavy payloads: calculate the per-motor load and verify you have enough margin for maneuver and wind correction on the highest-loaded motor, not just the average.

---

## Electrical Integration

### Power Budgeting for Payloads

Before wiring anything, add up the power draw of every peripheral. The payload power draw is in addition to the propulsion system — it directly reduces flight time.

| Payload | Typical Power Draw |
|---|---|
| FPV camera (analog) | 0.5–1W |
| Action camera (GoPro class) | 3–7W |
| Thermal camera (FLIR Boson) | 2–4W |
| 1080p USB camera | 1–3W |
| Raspberry Pi Zero 2W | 1–2W |
| Raspberry Pi 4 | 3–8W |
| NVIDIA Jetson Nano | 5–10W |
| NVIDIA Jetson Orin NX | 10–25W |
| LiDAR (RPLIDAR A3) | 3–5W |
| LiDAR (Ouster OS1) | 15–20W |
| RTK GNSS module | 0.5–2W |

**Derive flight time impact:**
```
Extra flight time consumed (min) = payload_watts / battery_voltage / hover_current_A × 60
```
A 10W payload on a 6S (22.2V) battery draws ~0.45A additionally. If the platform hovers at 12A without payload, 10W of payload costs about 3–4% more current — roughly 1–2 minutes on a 30-minute platform.

### Payload Power Sources

Never power a high-current payload directly from the FC's 5V pin. The FC's onboard regulator is typically rated 500mA–1A — enough for receiver and GPS, not for a companion computer or gimbal.

**Correct payload power architectures:**

For small payloads (<500mA at 5V): FC 5V output is fine.

For medium payloads (0.5–3A at 5V or 12V):
```
Battery → Dedicated BEC (3A–5A rated) → Payload
FC GND ─────────────────────────────→ Payload GND (shared)
```

For large payloads (>3A or custom voltage):
```
Battery → Power module or PDB → Payload power regulator → Payload
```
Payloads like the Ouster OS1 run at 24V and draw ~800mA — they need a boost/buck converter, not a BEC.

### Isolation and Noise

Camera payloads are high-frequency noise generators (USB 3.0 operates at 5GHz, HDMI at similar frequencies). These can affect GPS L1 (1.575GHz) if the payload is physically close to the GPS antenna.

**Rules:**
- Keep companion computer USB 3.0 ports and cables away from GPS antenna — minimum 15cm
- If using USB 3.0 to USB-C camera, use a cable with a ferrite clip
- Power the payload from a dedicated BEC with its own filter capacitor, not shared with the FC rail

---

## Firmware Integration: MAVLink Camera Protocol

ArduPilot and PX4 both support the MAVLink Camera Protocol (MAVLink v2), which defines a standard interface between the autopilot and camera/payload systems.

### What the Camera Protocol Provides

- **Shutter trigger via MAVLink:** The FC triggers the camera shutter synchronized to GPS time. Critical for photogrammetry — without GPS-synced triggers, your ground sampling distance calculations are based on estimated position, not actual.
- **Geotag injection:** ArduPilot can log shutter events with GPS position, allowing post-flight geotagging without a separate logger.
- **Camera status feedback:** Camera can report capture count, storage remaining, and error status back to GCS.
- **Video control:** Start/stop recording, zoom, change mode.

### Wiring a MAVLink Camera

The camera needs a MAVLink serial connection. For companion computers running the camera:

**Option A: Companion computer as camera manager**
```
FC UART (MAVLink2) ─── Companion computer (USB serial or GPIO UART)
Companion computer ─── Camera (USB, CSI, or Ethernet)
```
The companion computer runs camera control software (MAVProxy, MAVSDK, or custom) and translates MAVLink camera commands to the camera's native API.

**Option B: Direct MAVLink camera**
Some cameras (Sony a6xxx via Sony SDK, some GoPro Mods) support MAVLink directly. Wire UART TX/RX and configure the FC camera port.

ArduPilot configuration:
```
CAM1_TYPE = 1 (Servo)  or  3 (Relay)  or  4 (MAVLink)
CAM1_TRIGG_TYPE = 0 (distance) or 1 (time)
CAM1_TRIGG_DIST = 5  (meters between shots)
```

For MAVLink camera (TYPE=4), set the camera's MAVLink component ID and the serial port. The FC will send `MAV_CMD_IMAGE_START_CAPTURE` on trigger.

### Gimbal Control

Gimbals receive control commands via:

| Interface | Use Case | Notes |
|---|---|---|
| PWM (Servo) | Simple 1–3 axis, basic tilt control | Universally supported, low resolution |
| SBus | Multi-axis, smoother control | Single wire, widely supported |
| MAVLink (serial) | Full camera integration, stabilization telemetry back | Best for survey, requires compatible gimbal |
| CAN | Industrial gimbals (Gremsy, Zenmuse) | High reliability, hot-swap capable |

For ArduPilot:
```
MNT1_TYPE = 1 (Servo) or 4 (SToRM32 MAVLink) or 8 (Gremsy)
MNT1_ROLL_MIN / MNT1_ROLL_MAX
MNT1_TILT_MIN / MNT1_TILT_MAX
```

**Gimbal stabilization modes:**
- **RC passthrough:** Gimbal follows stick input directly. Use for FPV, not survey.
- **Stabilize mode:** Gimbal corrects for aircraft attitude, points where commanded. Standard for camera work.
- **GPS point-of-interest:** Gimbal tracks a GPS coordinate. Useful for inspection, requires ArduPilot 4.3+.

---

## LiDAR Integration

LiDAR payloads add complexity beyond cameras: they generate large data streams, require precise time synchronization, and need PPS (pulse-per-second) signals from the GNSS for accurate scan timing.

### The Time Sync Problem

A LiDAR spinning at 10–20Hz captures thousands of points per second. Each point must be timestamped to microsecond accuracy to fuse correctly with the INS position. Without accurate time sync, your point cloud will have "smear" artifacts proportional to platform velocity × time error.

**Required hardware:**
- GNSS receiver with PPS output (1Hz pulse, accurate to <1µs)
- PPS wired to both the LiDAR and the INS/GNSS module
- All devices sharing a common time base from GPS

Most mapping-grade LiDARs (Ouster, Velodyne, RIEGL) have PPS inputs. Consumer LiDARs (RPLIDAR, Livox Mid-360) have varying time sync quality — check the datasheet.

### Data Pipeline

LiDAR → Ethernet or USB → Companion computer → storage or real-time streaming

Most mapping workflows record raw LiDAR data plus IMU/GNSS data separately and post-process them (Inertial Explorer, Pix4D Matic, or open-source tools like LOAM/LeGO-LOAM).

Real-time SLAM (Simultaneous Localization and Mapping) is also possible — KISS-ICP, LIO-SAM, and Fast-LIO run on a Jetson Orin or similar at map-update rates of 10Hz. This enables obstacle avoidance and GPS-denied navigation rather than just post-flight mapping.

### Weight and Power Budget Example: RESEPI Ultra LITE

The RESEPI Ultra LITE (from Inertial Labs) is a representative small mapping payload:
- Weight: 380g
- Power: 30W (12–24V input)
- Interface: Ethernet + USB
- Data rate: ~100MB/min of LiDAR + imagery
- Requires: external GNSS antenna for INS, PPS from GNSS

On a 6S platform with 5,000mAh battery: the RESEPI draws ~1.35A at 22.2V. At 20A hover current, this is a 6.7% load increase — roughly 2–3 minutes flight time reduction.

---

## Thermal Camera Integration

Thermal cameras are simpler electrically than LiDAR but have their own quirks.

### Radiometric vs Non-Radiometric

- **Non-radiometric (NTSC/PAL video output):** Cheap, works as a standard analog FPV camera. Gives a thermal image but no temperature data. Connect to video input on FC or VTX.
- **Radiometric:** Each pixel carries temperature data. Requires digital interface (USB, CSI, Ethernet). Enables temperature measurement and alarm triggering. Required for industrial inspection.

### FLIR Boson / Lepton Integration

The FLIR Boson connects via UART (command) + either analog video or USB (image data). For analog FPV:
```
Boson analog out → VTX video input (same as any FPV camera)
Boson UART → FC UART (for camera control: shutter, gain, FFC)
```

For full radiometric data:
```
Boson USB → Companion computer (USB 2.0)
```
The FLIR SDK runs on the companion computer and handles data capture, temperature extraction, and trigger coordination with the autopilot.

### Sensor Fusion: Thermal + RGB

Most professional thermal payloads are paired with an RGB camera for context. The key challenge: the two sensors must be precisely co-registered spatially. This requires:
- Boresight calibration (measuring the angular offset between the two lenses)
- Time synchronization (both cameras triggered at the same moment)
- Lens distortion maps for both sensors

Skydio, Autel, and Parrot all ship dual-sensor payloads with factory boresight calibration. DIY thermal+RGB rigs require field calibration with a calibration target.

---

## Companion Computer Integration

The companion computer is the hub for payload data processing, MAVLink camera management, and any AI inference running onboard.

### FC to Companion Computer Interface

```
FC UART (MAVLink2) ─── Companion computer USB serial adapter or GPIO UART
FC 5V (small CC only) ─── or ─── Dedicated BEC → CC 5V input
```

ArduPilot configuration:
```
SERIAL2_PROTOCOL = 2 (MAVLink2)
SERIAL2_BAUD = 921600 (for Jetson/RPi)
```

### MAVSDK vs MAVProxy vs ROS2

| Framework | Best For | Weight | Notes |
|---|---|---|---|
| MAVSDK | Simple payload control, guided mode | Light | Python/C++ API, limited telemetry access |
| MAVProxy | GCS forwarding, scripting, full telemetry | Medium | Shell-based, good for scripted missions |
| ROS2 + MAVROS2 | Sensor fusion, SLAM, AI integration | Heavy | Full robotics stack, requires Jetson class hardware |
| DroneKit | Legacy Python API | Medium | Deprecated but widely used |

For a Raspberry Pi controlling a gimbal and triggering a camera: MAVSDK or MAVProxy.
For a Jetson running LiDAR-SLAM and real-time obstacle avoidance: ROS2 + MAVROS2.
