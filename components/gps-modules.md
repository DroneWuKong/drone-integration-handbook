# GPS & GNSS Modules

> **Forge cross-reference:** 76 entries in `gps_modules` category  
> **Related handbook chapters:** RTK/PPK GPS Integration, Navigation & PNT, Flight Controllers

## What GPS Modules Actually Do

A GPS module on a drone serves three functions: position hold, return-to-home, and mission execution. The quality of your GPS module determines how accurately the drone holds position in hover, how fast it acquires a lock at startup, and whether it maintains lock in challenging RF environments.

Most pilots underestimate how much GPS quality matters. A cheap M8N module will hold position to ±3m and drift visibly in hover. A quality M9N or M10 module holds to ±0.8m and feels locked to an invisible anchor. An RTK module holds to ±2cm. The difference is visible and operationally significant.

For the RTK and PPK precision mapping use case, see the dedicated `rtk-ppk-gps-integration.md` chapter. This chapter covers the standard position-hold and navigation GPS ecosystem used in most flight operations.

## GNSS Generations

### u-blox Generations (The Industry Standard)

u-blox (Swiss) is the dominant GNSS receiver chipset supplier for the drone market. Understanding their product generations clarifies almost every GPS module comparison.

**M8N / M8T (2014–2018)**  
The first generation widely adopted for drone use. GPS+GLONASS dual-constellation. 2.5m CEP positional accuracy. Adequate for basic position hold. Still common on older platforms and budget builds. The M8T variant supports raw pseudorange output for PPK post-processing.

**M9N (2020–present)**  
Significant improvement. GPS+GLONASS+Galileo+BeiDou concurrent tracking (4 constellations). 2.0m CEP. Faster acquisition. Better performance in partial sky view. The M9N is the practical baseline for any professional build — it's what's in most Holybro, CubePilot, and Lumenier GPS modules in the mid-range.

**M10 (2022–present)**  
Current u-blox generation for standard (non-RTK) positioning. All-constellation (GPS/GLONASS/Galileo/BeiDou/NavIC/QZSS). 1.5m CEP. Significantly improved performance in urban and multipath environments. Lower power than M9N. The M10 is where new designs should start.

**F9P (RTK)**  
u-blox's high-precision receiver used in RTK systems like the Here4, CubePilot, and Emlid Reach. Centimeter-level accuracy with corrections. See the RTK/PPK chapter.

### Other Chipsets

**UBLOX SAM-M10Q** — Module-level integration of M10 core from u-blox, used by Lumenier and ARK Electronics in their NDAA-compliant modules. Same chip, different PCB integration.

**SkyTraq** — Taiwan-based GNSS chip used in some budget modules. Not common in professional applications.

**Broadcom BCM47765** — Used in some DJI hardware. Higher-end consumer chip with strong multipath rejection.

## NDAA Compliance

GPS modules are one of the cleaner categories for NDAA compliance because the dominant chipset supplier (u-blox) is Swiss, and several US manufacturers produce NDAA-verified modules around Swiss/allied-nation chips.

| Product | Manufacturer | Origin | NDAA |
|---|---|---|---|
| CubePilot Here4 | CubePilot | Australia | ✓ |
| CubePilot Here3+ | CubePilot | Australia | ✓ |
| ARK GPS (M9N) | ARK Electronics | USA | ✓ |
| ARK GPS (M10) | ARK Electronics | USA | ✓ |
| Lumenier SAM-M10Q | Lumenier | USA | ✓ |
| mRo GPS u-Blox Neo-M9N | mRobotics | USA | ✓ |
| Holybro Micro M10 | Holybro | China | ✗ |
| Holybro M9N Standard | Holybro | China | ✗ |
| Matek SAM-M10Q | Mateksys | China | ✗ |
| HGLRC M100 | HGLRC | China | ✗ |

The u-blox chip itself is Swiss — the NDAA status depends on where the PCB is assembled and who manufactures the final module. ARK and Lumenier do final assembly in the USA around the Swiss chipset, which qualifies them.

