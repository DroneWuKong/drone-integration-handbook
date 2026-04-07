# Roadmap

Future chapters, sections, and improvements under consideration.
Open an issue to suggest additions or volunteer to write one.

## Recently Completed (2026-04-07 — continued)

- [x] **Weight enrichment to 100%** — All 3,615 parts now have weight_g. FPV cameras, GPS, VTX, stacks, control link, thermal cameras, AI accelerators, companion computers, mesh radios, EW systems, ESAD, counter-UAS, swarm software, military firmware, and remaining hardware filled via form-factor/stator/wheelbase/class inference.
- [x] **Mesh Radios** — `components/mesh-radios.md` — Rajant BreadCrumb, Silvus StreamCaster, Doodle Labs Mesh Rider, Elsight HALO; topology design, MAVLink-over-mesh, bandwidth planning.
- [x] **Control Link TX** — `components/control-link-tx.md` — ELRS modules, TBS Crossfire/Tracer TX, Spektrum; JR/nano bay formats, power levels, NDAA (TBS Swiss ✓, all ELRS Chinese ✗).
- [x] **FPV Detectors** — `components/fpv-detectors.md` — RF Explorer, ISDS204B, SDR-based detection; detection targets (analog/digital/FHSS), security monitoring deployment.
- [x] **Video Scramblers** — `components/video-scramblers.md` — Ukrainian-origin anti-detection systems, MAFIA system context, export controls.
- [x] **Payload Droppers** — `components/payload-droppers.md` — servo/magnet/winch mechanisms, ArduPilot Gripper integration, MAV_CMD_DO_GRIPPER.
- [x] **LiDAR Rangefinders** — `components/lidar-rangefinders.md` — LightWare, Benewake, Garmin LIDAR-Lite; terrain following, precision landing, NDAA table.
- [x] **Survey Sensors & Multispectral** — `components/sensors.md` — MicaSense RedEdge-P/Altum-PT (AgEagle ✓), Sentera 6X (John Deere ✓), Sony ILX-LR1, Phase One; NDVI pipeline, radiometric calibration.
- [x] **Weight: 100% coverage** — All 3,615 Forge parts now have weight_g values.
- [x] **Receivers** —  — 391 entries: ELRS/Crossfire/FrSky/Spektrum/FlySky protocols, NDAA landscape (TBS=Swiss NDAA-compliant, all ELRS brands Chinese), UART config, antenna placement, failsafe setup.
- [x] **GPS & GNSS Modules** —  — 76 entries: u-blox M8N→M10 generations, NDAA table (ARK/Lumenier/CubePilot ✓), DroneCAN integration, compass calibration, dual GPS redundancy.
- [x] **Antennas** —  — 394 entries: gain/polarization/radiation pattern, stub/cloverleaf/lollipop/patch/helical types, system design by use case, connector ecosystem (SMA/RP-SMA/U.FL/MMCX), NDAA (TrueRC/ImmersionRC ✓).

## Recently Completed (2026-04-07)

- [x] **Optical Flow & GPS-Denied Positioning** — `components/optical-flow.md` — 7 vetted entries: ARK Flow MR/Flow (USA NDAA), CubePilot HereFlow (Taiwan NDAA), Centeye neuromorphic (USA), Holybro H-Flow (unverified), Matek + DJI (China flagged). NDAA landscape table, PX4/ArduPilot integration, surface requirements. 48th component page.
- [x] **DB NDAA enrichment sprint** — 3,571/3,615 parts resolved (98.8%). FC research pass (72✓ 218✗ 37?), thermal cameras (39✓), thermal/counter-UAS/C2/sensors/navigation/propulsion all classified. Manufacturers documented: Teledyne FLIR, L3Harris, Hensoldt, Rohde & Schwarz, Silvus, Shield AI, Rajant, infiniDome, Honeywell, Anello, MicaSense, Sentera, DeepX, Kinara, etc.
- [x] **DB field enrichment** — 1,271 interface fields inferred (FC/ESC/RX/GPS/VTX); 1,496 weight_g values from stator/form factor (97% props, 94% ESCs, 96% batteries); tag taxonomy normalized to 1,366 canonical tags; canonical ndaa/china/usa/ukraine/nato/israel/five-eyes/blue-uas tags on all 3,573 parts.
- [x] **Browse modal overhaul** — NDAA shows ✓ green / ✗ red; weight, interface, firmware, price surfaced first; cyan tag chips; amber ndaa_note compliance warning box; links from new links[] field.
- [x] **Browse NDAA filter pills** — `All / NDAA ✓ / Non-NDAA ✗ / China / USA` quick-filter chips on every category, instant filter, color-coded.
- [x] **PIE DB integration** — generate_pie_from_db.py scans all 34 categories; 103 db_-prefixed auto-flags (landscape/supply_constraint/supply_chain_risk/diversion/compliance); wired into weekly GitHub Actions pipeline; supply_constraint flags 12→1 (documentation gaps resolved).

