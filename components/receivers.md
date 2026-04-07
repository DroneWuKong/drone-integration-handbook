# RC Receivers

> **Forge cross-reference:** 391 entries in `receivers` category  
> **Related handbook chapters:** CRSF & ELRS Protocol, Control Link TX, Flight Controllers

## The Control Link

The receiver is the drone side of your radio control link. It decodes signals from your ground transmitter and delivers stick/switch commands to the flight controller, while optionally sending telemetry back to the pilot. Getting receiver selection right determines your effective control range, link resilience under interference, and whether you can run encrypted binding in contested environments.

The market consolidated dramatically between 2020–2024. FrSky's ACCST protocol and Spektrum DSM fragmented the market for years. ELRS (ExpressLRS) unified the performance tier and is now the de facto standard for anything that needs range or low latency. Understanding why requires understanding the protocols.

## Protocol Landscape

### ExpressLRS (ELRS) — The Current Standard

ExpressLRS is an open-source radio control link protocol that launched as a community project in 2020 and has become the dominant choice for performance FPV and increasingly for fixed-wing BVLOS work. It runs on SX127x (900MHz) and SX1280 (2.4GHz) LoRa radio chips.

**Why ELRS won:**
- **Packet rate** — 500Hz standard, up to 1000Hz for racing, down to 25Hz for maximum range. Adjustable in the field.
- **Range** — At 100mW, 25Hz packet rate: 40km+ documented. At 250mW with directional TX: 80km+ documented.
- **Latency** — 6.5ms at 500Hz. Competitive with wired connections for all practical purposes.
- **Open source** — No manufacturer lock-in. Any ELRS TX module works with any ELRS receiver from any brand.
- **Encryption** — MILELRS branch adds AES-128 encrypted binding. See `components/military-firmware-forks.md`.
- **Frequency hopping** — ELRS uses FHSS to reduce vulnerability to narrowband jamming.

**Frequency options:**
- **900MHz ELRS** — Better penetration through obstacles, better range at equivalent power. More susceptible to 900MHz interference (LTE). Standard for long-range and most military-adjacent applications.
- **2.4GHz ELRS** — Lower power draw, smaller antennas, higher update rates at medium range. Preferred for racing and freestyle. More susceptible to 2.4GHz WiFi/interference.

**Key ELRS manufacturers:** RadioMaster, BetaFPV, Radiomaster, Jumper, iFlight, HappyModel, GEPRC, Matek, Team BlackSheep (ELRS hardware).

### Crossfire / CRSF — The Professional Tier

Team BlackSheep Crossfire (TBS Crossfire) introduced the CRSF protocol and the concept of low-latency, long-range RC links to the consumer market in 2017. CRSF (the protocol) is now used by ELRS, Tracer, and others — it's the serial communication format, not the RF link itself.

**TBS Crossfire:**
- 868/915MHz FSK radio link
- Up to 40km+ range at 2W
- CRSF serial protocol (19200 baud) — the standard for FC integration
- Robust to interference, proven in real deployments
- Nano receiver: 1.5g, excellent for long-range builds
- Downside: proprietary, more expensive than ELRS, slower adoption of new features

**TBS Tracer:**
- 2.4GHz variant of Crossfire
- Faster update rates than Crossfire 900MHz
- Smaller antennas
- Less range than Crossfire 900MHz

### FrSky — Legacy Market

FrSky dominated the market from ~2012–2020 with their ACCESS/ACCST protocols. Still widely deployed. Their XM+, R-XSR, and RX4R receivers are extremely common on builds from that era.

- **ACCESS protocol** — Current FrSky standard, replaced ACCST. D16 compatibility mode available.
- **SBUS output** — FrSky receivers output SBUS (inverted serial), which all flight controllers accept
- **F.Port** — Combines SBUS + telemetry in a single wire, reducing wiring complexity
- **Range** — Competitive at shorter distances, significantly worse than ELRS/Crossfire at range limits
- **Status** — No longer the choice for new builds, but massive installed base

### Spektrum DSM — RC Airplane Legacy

DSM2/DSMX protocol common in fixed-wing, sailplane, and RC helicopter applications. Spectrum analyzers the older generation of fixed-wing aircraft. DSMX adds frequency hopping for interference resistance.

- Mostly relevant for integrating drones with existing Spektrum radio systems
- Not competitive with ELRS for range or latency
- Some ELRS receivers support DSM satellite input for legacy compatibility

### FlySky AFHDS 2A — Budget Tier