## Form Factors

### Standard GPS Puck (20–50g)
The most common form factor for ArduPilot/PX4 platforms. Round or hexagonal PCB with integrated compass, enclosed in a plastic housing with a short mast or mounting plate. Usually includes a status LED. CubePilot Here3+, Holybro M9N Standard, and mRo U-Blox fall in this category.

**Compass integration** is standard in puck-form GPS modules. The external compass is mounted away from FC motor noise, significantly improving heading accuracy versus using the FC's onboard compass. Always enable the external compass and disable the internal one in ArduPilot/PX4 if running an external GPS with compass.

### Surface-Mount Module (5–15g)
Smaller PCB format for fixed-wing, racing, or weight-critical builds. RadioMaster ERS-GPS, Matek SAM-M10Q, HGLRC M100. Typically no compass, antenna is chip ceramic or small helical.

### Helical GPS Antenna
Separate helical antenna element for improved gain in low-elevation satellite environments. The CubePilot Here4 can use a helical antenna for better performance. Useful when the drone attitude frequently blocks the GPS puck's view of the horizon.

## Protocol & Wiring

All modern GPS modules communicate via UART at 9600–115200 baud using the UBX binary protocol or NMEA ASCII. UART is the universal interface — TX→RX, RX→TX, 3.3V or 5V power.

**Compass interface:** I2C (most common). Enable external compass in FC configuration and set the correct orientation offset if the GPS is mounted rotated relative to the FC.

**ArduPilot UART setup:**
```
SERIAL3_PROTOCOL = 5    # GPS
SERIAL3_BAUD = 38       # 38400 baud (or 115 for modern modules)
GPS_TYPE = 1            # u-blox auto-detect
COMPASS_USE = 1         # Use external compass
COMPASS_USE2 = 0        # Disable internal compass
```

**PX4 UART setup:**
```
GPS_1_CONFIG = TELEM1   # or whichever UART the GPS is on
GPS_1_PROTOCOL = 1      # u-blox
```

**DroneCAN GPS:** Newer ARK and CubePilot modules support DroneCAN (formerly UAVCAN), allowing GPS+compass data over the CAN bus. This reduces wiring, adds redundancy, and enables hot-swapping. CubePilot Here4 supports both UART and DroneCAN. ARK GPS modules are DroneCAN-native.

## Compass Calibration

A poorly calibrated external compass is one of the most common causes of erratic position hold and toilet-bowl circling. After installation:

1. Mount the GPS mast far from high-current wires (ESC power leads, battery leads)
2. Perform a full compass calibration (ArduPilot: `COMPASS_CAL` live calibration or MissionPlanner onboard)
3. Check compass motor interference by running motors at full throttle and watching compass heading deviation — acceptable is <30°
4. If using two compasses (FC internal + GPS external), verify they agree within 15° on heading

**Compass interference sources to avoid:**
- Battery cables running parallel to GPS mast
- Video transmitter near GPS mount
- Metal fasteners or standoffs directly under the GPS

## GPS Redundancy

For any operation where GPS loss is a critical failure:

- **Dual GPS** — Two independent GPS modules feeding the EKF. ArduPilot EKF3 supports multiple GPS instances and can switch mid-flight. Strongly recommended for BVLOS and any commercial operation.
- **GPS+Optical Flow** — Ground-referenced positioning from optical flow supplements GPS in low-altitude or indoor-transitioning scenarios. See `components/optical-flow.md`.
- **GPS+SLAM** — Companion computer SLAM provides GPS-independent positioning. See `components/companion-computers.md`.

## Forge Cross-Reference

76 GPS modules across the full range from $8 HGLRC M100 to the $400 CubePilot Here4. The NDAA ✓ filter in the Forge parts browser shows ~12 compliant options concentrated around ARK Electronics, Lumenier, CubePilot, and mRobotics. All are u-blox M9N/M10-based.
