# C2 Datalinks

> **Forge cross-reference:** 13 entries in `c2_datalinks` category  
> **Related handbook chapters:** Ch. 2 (Frequency Bands), Ch. 5 (Five Link Types), Comms & Datalinks, Mesh Radios

## What C2 Datalinks Do

Command and Control (C2) datalinks carry the mission-critical telemetry and commands between a ground operator and the drone. Unlike FPV video links (high bandwidth, loss-tolerant) or mesh radios (peer-to-peer, swarm-oriented), C2 datalinks prioritize reliability and deterministic latency. If the C2 link drops, the drone must execute a failsafe — return to launch, hold position, or land.

For BVLOS operations, the FAA requires a "reliable C2 link" as a condition of waiver approval. This has created a distinct hardware category separate from hobby-grade RC links like ELRS or Crossfire.

## Key Specifications

- **Frequency band** — Determines range, interference profile, and regulatory requirements. Most C2 links operate in 900 MHz ISM (US), 2.4 GHz ISM, or the dedicated 5030–5091 MHz CNPC (Command and Non-Payload Communications) C-Band reserved for UAS by the ITU.
- **Range** — Measured in line-of-sight (LOS) and non-line-of-sight (NLOS). Tactical MANET radios like Silvus claim 60+ km LOS; aviation-grade links like uAvionix microLink target 50+ km at certified power levels.
- **Latency** — Sub-100ms is typical for telemetry; sub-50ms is required for real-time manual control at range. MANET radios add hop latency in mesh configurations.
- **Throughput** — C2 telemetry itself is low-bandwidth (MAVLink at 10–50 kbps). Many C2 links also carry video, pushing bandwidth requirements to 2–20 Mbps.
- **Encryption** — AES-256 is standard for defense applications. Some links support Type-1 or FIPS 140-2/3 for classified operations.
- **SWaP** — Size, Weight, and Power. Group 1 UAS (<20 lbs) need radios under 100g and 5W. Group 2+ platforms can accommodate larger units.

## The Landscape

### Aviation-Grade (Certified / BVLOS-Focused)

- **uAvionix microLink** — FCC and IC approved 900 MHz C2 radio built specifically for BVLOS operations. Designed for integration with uAvionix ping200X transponder for a complete airspace-compliant package. The closest thing to a "certified" C2 link for commercial BVLOS in the US.
- **uAvionix muLTElink-5060** — Multi-datalink Airborne Radio System combining CNPC C-Band (5030–5060 MHz) with LTE cellular backup. Implements the Link Executive Manager concept from ASTM F3002 — automatically switches between radio and cellular based on link quality. Dual-redundant C2 in one box.

### Tactical MANET (Military / Defense)

- **Silvus StreamCaster SC4200EP** — 2×2 MIMO tactical MANET radio used across DoD UAS programs. Carries C2, video, and telemetry simultaneously in a single waveform. Self-forming, self-healing mesh. AES-256 encryption. The default C2 link for many Blue UAS platforms.
- **Silvus StreamCaster Lite SL5200** — Ultra-low SWaP version of the SC4200 designed for Group 1 UAS. Same MANET waveform and encryption in a form factor small enough for 5-inch FPV platforms.
- **L3Harris AMORPHOUS** — Swarm-optimized C2 system designed for controlling multiple autonomous platforms from a single operator station. Purpose-built for the multi-vehicle use case that standard MANET radios bolt onto.
- **XTEND XOS** — Software-defined C2 platform that abstracts the radio layer, allowing mission planning and vehicle control across heterogeneous link types.
- **Shield AI Hivemind** — AI-powered autonomy stack with integrated C2. Not just a radio — it includes the autonomy layer that decides what to do when C2 is degraded or denied.
- **PDW Blackwave** — Tactical waveform designed for contested electromagnetic environments.

### Integrated Systems (C2 + Video + GCS)

- **CubePilot Herelink V1.1** — All-in-one 2.4 GHz system with HD video transmission, C2 datalink, and Android-based ground controller. Integrated touchscreen GCS with QGroundControl preinstalled. 20 km range. Popular for commercial and research platforms where a single-box solution is preferred over separate C2 and video links.
- **Ultra (formerly dTEC) ADSI Gateway** — Airspace Deconfliction and Situational Integration gateway. Not a radio itself but a C2 middleware that connects drone C2 links to the broader military airspace management system.
- **DTC BluSDR/SOL8SDR** — Software-defined radios that can be configured for C2, video, or general-purpose tactical communications. Flexible but require RF engineering expertise to configure properly.
- **Kutta Technologies KGS** — GCS integration platform that bridges drone C2 links to military C4ISR networks (TAK, ATAK, JBC-P).

## Frequency Planning

C2 links must be planned alongside all other RF systems on the platform. See the Frequency Bands chapter for the complete deconfliction framework. Key considerations:

- 900 MHz C2 (microLink) conflicts with 900 MHz ELRS — cannot run both simultaneously
- 2.4 GHz C2 (Herelink) conflicts with 2.4 GHz ELRS, Wi-Fi, and some video links
- CNPC C-Band (5030–5091 MHz) is the only spectrum reserved exclusively for UAS C2 — no conflict with other drone subsystems, but requires specific authorization
- Silvus MANET radios are frequency-agile (can operate across wide bands) but must be coordinated with other MANET users in the battlespace

## NDAA and Blue UAS Considerations

Silvus and uAvionix are both US-manufactured and Blue UAS compatible. CubePilot Herelink is manufactured in China (HEX/ProfiCNC) — it is not NDAA-compliant and should not be used on defense programs despite its popularity in commercial applications.

For Blue UAS programs requiring C2 links, the practical options are Silvus, uAvionix, L3Harris, or purpose-built links from the platform manufacturer (e.g., Shield AI, Skydio).
