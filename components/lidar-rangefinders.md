# LiDAR Rangefinders

A single-point rangefinder and a scanning mapping LiDAR have different coverage and data contracts. A distance measurement is not automatically vertical terrain height: orientation, field of view, target reflectivity, ambient light and estimator use matter.

## Exact variant reference

| Model | Manufacturer-reported mass | Scope |
|---|---|---|
| Benewake TFmini-S | 5 ± 0.3 g | Exact module; installation/cables/mounts add mass |
| Benewake TFmini Plus | 12 ± 1 g | Different variant, not interchangeable by family name |

The former “TFmini 180 g” entry is withdrawn. Benewake advertises TFmini-S up to 12 m under its specified conditions; maximum range is not a universal obstacle-detection or terrain-following guarantee. [Benewake TFmini-S source](https://en.benewake.com/TFminiS/index.html), checked 2026-10-07; use its exact variant manual for interfaces and operating conditions.

[claim:tfmini-s-mass]

## Firmware integration

Use the exact sensor/transport driver in the target autopilot release. UART, I²C and CAN variants require different interfaces; a sensor family name is not a driver value. The previous unversioned `RNGFND1_TYPE` example and centimeter-unit limits are withdrawn. ArduPilot releases can change parameter names/units; look up the installed release and read back after configuration.

[ArduPilot rangefinder documentation](https://ardupilot.org/copter/docs/common-rangefinder-landingpage.html) and [Copter 4.7.1 parameter reference](https://ardupilot.org/copter/docs/parameters-Copter-stable-V4.7.1.html), checked 2026-10-07. For PX4, use the matching release's sensor and estimator documentation rather than a universal height-reference preset.

Observe missing, saturated, implausible and stale samples in software before hardware integration. A terrain database, range measurement and flight-mode terrain-following implementation are separate functions. Record the downward/body frame, sensor position and tested surface/lighting conditions.

## Procurement

Screen exact item/configuration and applicable authority using the [federal procurement guide](ndaa-compliance.md). Country of origin alone is not a certification or compliance determination.
