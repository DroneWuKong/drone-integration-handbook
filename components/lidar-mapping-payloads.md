# LiDAR & Mapping Payloads

LiDAR (Light Detection and Ranging) payloads for UAS fall into two distinct categories: **single-sensor rangefinders/scanners** used for altitude hold, obstacle avoidance, and SLAM; and **integrated mapping payloads** that combine a multi-beam scanner with a high-grade INS, camera, and onboard compute into a single deployable unit. This page covers the mapping payload tier. For rangefinders (LightWare, Benewake, TFMini), see the Forge sensor database.

---

## What Makes a Mapping Payload Different

A rangefinder measures distance to a surface. A mapping payload generates a georeferenced 3D point cloud of everything the aircraft flies over. The difference in system complexity is substantial:

- **Multi-beam rotating scanner** (32–128 channels, 360° FOV) vs. a single-beam sensor
- **Tactical or navigation-grade INS** with dual-antenna GNSS for precise position and attitude at every pulse
- **RGB camera** for colorizing the point cloud with real photographic texture
- **Onboard datalogger and compute** handling time-synchronization across all sensors
- **Post-processing (PPK/RTK) workflow** to refine GNSS accuracy from ~1m to 2–5cm

The result is deliverables: georeferenced point clouds, digital surface models, orthomosaics, and volumetric calculations — outputs that justify the payload weight and cost.

---

## The RESEPI Platform (Inertial Labs)

The most relevant mapping payload family for UAS integrators is Inertial Labs' **RESEPI™** (Remote Sensing Payload Instrument). It is also one of the most commonly white-labeled platforms in the industry — if you see a third-party branded drone LiDAR payload with a Hesai, Ouster, or Teledyne Geospatial scanner and a NovAtel GNSS receiver inside, there is a reasonable chance the core architecture is RESEPI.

Inertial Labs explicitly built RESEPI for white-labeling: all software (calibration tools, boresighting, point cloud viewer, web interface) accepts partner branding, and the hardware enclosure is designed for custom labeling. This is worth knowing when evaluating "branded" payloads from resellers.

**All current RESEPI variants are NDAA compliant.**

### Variant Comparison

| Model | Scanner | Channels | Accuracy | AGL | Weight | Key differentiator |
|---|---|---|---|---|---|---|
| **GEN-II OS1-ILX** | Ouster OS1-64 | 64 | 3–5 cm | 75 m | 1.7 kg | 64-channel density, 45° vertical FOV |
| **GEN-II M2X-ILX** | Hesai XT-32M2X | 32 | 2–3 cm | 150 m | 1.7 kg | Best accuracy + highest AGL in GEN-II line |
| **LITE XT-32** | Hesai XT-32 | 32 | 2–3 cm | 100 m | 0.9–4.3 kg | Most widely deployed globally; fully modular |
| **Ultra LITE** | Hesai XT-32 | 32 | 2–3 cm | 100 m | 1.2 kg | Lowest SWaP; SnapFit mount; single-antenna INS |
| **Teledyne EchoONE** | Teledyne Geospatial | — | 0.5 cm | 205 m | 1.65 kg | Sub-centimeter precision; highest AGL ceiling |

### GEN-II Platform (OS1-ILX and M2X-ILX)

The GEN-II represents a full platform rebuild over the original RESEPI LITE. Key upgrades:

