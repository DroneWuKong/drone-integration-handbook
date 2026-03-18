# Freefly Astro (Astro Max)

> **Category:** NDAA-Compliant / Blue UAS
> **NDAA Status:** Blue UAS certified (NDAA-compliant build available)
> **Manufacturer:** Freefly Systems (Woodinville, WA) — Made in USA

---

## Overview

American-made, open-architecture mapping and inspection drone built on PX4. Running Auterion Enterprise PX4 on a Skynode flight controller with triple-redundant IMUs. Blue UAS certified. Swappable payload via Smart Dovetail system. The Astro Max variant carries the 61MP Sony LR1 full-frame sensor. Over 100,000 commercial flights logged.

**This is the open-source success story.** PX4-based, MAVLink-native, with a real payload ecosystem and federal compliance.

---

## Specs

| Spec | Value |
|------|-------|
| Weight | ~2.3 kg (varies with payload) |
| Max Flight Time | 25 min with LR1 payload, 30 min with 2 lb payload |
| Payload Capacity | 2 lb (0.9 kg) |
| Flight Controller | Auterion Skynode (Pixhawk-class) |
| Firmware | Auterion Enterprise PX4 |
| IMU Redundancy | Triple-redundant |
| GNSS | Multi-band with RTK (NTRIP or base station) |
| Connectivity | LTE via AuterionOS, Doodle Labs RF link |
| Controller | Pilot Pro (ruggedized, hot-swap power) |
| Folded Size | ~390 × 178 mm — fits in a backpack |
| Batteries | Dual SL8-Air, 500+ cycle guarantee |

---

## RF Links

### Primary C2/Video

- **Radio:** Doodle Labs (NDAA compliant)
- **Protocol:** MAVLink v2 native
- **Encryption:** AES

### Backhaul

- **LTE:** Via Auterion Skynode — cloud connectivity, OTA updates, fleet management
- **Telemetry:** SiK-compatible for development environments

---

## Firmware & Software

- **Firmware:** Auterion Enterprise PX4 (open-source based, commercially supported)
- **GCS:** Auterion Mission Control (pre-installed)
- **Compatible GCS:** QGroundControl, UgCS, Esri SiteScan (validated)
- **Other PX4 GCS:** Works but not officially tested
- **Fleet Management:** AuterionOS provides predictive maintenance, geotagging, OTA updates
- **Auterion SDK:** For enterprise developers

This is a real PX4 platform. You get MAVLink. You get open parameters. You get QGC compatibility. But you also get commercial support, LTE connectivity, and fleet management that you won't get from a DIY Pixhawk build.

---

## Payload Integration

### Smart Dovetail System

Tool-less payload swap — slide on, lock, fly. Proprietary mechanical interface but open electrical/data bus.

### Native Payloads

- **Sony LR1:** 61MP full-frame — the Astro Max flagship sensor
- **Sony A7R IV:** 60MP (previous gen)
- **Various mapping payloads:** Third-party sensors via Smart Dovetail adapter
- **Thermal, LiDAR:** Via adapter — check Freefly for current payload catalog

---

## Gotchas

1. **25-minute flight time is shorter than competitors.** DJI M350 does 55 min. Inspired Flight IF1200A does 43 min. If endurance is critical, factor this in.

2. **Smart Dovetail is proprietary.** Third-party payloads need an adapter. Freefly's payload ecosystem is good but not as deep as DJI's gimbal lineup.

3. **NDAA/Blue build ships with GPS logging disabled by default.** You must enable it in settings before your first mapping mission or you'll get untagged imagery.

4. **Freefly keeps some PX4 code closed** — motor drives, autonomy, avoidance. The core flight stack is open, but not everything.

5. **Dual SL8-Air batteries are proprietary.** Guaranteed 500+ cycles, but no third-party alternatives exist.

6. **Network RTK requires Auterion licence (~$1,200)** for NTRIP caster access. Base-station RTK works with any multi-band GNSS base.

---

## When to Use This Platform

The Freefly Astro is the right choice when you need: Blue UAS compliance + open MAVLink + real payload flexibility + commercial support. It's the platform that proves you don't have to choose between open-source and enterprise readiness.

Best for: precision mapping, photogrammetry, inspection, agriculture. Not ideal for: long-endurance surveillance (25 min limit), heavy-lift (2 lb max), or thermal-primary missions (need to add thermal as a payload).

---

*Last updated: March 2026*