## Recently Completed (2026-04-05)

- [x] **Military Firmware Forks** — `components/military-firmware-forks.md` — MILELRS, MILBETA, FPV_VYZOV, BarvinokLRS/Barvinok-5, "1001" DJI mod, CIAJeepDoors, mLRS, DroneBridge ESP32. Full landscape of combat-adapted open-source firmware.
- [x] **Frames & Airframe Selection** — `components/frames-airframe-selection.md` — 349 frames: sizing, geometry, materials, stack mounting, arm design, durability, antenna routing
- [x] **FPV Cameras** — `components/fpv-cameras.md` — 193 cameras: analog vs digital (DJI/Walksnail/HDZero/OpenHD), sensor specs, contested environment considerations
- [x] **Video Transmitters (VTX)** — `components/video-transmitters-vtx.md` — 116 VTX: all systems compared, frequency bands, non-standard operation, 5-layer contested environment strategy
- [x] **Propellers** — `components/propellers.md` — 484 props: sizing, pitch, blade count, materials, balance, military considerations
- [x] **CRSF & ELRS Protocol** — `firmware/crsf-elrs-protocol.md` — Packet structure, ELRS rates, telemetry, binding, MILELRS encrypted binding context
- [x] **DShot & ESC Protocols** — `firmware/dshot-esc-protocols.md` — DShot packet format, bidirectional DShot, RPM filtering, BLHeli_32/AM32/Bluejay
- [x] **Crash Recovery & Field Repair** — `field/crash-recovery.md` — Post-crash assessment checklist, field repair matrix, field kit, Tooth integration

## Recently Completed (2026-04-04)

- [x] **Electronic Warfare Awareness** — `components/electronic-warfare.md` — 14 EW systems, operator-perspective coverage of jammers, GNSS protection, and operating in contested RF environments
- [x] **Ground Control Stations** — `components/ground-control-stations.md` — 13 GCS entries covering open-source software (QGC, Mission Planner), enterprise (UgCS, Auterion MC), hardware (GS-ONE, Herelink), and field considerations
- [x] **AI Accelerators** — `components/ai-accelerators.md` — 13 edge AI entries from Syntiant (10mW) to Axelera (214 TOPS), integration patterns, NDAA compliance
- [x] **C2 Datalinks** — `components/c2-datalinks.md` — 13 entries covering aviation-grade BVLOS (uAvionix), tactical MANET (Silvus), and integrated systems (Herelink)
- [x] **Navigation & PNT** — `components/navigation-pnt.md` — 12 entries across 6 technology tiers from MEMS IMU to quantum PNT, selection framework by threat environment
- [x] **Integrated Flight Stacks** — `components/integrated-stacks.md` — 5 entries (VOXL 2, Skynode, DTK APB, ARK FPV), when to use integrated vs modular
- [x] **Swarm Software** — `components/swarm-software.md` — 10 entries covering drone show (Skybrush) and tactical swarm (Crazyswarm2, ORCUS) platforms
- [x] **ESAD Safe-and-Arm** — `components/esad-safe-arm.md` — 12 entries from US and allied manufacturers, MIL-STD-1316 architecture
- [x] **Tactical Accessories** — `components/tactical-accessories.md` — Video scramblers (5) and payload droppers (4), Ukrainian-origin field equipment
- [x] **Appendix B: UART Maps** — `firmware/appendix-b-uart-maps.md` — 416 common FCs
- [x] **Pattern Intelligence Engine (PIE)** — `pipeline/` directory — Supply chain, regulatory, and competitive intelligence pipeline with 207 flags, 14 predictions, gray zone detection

## Planned Chapters

- [ ] **Payload Integration Patterns** — Mapping cameras, multispectral sensors, LiDAR, delivery mechanisms. Wiring, power, data flow, and the companion computer as integration hub.
- [ ] **Cellular / LTE for BVLOS** — When and how to use cellular modems for beyond-visual-line-of-sight. Hardware, SIM management, latency reality, regulatory considerations.
- [ ] **Fixed-Wing Specific** — Airspeed sensors, VTOL transitions, iNav vs ArduPilot for wings, long-range planning.
- [ ] **Fleet Management** — Managing 5-50 platforms. Configuration management, firmware versioning, battery tracking, maintenance schedules.
- [ ] **Power Systems Deep Dive** — Battery chemistry, BEC selection, power distribution boards, voltage sag under load, field charging.
- [ ] **Pattern Intelligence Methodology** — How PIE works: flag types, correlation engine, gray zone detection, supply chain forecasting methodology. Public-facing explanation of the intelligence pipeline.

