# Part 5 — Platform References

Full integration profiles for drone platforms across four categories. Each profile documents what an operator or integrator actually needs to know: RF links, firmware stack, payload integration, SDK access, companion computer options, and the gotchas that don't appear in marketing material.

**Vetted parts only. No sales pitch. Operator truth.**

---

## Commercial Off-the-Shelf (COTS)

| Platform | NDAA | Firmware | MAVLink | Flight Time | Thermal |
|----------|------|----------|---------|-------------|---------|
| [DJI Matrice 350 RTK](cots/dji-m350-rtk.md) | NO | Proprietary | No | 55 min | Via Zenmuse |
| [DJI Matrice 30T](cots/dji-m30t.md) | NO | Proprietary | No | 41 min | 640×512 |
| [DJI Mavic 4 Pro](cots/dji-mavic4-pro.md) | NO | Proprietary | No | 46 min | No |
| [Autel EVO MAX 4T V2](cots/autel-evo-max-4t.md) | XE only | Proprietary | No | 42 min | 640×512 |
| [Autel EVO II Enterprise V3](cots/autel-evo2-enterprise.md) | Check | Proprietary | No | 42 min | 640×512 |
| [DJI Agras T50](cots/dji-agras-t50.md) | NO | Proprietary | No | N/A (ag) | No |
| [DJI FlyCart 30](cots/dji-flycart-30.md) | NO | Proprietary | No | 29 min | No |
| [Flyability Elios 3](cots/flyability-elios-3.md) | No | Proprietary | No | 12–17 min | Radiometric |

## NDAA-Compliant / Blue UAS / Green UAS

| Platform | Blue UAS | Firmware | MAVLink | Flight Time | Thermal |
|----------|----------|----------|---------|-------------|---------|
| [Skydio X10 / X10D](blue-uas/skydio-x10.md) | X10D | Proprietary | X10D only | 40 min | Boson+ 640 |
| [Freefly Astro](blue-uas/freefly-astro.md) | YES | PX4 | Yes | 25 min | Via payload |
| [Inspired Flight IF1200A](blue-uas/inspired-flight-if1200a.md) | YES | ArduPilot | Yes | 43 min | Via payload |
| [Teal 2](blue-uas/teal-2.md) | YES | Proprietary | No | 30 min | Hadron 640R |
| [Parrot ANAFI USA](blue-uas/parrot-anafi-usa.md) | YES | Proprietary | No | 32 min | Boson 320 |
| [WingtraOne GEN II / WingtraRAY](blue-uas/wingtra-wingtraone.md) | YES | Proprietary | No | 59 min | Via sensor |

## Open-Source / Custom Build

| Platform | Firmware | MAVLink | Flight Time | Notes |
|----------|----------|---------|-------------|-------|
| [Holybro X500 V2 + Pixhawk 6X](open-source/holybro-x500-pixhawk6x.md) | PX4/ArduPilot | Yes | 18 min | Reference dev kit |
| [Custom ArduPilot / PX4 Builds](open-source/ardupilot-px4-reference.md) | PX4/ArduPilot | Yes | Varies | General integration reference |

## Tactical / Defense / PS-LE

| Platform | Blue UAS | Availability | Endurance | Notes |
|----------|----------|-------------|-----------|-------|
| [Anduril Ghost X](tactical/anduril-ghost-x.md) | YES | Govt/Mil only | 80–90 min | Helicopter-type, Lattice AI |
| [Teal Black Widow](tactical/teal-black-widow.md) | YES | Govt/Mil only | Classified | SRR Tranche 2 winner |
| [Skyfish Osprey](tactical/skyfish-osprey.md) | NDAA | Commercial | 45 min | Precision mapping/ISR |
| [SiFly Q12](tactical/sifly-q12.md) | NDAA | Commercial | Extended | Endurance-focused |

---

## Blue UAS Framework Components (2025)

Key NDAA-compliant components cleared under the Blue UAS Framework:

- **Flight Controllers:** ARK Electronics FMU
- **ESCs:** Vertiq Electronic Speed Control
- **GNSS:** Locus Lock GNSS receiver
- **Remote ID:** Pierce Aerospace B1 Beacon
- **Radios:** Mobilicom Skyhopper PRO/Lite, Doodle Labs Wi-Fi transceivers, UVX Swappable Radio Module
- **Compute:** Auterion Government Solutions Skynode S
- **Cameras:** RPX Technologies EmbIR
- **Autonomy:** Athena AI Computer Vision, SensorOps SynDOJO
- **Connectivity:** TILT Autonomy Lightweight Starlink PoE

Platforms with ATO from 2025 Blue UAS Challenge (29 Palms): Neros Archer (FPV), Hoverfly Spectre (tethered), Zone 5 Paladin.

The Blue UAS program transitioned from DIU to DCMA in December 2025.

---

## Platforms Not Yet Profiled

Worth investigating for future additions:

- DJI Matrice 400, DJI FlyCart 100 (heavy-lift delivery)
- Watts Innovations Prism, Harris Aerial H6
- Ascent Aerosystems (coaxial platforms)
- Flyability ELIOS (confined space)
- Hoverfly LiveSky (tethered)
- AgEagle/senseFly eBee X (fixed-wing mapping)
- Wingtra WingtraOne (VTOL mapping)
- JOUAV CW-25E (VTOL hybrid)
- Shield AI Nova 2 (autonomous indoor ISR)
- Neros Archer (Blue UAS FPV)
- AeroVironment Puma / Switchblade family
- L3Harris FVR-90 (VTOL fixed-wing)

*Open an issue or PR to contribute a platform profile. See [CONTRIBUTING.md](../CONTRIBUTING.md).*
