# Changelog

## [Session] - 2026-04-13 — Mass parts-db enrichment + duplicate PID removal

### Fixed
- **62 duplicate PIDs removed** across 8 files: receivers (32), control_link_tx (17), escs (2), flight_controllers (3), frames (1), mesh_radios (4), thermal_cameras (2), video_transmitters (1)

### Changed
- **Full parts-db enrichment pass** — all 38 categories brought to 95-100% field coverage:
  - VTX: `max_power_mw`, `channels`, `frequency_band`, `connector`, `power_w`, `protocol`, `mounting_pattern_mm` → 100%
  - Receivers: `diversity`, `size_class` → 100%
  - Antennas: `connector`, `polarization`, `antenna_type`, `gain_dbi` → 100%
  - Stacks: `imu`, `cell_count_min/max`, `esc_firmware` → 100%
  - Flight Controllers: `imu`, `firmware_targets`, `mcu_family` → 100%
  - GPS: `gnss_chipset`, `constellations` → 100%
  - ESCs: `mcu_family`, `esc_firmware`, `cell_count_min/max`, `mounting_pattern_mm` → 100%
  - Mesh Radios: 10 spec fields (band, throughput, encryption, range, mimo, freq, waveform, latency, nodes, ndaa) → 100%
  - Counter-UAS: `defeat_method`, `form_factor`, `compliance` → 100%
  - Thermal Cameras: `frame_rate_hz`, `interface`, `lens_fov_deg`, `netd_mk`, `pixel_pitch_um`, `resolution_h/v`, `spectral_band`, `power_w` → 100%
  - Motors: `best_for_inches`, `prop_shaft_style` → 100%
  - Propellers: `diameter_inches` → 100%, `pitch_inches` → 92%
  - Batteries: `cell_format`, `energy_density_wh_kg`, `cycle_life` → 97%
  - FPV Cameras: `camera_size`, `sensor_size` → 100%
  - Gimbals: `interfaces`, `ip_rating` → 100%
  - LiDAR Rangefinders: `fov_deg`, `ip_rating`, `signal_processing` → 100%
  - AI Accelerators: 25+ spec fields → 92-100%
  - C2 Datalinks: `datalink_type`, `frequency_band`, `encryption`, `architecture` → 100%
  - EW Systems: `defeat_method`, `frequency_bands`, `capabilities`, `form_factor`, `platform`, `passive` → 100%
  - Navigation/PNT: `sensor_type`, `technology`, `power_w`, `anti_jam`, `anti_spoof` → 100%
  - Sensors: `sensor_type`, `technology`, `power_w`, `interface`, `manufacturer_country`, `itar_free` → 100%

