# MRM2-10 — Operator Quick-Start Guide

> **AI Wingman Handbook** | Quick-Start
> Orqa MRM2-10 Multi-Role 10" Drone (H7 QuadCore)

---

## Pre-Flight Checklist

### 1. Antennas — DO THIS FIRST

⚠️ **NEVER power on without all three antennas attached. 3W reflected RF = permanent electronics damage.**

| Antenna | Frequency | Location | Connector |
|---------|-----------|----------|-----------|
| Shadow band | 4xx MHz | Front LEFT (blue marking) | RP-SMA |
| Primary | 9xx MHz | Front RIGHT (green marking) | RP-SMA |
| Video | 5.8 GHz | Rear | RP-SMA |

**Swapping front antennas causes damage at high power.**

### 2. Battery
- Recommended: 6S4P Samsung 40T 21700 Li-Ion (~16000 mAh)
- Tattu 6S 16000 mAh LiPo compatible (shorter range)
- Connectors: 1× XT90 (large pack) + 2× XT60 (parallel smaller packs)
- ⚠️ **All connectors are on the same circuit — NEVER mix voltage levels**
- Secure XT90 cable to battery with strap (vibration can disconnect)

### 3. Propellers
- **Remove props before connecting battery indoors**
- Props-out configuration
- **1045MR** = CW | **1045MRP** = CCW
- Text faces UP always
- Front: outward from camera | Rear: outward from tail

### 4. Camera
- Remove Orqa Justice camera lens cap

### 5. Binding
- Tac.Ctrl mandatory for MRM2-10
- New drone: auto bind mode on first power-up
- Initiate binding on Tac.Ctrl → connect battery → wait 30 sec
- Binding transmits frequency settings (9xx + 4xx MHz) to drone
- One controller can bind to multiple drones

### 6. Channel Map
| CH | Function | Control |
|----|----------|---------|
| 1 | Roll | Right stick L/R |
| 2 | Pitch | Right stick U/D |
| 3 | Throttle | Left stick U/D |
| 4 | Yaw | Left stick L/R |
| 5 | Arm/Disarm | Left rocker |
| 6 | Camera | Right rocker |
| 7 | Payload | Left button |
| 8 | Payload | Right button |
| 9 | Flight Mode | Left switch TL1 |
| 10 | Pre-Arm | Left switch TL2 |
| 11 | VTx On/Off | Right switch TR1 |
| 12 | Payload | Right switch TR2 |
| 15 | C2 Band/Power | Left slider |
| 16 | VTx Profile/Power | Right slider |

---

## Flight Envelope

| Parameter | Value |
|-----------|-------|
| Cruise speed (optimal efficiency) | ~70 km/h |
| Range (6S4P, loaded) | ~20 km |
| Max payload | 2.5 kg (up to 3 kg depending on conditions) |
| Wheelbase | 465 mm |
| Motor current (continuous) | 70A per motor |

**mAh/km** is displayed on OSD — optimize by adjusting speed (lower = longer range).

---

## EW Operations

- Primary: 9xx MHz | Shadow: 4xx MHz
- Drone in listening mode — minimal TX, telemetry only
- Shadow band silent until pilot activates it
- Switch to shadow only under active jamming
- Power levels settable independently per band
- Recommended: 1W primary / 3W shadow for jamming scenarios

### Range Testing Math
- 100 mW = 20 dBm → 4 km typical
- 3W = ~35 dBm → ~22 km (15 dB = 5.62× range increase)

---

## Status LEDs

| Color | Meaning |
|-------|---------|
| Blue (solid) | Bind mode — waiting for known TX |
| Blue (flashing) | Bind mode — open |
| Purple | Scanning RF modes |
| Red/Green (alternating) | Normal operation |
| Red | Failsafe / lost link |

---

## Hardware Notes

- **FC:** H7 QuadCore (STM32H743) — supports BF, iNav, ArduPilot, PX4
- **ESC:** 70A continuous / 80A burst per motor (AM32)
- **Motors:** 2814 class, 880kv, 14-pole
- **GPS:** with integrated compass + auxiliary barometric sensor
- **USB-C port** on frame for BF Configurator access
- **DFU button** next to USB-C for firmware recovery
- **BF version:** 4.1 (factory default) — use Configurator v10.10.0+
- H7 firmware updates: contact Orqa support

---

## VTx Notes

- Set channel/band/power in IRONghost "Video Tx" menu on Tac.Ctrl
- Must press "Send" after changes
- Set "PowerUp VTx" to "On" or assign On/Off switch, else VTx won't start
- ⚠️ **Do not leave VTx at max power on ground without airflow — thermal damage risk**

---

## Maintenance

- Inspect frame screws before and after every flight (arm-to-body joints)
- Blow out motors with compressed air after dusty conditions
- Check propellers for nicks — replace if edge damage beyond superficial
- Clean camera lens with anti-static cloth + optical cleaning fluid
- Store batteries at ~3.7V/cell in cool, dry location

---

## Wingman Buddy Connection

- H7 board detection: MSP_BOARD_INFO will return H7 QuadCore identifiers
- UART layout differs from F405 — pull configuration dynamically via MSP
- For Tooth integration: identify free UART via Ports tab in BF Configurator
- MRM2-10 has 8 UARTs on H743 — more flexibility for Tooth placement

---

## Support
- Portal: defensesupport.orqafpv.com
- Email: support@orqafpv.com
