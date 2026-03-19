# Data Enrichment Research Queue

**Total remaining: ~1,783 fields across 10 stages**
Work through 1-2 stages per session. Each stage targets one manufacturer group at a time.

---

## Stage 1: FC IMU Completion ⭐ HIGH PRIORITY
- **Field:** `flight_controllers.imu`
- **Remaining:** 137 / 395 (65.3% → target 95%)
- **Method:** Web scrape manufacturer product pages
- **Priority manufacturers:** Holybro (32), MatekSys (10), CubePilot (9), Flywoo (9), T-Motor (8)
- **Approach:** Search `{manufacturer} {model} IMU gyro specs` → fill ICM42688P/BMI270/MPU6000

## Stage 2: Stack IMU Completion
- **Field:** `stacks.imu`
- **Remaining:** 52 / 102 (49% → target 90%)
- **Method:** Same manufacturer pages as Stage 1
- **Priority:** SkyStars (16), Flywoo (7), T-Motor (6), Diatone (3)

## Stage 3: Antenna Connector
- **Field:** `antennas.connector`
- **Remaining:** 218 / 439 (50.3% → target 85%)
- **Method:** Product page lookups + name pattern matching
- **Priority:** Video Aerial Systems (53), Lumenier (47), TrueRC (42), TBS (11)
- **Values:** SMA, RP-SMA, MMCX, U.FL

## Stage 4: Antenna Polarization + Type
- **Field:** `antennas.polarization` + `antenna_type`
- **Remaining:** ~266 combined
- **Current:** pol 69%, type 71%
- **Method:** Manufacturer catalog cross-reference — same parts as Stage 3

## Stage 5: VTX Power Output
- **Field:** `video_transmitters.max_power_mw`
- **Remaining:** 93 / 125 (25.6% → target 80%)
- **Method:** Product specs — many VTX names include power rating
- **Quick win:** Most analog VTX have power in name (400mW, 800mW, etc.)

## Stage 6: FC Firmware + MCU (remaining ~25%)
- **Field:** `flight_controllers.firmware_targets` + `mcu_family`
- **Remaining:** ~206 combined
- **Current:** fw 73%, mcu 75%
- **Method:** Cross-reference Betaflight firmware target list
- **Source:** https://github.com/betaflight/betaflight/tree/master/src/main/target

## Stage 7: Frames Subtype + Manufacturer
- **Field:** `frames.vehicle_subtype` + `manufacturer`
- **Remaining:** ~335 combined
- **Current:** sub 45%, mfr 86%
- **Method:** Name pattern matching + store catalog (GetFPV, RaceDayQuads)

## Stage 8: FPV Camera Size + Sensor
- **Field:** `fpv_cameras.camera_size` + `sensor_size`
- **Remaining:** ~255 combined
- **Current:** size 69%, sensor 3%
- **Method:** Caddx/Foxeer/RunCam product page scrape
- **Note:** sensor_size (1/3", 1/2") is rarely in product names — needs spec sheet lookups

## Stage 9: Receiver Diversity + Frequency
- **Field:** `receivers.diversity` + `frequency_ghz`
- **Remaining:** ~171 combined
- **Current:** div 21%, freq 77%
- **Method:** ELRS/Crossfire/FrSky product catalogs
- **Quick win:** Most ELRS are 2.4GHz, most Crossfire are 915MHz

## Stage 10: Mesh Radios Deep Fill
- **Field:** All mesh_radios fields (band, throughput, encryption, range, MIMO)
- **Remaining:** ~50 fields across 13 radios
- **Current:** 23%
- **Method:** Silvus StreamCaster / Doodle Labs Helix / Persistent MPU5 / Rajant spec sheets
- **Note:** These are high-value defense components — specs may require registration

---

## Completed (this session)
- ✅ FPV Cameras video_system: 19% → **98%**
- ✅ Video TX video_system: 49% → **93%**
- ✅ Receivers protocol: 85% → **93%**
- ✅ FC mounting_pattern: 54% → **100%**
- ✅ FC cell_count_max: 27% → **100%**
- ✅ Frames arm_config: 5% → **100%**
- ✅ Frames manufacturer: 58% → **86%**
- ✅ ESC firmware: 67% → **83%**
- ✅ Batteries discharge_rate: 34% → **82%**
- ✅ Antennas gain_dbi: 1% → **71%**
- ✅ All pricing stripped
- ✅ 25 miscategorized items cleaned out
- ✅ 128 junk cross-contaminated fields removed
