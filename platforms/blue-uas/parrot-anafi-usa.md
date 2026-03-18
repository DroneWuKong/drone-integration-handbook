# Parrot ANAFI USA

> **Category:** NDAA-Compliant / Blue UAS
> **NDAA Status:** Blue UAS listed
> **Manufacturer:** Parrot (Paris, France) — NDAA Compliant

---

## Overview

One of the lightest enterprise drones on the market at 500g. French-designed. Triple-sensor payload (32x zoom, wide, FLIR thermal). GOV and MIL variants. The MIL version adds a Microhard radio for extended comms. ISO9001 certified manufacturing.

---

## Specs

| Spec | Value |
|------|-------|
| Weight | 500g (GOV) / 1.16 kg (MIL with Microhard) |
| Max Flight Time | 32 min |
| Max Speed | 14.7 m/s (33 mph) |
| Cameras | 32x zoom (21MP), wide (48MP), FLIR Boson 320 thermal |
| Encryption | AES-XTS 256-bit |
| Video Output | RTSP via Ethernet from Skycontroller |
| Transmission | Wi-Fi 802.11 a/b/g/n (GOV); + Microhard radio (MIL) |

---

## RF Links

- **GOV version:** Wi-Fi based control/video via Skycontroller
- **MIL version:** Adds Microhard radio for longer range and better RF penetration
- **Video sharing:** RTSP stream via Ethernet (RJ45) to VLC-equipped PC, or via FFmpeg
- **Fly-by-coordinates:** GPS coordinate display and sharing for any visible POI

---

## Firmware & Software

- **App:** FreeFlight 6 Enterprise
- **SDK:** Open Flight SDK for developer integration
- **No MAVLink**

---

## Gotchas

1. **Wi-Fi link on GOV version is range-limited** and susceptible to interference in dense RF environments.
2. **Small thermal sensor** — FLIR Boson 320 vs competitors at 640×512. Adequate for detection, not ideal for detailed thermal analysis.
3. **No payload swap.** The integrated sensor package is all you get.
4. **Lightweight is a double-edged sword** — extremely portable, but poor wind resistance.
5. **Parrot's enterprise support** has historically been inconsistent compared to DJI/Autel/Skydio.

---

## When to Use This Platform

Ultra-portable Blue UAS recon. When you need the smallest possible compliant drone with thermal capability. The MIL variant with Microhard is the more serious option for government work. Not a primary inspection or mapping platform.

---

*Last updated: March 2026*
