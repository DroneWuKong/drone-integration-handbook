# Orqa Hardware — Flight Controllers, ESCs, and FPV Systems

> Orqa d.o.o. is a Croatian company producing flight controllers, ESCs, and FPV goggles
> used across both commercial FPV and defense-adjacent applications. Their
> Croatian origin (EU) is relevant for US government procurement pathways.
> US subsidiary: Orqa Inc. (Delaware).

---

## Product Line Overview

| Product | PID | Type | MCU | Primary Use |
|---------|-----|------|-----|-------------|
| QuadCore H7 | FC-1008 | Flight Controller | STM32H743 | FPV racing/freestyle/tactical |
| 3030 Lite F405 | FC-1011 | Flight Controller | STM32F405 | FPV racing/freestyle |
| WingCore H7 | FC-1420 | Flight Controller | STM32H743 | Fixed-wing / VTOL (PX4/ArduPilot) |
| 3030 70A ESC | ESC-1005 | 4-in-1 ESC | BLHeli_32 | Pairs with QuadCore/3030 Lite |
| DTK APB | IS-0001 | FC + Companion | STM32H7 + i.MX8M Plus | All-in-one autonomous platform |
| FPV.One | — | FPV Goggles | — | Pilot display |
| FPV.Connect | — | Video/RC Module | — | Digital FPV link for WingCore |

---

## Orqa QuadCore H7 (FC-1008)

### Specifications
- **MCU:** STM32H743VIT6
- **IMU:** Dual ICM-42688-P
- **Barometer:** DPS310
- **OSD:** AT7456E (integrated)
- **Mounting:** 30.5×30.5mm (M3)
- **BEC:** 5V/2A + 9V/2A
- **Weight:** 9g
- **Betaflight Target:** `ORQA_QUADCORE_H7`
- **Country:** Croatia (EU) — NDAA compliant

### UART Layout (7 UARTs)

| UART | Location | Recommended Use |
|------|----------|-----------------|
| UART1 | VCP/USB | Debug only — do NOT use for peripherals |
| UART2 | DJI JST-GH connector (TX2/RX2) | DJI / Walksnail / HDZero — enable MSP for OSD |
| UART3 | TX3/RX3 solder pads (bottom) | GPS |
| UART4 | TX4/RX4 solder pads (bottom) | Receiver (CRSF/ELRS) |
| UART5 | TX5 only (bottom) | SmartAudio or ESC telemetry |
| UART6 | TX6/RX6 solder pads (bottom) | Available |
| UART7 | TX7/RX7 solder pads (bottom) | Available |

**Physical layout:**
- Top side: DJI JST-GH connector, USB-C port, boot button
- Bottom side: solder pads for all UARTs, M1-M4 motor signals, VBAT, GND, 5V, 9V, LED, buzzer

### Betaflight Setup

The dual ICM-42688-P gyros require Betaflight 4.4 or later.

**Key CLI settings:**
```
set gyro_lpf1_static_hz = 0
set gyro_lpf2_static_hz = 0
set dyn_notch_count = 4
set motor_pwm_protocol = DSHOT600
```

**Ports tab configuration (typical):**
| Port | Function |
|------|----------|
| UART2 | MSP (for DJI/Walksnail/HDZero OSD) |
| UART4 | Serial RX (CRSF/ELRS) |
| UART5 | Peripherals → TBS SmartAudio |

### Stack Pairing
Designed to stack with the **Orqa 3030 70A ESC** (ESC-1005) via 8-pin connector. 30.5mm mounting pattern matches.

---

## Orqa 3030 Lite F405 (FC-1011)

### Specifications
- **MCU:** STM32F405RGT6
- **IMU:** ICM-42688-P
- **Barometer:** DPS310
- **OSD:** AT7456E (integrated)
- **Mounting:** 30.5×30.5mm (M3)
- **BEC:** 5V/2A
- **Weight:** 14g
- **Betaflight Target:** `ORQA_3030LITE_F405`
- **Country:** Croatia (EU) — NDAA compliant

### UART Layout (5 UARTs)

| UART | Recommended Use |
|------|-----------------|
| UART1 | VCP/USB |
| UART2 | Receiver (CRSF/ELRS) — TX2/RX2 pads |
| UART3 | GPS — TX3/RX3 pads |
| UART4 | Available — TX4/RX4 pads |
| UART5 | SmartAudio — TX5 only |

### Betaflight Setup
Same ICM-42688-P gyro settings as the QuadCore H7. Requires Betaflight 4.4+.

### Stack Pairing
Designed to pair with the **Orqa 3030 70A ESC** (ESC-1005) in a 30.5mm stack.

---

## Orqa WingCore H7 (FC-1420)

### Specifications
- **MCU:** STM32H743VIT6
- **IMU:** Dual ICM-42688-P (orthogonal mounting for vibration rejection)
- **Barometer:** DPS310
- **PWM Outputs:** 14 (10 servo + 4 motor)
- **Current Sensor:** 160A onboard
- **Power:** Dual redundant power input
- **Weight:** 5g
- **Firmware:** PX4 / ArduPilot
- **PX4 Target:** `orqa_wingcore_h7`
- **ArduPilot Target:** `OrqaWingCoreH7`
- **Country:** Croatia (EU) — NDAA compliant

