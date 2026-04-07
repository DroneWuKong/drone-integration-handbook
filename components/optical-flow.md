# Optical Flow & GPS-Denied Positioning

> **Forge cross-reference:** 7 entries in `optical_flow` category  
> **Related handbook chapters:** Navigation & PNT, Companion Computers, Flight Controllers

## The Problem Optical Flow Solves

GPS works outdoors in open sky. It fails indoors, in tunnels, under dense canopy, in urban canyons, and in any environment where adversaries are actively jamming GNSS. For a drone without a fallback positioning system, GPS loss means position hold fails, the drone drifts, and the operator loses control authority.

Optical flow sensors are the primary GPS-denied positioning solution for Group 1 UAS — small, lightweight, and low-power. They work by analyzing movement of visual features in a downward-facing camera feed, combined with altitude measurement from a time-of-flight distance sensor, to compute horizontal velocity and hold position without any external reference.

The result: stable indoor hover, corridor flight, and position hold at low altitude where GPS is unavailable.

## How It Works

An optical flow sensor mounts on the underside of the drone, pointing downward. It contains:

1. **Optical flow sensor** — a specialized image sensor (typically PixArt PMW3901 or PAA3905) that detects pixel motion between frames at high speed. Think of it as a very fast, very specialized camera designed specifically for motion detection rather than image capture.
2. **Time-of-flight (ToF) distance sensor** — measures altitude above ground using a laser pulse (typically Broadcom AFBR series). Required to convert angular motion to actual velocity — without altitude, the flow sensor can't determine if a small pixel shift represents slow motion at low altitude or fast motion at high altitude.
3. **IMU** — accelerometer and gyroscope to compensate for vehicle attitude changes and vibration.

The flight controller fuses optical flow data with IMU data to estimate horizontal velocity and maintain position. PX4 and ArduPilot both support optical flow fusion natively via DroneCAN or UART.

**Operational envelope:**  
Optical flow works best at 0.5–8m AGL over textured surfaces (grass, gravel, concrete). It degrades over featureless surfaces (water, uniform carpet, snow), in very low light, and at altitude beyond 30–50m where pixel resolution becomes insufficient.

## NDAA Landscape

The optical flow market has a significant compliance gap. The dominant consumer solution — Matek 3901-L0X — is made in China and cannot be used in NDAA-covered programs. The two legitimate alternatives for federal procurement are both significantly more expensive.

| Product | Origin | NDAA | Price | Range |
|---|---|---|---|---|
| ARK Flow MR | USA | ✓ | $650 | 50m |
| ARK Flow | USA | ✓ | $320 | 8m |
| CubePilot HereFlow | Taiwan (allied) | ✓ | $85 | 3m |
| Centeye Vision Suite | USA | ✓ | Quote | 5m (IR) |
| Holybro H-Flow | China (unverified) | ⚠ | $45 | 35m |
| Matek 3901-L0X | China | ✗ | $28 | 2m |

The 8–22× price premium of NDAA-compliant optical flow over the Chinese benchmark is the defining procurement reality for any government UAS program requiring GPS-denied capability.

## Products

### ARK Flow MR — The NDAA Standard
*ARK Electronics, USA | $650 | DroneCAN*

The current benchmark for NDAA-compliant optical flow. Launched March 2025 as a drop-in upgrade to the original ARK Flow with extended range. Designed and manufactured in the United States with full supply chain documentation.

**Key specs:**  
- PAA3905 optical flow sensor (PixArt, Taiwan) — improved detection over the PAW3902 in the original ARK Flow
- Broadcom AFBR-S50LX85D ToF sensor — 50m range, dramatically extending outdoor operational altitude versus the 8m limit of the original
- InvenSense IIM-42653 IMU
- DroneCAN / CAN interface
- PX4 and ArduPilot support with firmware updates over DroneCAN
- ROS2 compatible
- Adds only 5g over the base ARK Flow

**Why it matters:** The only NDAA-compliant optical flow module with meaningful outdoor range. 50m AGL is enough for standard DFR approach altitudes. The base ARK Flow's 8m ceiling limited it to indoor and very low-altitude use.

**Limitation:** At $650, it is 23× the cost of the Matek benchmark. For high-volume production programs, this is a significant BOM impact.

### ARK Flow — The Baseline
*ARK Electronics, USA | $320 | DroneCAN*

The predecessor to the MR. Uses PAW3902 optical flow sensor (older generation), Broadcom AFBR-S50LV85D ToF (8m range), and BMI088 IMU. Still the appropriate choice for indoor-only missions where the 8m range ceiling is acceptable, and where the $330 cost savings over the MR is meaningful.

**Integration note:** Recommended mounting orientation has connectors pointing toward the rear of the vehicle. Multiple sensors can be daisy-chained via the second CAN port for redundancy.

### CubePilot HereFlow — The Value Option
*CubePilot (Hex Technology), Taiwan | $85 | DroneCAN*

The only NDAA-compliant optical flow module in the sub-$100 range. At 1.2g, it is the only viable option for nano and micro platforms where every gram matters.

