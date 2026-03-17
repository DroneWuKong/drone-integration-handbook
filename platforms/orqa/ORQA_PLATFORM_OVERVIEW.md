# Orqa MRM Platform Family — Handbook Reference

> **AI Wingman Handbook** | Platform Reference
> **Classification:** CONFIDENTIAL — Orqa Ltd. product data
> **Last Updated:** 2026-03-16

---

## 1. Platform Summary

Orqa Ltd. (Croatia) manufactures a family of multi-role FPV multicopter UAVs designed for defense and tactical applications. The **MRM (Multi-Role Multicopter)** product line shares a common EW-resilient architecture built around the proprietary **IRONghost** dual sub-GHz control link system.

All MRM platforms run **Betaflight** as the default flight controller firmware, with documented support for iNav, ArduPilot, and PX4 on the H7-class hardware. All use **GHST (Ghost)** or **IRONghost** serial protocols for RC link, and integrate **MAVLink telemetry** for ATAK/TAK interoperability via the Orqa Tac.Ctrl tactical controller.

### Platform Matrix

| Attribute | MRM1-5 | MRM2-10 | MRM2-10F |
|-----------|--------|---------|----------|
| **Class** | 5" robust multi-role | 10" multi-role | 10" foldable multi-role |
| **FC** | 30×30 F405 | H7 QuadCore (STM32H743) | F405 (inferred from BF dump) |
| **MCU** | STM32F405 | STM32H743 | STM32F405 |
| **ESC** | 30×30 60A (AM32) | 30×30 70A cont / 80A burst (AM32) | Integrated |
| **Motors** | 2408 2200kv | 2814 880kv | Integrated |
| **Props** | 5" (5144/5144R) | 10" (1045MR/1045MRP) | 10" (1045MR/1045MRP) |
| **Motor Config** | Props-out, QUADX | Props-out, QUADX | Props-out, QUADX |
| **Camera** | Orqa Justice Analog (1200 TVL) | Orqa Justice Analog (1200 TVL) | Analog (5.8 GHz) |
| **C2 Link** | ISM: Ghost 2G4 Hybrid Duo / EW: IRONghost Dual Sub-GHz | IRONghost Dual Sub-GHz | IRONghost Dual Sub-GHz |
| **Video** | 5.8 GHz analog | 5.8 GHz analog | 5.8 GHz analog |
| **GPS** | Yes (integrated) | Yes + compass + baro | Yes |
| **Battery** | 4S P50B Li-Ion (1P or 2P) | 6S4P Samsung 40T 21700 Li-Ion | 6S4P Molicel P45B Li-Ion |
| **Connectors** | 1× XT60 | 1× XT90 + 2× XT60 (parallel) | 1× XT90 + 2× XT60 (parallel) |
| **Max Payload** | 1 kg | 2.5 kg (up to 3 kg) | 2.5 kg |
| **Max Speed** | 130 km/h (no payload) | — | — |
| **Cruise Speed** | ~40 km/h (loaded) | ~70 km/h | ~70 km/h |
| **Range (loaded)** | >5 km (1 kg payload, 4S2P) | ~20 km | ~20 km |
| **Flight Time** | >15 min (no payload) | — | — |
| **Weight (no batt)** | ISM: 562 g / EW: 590 g | — | — |
| **Foldable** | No | No | Yes (~10 sec deploy) |
| **BF Version** | 4.4.1 (F405) | 4.1 (H7) | 4.1 |
| **Board Target** | ORQA F4PRO (S405) | H7 QuadCore | — |
| **ATAK/MAVLink** | Yes (via Tac.Ctrl) | Yes (via Tac.Ctrl) | — |

---

## 2. IRONghost EW Architecture

The IRONghost system is Orqa's proprietary dual sub-GHz control link, designed for electronic warfare resilience. Key characteristics:

### Dual-Band Operation

- **Primary band:** 915 MHz — main operating frequency, factory-optimized to resist common jammers even on the same band
- **Shadow band:** 490 MHz (MRM2-10, MRM2-10F) or 433 MHz (MRM1-5 EW) — backup low-frequency link
- Frequency settings are transmitted from the Tac.Ctrl to the drone during the binding process
- Each band has at least two frequency options configurable on the controller

