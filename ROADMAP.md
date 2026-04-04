# Roadmap

Future chapters, sections, and improvements under consideration.
Open an issue to suggest additions or volunteer to write one.

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
