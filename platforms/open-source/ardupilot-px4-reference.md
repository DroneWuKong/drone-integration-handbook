# Custom ArduPilot / PX4 Builds — General Integration Reference

> **Category:** Open-Source / Custom Build
> **Firmware:** ArduPilot or PX4 (open source)
> **Protocol:** MAVLink v2

---

## Overview

Any drone built on ArduPilot or PX4 firmware running Pixhawk-compatible hardware. This covers hundreds of commercial products (Freefly Astro, Inspired Flight IF1200, Watts Innovations Prism, Harris Aerial H6, CubePilot-based builds) and thousands of custom builds. The open-source ecosystem is the backbone of non-DJI drone integration.

---

## Common Flight Controllers

| Controller | Processor | IMUs | Notes |
|-----------|-----------|------|-------|
| Pixhawk 6X / 6X Pro (Holybro) | STM32H753 | 3x | Triple redundant, Ethernet, top tier |
| CubePilot Cube Orange+ | STM32H757 | 3x | Vibration-isolated, carrier board ecosystem |
| Matek H743 | STM32H743 | 2x | Compact, affordable, iNav/ArduPilot |
| SpeedyBee F405 | STM32F405 | 1x | Budget ArduPilot FC, smaller builds |
| ARK Electronics FMU | — | — | Blue UAS Framework listed, NDAA compliant |
| Auterion Skynode S | — | 3x | Blue UAS Framework, commercial PX4 |

---

## Key Integration Points

All ArduPilot/PX4 platforms share:

- **MAVLink v2** as the telemetry protocol
- **UART-based** peripheral connections (GPS, telemetry, RC, rangefinder)
- **PWM/DShot** motor outputs
- **I2C/SPI** sensor buses
- **USB** for configuration and companion computer
- **SD card** for logging and parameter storage

The handbook's chapters on UART layout (Ch 8), MAVLink (Ch 7), MSP (Ch 6), and companion computers (Ch 13) are written specifically for this ecosystem.

---

## Telemetry Radio Options

| Radio | Band | Bandwidth | Range | Notes |
|-------|------|-----------|-------|-------|
| SiK (3DR-style) | 915/433 MHz | ~64 kbps | 1–2 km | Simple, cheap, point-to-point |
| RFD900x | 900 MHz | Higher | 5–40 km | Configurable, long range |
| Doodle Labs Mesh Rider | Multi-band | High | 5–15 km | Mesh, EW-resistant, Blue UAS |
| Microhard P900 | 900 MHz | High | 10+ km | Robust, industrial |
| Herelink | 2.4 GHz | Integrated | 5–20 km | Video + telemetry + RC, Android GCS |

---

## Ground Control Stations

| GCS | Primary Firmware | Platform | Notes |
|-----|-----------------|----------|-------|
| Mission Planner | ArduPilot | Windows | Full-featured, parameter management |
| QGroundControl | PX4 (+ ArduPilot) | Cross-platform | Clean UI, PX4 default |
| Auterion Mission Control | PX4 (Auterion) | Skynode | Enterprise, fleet management |
| UgCS | Both | Desktop | Professional mission planning, 3D |
| MAVProxy | Both | CLI | Lightweight, scriptable |

---

## Common Commercial Platforms Using ArduPilot/PX4

- **Freefly Astro:** PX4 (Auterion), Blue UAS, mapping/inspection
- **Inspired Flight IF1200/IF800:** ArduPilot, Blue UAS, heavy-lift
- **Watts Innovations Prism:** Multi-payload, industrial
- **Harris Aerial H6:** Heavy-lift surveying/mapping
- **Aurelia Drones:** Industrial-grade, high payload
- **CubePilot-based custom builds:** Anything you can imagine

---

## The ArduPilot vs PX4 Decision

| Factor | ArduPilot | PX4 |
|--------|-----------|-----|
| Vehicle Support | Widest (copter, plane, heli, rover, sub, boat) | Broad (copter, plane, VTOL) |
| Community | Larger, more hobbyist/operator focus | Smaller, more developer/research focus |
| Documentation | Extensive, community-driven | Good, structured |
| Commercial Use | Widespread (IF1200, many custom builds) | Freefly Astro, Auterion ecosystem |
| Licensing | GPL v3 (copyleft) | BSD (permissive) |
| Default GCS | Mission Planner | QGroundControl |
| Configuration | More parameters, more flexibility, steeper curve | Modular, cleaner architecture |

Both speak MAVLink. Both run on Pixhawk. Both work. Pick based on your ecosystem and support needs.

---

## Integration Tips for Custom Builds

1. **Map your UARTs before you build.** See Chapter 8. You will run out.
2. **Separate RC and video bands.** 2.4 GHz RC + 5.8 GHz video, or 900 MHz RC + 5.8 GHz video. Never both on 2.4 GHz.
3. **CRSF protocol at 420000 baud** for ELRS/Crossfire RC links. Not 115200.
4. **MAVLink stream rates matter.** Too high floods the telemetry link. Start with SR0_POSITION=2, SR0_EXTRA1=4.
5. **Test failsafe before you need it.** Every firmware handles it differently. Know yours.
6. **Blackbox logging is your post-flight truth.** See Chapter 10.
7. **PID tune in the field, not in simulation.** See Chapter 11.

---

*Last updated: March 2026*