FlySky's AFHDS 2A protocol is common on budget platforms (Eachine, some Hubsan, budget quads). IBUS serial protocol. Not used in serious builds.

## NDAA Landscape

Receivers are predominantly Chinese-manufactured, which creates significant procurement issues for federal programs.

| Manufacturer | Origin | NDAA |
|---|---|---|
| Team BlackSheep | Switzerland (EU) | ✓ Allied |
| RadioMaster (ELRS) | China | ✗ |
| BetaFPV (ELRS) | China | ✗ |
| Happymodel (ELRS) | China | ✗ |
| GEPRC (ELRS) | China | ✗ |
| iFlight (ELRS) | China | ✗ |
| Matek (ELRS) | China | ✗ |
| FrSky | China | ✗ |
| FlySky | China | ✗ |
| Spektrum/Horizon Hobby | USA | ✓ |
| Futaba | Japan | ✓ Allied |

**The problem:** ELRS hardware is nearly entirely manufactured in China. TBS Crossfire/Tracer (Swiss) is the primary NDAA-compliant option for ELRS-class performance. Spektrum provides NDAA-compliant receivers but is not competitive with ELRS on range/latency.

**For federal procurement:** TBS Crossfire Nano or TBS Tracer Nano are the primary options that combine NDAA compliance with competitive performance. Verify per SKU — TBS manufactures in Switzerland but some accessories vary.

## Form Factor Guide

### Nano Receivers (1–2g)
The standard for 3–7" FPV builds. Solder directly to UART pads on the FC. Typically 15×11mm or smaller.

- TBS Crossfire Nano — 1.5g, 2× U.FL antenna ports
- ELRS Nano variants (RadioMaster, BetaFPV, GEPRC) — 0.9–1.5g
- No external antenna option on most — rely on ceramic chip antennas or small dipoles

### Micro Receivers (2–5g)
Slightly larger, typically with JST connector and better antenna options. Good for 5–10" builds where you have room.

### Full-Size Receivers (5–25g)
Fixed-wing, large platforms, when you need full telemetry channels, multiple satellite inputs, or SBUS + S.Port. The FrSky R9M/RX series falls here.

### AIO (All-in-One) FC+RX
Many flight controllers now include an integrated ELRS receiver, eliminating the separate RX entirely. Examples: SpeedyBee F405 Wing ELRS, Holybro Kakute H7 ELRS. The RX shares the MCU clock and requires no UART allocation.

## Integration

### UART Configuration
ELRS/CRSF receivers connect via UART (TX→RX, RX→TX). In Betaflight/INAV:

1. Enable Serial RX on the UART the receiver is wired to
2. Set Receiver Mode: Serial-based receiver, CRSF
3. Set RSSI Channel if using ELRS RSSI telemetry

ELRS also supports signal inversion on some FCs — verify `set sbus_config` is not inverted for CRSF.

### Betaflight ELRS Setup
```
set receiver_type = SERIAL
set serialrx_provider = CRSF
set serialrx_inverted = OFF
set serialrx_halfduplex = OFF
```

**UART speed for CRSF:** 420000 baud is standard. Ensure your FC UART supports 420k — most F4/F7/H7 boards do.

### Antenna Placement
The single most impactful factor for link reliability after receiver selection:

- **Minimum 30° separation** between the two receiver antennas
- **Keep antennas away from carbon fiber** — CF is conductive and absorbs RF. Mount on plastic standoffs or route antennas outside the frame.
- **Vertical polarization** matches transmitter antennas on most ground setups
- **For 900MHz:** Antennas should ideally be ≥75mm long (quarter-wave). Longer = better omnidirectional pattern.

### Failsafe Configuration
Configure failsafe BEFORE your first flight. In Betaflight:

1. In the Failsafe tab, set Stage 2 failsafe to LAND (altitude-aware) or SET_THROTTLE → 0 depending on platform
2. Set failsafe_throttle to something that won't crash but will descend (if no barometer)
3. Test failsafe by turning off TX while motors are not spinning — verify expected behavior

For ArduPilot/PX4, set `FS_THR_ENABLE` and `FS_THR_VALUE` and test in SITL before flight.

## Forge Cross-Reference

The 391 receiver entries span every protocol tier. Use the NDAA ✓ filter in the Forge parts browser to immediately isolate the ~8 NDAA-compliant entries from the ~380+ Chinese-manufactured receivers. For contested-environment builds, see `components/military-firmware-forks.md` for MILELRS encrypted binding.