## Planned Field Guides — "Stuff Nobody Has Written"

Operator-level quick references. Laminate-and-carry format. Each fills a gap where the knowledge exists only as tribal knowledge, scattered forum posts, or classified TTPs — nothing consolidated and public.

- [x] **EW Countermeasures Field Card** — `field/ew-countermeasures.md` — "I'm being jammed, now what?" Decision tree by symptom: video freeze, LQ drop, GPS drift, total blackout. Pre-configured firmware settings, band-switching procedures, abort criteria. The operator-level companion to `components/electronic-warfare.md`.
- [x] **Frequency Planning Worksheet** — `field/frequency-planning.md` — Multi-drone frequency deconfliction. Control link, video link, GPS across a 6-drone flight. Channel assignment templates, self-interference avoidance, band planning for contested environments.
- [x] **Supply Chain Substitution Guide** — `field/substitution-guide.md` — Drop-in component replacements mapped by pinout, protocol, mounting, and firmware compatibility. "My EP2 is out of stock — what fits?" Consolidated from scattered forum knowledge.
- [x] **Fiber-Optic FPV Integration** — `field/fiber-optic-fpv.md` — Spool integration, FC compatibility, cable management, spool motor wiring, weight/range tradeoffs. Both sides mass-producing, near-zero public documentation.
- [x] **Thermal / Night FPV Operations** — `field/night-ops.md` — Low-lux camera selection, IR illuminator integration, OSD config for night, cold-weather battery behavior, operational patterns. Pioneered by Wild Hornets, knowledge currently internal.
- [x] **Drone-to-Drone Intercept Playbook** — `field/intercept-ops.md` — FPV interceptor requirements (speed, approach angles, prop selection), video settings for tracking airborne targets. Wild Hornets Werewolf/Sting class. Zero public documentation exists.
- [x] **Repeater / Relay Deployment** — `field/repeater-relay.md` — Mother drones and fixed repeaters for FPV range extension. Antenna placement, link budget for relay hop, latency impact, when to relay vs fly closer. Generic guide for what TAF Kolibri 13 FR1 does.
- [x] **Attritable Drone Production Handbook** — `field/attritable-production.md` — Decentralized manufacturing at scale. Component sourcing, QC checklist for volume production, firmware flashing at scale, pre-flight batch testing for 50+ units. Process knowledge from 160+ Ukrainian manufacturers, currently tribal.
- [x] **ELINT for Drone Operators** — `field/elint-operators.md` — Reading spectrum analyzer output, identifying enemy video/control frequencies from SIGINT, correlating ELINT to threat assessment. Taught informally by Flash (Serhii Beskrestnov), never written down.

## Planned Appendices

- [ ] **Appendix A: Frequency Quick Reference Card** — One-page printable frequency plan template
- [x] **Appendix B: UART Maps for Common FCs** — 416 FCs mapped
- [ ] **Appendix C: MAVLink Message Quick Reference** — The 20 messages you actually use
- [ ] **Appendix D: MSP Function Code Quick Reference** — The 15 function codes you actually use
- [ ] **Appendix E: CoT Type Code Reference** — Common MIL-STD-2525C codes for drone operations

## Planned Templates

- [ ] Frequency plan worksheet (printable)
- [ ] UART allocation worksheet (printable)
- [ ] Pre-flight checklist card (laminated field card format)
- [ ] Link budget calculator (spreadsheet)
- [ ] Mesh network planning template

## Improvements to Existing Content

- [ ] Add diagrams for antenna radiation patterns (Ch 3)
- [ ] Add wiring diagrams for common FC-to-companion connections (Ch 13)
- [ ] Add mesh network topology diagrams (Ch 14)
- [ ] Add CoT message flow diagrams (Ch 15)
- [ ] Add blackbox trace screenshots with annotations (Ch 10)
- [ ] Wire new component docs into `build.py` navigation so they render on nvmilldoitmyself.com
- [ ] Cross-reference PIE flags from component docs where supply chain constraints are relevant

## Community Requests

*Open an issue to suggest additions to this roadmap.*