### Listening Mode

The drone operates in a minimal-emission state during flight:
- Communication to GCS-1 is kept to absolute minimum (telemetry only)
- The shadow band never transmits packets until the pilot explicitly requests it
- Best practice: switch to shadow band only in the presence of active jamming on the primary link

### Power and Range

- Maximum TX power: 3W (~35 dBm) via JR module
- At 100 mW (20 dBm), typical range ~4 km → at 3W, ~22 km (15 dB = 5.62× range multiplier)
- Primary and shadow band power levels can be set independently
- Recommended: 1W on 915 MHz primary, 3W on shadow band for extra security during jamming

### Frequency Limits

- Maximum usable frequency: ~6.02 GHz (above range of most conventional jammers)
- The Dual SubGHz system radios are firmware-updatable for continuous EW resilience improvements

### Antenna Critical Notes

- **NEVER power on without all antennas attached** — reflecting 3W back into amplifiers causes permanent damage
- Connectors are **RP-SMA** (not SMA)
- Front connectors are factory-marked: low-frequency (shadow) on LEFT, 915 MHz on RIGHT (when facing camera)
- **Swapping antenna positions causes damage at high power settings**
- Video antenna (5.8 GHz) is at the rear
- Omnidirectional antennas have a toroidal radiation pattern — never point the tip directly at the drone

### Range Extension

- Directional antennas increase range and building penetration
- TrueRC Sniper 5.8 GHz recommended for video downlink
- IRONghost GCS-1 ground unit with IRONghost GU RF 5.3-6.0 for maximum control range
- IRONghost Repeater 5.8 GHz enables NLOS operations via aerial relay drone

---

## 3. Flight Controller Configuration

### Orqa F405 Pro (MRM1-5, MRM2-S variants)

**Board Identity:**
- `board_name`: F4PRO
- `manufacturer_id`: ORQA
- Target: STM32F405 (S405)
- BF version: 4.4.1

**Gyro/Sensors:**
- MPU6000 on SPI1 (CS: A04, EXTI: C04)
- Gyro alignment: CW180
- Board alignment: Roll 180°
- DPS310 barometer on I2C1 (address 119 / 0x77)
- QMC5883 magnetometer on I2C1 (alignment: yaw 1800)
- Blackbox flash: W25Q128FV on SPI3 (CS: B03)
- OSD: MAX7456 on SPI2 (CS: B12)

**UART Layout:**

| UART | Function | Serial Config | TX Pin | RX Pin |
|------|----------|--------------|--------|--------|
| UART1 | MSP / Configurator | `serial 0 64 115200` | A09 | A10 |
| UART3 | MAVLink Telemetry | `serial 2 2 115200 115200` | B10 | B11 |
| UART5 | Ghost RX (GHST) | `serial 20 1 115200` | — | D02 (RX only) |
| UART6 | GPS (UBLOX) | `serial 4 1024 115200` | C06 | C07 |
| — | Serial 5 | `serial 5 0 115200` (unused) | — | — |

**Serial Function Codes:**
- 1 = MSP
- 2 = MAVLink telemetry (function 2 at 115200 TX and RX)
- 64 = MSP (function 64 on UART1 — USB/VCP)
- 1024 = GPS

**Motor Outputs:**
- Motor 1: A03 (TIM2 CH4)
- Motor 2: B00 (TIM3 CH3)
- Motor 3: B01 (TIM3 CH4)
- Motor 4: A02 (TIM2 CH3)
- Protocol: DSHOT300, bidirectional
- Motor poles: 14
- Yaw motors reversed: ON

**Servo Outputs:**
- Servo 1: A00 (TIM5 CH1) — payload/camera
- Servo 2: A01 (TIM5 CH2) — payload/camera

**Features Enabled:**
- RX_SERIAL, GPS, TELEMETRY, OSD, AIRMODE, ESC_SENSOR, ANTI_GRAVITY

**PINIO:**
- PINIO 1: B09 (box 43 — USER1, camera switching)

