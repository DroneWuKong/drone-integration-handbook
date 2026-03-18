# Holybro X500 V2 + Pixhawk 6X (PX4 Dev Kit)

> **Category:** Open-Source / Custom Build
> **NDAA Status:** NOT compliant (Chinese-sourced components)
> **Manufacturer:** Holybro (Shenzhen, China)

---

## Overview

The reference development platform for PX4 and ArduPilot. Carbon fiber frame with no-solder assembly. Ships with Pixhawk 6X (or 6C), M10 GPS, and SiK telemetry radio. Mounts for Raspberry Pi, Jetson Nano, and Intel RealSense depth cameras.

**If you want to understand every layer of the drone integration stack, this is where you start.** Every UART is documented. Every protocol is open. Every parameter is tunable. The handbook's chapters on UART layout, MAVLink, PID tuning, and companion computers were written with platforms like this in mind.

---

## Specs

| Spec | Value |
|------|-------|
| Frame | Carbon fiber twill, 500mm class |
| Flight Controller | Pixhawk 6X (STM32H753 H7, triple IMU, Ethernet) or Pixhawk 6C |
| Firmware | PX4 (ships default) / ArduPilot compatible |
| GPS | Holybro M10 (requires PX4 1.14+ / ArduPilot 4.3+) |
| Telemetry | SiK radio (915 MHz or 433 MHz), plug-and-play |
| Flight Time | ~18 min hover (no payload, 5000mAh 4S) |
| Payload Capacity | ~1.5 kg (at 70% throttle) |
| Companion Mount | RPi 4, Jetson Nano, Intel RealSense |
| Assembly Time | ~30 min, no soldering |

---

## RF Links

### Link 1 — RC Control

Add your own. Any standard RC receiver via UART:
- ELRS 2.4 GHz or 900 MHz (CRSF protocol, UART, 420000 baud)
- TBS Crossfire (CRSF)
- FrSky (SBUS)
- FlySky (IBUS)

### Link 2 — Telemetry

- **SiK radio:** 915 MHz (Americas) or 433 MHz (EU/Asia), MAVLink, ~64 kbps, point-to-point
- Connects to Mission Planner or QGroundControl on ground station

### Link 3 — Video

Add your own:
- Analog 5.8 GHz VTX
- DJI O3 Air Unit / HDZero (for FPV)
- IP camera via companion computer (RPi + camera module)
- No integrated video link — build-your-own

---

## Firmware & Software

- **PX4 or ArduPilot** — both fully open source
- **GCS:** QGroundControl (PX4 default) or Mission Planner (ArduPilot default)
- **Protocol:** MAVLink v2 — full parameter access, mission upload, telemetry streaming
- **Simulation:** PX4 SITL for testing before flight
- **Pixhawk 6X Ethernet** interface for high-speed companion computer integration

---

## Pixhawk 6X Flight Controller Details

| Feature | Spec |
|---------|------|
| Processor | STM32H753 (Arm Cortex-M7 @ 480 MHz) |
| Flash / RAM | 2MB / 1MB |
| IMUs | 3x (triple redundant, isolated sensor domains) |
| Barometers | 2x |
| Interfaces | Multiple UART, I2C, SPI, CAN, ADC, Ethernet |
| Vibration Isolation | Custom-formulated durable material |
| Temperature Control | On-board heating for IMU temp stability |
| Connector Standard | Pixhawk Autopilot Bus (100-pin + 50-pin) |
| Debug | Pixhawk Debug Full (JST SM10B) |

---

## Companion Computer Integration

The X500 V2 has mounting holes and platform board space for:

- **Raspberry Pi 4:** Standard mount, USB connection to Pixhawk
- **NVIDIA Jetson Nano:** Direct mount on platform board
- **Intel RealSense:** Depth camera mount on rail system (D435, T265)
- **Pixhawk 6X Ethernet:** High-speed connection for data-intensive applications

Communication: MAVLink via serial UART or USB. MAVSDK / DroneKit for programmatic control.

---

## Gotchas

1. **18-minute flight time is short.** Bigger batteries help but add weight. Budget for multiple batteries.
2. **No obstacle avoidance out of the box.** Add Intel RealSense + PX4 avoidance module if needed.
3. **No weatherproofing.** This is a fair-weather development platform.
4. **SiK radios are low-bandwidth** (~64 kbps). Fine for MAVLink telemetry, not for video.
5. **Pixhawk 6X PM02D-HV power module** requires firmware setting (`SENS_EN_INA228`) and ArduPilot 4.4+.
6. **M10 GPS** needs PX4 1.14+ or ArduPilot 4.3+. Older firmware won't see it.
7. **Chinese-sourced components — not NDAA compliant.** For federal work, look at ARK Electronics FC + U.S.-sourced components.

---

## Why This Platform Matters

This is the teaching platform. Every concept in the handbook — the five link types, UART allocation, MAVLink telemetry, PID tuning, companion computers, mesh radios — can be implemented, tested, and understood on an X500. It's not the best at anything, but it teaches you everything.

---

*Last updated: March 2026*