### Port Layout (All JST-GH — Pixhawk Standard)

**No solder pads.** Everything connects via JST-GH connectors.

| Port | Connector | Purpose |
|------|-----------|---------|
| TELEM1 | JST-GH | Primary telemetry (SiK radio, companion computer) |
| TELEM2 | JST-GH | Secondary telemetry |
| GPS1 | JST-GH | Primary GPS + I2C compass |
| GPS2 | JST-GH | Secondary GPS |
| RC | JST-GH | Receiver input (SBUS/CRSF/ELRS) |
| VTX | JST-GH | Direct connection to Orqa FPV.Connect module |
| DEBUG | USB-C | Console / firmware flash |
| CAN | JST-GH | DroneCAN bus |

### ioTag Encoding (for iNav/firmware development)
```
ioTag = (port_index << 4) | pin_number
// PA4 = (0 << 4) | 4 = 0x04
// PB8 = (1 << 4) | 8 = 0x18
```

### DFU Flashing
1. Hold BOOT button while connecting USB
2. Open STM32CubeProgrammer
3. Select USB DFU connection
4. Load .bin file (not .hex for DFU mode)
5. Click Start Programming

### Target Platform
Designed for the **Orqa MRM2-10** multi-rotor platform. The VTX port connects directly to the Orqa FPV.Connect C2 module.

---

## Orqa 3030 70A 4-in-1 ESC (ESC-1005)

### Specifications
- **Current:** 70A continuous per motor, 80A burst
- **Voltage:** 3-6S (12.6-25.2V)
- **Firmware:** BLHeli_32
- **Protocol:** DShot150/300/600, Oneshot, Multishot, PWM
- **Mounting:** 30.5×30.5mm (M3)
- **Weight:** 13g
- **Features:** Current sensor, temperature sensor, LED support
- **Country:** Croatia (EU) — NDAA compliant

### Stack Connector (8-pin)

| Pin | Signal |
|-----|--------|
| 1 | M1 (motor 1 signal) |
| 2 | M2 (motor 2 signal) |
| 3 | M3 (motor 3 signal) |
| 4 | M4 (motor 4 signal) |
| 5 | CURR (current sensor) |
| 6 | VBAT |
| 7 | GND |
| 8 | ESC telemetry TX |

Can connect via ribbon cable or direct solder.

---

## Orqa DTK APB (IS-0001)

### Overview
Single-board platform combining flight controller and companion computer. Eliminates the traditional FC + separate companion model.

### Specifications
- **FC MCU:** STM32H7 (running PX4)
- **Companion:** NXP i.MX8M Plus (running Linux)
- **NPU:** 2.3 TOPS (onboard AI inference)
- **Weight:** 13g
- **Connectors:** All JST-GH (Pixhawk standard)
- **Features:** MAVLink bridge built-in, no separate companion wiring needed
- **Country:** Croatia (EU) — NDAA compliant

### Why It Matters
No separate companion computer wiring. The MAVLink bridge between FC and companion is built into the board. Direct Ethernet and serial between FC and companion. The NPU enables onboard AI inference (object detection, terrain classification) without external hardware.

---

## Orqa Antennas

| Product | PID | Band | Connector | Polarization |
|---------|-----|------|-----------|-------------|
| spiroNET Mox 915MHz | ANT-1001 | 915 MHz | RP-SMA | — |
| spiroNET Mox 490MHz | ANT-1002 | 490 MHz | RP-SMA | — |
| FPV.01 Pro Omni (LHCP) | ANT-1181 | 5.8 GHz | SMA | LHCP |
| FPV.01 Pro Omni (RHCP) | ANT-1229 | 5.8 GHz | SMA | RHCP |
| FPV.P1.Pro Patch | ANT-1185 | 5.8 GHz | SMA | Directional |
| FPV.P1 Patch (LHCP) | ANT-1290 | 5.8 GHz | SMA | LHCP |

---

## Orqa Platforms

| Platform | Type | Notes |
|----------|------|-------|
| MRM2-10 | Multi-rotor | Uses WingCore H7 + FPV.Connect |
| MRM2-10F | Multi-rotor (fixed) | Fixed-arm variant |
| MRM1-5 | Multi-rotor (small) | Smaller platform |

---

## Compliance and Procurement

- **Origin:** Orqa d.o.o., Zagreb, Croatia (EU)
- **US Subsidiary:** Orqa Inc. (Delaware)
- **NDAA §848:** NOT a covered entity (not Chinese/Russian/Iranian)
- **FOCI:** Foreign Ownership, Control, or Influence mitigation may be required for classified DOD programs
- **SAM.gov:** Registration required for US government contracting
- **TReX II:** Consortium pathway for defense sales
- **Blue UAS:** Not currently on the DIU Blue UAS cleared list (Croatian origin requires separate pathway)
- **ITAR:** Standard EAR99 classification for commercial drone components

---

## Related

- [Flight Controller Selection](flight-controller-selection.md)
- [The Four Firmwares](../firmware/four-firmwares.md)
- [NDAA Compliance](ndaa-compliance.md)
- [Comms and Datalinks](comms-datalinks.md)
