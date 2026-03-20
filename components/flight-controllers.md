# Flight Controllers — The Brain of the Drone

> **Part 6 — Components**
> The flight controller runs the stabilization loop, executes
> autonomous behaviors, and interfaces with every other system.
> Where it's manufactured determines compliance.

---

## The Ecosystem

Flight controllers split into two firmware families: MSP-based
(Betaflight, iNav) and MAVLink-based (ArduPilot, PX4). The
Handbook's firmware chapters cover protocol details. This chapter
covers the hardware — who makes it and what's NDAA compliant.

The parts-db has 420 FCs — good hobby coverage but weak on
commercial and defense options. Most hobby FCs are Chinese-
manufactured (MATEKF405, SpeedyBee F7, etc.) regardless of
brand. The NDAA-compliant FC market is small but growing rapidly.

---

## ARK Electronics — The NDAA Standard

ARK builds the most comprehensive NDAA-compliant drone electronics
stack in the market. 7 products on the Blue UAS Framework. All
made in USA. Open-source hardware and firmware (PX4, ArduPilot).

### ARKV6X Flight Controller

| Detail | Value |
|--------|-------|
| Blue UAS | Framework listed |
| NDAA | Compliant, made in USA |
| MCU | STM32H743IIK6 |
| IMUs | Triple-synced: 2× ICM-42688-P + 1× IIM-42652 (industrial) |
| Barometer | BMP390 |
| Magnetometer | BMM150 |
| Form Factor | Pixhawk Autopilot Bus (PAB) |
| Firmware | PX4 (default), ArduPilot (supported) |
| Power | 5V, 500mA total (300mA main + 200mA heater) |
| Price | ~$320–$770 (depending on variant/bundle) |

### ARKV6X Extended Range

Same platform with triple IIM-42653 industrial IMUs — 4000 dps
gyro range, 32g accelerometer. Designed for high-vibration and
high-G maneuvers (FPV, interceptors, aggressive flight profiles).

### ARK FPV Flight Controller

NDAA-compliant FC with regulated 12V output for VTX and payloads.
Betaflight support. Designed for the tactical FPV market.

### ARK Pi6X / Pi6X Flow

Integrates ARKV6X with Raspberry Pi CM4 carrier, PAB power module,
and 4-in-1 ESC on a single board. The Flow variant adds integrated
optical flow sensors. Blue UAS Framework listed.

### Full ARK Electronics Stack

| Product | Category | Blue UAS |
|---------|----------|----------|
| ARKV6X | Flight Controller | Yes |
| ARKV6X Extended Range | Flight Controller (high-G) | Yes |
| ARK FPV FC | Flight Controller (Betaflight) | Yes |
| ARK Pi6X | FC + CM4 Carrier + ESC | Yes |
| ARK 4IN1 ESC CONS | ESC | Yes |
| ARK TESEO GPS | GPS Module | Yes |
| ARK Flow MR | Optical Flow Sensor | Yes |
| ARK M.2 LTE Module | Connectivity | Yes |
| ARK Just a Jetson | Jetson Carrier Board | NDAA |
| ARK Jetson PAB Carrier | Jetson + FC Carrier | NDAA |
| ARK VOXL2 RTK PAB Carrier | ModalAI VOXL2 Carrier | Blue UAS |

ARK + Mobilicom partnership for cybersecure AI drone solutions.

---

## Auterion — Skynode / AuterionOS

| Detail | Value |
|--------|-------|
| HQ | USA / Switzerland |
| Blue UAS | Framework component (Skynode S) |
| Product | Skynode S (FC + mission computer) |
| Processor | ARM Cortex-A53 Quad @ 1.8 GHz |
| NPU | 2.3 TOPS |
| Software | AuterionOS (Linux), PX4, Auterion SDK, ROS 2, MAVLink |
| Deployed | 50,000+ Skynodes |
| Interfaces | USB-C, 2× MIPI-CSI, CAN, UART, SPI |
| Input Voltage | 12-36V |
| Weight | 38g |
| Mounting | 30.5mm × 30.5mm M3 |

Skynode is a converged FC + companion computer. AuterionOS runs
PX4 natively with containerized applications. ROS 2 and TAK
integration. DDG Phase I: Auterion placed top 5 (~77-80 points).

---

## ModalAI — VOXL 2

VOXL 2 is technically a companion computer but runs PX4 natively,
making it a converged FC + compute platform. See the companion
computers section for full specs. 16 Blue UAS Framework components.

---

## Other NDAA-Compliant FC Sources

### mRo (mRobotics)

US-manufactured Pixhawk-compatible FCs. PixRacer Pro series. NDAA
compliant. Smaller operation than ARK but established in the PX4
community.

### CubePilot / Hex

| Detail | Value |
|--------|-------|
| HQ | Australia |
| Products | CubeOrange+, CubeOrange, Herelink GCS |
| Firmware | ArduPilot (primary), PX4 |
| NDAA | Australian manufacturing — likely compliant, verify |

CubePilot is the most widely used ArduPilot FC in commercial builds.
The Herelink system (RC + video + GCS) is a popular integrated
solution. Non-Chinese manufacturing (Australia/Taiwan — verify
specific components).

### Veronte / Embention

| Detail | Value |
|--------|-------|
| HQ | Spain |
| Product | Veronte Autopilot 1x |
| Key Feature | EASA certifiable, redundant architecture |
| Market | Industrial, defense, certified operations |

Spanish manufacturer targeting the certified/regulated drone market.
Veronte is one of few FCs with a path to EASA type certification.

---

## Chinese FCs (Context — NOT NDAA)

The vast majority of hobby FCs are Chinese-manufactured:
Matek, SpeedyBee, BetaFPV, Foxeer, etc. T-Motor also makes FCs.
All entries in parts-db from the GetFPV catalog are Chinese hardware.

For operators without compliance requirements, these remain the
most capable and cost-effective options. SpeedyBee's mobile app
integration is the closest commercial competitor to Wingman Buddy's
feature set.

**All Chinese FC entries in the parts-db need compliance flags
added: NOT NDAA COMPLIANT.**

---

## Choosing a Flight Controller

1. **Firmware first.** Decide between Betaflight/iNav (MSP, FPV/racing)
   and ArduPilot/PX4 (MAVLink, autonomous operations). The FC must
   support your firmware choice.

2. **MCU determines capability.** F4 (STM32F405) is legacy. F7 is
   current standard. H7 (STM32H743) is top-tier (more flash, faster
   processing, more UARTs).

3. **IMU quality matters.** BMI270 is the hobby standard. ICM-42688-P
   is better. IIM-42652/42653 is industrial-grade. Triple-redundant
   IMUs (ARK) enable voting and fault detection.

4. **For NDAA builds:** ARK ARKV6X + PX4 is the cleanest path.
   For Betaflight FPV: ARK FPV FC or Orqa QuadCore H7 / F405 3030
   (EU-manufactured, JST-GH no-solder connectors). For converged
   compute: Auterion Skynode S or ModalAI VOXL 2. See the
   [Orqa Ecosystem chapter](orqa-ecosystem.md) for the complete
   Orqa FC/ESC/Rx stack.

---

*Last updated: March 2026*
