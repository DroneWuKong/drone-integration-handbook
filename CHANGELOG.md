# Changelog

## [Session] - 2026-07-02 — Packable Antennas — Range You Can Carry

### Added
- **Ch. 37 — Packable Antennas — Range You Can Carry** (`fundamentals/packable-antennas.md`, Part 1): field-portable antenna selection framed as a three-way trade (gain vs beamwidth vs pack size/deploy time), for WiFi-broadcast/mesh links on cards like the MT7612U. Covers the **polarization trap** (the antenna sets polarization, not the WiFi card; matched-hand CP-CP = 0 dB, opposite-hand CP = -20 to -30 dB, CP↔linear = a consistent -3 dB), **mesh-topology antenna choice** (Babel/RFC 8966 needs omni on moving/peer nodes, gain only on the fixed sector-facing end, and a healthy return path), a **packable antenna menu** (air-side omni + ground-side directional tables with gain/beamwidth/pack size — TrueRC X-Air ~10 dBic flat CP patch, X²-Air ~13 dBic, Alfa APA-M25 dual-band linear panel), and a **worked link budget** for a 3 dBic CP omni air + X-Air ground + MT7612U setup (real ~18 dBm output, not the box's 23 dBm): ~3.5 km expected / ~11 km theoretical on 2.4 GHz, ~1.5 km / ~4.5 km on 5.8 GHz. Cross-links Antennas (Ch. 3), Link Budgets (Ch. 4), Frequency Bands (Ch. 2).
- Registered in `build.py` CHAPTERS (37) and added to "Part 1 — RF Fundamentals" PARTS. Build verified (`#ch37` renders, TOC entry present).
- Added an **"Anatomy of a Range Record"** callout to Ch. 37: how WiFi-broadcast systems (OpenHD) reach 60–75 km on the same physics — a lever-by-lever table (tracked 20–30 dBi ground antenna ≈ 30 dB, altitude/terrain to make the horizon exist, 5/10 MHz narrow channel ≈ 3–6 dB, MCS0 + FEC, RTL8812AU/EU over MT7612U, RX diversity + clean spectrum), the ~143 dB / ~58 dB budget for 60 km on 5.8 GHz, and the envelope-narrowing failure mode of chasing records.

## [Session] - 2026-06-16 — Portable Telemetry Edge Node (K3s)

### Added
- **Ch. 36 — Portable Telemetry Edge Node (K3s)** (`integration/edge-node-k3s.md`, Part 4): field-deployable K3s ground node that aggregates multi-vehicle MAVLink off a mesh, stores it locally (VictoriaMetrics), and store-and-forwards a refined copy to the cloud over a flaky uplink. Covers when an edge node beats a GCS/companion, why K3s for austere edge, the MQTT-bus data path, **B.A.T.M.A.N. adv tuning for telemetry** (OGM interval, hop penalty, bridge-loop-avoidance, fixed-rate links — with field jitter numbers), the **match-payload-to-pipe** rule (LoRaWAN = distilled status only), and the store-and-forward queue design + sizing. Cross-links companion (Ch. 13), mesh radios (Ch. 14), and CoT/TAK (Ch. 15).
- Registered in `build.py` CHAPTERS (36) and added to "Part 4 — Integration" PARTS. Build verified (`#ch36` renders).
- The runnable reference deployment (manifests, MAVLink→MQTT decoder, vmagent store-and-forward config) lives in `Ai-Project` at `infra/edge-node/`; this chapter is the field-facing companion.

## [Session] - 2026-06-01 — Levels of Drone Autonomy (Part 6 lead chapter)

### Added
- **Ch. 20 — Levels of Drone Autonomy** (`autonomy/autonomy-levels.md`): our own 0–5 (+4A/4B/4C) autonomy ladder, derived from SAE J3016 and the Exyn aerial-autonomy levels. Adds the two rows those charts omit — **ODD** (where each level is valid) and **fallback / minimal-risk** — plus a **hardware-minimum row** naming real 2026 parts per level (Betaflight FC → Pixhawk + flow/GPS → Jetson Orin + 3-D LiDAR/FAST-LIO2 → AGX Orin + thermal). Maps every level to the **Prismo stack** (Prime GCS + APB on-board) and cross-links Perception/Detection/Onboard-AI/Datasets.
- **Self-contained SVG chart** `assets/aerial-autonomy-levels.svg` (dark theme matching the site), embedded inline in the chapter so it renders on the single-page build; canonical generator `assets/aerial-autonomy-levels.svg.py`.

### Changed
- Part 6 renumbered: levels chapter inserted as **Ch. 20** (lead-in); Datasets/Perception/Detection/Onboard-AI shifted to **21–24**. `build.py` CHAPTERS + PARTS updated; build verified. Cross-links resolve by filename, so no internal links broke.

## [Session] - 2026-05-31 — Part 6: Autonomy (4 chapters)

### Added
- **Part 6 — Autonomy** (chapters 20–23): `autonomy/datasets.md` (datasets & benchmarks + the license trap), `autonomy/perception.md` (VIO/SLAM, relative vs absolute fixes, GPS-denied failure modes), `autonomy/detection.md` (RF + visual, bird false-positives, detection→navigation), `autonomy/onboard-ai-control.md` (confidence-driven authority, EW/capability-aware autonomy).
- Registered in `build.py` CHAPTERS (chapters 20–23; vendor guides own 18–19) + new "Part 6 — Autonomy" PARTS entry. Build verified.
- Backed by the forge-data autonomy dataset registry (`autonomy/datasets.json`); Forge interactive browser is Phase 2 (droneclear_Forge FEAT-028).


## [Session] - 2026-05-31 — Appendix F: Regulatory & Open Resources

### Added
- **Appendix F — Regulatory & Open Resources** (`appendices/appendix-f-regulatory-resources.md`): curated, open-access regulatory/safety references (FAA Part 107 + policy library, NCSL state-law tracker, FAA ASIAS incident DB, Eurocontrol, UK CAA, AUVSI, ASSURE, UAS Magazine).
- `data/erau_resources.json` — machine-readable backing data, tagged by consuming property.
- Chapter 2 (Frequency Bands & Regulatory Reality) now links to Appendix F from a new "regulatory side of reality" section.


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

