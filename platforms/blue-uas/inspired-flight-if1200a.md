# Inspired Flight IF1200A

> **Category:** NDAA-Compliant / Blue UAS
> **NDAA Status:** Blue UAS certified, NDAA compliant, Green UAS certified
> **Manufacturer:** Inspired Flight Technologies (San Luis Obispo, CA) — Made in USA

---

## Overview

Heavy-lift hexacopter developed to U.S. Air Force standards. The workhorse of the NDAA-compliant drone world. Carries large payloads (LiDAR, EO/IR, Phase One cameras) with 43-minute endurance. Open payload interface. ArduPilot-based. SAFE motor-out redundancy keeps flying if a motor fails.

---

## Specs

| Spec | Value |
|------|-------|
| Configuration | Hexacopter (coaxial dual-prop) |
| Max Payload | 19.1 lb (8.66 kg) under Part 107; 28.7 lb with certification |
| Max Flight Time | 43 min (no payload) |
| Real-World with 8 lb Payload | 30+ min |
| Max Speed | 56 mph (25 m/s) |
| Wind Resistance | 29 knots |
| Batteries | 16000mAh intelligent batteries |
| GPS | Dual GPS units |
| FPV | Built-in FPV camera |
| Remote ID | Integrated |

---

## RF Links

- **C2/Video:** Doodle Labs or similar NDAA-compliant radio
- **GCS:** GS-ONE ground control station (integrated controller + display)
- **Protocol:** MAVLink v2
- **Telemetry:** Standard MAVLink telemetry stream

---

## Firmware & Software

- **Firmware:** ArduPilot-based
- **GCS:** Mission Planner, QGroundControl
- **Flight Modes:** Position Hold, Loiter, Auto, Return-to-Launch
- **Open system architecture** — configurable for specific missions

---

## Payload Integration

Universal payload interface supports:

- **EO/IR:** FLIR, L3Harris
- **LiDAR:** Yellowscan, RIEGL, Velodyne
- **Optical Imaging:** Phase One, Sony
- **Multispectral:** Sentera 6X series
- **Payload adapter guides** available from Inspired Flight

---

## Gotchas

1. **Heavy platform — not backpackable.** This is a truck drone, not a backpack drone.
2. **Folding arms can be stiff after flight** — thrust loads the locking mechanism. Support the arm bottom with upward force while sliding the lock.
3. **Requires Part 107 waiver** if total weight (aircraft + payload) exceeds 55 lb.
4. **Batteries are proprietary.**
5. **No integrated camera** — payload must be purchased separately. Budget accordingly.
6. **SAFE motor-out capability** is a lifesaver for expensive payloads but requires pilot awareness — land promptly when alerted.

---

## When to Use This Platform

The IF1200A is the platform when you need to carry heavy sensors (LiDAR, Phase One, EO/IR) with NDAA/Blue UAS compliance. Nothing else in the Blue UAS ecosystem comes close on payload capacity. ArduPilot firmware means full MAVLink access and Mission Planner compatibility.

---

*Last updated: March 2026*