### H7 QuadCore (MRM2-10)

- STM32H743 processor
- Supports Betaflight, iNav, ArduPilot, PX4
- Detailed pin mapping not available in current docs — contact Orqa support for H7 QuadCore config
- Firmware updates via Orqa support

---

## 4. Default Tune (MRM2-S / F405 Platforms)

### PID Profile (Profile 0)

| Axis | P | I | D | F (FF) | D_min |
|------|---|---|---|--------|-------|
| Roll | 50 | 107 | 78 | 168 | 54 |
| Pitch | 52 | 112 | 108 | 175 | 74 |
| Yaw | 63 | 134 | 0 | 134 | 0 |

**Simplified PID Settings:**
- Mode: RPY
- Master multiplier: 140
- I gain: 120
- D gain: 130
- PI gain: 80
- D-max gain: 130
- FF gain: 100
- Pitch D gain: 120
- Pitch PI gain: 100

**Other PID Settings:**
- Anti-gravity gain: 180
- TPA mode: D, rate 65, breakpoint 1350
- Throttle boost: 5
- iterm_relax: RP (setpoint), cutoff 5
- iterm_windup: 85
- Thrust linear: 30

### Rate Profile (Profile 0)

| Parameter | Roll | Pitch | Yaw |
|-----------|------|-------|-----|
| RC Rate | 7 | 7 | 7 |
| Super Rate | 53 | 53 | 53 |
| Expo | 0 | 0 | 0 |

- Rates type: ACTUAL
- Rate limit: 1998 °/s all axes
- Throttle mid: 50, expo: 0

### Filter Configuration

**Gyro Filters:**
- LPF1: Dynamic (0–650 Hz, expo 5), PT1
- LPF2: Static 650 Hz, PT1
- Simplified gyro filter multiplier: 130

**D-term Filters:**
- LPF1: Dynamic (37–75 Hz, expo 5), PT3
- LPF2: Static 75 Hz, PT1
- Simplified D-term filter multiplier: 50

**Dynamic Notch:**
- Count: 2
- Q: 500
- Range: 60–300 Hz

**RPM Filter:**
- Harmonics: 3
- Q: 500
- Min Hz: 100
- Fade range: 50 Hz
- LPF: 150 Hz

### Failsafe Configuration

- Delay: 100 (10 seconds)
- Procedure: DROP
- Switch mode: STAGE1
- Throttle: 1000 (zero)
- Recovery delay: 10

### GPS Rescue

- Min start distance: 30m
- Return altitude: 30m
- Ground speed: 750 cm/s
- Min sats: 8
- Throttle hover: 1275
- Use mag: ON
- Sanity checks: FS_ONLY

---

## 5. Binding and Radio Setup

### Channel Map (All Platforms)

| Function | Channel | Notes |
|----------|---------|-------|
| Roll | CH1 | Right stick L/R |
| Pitch | CH2 | Right stick U/D |
| Throttle | CH3 | Left stick U/D |
| Yaw | CH4 | Left stick L/R |
| Arm/Disarm | CH5 | Left rocker (RL) |
| Camera Control | CH6 | Right rocker (RR) — MRM2-10 |
| Payload Activation | CH7 | Left button (BL) — MRM2-10 |
| Payload Activation | CH8 | Right button (BR) — MRM2-10 |
| Flight Mode | CH9 | Left switch (TL1) — MRM2-10 |
| Pre-Arm | CH10 | Left switch (TL2) — MRM2-10 |
| VTx On/Off | CH11 | Right switch (TR1) |
| Payload | CH12 | Right switch (TR2) — MRM2-10 |
| C2 Band/Power | CH15 | Left slider (SL) — MRM2-10 |
| VTx Profile/Power | CH16 | Right slider (SR) — MRM2-10 |

- Channel map: AETR (BF `map AETR1234`)
- RC protocol: GHST (Ghost) or IRONghost
- Aux 0: ARM on CH5 (AUX1), range 1700–2100

### Binding Procedure

