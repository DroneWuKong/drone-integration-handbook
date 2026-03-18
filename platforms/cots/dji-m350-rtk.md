# DJI Matrice 350 RTK

> **Category:** Commercial Off-the-Shelf (COTS)
> **NDAA Status:** NOT compliant — banned from U.S. federal procurement as of Dec 2025 (American Security Drone Act)
> **Manufacturer:** DJI (Shenzhen, China)

---

## Overview

The DJI M350 RTK is DJI's flagship enterprise platform and the successor to the M300 RTK. It is the most widely deployed commercial drone for inspection, mapping, and public safety worldwide. Closed ecosystem, but deep third-party payload support via E-Port and Payload SDK.

---

## Specs

| Spec | Value |
|------|-------|
| Weight (no payload) | ~3.77 kg (8.31 lb) |
| Max Takeoff Weight | 9.2 kg (20.3 lb) |
| Max Payload | 2.73 kg (6.01 lb) — triple gimbal support |
| Max Flight Time | 55 min (no payload, no wind) |
| Max Speed | 23 m/s (51.5 mph) |
| Max Altitude | 7000 m (with high-altitude propellers) |
| IP Rating | IP55 |
| Operating Temp | -20°C to 50°C |
| RTK Positioning | 1 cm + 1 ppm (H) / 1.5 cm + 1 ppm (V) |

---

## RF Links

### Link 1 — Control & Video (Combined)

- **System:** DJI O3 Enterprise transmission
- **Frequencies:** 2.4 GHz / 5.8 GHz (auto-switching)
- **Max Range:** 20 km (FCC) / 8 km (CE)
- **Video Downlink:** 1080p/30fps to DJI RC Plus controller
- **Dual Operator:** Supported — pilot + payload operator on separate controllers
- **Cellular Backup:** Optional 4G dongle for cellular C2

### Link 2 — Telemetry

- **Protocol:** Proprietary DJI protocol — **no native MAVLink**
- **Access:** Telemetry data available via DJI MSDK / Cloud API for third-party GCS integration
- **Fleet Management:** DJI FlightHub 2

---

## Firmware & Software

- **Firmware:** Proprietary DJI firmware
- **Updates:** DJI Pilot 2 app (OTA or offline SD card), or DJI Assistant 2 (Enterprise Series) via USB
- **GCS:** DJI Pilot 2 (Android, on RC Plus)
- **Third-Party GCS:** DroneSense, Pix4Dcapture, DJI FlightHub 2 — all via Mobile SDK
- **No QGroundControl or Mission Planner support**

---

## Payload Integration

- **Gimbal Mounts:** 3 — single upward + dual downward
- **Native Payloads:** Zenmuse H30/H30T, H20/H20T/H20N, L2, L1, P1, S1, V1
- **Third-Party Payloads:** Skyport V2 adapter or E-Port
- **E-Port:** UART, USB, SDK API, 24V power — replaces the old Onboard SDK port
- **DJI X-Port:** For lightweight third-party gimbals
- **Payload SDK:** Custom camera control, data streaming, widget display on Pilot 2

---

## Companion Computer / SDK

- **E-Port:** USB device connection for companion computers (Jetson, RPi, etc.)
- **CRITICAL:** Companion computer must operate as USB **device** (not host) — opposite of the old OSDK port
- **SDKs:** Payload SDK (PSDK), Mobile SDK (MSDK), Cloud API
- **No open MAVLink access**

---

## Gotchas

1. **NOT NDAA compliant.** Banned from U.S. federal procurement as of December 2025 under the American Security Drone Act. If your funding source is federal, you cannot buy this.

2. **E-Port USB role is reversed from OSDK.** If you're migrating from M300 with an existing companion computer setup, the USB host/device relationship is flipped. You need to rewire or re-architect.

3. **M300 Skyport V1 payloads need V2 adapter.** Not all V1 payloads have V2 updates available from their manufacturers.

4. **DJI firmware updates can break third-party integrations without warning.** Pin your firmware version and test updates before deploying to your fleet.

5. **Geofencing is aggressive.** GEO 2.0 system can prevent flight in restricted areas without unlock authorization. This is a problem for emergency responders who need to fly NOW.

6. **Data stays local** unless operator enables FlightHub. No mandatory cloud connection — but also no easy way to share fleet data without buying into DJI's ecosystem.

---

## When to Use This Platform

Despite the NDAA issues, the M350 RTK remains the most capable enterprise drone on the market in terms of raw performance, payload flexibility, and ecosystem maturity. If your use case is commercial (not federally funded), and you need a workhorse that Just Works, this is still the benchmark.

If you need NDAA compliance, look at Freefly Astro, Inspired Flight IF1200A, or Skydio X10D.

---

*Last updated: March 2026*
