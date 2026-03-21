# Detect-and-Avoid (DAA) Integration

Detect-and-Avoid is a prerequisite for FAA Part 108 BVLOS Permit operations and a practical necessity for any flight in shared airspace. This guide covers the hardware options, wiring, and firmware configuration for DIY DAA implementation on ArduPilot and PX4 platforms.

---

## What DAA Needs to Detect

Not all aircraft broadcast their position. The DAA problem has two different difficulty levels:

**Equipped aircraft (ADS-B Out):** Commercial airliners, most turboprops, most general aviation aircraft, and many helicopters broadcast ADS-B Out — GPS position, altitude, heading, speed, and tail number on 1090MHz. This is detectable at ranges of 20–150km depending on altitude and antenna. ADS-B In receivers solve this problem inexpensively.

**Unequipped aircraft:** Gliders, ultralights, older GA aircraft, other drones, low-flying helicopters, agricultural aircraft. No broadcast, no detection without active sensing (radar, optical, acoustic). This is the hard problem. Part 108 does not require detection of unequipped aircraft — the regulatory approach is procedural deconfliction (fly at appropriate times and places) rather than technology.

A realistic DAA system for a Group 1 UAS addresses equipped aircraft. For unequipped aircraft, awareness and operational procedures are the current state of the art.

---

## ADS-B In: Detecting Equipped Aircraft

### Hardware Options

| Receiver | Weight | Power | Interface | Price | Notes |
|---|---|---|---|---|---|
| uAvionix Ping2020i | 16g | 1.5W | UART (MAVLink) | ~$600 | Industry standard; ArduPilot native; dual band (978/1090MHz) |
| uAvionix Ping1090i | 12g | 0.8W | UART (MAVLink) | ~$400 | 1090MHz only; no UAT (978MHz) |
| mRo ACSP7 | 8g | 0.4W | UART | ~$200 | Compact; ArduPilot compatible |
| Sagetech MXS | 55g | 4W | UART/RS-232 | ~$1,500 | Full transceiver (In + Out); DO-160 qualified |
| Radionics RX-978 | 22g | 1.2W | UART | ~$300 | UAT (978MHz) only; US domestic focus |

For most DIY BVLOS platforms, the **uAvionix Ping2020i** is the standard choice — dual-band, ArduPilot native, and a well-established track record in FAA BEYOND program operations.

### ADS-B Bands

- **1090MHz (Mode S/ES):** International standard. Required for aircraft >12,500 lbs and above FL180. Nearly all commercial aviation. Global use.
- **978MHz (UAT):** US domestic only, below FL180. General aviation and hobbyists. Only detectable in the continental US.

For US domestic BVLOS: use a dual-band receiver to catch both. For international operations: 1090MHz only.

### Wiring

Connect to any free FC UART. The Ping2020i uses a standard UART interface:

```
FC UART TX → Ping RX
FC UART RX → Ping TX
FC GND     → Ping GND
5V         → Ping power (from dedicated BEC, not FC 5V pin — draws up to 300mA)
```

The receiver antenna should be mounted with clear sky view — away from carbon fiber (RF-opaque), away from power leads, and with the antenna plane horizontal for omnidirectional coverage. A 1/4-wave whip or blade antenna works; a patch or helical antenna provides better gain in one direction.

### ArduPilot Configuration

```
# Enable ADS-B
ADSB_ENABLE = 1
ADSB_TYPE = 1   # uAvionix Ping or compatible MAVLink
SERIAL3_PROTOCOL = 1  # (or whichever UART you wired to)
SERIAL3_BAUD = 57600

# Avoidance behavior
AVOID_ENABLE = 3     # Enable avoidance for proximity and fence
AVD_ENABLE = 1       # ADS-B avoidance enabled
AVD_F_ACTION = 2     # 0=None, 1=Report only, 2=Climb, 3=Move horizontally, 4=Move perpendicularly
AVD_F_WARN_TIME = 30 # Warn N seconds before threat
AVD_F_DIST_XY = 200  # Horizontal distance threshold (meters)
AVD_F_DIST_Z = 30    # Vertical distance threshold (meters)
AVD_W_ACTION = 1     # Warning-level action (report only)
```

