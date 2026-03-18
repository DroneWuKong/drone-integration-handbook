# Autel Robotics EVO MAX 4T V2

> **Category:** Commercial Off-the-Shelf (COTS)
> **NDAA Status:** XE variant is NDAA compliant; standard V2 has mixed sourcing
> **Manufacturer:** Autel Robotics (Bothell, WA / Shenzhen assembly)

---

## Overview

Autel's flagship enterprise drone and the most direct competitor to the DJI M30T. Quad-sensor gimbal (wide, zoom, thermal, laser rangefinder), GPS-denied flight via SLAM, A-Mesh drone-to-drone networking, and **no geofencing**. Positioned as the go-to DJI alternative for public safety and inspection operators.

---

## Specs

| Spec | Value |
|------|-------|
| Weight | ~1.185 kg (2.61 lb) takeoff |
| Max Flight Time | 42 min |
| Max Speed | 23 m/s |
| Service Ceiling | 23,000 ft |
| Wind Resistance | 27 mph |
| IP Rating | IP43 |
| Operating Temp | -20°C to 50°C (-4°F to 122°F) |

### Sensors

| Sensor | Spec |
|--------|------|
| Wide Camera | 50MP 1/1.28″ CMOS, f/1.9, 85° DFOV |
| Zoom Camera | 48MP, 10x optical / 160x hybrid zoom, 8K |
| Thermal | 640×512, 13mm, 16x digital zoom, -20°C to 550°C |
| Laser Rangefinder | 5–1200 m, ±1 m accuracy |
| Obstacle Avoidance | 720° — binocular vision + mmWave radar |

---

## RF Links

### SkyLink 3.0

- **Antennas:** 6 (4 tx, 6 rx)
- **Frequency Bands:** 900 MHz, 2.4 GHz, 5.2 GHz, 5.8 GHz — adaptive frequency hopping
- **Range:** 20 km (12.4 mi) — FCC
- **Video Quality:** 1080p/60fps, <150ms latency
- **Encryption:** AES-256 full-link
- **Cellular:** Optional 4G dongle
- **A-Mesh 1.0:** Drone-to-drone autonomous communication — drones relay comms and extend network coverage without ground infrastructure

### Frequency Restrictions

- 5.2 GHz only available in FCC, CE, UKCA regions
- 900 MHz only available in FCC regions

---

## Firmware & Software

- **GCS:** Autel Enterprise App (Android, on Smart Controller V3)
- **Firmware:** Proprietary, OTA updates
- **SDK:** UX SDK (iOS/Android), Payload SDK for third-party mounts
- **No MAVLink, no QGroundControl**
- **Data stays local** — no mandatory cloud connection, no cloud upload unless operator enables it

---

## Autonomy & GPS-Denied Flight

- **Autel Autonomy Engine:** Real-time 3D scene reconstruction and autonomous path planning
- **GNSS-Denied Navigation:** SLAM-based visual navigation for indoors, underground, urban canyons
- **AI Target Detection:** Auto-identify and lock onto heat sources, people, vehicles
- **Mission Reproduction:** Fly once manually, the drone replays the exact mission autonomously
- **Triple Anti-Jamming:** RFI, EMI, and GPS spoofing countermeasures

---

## Payload Integration

- **Integrated quad-sensor gimbal — not swappable**
- Payload SDK interface for accessories (loudspeaker, spotlight, RTK module)
- RTK module available for cm-level positioning
- Compatible with EVO Nest for automated remote operations

---

## Gotchas

1. **No geofencing** — good for operators who need flexibility, but means no built-in airspace safety net. Know your airspace.

2. **NDAA compliance depends on variant.** The XE model is purpose-built for compliance. The standard V2 may contain restricted components. Ask your dealer specifically about the XE if compliance matters.

3. **A-Mesh requires multiple Autel aircraft.** No cross-manufacturer mesh networking.

4. **Smart Controller V3 is proprietary** — no third-party controller support.

5. **Integrated gimbal means no payload swap.** If you need LiDAR, this is the wrong platform.

6. **900 MHz band only in FCC regions.** International operators lose a frequency band.

---

## When to Use This Platform

The MAX 4T V2 is the strongest DJI M30T competitor for public safety and inspection. The quad-sensor gimbal, GPS-denied flight, and A-Mesh networking give it capabilities DJI doesn't offer. No geofencing is a feature, not a bug, for operators who know what they're doing. The XE variant solves the NDAA question for agencies that need it.

---

*Last updated: March 2026*