- **175% more compute, 700% more memory** vs LITE — enables real-time point cloud visualization in the field
- **Tactical-grade IMU**: Kernel-210 (Inertial Labs' own) running their Extended Kalman Filter
- **Sensor expansion ports**: accepts external IMU, wheel encoders, air data computers as additional navigation aiding sources
- **MAVLink and DJI PSDK integration** — plug-and-play with DJI M300/M350, Freefly Astro, Sony Airpeak S1, WISPR Ranger Pro 1100
- **61 MP Sony ILX-LR1** global shutter camera on both variants
- **512 GB onboard SSD**; 9–50V input; 25–29W draw
- Supports Aerial, Mobile, and Handheld/Backpack operating modes

The two GEN-II variants differ primarily in scanner: the OS1-ILX uses Ouster's 64-channel sensor (higher point density, 45° vertical FOV, 75m AGL ceiling) while the M2X-ILX uses the Hesai XT-32M2X (32 channels, better linear accuracy at 2–3cm, 150m AGL ceiling). Pick OS1-ILX for dense urban/forestry canopy work; M2X-ILX for corridor surveys and open terrain at higher altitude.

### RESEPI LITE XT-32

The workhorse. More RESEPI LITE units are deployed globally than any other variant. Built on a navigation-grade INS (not tactical) but delivers the same 2–3 cm system accuracy for typical survey missions.

Fully modular by design: the integrator can supply their own GNSS receiver, their own LiDAR scanner, or both — Inertial Labs provides the INS/compute/datalogger core and the calibration/boresighting/PPK software stack. Single-button operation or web UI. Backpack/handheld kit available for ground survey.

Weight range (0.9–4.3 kg) reflects different scanner and mount configurations.

### RESEPI Ultra LITE

Built on the LITE architecture but trimmed for small UAS where 1.7 kg is too heavy. Single-antenna INS (vs dual on LITE and GEN-II) is the main tradeoff. SnapFit mount for rapid platform swaps. At 1.2 kg it fits platforms like the DJI M30 that can't carry a full LITE rig. Suitable for survey missions where slightly degraded heading accuracy (single vs dual antenna) is acceptable.

### Teledyne EchoONE

The premium tier. Powered by the GEN-II core but paired with a Teledyne Geospatial scanner, delivering **0.5 cm data precision** — the tightest in the RESEPI family by a factor of 4–6×. At 205 m AGL ceiling it also has the highest operational altitude. Trade-offs: 75 W power draw (vs 25–29 W for GEN-II), aerial-only operating mode (no backpack/MMS), no SLAM. The right choice for infrastructure inspection and high-precision corridor mapping where ground truth accuracy matters more than versatility.

---

## Integration Notes

**Power**: GEN-II and LITE units run 9–50V, making them compatible with both 6S (25.2V) and 12S (50.4V) UAS power rails. The EchoONE's 75W draw at 12V is ~6.3A — factor this into your power budget carefully.

**Flight time**: Inertial Labs rates maximum flight time at 33 minutes on a DJI M300, consistent with typical 6S/12S survey drone endurance carrying a ~1.7 kg payload.

**GNSS corrections**: All variants support RTCM corrections via embedded cellular modem or WiFi. For PPK workflows without cellular coverage, raw GNSS data is logged for post-processing against a base station.

**Drone compatibility**: GEN-II explicitly supports DJI M300/M350 (DJI PSDK), Freefly Astro, Sony Airpeak S1, and WISPR Ranger Pro 1100 via SnapFit or direct mount. LITE variants are more generic — standard vibration-isolated mount, user-supplied brackets.

**Software stack**: All RESEPI variants ship with LiDAR calibration software, automated boresighting, and PPK post-processing powered by NovAtel's Waypoint Inertial Explorer (Hexagon). GEN-II and EchoONE add real-time point cloud visualization.

---

## White-Label Note

If you are evaluating a third-party branded drone LiDAR payload that lists a Hesai, Ouster, or Teledyne Geospatial scanner paired with a NovAtel dual-antenna GNSS and an Inertial Labs INS, you are almost certainly looking at a RESEPI variant. Ask the vendor directly. This is not a criticism — the white-label model lets integrators focus on applications and customer relationships rather than developing payload hardware — but it is worth knowing for supply chain and support reasons. Source specs and firmware updates will ultimately trace back to Inertial Labs regardless of the label.

---

*See also: [Forge LiDAR database](/browse?category=lidar) — all RESEPI variants with full spec tables*
