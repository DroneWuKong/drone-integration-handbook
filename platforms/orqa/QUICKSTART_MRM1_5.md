# MRM1-5 — Operator Quick-Start Guide

> **AI Wingman Handbook** | Quick-Start
> Orqa MRM1-5 Robust Multi-Role 5" Drone

---

## Pre-Flight Checklist

### 1. Identify Your Variant
- **ISM version:** Ghost 2G4 Hybrid Duo (2.4 GHz) — two 2.4 GHz antennas visible
- **EW version:** IRONghost Dual Sub-GHz — 915 MHz + 433 MHz antennas visible

### 2. Battery
- Included: P50B 4S1P Li-Ion (321 g)
- Recommended for payload ops: P50B 4S2P Li-Ion
- Connector: 1× XT60

### 3. Propellers
- Props-out configuration
- **5144** = CCW (counter-clockwise)
- **5144R** = CW (clockwise)
- Text faces UP on all propellers
- Front props spin outward from camera, rear props spin outward from tail

### 4. Camera
- Remove Orqa Justice camera lens cap before flight

### 5. Binding
- New drone: auto-enters bind mode on first power-up
- EW: use Tac.Ctrl → initiate binding → connect battery → wait 30 sec
- ISM: use FPV.Ctrl with Ghost UberLite TX module (or any 2.4 GHz RC)
- Re-bind: press BIND button on powered drone, then bind from new controller
- Factory reset: hold BIND while battery disconnected, then connect battery

### 6. Channels
| Function | Channel |
|----------|---------|
| Roll | CH1 |
| Pitch | CH2 |
| Throttle | CH3 |
| Yaw | CH4 |
| Arm | CH5 |
| VTx On/Off | CH11 |

---

## Flight Envelope

| Condition | Speed | Range | Flight Time |
|-----------|-------|-------|-------------|
| No payload (4S1P) | up to 130 km/h | up to 15 km | >15 min |
| 1 kg payload (4S2P) | ~60 km/h | up to 7 km | ~10 min |

**Max recommended payload: 1 kg.** Center payload on frame for balanced motor loading.

---

## EW Operations (EW Variant Only)

- Primary: 915 MHz | Shadow: 433 MHz
- Drone operates in listening mode (minimal TX)
- Shadow band only activates when pilot requests it
- Switch to shadow band only under active jamming

---

## Wingman Buddy Connection

1. Connect USB-C cable from phone to FC USB-C port
2. App detects ORQA F4PRO board
3. Pull params → view PIDs, Rates, Filters
4. For blackbox: use Tooth USB-C bridge on free UART

---

## Emergency

- **Failsafe:** DROP (motors cut on signal loss after 10 sec delay)
- **Disarm:** CH5 to low position
- **VTx kill:** CH11

---

## Support
- Portal: defensesupport.orqafpv.com
- Email: support@orqafpv.com
