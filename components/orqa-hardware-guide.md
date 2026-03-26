# Orqa Hardware — Flight Controllers, ESCs, and FPV Systems

> Orqa d.o.o. is a Croatian company founded in 2018 in Osijek, producing
> flight controllers, ESCs, FPV goggles, and complete drone platforms.
> Full vertical integration — they design and manufacture every component.
> Croatian origin is relevant for US government procurement pathways (non-NDAA §848).

---

## Product Line Overview

| Product | Type | MCU / Key Spec | Primary Use |
|---------|------|---------------|-------------|
| QuadCore H7 | Flight Controller | STM32H743 | Multi-rotor (BF/iNav/AP/PX4) |
| 3030 Lite F405 | Flight Controller | STM32F405 | FPV racing/freestyle |
| H7 WingCore | Flight Controller | STM32H743 | Fixed-wing / VTOL |
| 3030 70A ESC | 4-in-1 ESC | BLHeli_32, 70A | Multi-rotor |
| DTK APB | FC + Companion | STM32H7 + i.MX8M Plus | Development / AI |
| FC2020-F722 | Flight Controller | STM32F722 | 20x20mm micro builds |
| ESC2020 | 4-in-1 ESC | 20x20mm | Micro builds |
| FPV.One | FPV Goggles | — | Pilot display |
| FPV.Connect | Video/RC Module | — | Digital FPV + C2 link |

---

## Orqa QuadCore H7

The flagship quad flight controller. NDAA-compliant.

### Specifications (from public product listings)
- **MCU:** STM32H743
- **Gyro:** ICM-42688-P (dual)
- **Barometer:** DPS310
- **OSD:** MAX7456 compatible
- **Firmware:** Betaflight, iNav, ArduPilot, PX4
- **Mounting:** 30.5 x 30.5mm
- **BEC:** 5V + regulated supplies
- **PWM Outputs:** Up to 10 (via JST-GH ESC and MFC connectors + servo pads)
- **Weight:** ~9g

### ArduPilot UART Configuration (from ArduPilot GitHub)
RC input is on UART3 TX (half-duplex by default for GHST/SRXL2).
For CRSF/ELRS: connect to R3/T3, set `SERIAL1_OPTIONS` to 0.

**ArduPilot target:** `OrqaH7QuadCore`

### Betaflight
**Target:** `ORQA_QUADCORE_H7`

Requires Betaflight 4.4+ for full ICM-42688-P gyro support.

### DFU Flashing
1. Hold BOOT button while connecting USB
2. Open STM32CubeProgrammer
3. Select USB DFU connection
4. Load .bin file (not .hex for DFU mode)
5. Click Start Programming

---

## Orqa 3030 Lite F405

Lightweight quad FC designed to pair with the 3030 70A ESC in a stack.

### Specifications
- **MCU:** STM32F405
- **Gyro:** ICM-42688-P
- **Barometer:** DPS310
- **OSD:** Integrated
- **Firmware:** Betaflight
- **Mounting:** 30.5 x 30.5mm

**Betaflight target:** `ORQA_3030LITE_F405`

---

## Orqa H7 WingCore

Fixed-wing and VTOL flight controller. All JST-GH connectors (Pixhawk-style, no solder pads).

### Specifications (from Orqa shop)
- **MCU:** STM32H743
- **IMU:** Twin orthogonal ICM-42688
- **Barometer:** DPS310
- **OSD:** Orqa custom NDAA-compliant OSD (Text + Graphics)
- **Power Supply:** 11.1 – 44.4 VDC (3–12S LiIon)
- **BEC:** 5V/8A, 6/7.2V/10A
- **Current Sensor:** 160A on-board
- **Firmware:** iNav, ArduPilot, PX4
- **Camera Inputs:** Twin analog switchable inputs
- **Motor Outputs:** 4x (PWM, DShot, CAN bus)
- **Interfaces:** 1x full UART, 3x GPIO, 3x ADC, 1x PWM, 1x I2C, CAN bus, USB-C, Micro SD, GPS/Magnetometer
- **Buzzer:** On-board integrated
- **Mounting:** 30.5 x 30.5mm
- **Dimensions:** 54 x 39 x 17mm
- **Weight:** 36.6g
- **Price:** €259

### Included Cables
- FC → Hybrid VTx/C2 Rx (GH 6-pin, 150mm)
- FC → VTX (GH 7-pin, 150mm)
- FC → Camera 1/2 (GH 6-pin → 2x PicoBlade 3-pin, 200mm)
- FC → GPS (GH 6-pin, 150mm)
- FC → Airspeed sensor cable

Designed for the Orqa MRM2-10 platform. Direct solder-free connection to Orqa C2 links and video downlinks.

---

## Orqa 3030 70A 4-in-1 ESC

### Specifications
- **Current Rating:** 70A continuous per motor, 80A burst
- **Voltage:** 3–6S
- **Firmware:** BLHeli_32
- **Protocol:** DShot150/300/600, Oneshot, Multishot, PWM
- **Mounting:** 30.5 x 30.5mm
- **Features:** Current sensor, temperature sensor, LED support
- **NDAA Compliant**

Designed to stack with the QuadCore H7 or 3030 Lite F405.

---

## Orqa DTK APB (All-Purpose Board)

Single-board platform combining flight controller and companion computer.

### Specifications (from Orqa developer site)
- **Flight Controller:** H7 series STM32 (runs PX4, ArduPilot, Betaflight, iNav)
- **Companion Computer:** NXP i.MX8M Plus SoC
- **AI Capability:** Real-time AI, sensor integration, video processing
- **Camera Inputs:** Dual digital and analog
- **Expansion:** PCIe extension
- **Ecosystem:** Part of the DTK (Development Tool Kit) family

The APB eliminates the traditional separate FC + companion computer architecture. MAVLink bridge between FC and companion is built in.

---

## Orqa FC2020-F722 + ESC2020

20x20mm micro stack for smaller builds.

### FC2020-F722
- **MCU:** STM32F722
- **Mounting:** 20 x 20mm
- **Variants:** HD (digital VTX support) and Analog
- **Price:** €65 (Analog), €85 (HD)

### ESC2020
- **Mounting:** 20 x 20mm
- **Price:** €79

Available as a bundle (FC + ESC) at €139.99 (Analog) or €159.99 (HD).

---

## Compliance

Orqa d.o.o. is Croatian (Osijek, Croatia) with a Delaware US subsidiary (Orqa Inc.).
- **Not a covered entity** under NDAA §848 (which targets Chinese companies: DJI, Autel, Dahua, Hikvision)
- FOCI (Foreign Ownership, Control, or Influence) mitigation may be required for classified DOD programs
- SAM.gov registration required for US government contracting
- Full vertical integration — no Chinese-sourced critical components

---

## Related

- [Flight Controller Selection](flight-controller-selection.md)
- [The Four Firmwares](../firmware/four-firmwares.md)
- [NDAA Compliance](ndaa-compliance.md)
- [ESCs](escs.md)
