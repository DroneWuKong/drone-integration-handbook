# MRM2-10F — Operator Quick-Start Guide

> **AI Wingman Handbook** | Quick-Start
> Orqa MRM2-10F Foldable Multi-Role 10" Drone

---

## Pre-Flight Checklist

### 1. Unfold Drone (~10 seconds)
- Follow the 12-step unfolding sequence (front arms first, then rear, then legs)
- Ensure arms **click** securely into clips at steps 2a and 4a
- Props do NOT need to be removed each time you fold

### 2. Antennas — BEFORE POWER ON

⚠️ **NEVER power on without antennas. 3W reflected = permanent amplifier damage.**

| Antenna | Frequency | Location | Connector |
|---------|-----------|----------|-----------|
| Shadow (low-freq) | 490 MHz | Front LEFT (when facing camera) | RP-SMA |
| Primary | 915 MHz | Front RIGHT | RP-SMA |
| Video | 5.8 GHz | Rear | SMA |

**Swapping front antennas causes damage at high power.**

### 3. Battery
- Recommended: 6S4P Molicel P45B Li-Ion (~16000 mAh)
- Tattu 6S 16000 mAh LiPo compatible (shorter range)
- Connectors: 1× XT90 + 2× XT60 (all parallel)
- ⚠️ **NEVER mix battery voltages/charge levels across parallel connectors**

### 4. Propellers
- Props-out configuration
- **1045MR** = CW | **1045MRP** = CCW
- Text faces UP on all propellers (including inverted rear motors)
- ⚠️ **Rear motors face DOWN — but prop text still faces UP. Wrong = no lift.**

### 5. Camera
- Remove lens cap

### 6. Binding
- Tac.Ctrl mandatory
- New drone: bind mode on first power-up
- Initiate on Tac.Ctrl → connect battery → 30 sec
- Frequency settings (915 MHz + 490 MHz) transferred during binding
- Factory reset: hold BIND button → connect battery while holding

### 7. Channels
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

| Parameter | Value |
|-----------|-------|
| Cruise speed | ~70 km/h |
| Range (recommended battery, loaded) | ~20 km |
| Max payload | 2.5 kg |
| Deploy time | ~10 seconds from folded |

**Payload mounting:** Use steel cable ties and screws through bottom plate holes. Keep CoG centered. Zip ties are a less secure alternative.

---

## EW Operations

- Primary: 915 MHz | Shadow: 490 MHz
- Listening mode: drone minimizes TX (telemetry only)
- Shadow band silent until pilot activates
- Switch to shadow only when jammed on primary
- Independent power control per band

### Range Math
- 100 mW (20 dBm) → ~4 km
- 3W (~35 dBm) → ~22 km (5.62× multiplier)

---

## VTx
- Set via "Video Tx" in IRONghost menu on Tac.Ctrl
- Press "Send" after changes
- Set "PowerUp VTx" to "On" or assign CH11 switch
- BF firmware: v4.1 — use Configurator v10.10.0+

---

## Folding for Transport
- Reverse the 12-step unfolding sequence
- Props can stay on during folding
- Compact package for rapid deployment

---

## Support
- Portal: defensesupport.orqafpv.com
- Email: support@orqafpv.com