1. Power on controller (Tac.Ctrl for EW, FPV.Ctrl for ISM)
2. Initiate binding in controller menu
3. Connect battery to drone (new drones are in bind mode by default)
4. Wait ~30 seconds for binding to complete
5. Binding also transmits frequency settings from controller to drone

**Re-bind to different controller:** Press BIND button on powered drone, then initiate binding on new controller.

**Factory reset (virgin mode):** Hold BIND button while battery is disconnected, then connect battery while holding.

**OTA firmware update:** May be offered during binding — confirmed on controller, completes in <60 seconds wirelessly.

### Status LEDs (MRM2-10)

| Color | Meaning |
|-------|---------|
| Blue (solid) | Bind mode — waiting for known TX |
| Blue (flashing) | Bind mode — linking with any TX |
| Purple | Scanning — attempting different RF modes |
| Red/Green (alternating) | Normal operation — receiving data |
| Red | Connection loss (failsafe) |

---

## 6. Operational Notes

### Battery Warnings

- XT90 and XT60 connectors are wired **in parallel** — NEVER connect batteries of different voltages or charge levels simultaneously (will cause short circuit and fire)
- Remove props before connecting battery indoors
- Secure XT90 cable to battery with strap to prevent vibration disconnect
- Storage voltage: ~3.7V per cell
- Do not ship batteries to Orqa for warranty service

### Propeller Installation

All platforms use **props-out** configuration:
- Front motors spin outward from camera
- Rear motors spin outward from tail
- 1045MR / 5144R = CW (clockwise)
- 1045MRP / 5144 = CCW (counter-clockwise)
- Text on propeller faces UP always (even on inverted rear motors on MRM2-10F)

### Video Transmitter

- VTx channel/band/power set via IRONghost or Ghost menu on controller
- Must select "Send" after changing settings
- "PowerUp VTx" option controls auto-start on battery connect
- Default VTx control: CH11
- **Do not run VTx at max power on the ground without airflow** — risk of permanent damage without prop cooling

### Maintenance

- Inspect carbon frame screws before/after every flight (especially arm-to-body joints)
- Blow out motor internals with compressed air after dusty operations
- Clean Justice camera with anti-static cloths and optical cleaning fluid
- Replace any propeller with edge damage beyond superficial scratches

---

## 7. Wingman Buddy Integration Notes

### Auto-Detection

The Orqa F405 Pro can be identified via MSP_BOARD_INFO:
- `board_name` = "F4PRO"
- `manufacturer_id` = "ORQA"

On detection, Wingman Buddy should:
1. Display "Orqa F405 Pro" as the board name
2. Show the known UART layout (Ghost RX on UART5, GPS on UART6, MAVLink on UART3)
3. Pre-populate the default PID/Rate/Filter preset values from this document
4. Flag that blackbox is on SPI flash (W25Q128FV) — MSP_DATAFLASH_READ supported

### Tooth Provisioning Payload

The golden config (`MRM2-S_BF.txt`) is the reference provisioning payload for The Tooth. For fleet deployment:
1. Load golden config onto Tooth
2. Plug Tooth into FC USB-C (or wire to UART)
3. Tooth sends `batch start` → resource/feature/serial/set commands → `batch end`
4. Verify via MSP read-back
5. The config includes full resource mapping, feature set, serial assignments, PID/rate/filter tune, OSD layout, GPS rescue, and failsafe settings

### Known UART Availability for Tooth

On the Orqa F405 Pro:
- UART1 (serial 0): MSP — **this is the Tooth's entry point** for USB-C CDC bridge
- UART5 (serial 20): Ghost RX (RX-only, pin D02) — occupied
- UART3 (serial 2): MAVLink telemetry — occupied
- UART6 (serial 4): GPS — occupied
- The Tooth USB-C bridge connects to UART1 for MSP access

---

## 8. Support

- Defense support portal: [defensesupport.orqafpv.com](https://defensesupport.orqafpv.com)
- Email: support@orqafpv.com
- Website: https://orqafpv.com
- H7 QuadCore firmware updates: contact Orqa support directly
- Warranty: 2-year limited, transferable with proof of purchase
- Governed by Croatian law
