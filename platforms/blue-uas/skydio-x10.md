# Skydio X10 / X10D

> **Category:** NDAA-Compliant / Blue UAS
> **NDAA Status:** X10 is NDAA compliant; X10D is Blue UAS listed
> **Manufacturer:** Skydio (San Mateo, CA) — Made in USA

---

## Overview

Skydio's flagship AI-autonomous drone. The X10 is the commercial/public safety variant; the X10D is the defense variant with hardened comms, MAVLink support, and RAS-A compliance. Both feature six navigation cameras, NVIDIA Jetson Orin GPU, and the industry's most capable obstacle avoidance. Best-in-class autonomy. Built in the USA.

---

## Specs

| Spec | Value |
|------|-------|
| Weight | <4.7 lb (2.13 kg) |
| Max Flight Time | ~40 min |
| Max Speed | 45 mph (20 m/s) |
| Processors | NVIDIA Jetson Orin + Qualcomm QRB5165 |
| Nav Cameras | Six 32MP custom cameras (360° coverage) |
| Encryption | AES-256 |
| IP Rating | IP55 |
| GNSS | GPS, GLONASS, Galileo, BeiDou + ADS-B In receiver |
| Deployment | Folds to 13.8″, sub-40 second launch |
| Modular Payload | 4 attachment bays, 340g max |

### Sensor Packages (choose at purchase)

| Package | Wide | Narrow | Thermal | Telephoto |
|---------|------|--------|---------|-----------|
| VT300-L | 50MP 1″ f/1.95 | 64MP 1/1.7″ f/1.8 | FLIR Boson+ 640×512 | — |
| VT300-Z | 50MP 1″ f/1.95 | 64MP 1/1.7″ f/1.8 | FLIR Boson+ 640×512 | 48MP 190mm f/2.2 (128x zoom) |
| V100-L | 50MP 1″ f/1.95 | 64MP 1/1.7″ f/1.8 | — (LED flashlight) | — |

---

## RF Links

### X10 (Commercial)

- WiFi-based control/video link
- 5G/LTE unlimited range via Connect Fusion (optional)
- AES-256 encrypted

### X10D (Defense)

- Dedicated defense comms (Doodle Labs Mesh Rider radio options)
- RAS-A v1.2 compliant
- **Open MAVLink protocol** for third-party GCS
- Multi-band operation

Both variants support Remote Ops for browser-based remote piloting from any location, and DFR Command for drone-as-first-responder workflows.

---

## Firmware & Software

- **Firmware:** Proprietary Skydio Autonomy software
- **X10 Controller:** Skydio Flight Deck ONLY — no third-party controller support
- **X10D:** MAVLink support, QGroundControl compatible, third-party GCS
- **SDKs:**
  - Cloud API — mission planning, fleet management, media sync
  - Extend API — workflow integration (evidence management, inspection platforms)
  - Mobile SDK — Android apps on controller
  - Attachment ICD — custom payload mechanical/electrical specs

---

## Autonomy

This is where Skydio leads the industry:

- **GPS-denied navigation** via visual-inertial odometry — flies in parking garages, under bridges, inside structures
- **NightSense:** Zero-light autonomous flight using visible or IR illumination (X10D)
- **Subject Tracking (Shadow):** Maintains lock on people/vehicles even through brief occlusions
- **Scout:** Autonomous overwatch mode
- **Map Capture:** 2D orthomosaic generation
- **Onboard 3D Modeling:** Low-res 3D preview on-device for field decisions
- **Anchor Points:** GPS-denied return-to-home via visual reference placement
- **Crosshair Coordinates:** Identify POI coordinates from air

---

## Attachments

- Parachute — safety fallback for operations over people
- NightSense Visible/IR Light — zero-light autonomous flight
- Spotlight — nighttime visibility
- Speaker — communicate in high-risk situations
- RTK/PPK — precision mapping
- Dropper (planned) — payload release
- Connect Fusion+ (coming) — second cellular connection

---

## Gotchas

1. **X10 (commercial) is locked to Skydio software.** No MAVLink, no QGC, no Mission Planner. If you need open protocol access, you need the X10D — which costs more and requires government/defense procurement.

2. **Attachment bays limited to 340g total.** No heavy payloads. This is not a mapping drone with a LiDAR rig.

3. **No swappable primary sensor.** You pick VT300-L, VT300-Z, or V100-L at purchase. Want a different sensor package? Buy another drone.

4. **LTE connectivity requires active cellular plan.** Remote Ops is browser-based but needs internet on both ends.

5. **Thermal on VT300-L/Z is FLIR Boson+ 640×512** — excellent sensitivity (<30mK) but verify radiometric measurement support on your firmware version.

6. **10x more computing power than previous gen** means higher power draw — the 40-minute flight time reflects this.

---

## When to Use This Platform

Best autonomous flight in the industry, period. If your mission requires flying in GPS-denied environments, around obstacles, at night, or with minimal pilot training, Skydio X10 is the answer. The X10D is the only Blue UAS platform with this level of autonomy.

Not the right platform for heavy-lift mapping, LiDAR, or custom payload integration. For that, look at Freefly Astro or Inspired Flight IF1200A.

---

*Last updated: March 2026*
