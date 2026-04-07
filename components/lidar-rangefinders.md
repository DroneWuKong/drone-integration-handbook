# LiDAR Rangefinders

> **Forge cross-reference:** 13 entries in `lidar_rangefinders` category  
> **Related handbook chapters:** LiDAR & Mapping Payloads, Optical Flow, Navigation & PNT

## Rangefinders vs. Mapping LiDAR

The `lidar_rangefinders` category is distinct from `lidar` (the mapping/scanning LiDAR category). Rangefinders measure distance to a single point directly below or ahead of the drone. Mapping LiDAR scans a point cloud of the environment in 3D.

Rangefinders serve three functions on a drone:
1. **Altitude above ground (AGL):** More accurate than barometer for terrain following and precision landing
2. **Terrain following:** Combined with GPS position, enables the drone to maintain constant height above uneven terrain
3. **Obstacle detection:** Forward-facing rangefinders provide basic proximity sensing

The physics is the same as mapping LiDAR — a laser pulse is emitted, reflects off a surface, and the time-of-flight gives distance. The difference is resolution: a rangefinder measures one point, a mapping LiDAR measures millions per second.

## Key Products

### LightWare LW20 / SF11 / LW3
LightWare Lidar (South Africa — allied ✓) produces the most widely-used rangefinders in the ArduPilot/PX4 ecosystem. The SF11/C (120m range, I2C/serial, 20g) and LW20/C (100m, I2C/serial, 22g) are reference integrations in both autopilot firmware stacks.

**Why LightWare dominates:** Their sensors are explicitly listed in ArduPilot and PX4 documentation, have UAVCAN/DroneCAN support in newer versions, and have a decade of drone integration history. The SF11 is what most documentation examples reference.

**LW3:** Newer generation with 200m range, industrial-grade, used in survey platforms and large commercial drones.

### Benewake TFmini / TF03
Benewake (China — NDAA ✗) produces inexpensive ToF rangefinders. The TFmini (180g, 12m range, UART, ~$40) is extremely common in DIY drone builds. TF03 extends range to 180m.

**Not for federal procurement.** For commercial non-federal use, TFmini is the practical budget option and is widely supported in Betaflight, ArduPilot, and PX4.

### Garmin LIDAR-Lite v3/v4
Garmin (USA — NDAA ✓) produces the LIDAR-Lite series. v3 (40m, I2C/PWM, 22g) was the first widely integrated rangefinder in the ArduPilot ecosystem. v4 improves performance in bright sunlight (common failure mode for optical rangefinders).

**Limitation:** 40m range limits usefulness for fixed-wing or high-altitude operations.

### TeraRanger (Terabee)
Terabee (France — EU/NATO ✓) produces multi-zone ToF sensors. TeraRanger One and Evo series offer I2C/serial interfaces and up to 14m range. Designed specifically for drone integration. Compact and light.

### LightWare GRF-500
Designed for precision landing on the LightWare SF platform. 50m range, GPS-fused altitude estimation. DroneCAN support.

## Integration

### ArduPilot
```
RNGFND1_TYPE = 7         # LightWare serial (or appropriate type for your sensor)
RNGFND1_MIN_CM = 5
RNGFND1_MAX_CM = 10000   # in cm — 100m
RNGFND1_ORIENT = 25      # downward facing
SERIAL4_PROTOCOL = 9     # rangefinder on UART4
```

### PX4
Set `EKF2_HGT_REF = 2` to use rangefinder as primary altitude reference when below `EKF2_RNG_A_HMAX` (typically 8m).

**Terrain following:** In ArduPilot, `TERRAIN_ENABLE = 1` combined with a downward rangefinder enables true terrain following — the drone maintains constant AGL altitude over hills and valleys.

### Precision Landing
A downward rangefinder is required for precision landing accuracy below ~1m altitude where GPS altitude measurement becomes unreliable. Combined with optical flow and an IR beacon, rangefinders enable sub-0.5m landing accuracy.

## NDAA Summary

LightWare (South Africa), Garmin (USA), and Terabee (France) are the NDAA-compliant options. Benewake (China) is non-compliant. For federal programs, LightWare SF11/C or Garmin LIDAR-Lite v4 are the practical choices with full ArduPilot/PX4 support.