**Key specs:**  
- PMW3901 optical flow sensor (older PixArt generation — lower performance than PAA3905)
- Built-in short-range LiDAR (very limited range outdoors)
- ICM20602 6D IMU
- CAN protocol
- NDAA 2024 compliant — all chips and components sourced and assembled in allied nations (Taiwan)
- Blue UAS Framework listed

**Critical limitation:** The built-in LiDAR is effectively useless outdoors beyond a few meters. ArduPilot documentation explicitly recommends pairing HereFlow with a dedicated external longer-range LiDAR for outdoor use. For indoor-only operations, it is sufficient.

**Best use case:** Nano/micro platforms (sub-250g) where ARK Flow weight is prohibitive. Indoor inspection, research platforms, small DFR scouts.

### Centeye Vision Suite — Advanced Research / Defense
*Centeye, Washington DC, USA | Quote | Custom integration*

Centeye is the original optical flow company — their principals were the first to fly an optical flow sensor on a drone in the late 1990s, and the first to provide altitude control via optical flow. Their current products use proprietary neuromorphic vision chips designed ground-up for drone autonomy rather than adapted consumer sensors.

**Why it's different:**  
Unlike commodity optical flow sensors that use adapted mouse-tracking chips, Centeye's neuromorphic vision chips are co-designed with algorithms from the silicon level up. This produces dramatically better performance in challenging conditions (low light, high dynamic range, rapid illumination changes) and supports stereo depth perception and proximity sensing alongside optical flow.

**Specs:** Sensors from 1g. Up to 150° field of view. IR illumination for operation in pure darkness (850nm, up to 5m range). Stereo depth + optical flow in one package.

**Limitation:** Not a plug-and-play product. Centeye sells integrated solutions and OEM chipsets requiring custom integration work. Not compatible with standard PX4/ArduPilot optical flow interfaces without custom firmware. Best suited for defense programs with engineering resources or research platforms.

### Holybro H-Flow — Verify Before Federal Use
*Holybro, Shenzhen, China | $45 | DroneCAN*

The H-Flow uses excellent component selection: PAA3905E1 (same PixArt sensor as ARK Flow MR), Broadcom AFBR-S50LV85D ToF, and ICM-42688-P IMU. On paper it is hardware-equivalent to ARK Flow at $45 vs $320.

**The problem:** Holybro's headquarters are in Shenzhen, China. Board assembly is Chinese. NDAA status has not been independently verified and Holybro has not published formal supply chain compliance documentation. It cannot be used in federal contracts or federally-funded programs without written NDAA compliance documentation from Holybro — documentation that does not currently exist in the public record.

For commercial non-federal applications, H-Flow is a reasonable budget choice. For any government-adjacent work, use ARK Flow or HereFlow.

### Matek 3901-L0X — The Consumer Benchmark
*Mateksys, China | $28 | UART*

The de facto standard for hobby/commercial FPV optical flow. PMW3901 + VL53L0X LiDAR (2m range), UART interface, iNAV/ArduPilot compatible. Widely documented, cheap, and broadly available. Listed in Forge for awareness — it is what most operators use on non-NDAA platforms.

**Cannot be used for:** Any federal contract, DoD program, FEMA/DHS grant-funded procurement, or any work covered by ASDA (American Security Drone Act). The board is designed and manufactured in China (Mateksys, Shenzhen).

## Integration Notes

### PX4 / ArduPilot Setup

Both firmware stacks support optical flow via DroneCAN (preferred for ARK/HereFlow) or MAVLink (for older sensors). Core parameters for PX4:

- `SENS_FLOW_MINHGT` — minimum altitude for flow to be used (typically 0.3m)
- `SENS_FLOW_MAXHGT` — maximum altitude (match to your ToF sensor range)
- `EKF2_OF_CTRL` — enable optical flow fusion
- `EKF2_HGT_REF` — set to range sensor if using optical flow for altitude

ArduPilot uses `FLOW_TYPE` to select the sensor interface and `FLOW_FXSCALER`/`FLOW_FYSCALER` for calibration.

### Mounting

The sensor must face directly downward with a clear view of the ground. Mounting position relative to the flight controller should be configured in the position offsets parameters (`SENS_FLOW_ROT` in PX4). For best results:

- Mount away from motor vibration paths
- Ensure no propeller wash obscures the downward view
- On vehicles with landing gear, verify the gear does not block the sensor's field of view during low-altitude hover

### Surface Requirements

Optical flow requires visual texture in the sensor's field of view. Test performance before deployment over:

- ✓ Grass, gravel, dirt, concrete, patterned flooring
- ⚠ Short pile carpet, sand — marginal
- ✗ Water, snow, uniform white/black surfaces, mirror finishes

For operations over problematic surfaces (water search and rescue, snow survey), consider supplementing with downward-facing LiDAR or radar altimetry and accepting reduced position hold accuracy.

## Forge Cross-Reference

The 7 parts in the `optical_flow` category represent the current vetted landscape. Use the NDAA filter in the parts browser to quickly see the 4 NDAA-verified options vs the 2 confirmed non-compliant.

**PIE signal:** Optical flow is identified as a supply chain risk category — the NDAA-compliant ecosystem is thin (effectively ARK Electronics as the sole US standalone manufacturer) and the price premium over Chinese alternatives is structural, not temporary. This is one of the clearest cases where domestic manufacturing investment is needed to reduce procurement risk.