**What happens on a threat detection:**
1. A target with projected intercept appears in the ADS-B feed
2. ArduPilot reports the threat to GCS (visible in Mission Planner's Status tab as ADSB_VEHICLE)
3. If `AVD_F_ACTION = 2` (climb), ArduPilot automatically commands a climb at a rate determined by the threat severity
4. The operator is notified via GCS HUD

**Tuning the thresholds:** The defaults are conservative — 200m horizontal and 30m vertical. In high-traffic airspace, these will generate many nuisance alerts. For low-traffic rural BVLOS, tighten to 100m/20m to reduce false positives while maintaining a meaningful safety margin.

### PX4 Configuration

PX4 uses the `px4-adsb` driver and uORB messaging:

```
adsb start
param set ADSB_ICAO_ID 1234567   # Your aircraft ICAO ID
param set ADSB_SQUAWK 1200       # VFR squawk code
param set ADSB_EMERGC 0          # No emergency
```

PX4's avoidance integration requires the companion computer running a collision avoidance algorithm (via MAVROS or PX4 external avoidance) — PX4 does not handle avoidance autonomously the way ArduPilot does. For DIY DAA without a companion computer, ArduPilot is simpler.

---

## Radar-Based Obstacle Avoidance

Radar detects non-ADS-B objects: terrain, power lines, buildings, birds, other drones. The detection range and accuracy depend heavily on the sensor's beam pattern and the target's radar cross-section.

### Hardware Options

| Sensor | Range | Update Rate | Mass | Power | Interface | Notes |
|---|---|---|---|---|---|---|
| Ainstein US-D1 | 0.5–50m | 100Hz | 65g | 1W | UART/CAN | Altitude radar; widely used in ArduPilot for terrain following |
| Ainstein US-1 | 0.5–50m | 100Hz | 65g | 1W | UART | Short-range, good below canopy |
| LeddarOne | 0.05–40m | 100Hz | 35g | 1.5W | UART | Narrow beam, good for landing |
| Lightware LW20/C | 0.01–100m | 388Hz | 30g | 0.5W | UART/I2C | Long-range LiDAR rangefinder |
| Benewake TFMini-S | 0.1–12m | 100Hz | 5g | 0.15W | UART/I2C | Ultra-compact, limited range |
| SF11/C (LiDAR) | 0.01–120m | 200Hz | 27g | 0.5W | UART | Robust, wide deployment |

Radar and LiDAR rangefinders measure distance in one direction (the beam direction). They're most useful for:
- **Terrain following / altitude hold:** Downward-facing rangefinder gives AGL altitude independent of barometric pressure. Critical over water, canopy, and variable terrain.
- **Landing zone detection:** Downward rangefinder prevents hard landings on sloped or uneven terrain.
- **Proximity sensing in one axis:** Forward-facing rangefinder for wall-following or corridor navigation.

For full 360° obstacle avoidance, you need a scanning sensor (LiDAR) or an array of rangefinders. Scanning LiDARs add significant weight and cost — the Benewake CE30 or RPLIDAR S2 are lower-cost options, while the Ouster or Velodyne sensors are mapping-grade.

### ArduPilot Rangefinder Configuration

```
RNGFND1_TYPE = 17   # Lightware serial, or see full list in AP docs
RNGFND1_ORIENT = 25 # 25 = Downward
RNGFND1_MIN_CM = 20
RNGFND1_MAX_CM = 10000  # 100m
SERIAL4_PROTOCOL = 9   # Rangefinder
SERIAL4_BAUD = 115200

# Enable terrain following
TERRAIN_ENABLE = 1
TERRAIN_FOLLOW = 1   # Follow terrain in AUTO mode
```

For obstacle avoidance (proximity sensing):
```
PRX1_TYPE = 4   # RPLidar
PRX1_ORIENT = 0 # Forward-facing
AVOID_ENABLE = 3
AVOID_DIST_MAX = 5  # Start avoiding when object within 5m
```

---

## Radar Altimeter Integration

A dedicated radar altimeter is different from a rangefinder — it uses a wider beam pattern optimized for measuring height above ground (AGL), not object detection. The Ainstein US-D1 is the most widely used in ArduPilot BVLOS operations.

The advantage: over water, wetlands, canopy, and low-reflectance surfaces where barometric altimeters are unreliable and ultrasonic rangefinders struggle, a 24GHz FMCW radar altimeter gives consistent AGL altitude down to centimeter accuracy.

Typical BVLOS use: hover at a precise 20m AGL over varying terrain (riverbank survey, coastal mapping, pipeline inspection over varied ground cover) using the radar altimeter as the primary altitude reference in ALT_HOLD and AUTO modes.

---

## Integration with the Full BVLOS Stack

In a BVLOS Part 108 operation, DAA is one component of a layered safety architecture:

```
Airspace awareness (LAANC, NOTAMs) ─── Preflight
ADS-B In ─────────────────────────────── In-flight (equipped traffic)
Procedural deconfliction ──────────────── In-flight (unequipped)
Radar altimeter ───────────────────────── In-flight (terrain)
Proximity LiDAR ───────────────────────── In-flight (objects)
Remote ID broadcast ───────────────────── All phases
C2 link monitoring ────────────────────── All phases
Lost link action ──────────────────────── Failsafe
```

No single sensor solves all of DAA. The practical minimum for a Part 108 Permit application is ADS-B In with active avoidance enabled, plus documented operational procedures for unequipped aircraft scenarios.

---

## Logging and Reporting

ArduPilot logs all ADS-B events in the dataflash log. In Mission Planner: Ctrl+F → Logs → ADSB messages. This log is your evidence of DAA activity for any Part 108 reporting requirement.

Key fields logged per ADS-B contact:
- ICAO address and callsign
- Position at time of contact
- Relative position and altitude
- Threat classification (warning vs emergency)
- Any avoidance action taken

Preserve flight logs for 90 days minimum for any BVLOS operation — this is consistent with Part 108's expected recordkeeping requirements and best practice for incident investigation.
