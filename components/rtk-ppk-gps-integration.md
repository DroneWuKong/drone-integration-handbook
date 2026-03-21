# RTK/PPK GPS Integration

Standard drone GPS gives you 2–5 meter horizontal position accuracy. RTK and PPK give you 1–3 centimeter accuracy. For mapping, survey, precision agriculture, and BVLOS operations, the difference matters. This guide covers wiring an RTK receiver into ArduPilot or PX4, setting up a base station, and choosing between real-time RTK and post-processed PPK.

---

## How RTK and PPK Work

Both methods exploit the same physics: a GPS receiver doesn't just measure the time of arrival of satellite signals — it also measures the carrier phase of the signal, which can resolve position to millimeter precision. The problem is ambiguity: carrier phase measurements have an inherent integer ambiguity (which wave cycle you're on), and resolving that ambiguity requires a reference point.

**RTK (Real-Time Kinematic):** A base station at a known location sends its raw carrier phase observations to the rover (your drone) via a radio or cellular link. The rover uses both sets of measurements to compute a "baseline vector" relative to the base station, resolving position to centimeter accuracy in real time. This requires a continuous data link during flight.

**PPK (Post-Processed Kinematic):** The rover logs its raw observations during flight. The base station logs its raw observations simultaneously. After the flight, you run a processing algorithm (in Emlid Studio, Novatel Inertial Explorer, or open-source RTKLIB) that computes the precise positions after the fact. No real-time link required; works even if the link drops during flight.

**When to use which:**
- **RTK:** When you need centimeter accuracy during the flight for guidance (precision landing, crop row following, survey that requires real-time confirmation of coverage)
- **PPK:** When you need centimeter accuracy in the final data product, the real-time link is impractical, or you want belt-and-suspenders reliability (log both; compute PPK if RTK lock drops mid-flight)

---

## Hardware Options

### Rover (Onboard)

| Module | Weight | Interface | RTK | PPK | Price | Notes |
|---|---|---|---|---|---|---|
| Emlid Reach M3 | 15g | UART/USB | Yes | Yes | ~$300 | Popular, lightweight, good ArduPilot integration |
| Emlid Reach M2 | 20g | UART | Yes | Yes | ~$400 | Multi-constellation, widely deployed |
| u-blox ZED-F9P module | 5g (bare) | UART/I2C | Yes | Yes | ~$160 | Raw chipset; needs a carrier board |
| Holybro H-RTK F9P Rover | 24g | UART/CAN | Yes | Yes | ~$200 | Pre-built F9P board, ArduPilot plug-in |
| CUAV C-RTK 2 HP | 49g | UART/CAN | Yes | Yes | ~$350 | Integrated antenna + receiver |
| ArduSimple simpleRTK2B | 10g | UART | Yes | Yes | ~$190 | ZED-F9P-based, popular in community |

For new ArduPilot builds: the **Holybro H-RTK F9P** or **Emlid Reach M3** are the easiest integrations. For weight-critical platforms: the bare **u-blox ZED-F9P** on a minimal carrier board.

### Base Station

The base station must stay fixed during the flight. Options:

**Option A: Temporary base (known point or averaged)**
Set up a tripod-mounted receiver at a surveyed benchmark or let it average its position for 5–10 minutes (accurate to ~30cm without corrections, ~10cm with prolonged averaging). This is "relative accuracy" — your map will be internally consistent to centimeter level but may be offset from absolute coordinates by the base station's own uncertainty.

**Option B: Network RTK / NTRIP**
Use an existing CORS (Continuously Operating Reference Station) network to provide corrections over the internet. No base station hardware needed. Services: RTK2go (free, community), NGS OPUS, state DOT CORS networks, Trimble RTX, Hexagon SmartNet.

```
NTRIP workflow:
1. Subscribe to NTRIP service (many are free)
2. Configure a Ground Control Station phone/laptop as NTRIP client
3. Corrections flow: NTRIP server → GCS → radio link → drone receiver
```

**Option C: Emlid RS2 / RS3 base station**
A complete base station in a weatherproof enclosure. Self-contained, logs raw data for PPK, transmits corrections via LoRa radio (built-in) or NTRIP forwarding via cellular.

---

## Wiring Into ArduPilot

### Serial Connection

The RTK receiver connects to a free UART on the FC:

```
RTK module TX → FC UART RX
RTK module RX → FC UART TX
RTK module GND → FC GND
RTK module power → FC 5V or dedicated BEC (check module current draw)
```

The u-blox ZED-F9P draws ~200mA — fine from a 500mA+ FC 5V rail. The Emlid Reach M3 draws ~350mA and should use a dedicated BEC or powered hub.

### ArduPilot Parameters

```
# GPS type for the RTK receiver
GPS1_TYPE = 17   # UBX (u-blox ZED-F9P, Holybro, ArduSimple)
# or
GPS1_TYPE = 15   # Emlid Reach (for Reach M2/M3 via NMEA+RTCM)

GPS1_RATE_MS = 100   # 10Hz updates (200ms for 5Hz, 67ms for 15Hz)

# UART for the GPS
SERIAL3_PROTOCOL = 5   # GPS
SERIAL3_BAUD = 230400  # or 115200 for slower configs

# If corrections are injected via GCS (MAVLink injection):
GPS1_INJECT_TO = 1   # Enable MAVLink RTK correction injection
```

**Correction injection methods:**
1. **Radio link (dedicated):** Base station transmits RTCM3 corrections over a dedicated 915MHz or 433MHz radio link. Rover FC receives and passes to GPS module via UART.
2. **MAVLink injection:** GCS forwards RTCM3 corrections from an NTRIP source to the FC via MAVLink `GPS_RTCM_DATA` messages. The FC passes them to the GPS module's serial port. Works over cellular or standard telemetry link.
3. **Emlid LoRa:** Emlid Reach base and rover use a built-in LoRa radio for corrections. Simple and reliable to ~8km.

### Checking RTK Fix Status

In Mission Planner, the GPS status bar shows:
- **3D Fix:** Standard GPS, 2–5m accuracy
- **3D RTK Float:** Carrier phase initialized but integer ambiguity not resolved. ~20–50cm accuracy.
- **3D RTK Fixed:** Integer ambiguity resolved. 1–3cm accuracy. This is what you want.

Time to RTK Fixed: typically 30–120 seconds after both base and rover have satellite lock. Cold start (no almanac, new location) can take 5–15 minutes.

---

## PPK Workflow

For mapping/survey missions where real-time RTK isn't essential:

**Pre-flight:**
1. Set up base station. Start logging raw observations (RINEX 3.x format) at 1Hz.
2. Verify rover is logging raw observations to onboard storage.
3. Note the base station coordinates (or post-process them against NTRIP for absolute accuracy).

**Flight:**
1. Fly the mission normally.
2. Confirm rover log is running continuously.

**Post-flight processing:**
1. Download rover observation log and FC flight log.
2. Download base station observation log.
3. Load both into Emlid Studio (free), RTKLIB (open-source), or Novatel Inertial Explorer.
4. Set base station coordinates (absolute or relative).
5. Run forward-backward processing. Output: precise trajectory as a time-series of positions.
6. Apply trajectory to geotagged photos or LiDAR scan using Pix4D, Agisoft Metashape, or CloudCompare.

**MRK files:** Some cameras (Sony a6xxx, Phase One) output a `.MRK` or `.SHUTTER` log with precise shutter timestamps. Emlid Studio can fuse these with the PPK trajectory for sub-centimeter geotag accuracy.

---

## Why FC GPS Accuracy ≠ Survey Accuracy

This is the most common confusion for operators moving from hobbyist to survey work.

The GPS status in your GCS shows the position reported by the onboard receiver. But your final data product accuracy depends on more than just receiver accuracy:

**1. Ephemeris vs. precise ephemeris:** The FC GPS uses broadcast ephemerides (satellite position predictions). Survey-grade processing uses precise ephemerides from IGS, which are accurate to a few centimeters vs. the broadcast's 1–2m. For RTK, this matters less because the base-rover differential eliminates most orbital error.

**2. Shutter sync:** If the camera shutter fires at an unknown time (no sync signal to GPS), the position at capture time must be interpolated. At 10m/s groundspeed, 50ms timing uncertainty = 50cm position error. Sync the shutter to GPS PPS for centimeter-level geotag accuracy.

**3. Antenna phase center:** The GPS antenna has a phase center that's not exactly at the mechanical center. For centimeter surveys, apply the antenna offset (calibrated from manufacturer spec) as an offset correction in your PPK software. ArduPilot parameter: `GPS1_POS_X/Y/Z` — the offset of the GPS antenna from the IMU.

**4. IMU lever arm:** For systems where the GPS antenna is not coincident with the IMU (separate modules with a physical offset), the lever arm creates position errors proportional to attitude angle × separation distance. A 15cm lever arm at 30° roll creates a 7.5cm lateral error in GPS-reported position. Compensate with `GPS1_POS_X/Y/Z` offsets in ArduPilot.

**5. Base station accuracy:** If your base station position is off by 30cm (averaged position without NTRIP corrections), your entire dataset is offset by 30cm. Relative accuracy (internal consistency) can be centimeter-level while absolute accuracy (position on Earth) is 30cm off. For relative surveys (volume calculations, change detection) this doesn't matter; for absolute surveys (cadastral, infrastructure) it does.

---

## Quick Config Reference

### ArduPilot + u-blox F9P + MAVLink NTRIP Injection

```
GPS1_TYPE = 17          # UBX
SERIAL3_PROTOCOL = 5    # GPS
SERIAL3_BAUD = 230400
GPS1_INJECT_TO = 1      # Accept MAVLink injection
GPS1_RATE_MS = 100      # 10Hz
GPS1_GNSS = 0           # Use all constellations (auto)
GPS1_POS_X = 0.05       # Antenna offset from IMU X (meters, forward)
GPS1_POS_Y = 0.0        # Antenna offset Y (meters, right)
GPS1_POS_Z = -0.03      # Antenna offset Z (meters, down)
```

In Mission Planner: Config → Planner → NTRIP → enter service URL, credentials, and mount point. MP will forward RTCM3 corrections to the FC via MAVLink at ~1Hz.
