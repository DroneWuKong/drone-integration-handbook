# Supply Chain Substitution Guide

> Your preferred receiver is out of stock. Your ESC supplier raised MOQ to
> 500 units. The FC you spec'd got discontinued. This guide maps drop-in
> replacements by pinout, protocol, mounting, and firmware compatibility —
> so you can swap without redesigning your build or reflashing your stack.

**Cross-references:** [Flight Controllers](../components/flight-controllers.md) ·
[ESCs](../components/escs.md) · [Comms & Datalinks](../components/comms-datalinks.md) ·
[CRSF & ELRS Protocol](../firmware/crsf-elrs-protocol.md) ·
[DShot & ESC Protocols](../firmware/dshot-esc-protocols.md) ·
[UART Layout](../firmware/uart-layout.md) ·
[NDAA Compliance](../components/ndaa-compliance.md)

---

## How to Use This Guide

1. Find your out-of-stock component's category below
2. Check the compatibility matrix for your specific part
3. Verify the three swap criteria: **pinout**, **protocol**, **mounting**
4. Flash firmware if needed — the guide notes when a reflash is required

**"Drop-in"** means same pinout, same protocol, same mounting — solder it
in place of the old part and it works. **"Near-drop-in"** means one thing
differs (usually a wire swap or a firmware setting change).

---

## ELRS Receivers (900 MHz)

The most commonly stocked-out component. All ELRS receivers speak CRSF over
UART and are cross-compatible on the air side regardless of brand. The
differences are physical: pinout, antenna connector, size, and whether they
have a PA/LNA.

### Nano Form Factor (no PA/LNA)

| Part | Pinout | Antenna | Size | Notes |
|------|--------|---------|------|-------|
| HappyModel EP1 | Standard 5-pin | UFL ceramic | 12x12mm | The original nano. Baseline. |
| HappyModel EP2 | Standard 5-pin | UFL ceramic | 12x12mm | EP1 successor, same pinout |
| BetaFPV Nano 900 | Standard 5-pin | UFL ceramic | 12x12mm | Drop-in EP1/EP2 replacement |
| iFlight 900 Nano | Standard 5-pin | UFL | 12x12mm | Drop-in EP1/EP2 replacement |
| JHEMCU SP9 | Standard 5-pin | UFL | 10x10mm | Smaller, same pinout |
| Foxeer 900 Nano | Standard 5-pin | UFL | 12x12mm | Drop-in |

**Swap rule:** any standard 5-pin nano ELRS 900 MHz receiver replaces any
other. Check that the UFL antenna connector orientation matches your frame's
antenna routing — some have UFL on the top, some on the side.

### With PA/LNA (better range)

| Part | Pinout | Antenna | Power | Notes |
|------|--------|---------|-------|-------|
| HappyModel ES900RX | 6-pin with boot pad | UFL | 100 mW telem | Standard PA/LNA unit |
| BetaFPV 900 RX | 6-pin | UFL | 100 mW | Near drop-in for ES900RX |
| RadioMaster BR1 | 6-pin | UFL | 100 mW | Different boot pad location |
| NeutronRC 900 | 6-pin | UFL | 100 mW | Drop-in for ES900RX |

**Swap rule:** PA/LNA receivers are physically larger than nanos. If your
frame fits one, it'll fit any other in this class. Pin functions are the
same (VCC, GND, TX, RX, boot) but pad layout may differ — check before
soldering.

### Diversity Receivers (dual antenna)

| Part | Antennas | Notes |
|------|----------|-------|
| HappyModel ES900 Dual | 2x UFL (900 MHz) | True diversity |
| BetaFPV SuperD 900 | 2x UFL (900 MHz) | True diversity |
| RadioMaster BR3 | 2x UFL (900 MHz) | True diversity, different form factor |
| GEPRC True Diversity 900 | 2x UFL | Same capability, different board shape |

**Swap rule:** diversity receivers are all functionally equivalent but
physically different. Check board dimensions against your frame's available
space. All use CRSF over UART — firmware compatibility is identical.

---

## ELRS Receivers (2.4 GHz)

Same cross-compatibility rules as 900 MHz but on 2.4 GHz hardware.

### Nano Form Factor

| Part | Antenna | Notes |
|------|---------|-------|
| HappyModel EP1 2.4 | Ceramic patch | Smallest option |
| BetaFPV Nano 2.4 | Ceramic patch | Drop-in for EP1 2.4 |
| HappyModel EP2 2.4 | Ceramic + diversity | Slightly larger |

**Swap rule:** 2.4 GHz nanos are interchangeable. The ceramic patch antenna
is built in — no external antenna to route. Simplest swap category.

---

## Flight Controllers

FC swaps are the most complex because they involve multiple interfaces:
gyro, UARTs, motor outputs, OSD chip, and mounting pattern.

### 30.5x30.5mm F405 Class

| Part | MCU | Gyro | UARTs | OSD | Notes |
|------|-----|------|-------|-----|-------|
| SpeedyBee F405 V4 | STM32F405 | BMI270 | 6 | AT7456E | Common baseline |
| MAMBA F405 MK4 | STM32F405 | BMI270 | 6 | AT7456E | Near drop-in |
| JHEMCU F405 Pro | STM32F405 | ICM-42688 | 6 | AT7456E | Better gyro |
| Foxeer F405 V2 | STM32F405 | BMI270 | 5 | AT7456E | 1 fewer UART |
| Orqa 3030 Lite | STM32F405 | BMI270 | 5 | AT7456E | JST-GH connectors |

**Swap criteria:**

1. **Mounting pattern** — all 30.5x30.5mm, M3 holes. Physical drop-in.
2. **UART assignment** — this is where swaps break. Each FC assigns
   different functions to different UARTs. Your ELRS RX on UART2 might
   need to move to UART3 on the new FC. **Always check the UART map
   before soldering.** See [Appendix B](../firmware/appendix-b-uart-maps.md).
3. **Betaflight target** — each FC has a specific firmware target. You must
   flash the correct target for the new FC. The CLI dump from your old FC
   can be loaded onto the new one after flashing, but verify UART
   assignments, motor outputs, and LED pin mappings.
4. **Motor connector** — some FCs use solder pads, some use JST-SH
   connectors. If swapping between connector types, you need to re-terminate
   your motor wires.

**The most common gotcha:** UART numbers don't match between FCs. Your old
FC had ELRS on UART2 pad. The new FC's UART2 pad is in a different physical
location, or the new FC uses UART2 for something else internally. Always
verify with the new FC's pinout diagram.

### 30.5x30.5mm H7 Class

| Part | MCU | Gyro | UARTs | Notes |
|------|-----|------|-------|-------|
| SpeedyBee F405 V4 | STM32H743 | Dual BMI270 | 8 | Premium option |
| Orqa QuadCore H7 | STM32H743 | Dual ICM-42688 | 7 | Top-tier |
| MAMBA H743 | STM32H743 | ICM-42688 | 8 | Good availability |
| BetaFPV F722 | STM32F722 | BMI270 | 6 | F7, not H7 — different tier |

**Note:** H7 FCs are not direct drop-ins for F405 FCs despite same mounting
pattern. The MCU is different, the firmware target is different, and the
additional UARTs may have different pad locations. Treat H7 as a near-drop-in
that requires firmware reflash and UART re-verification.

---

## ESCs (4-in-1)

### 30.5x30.5mm, 30A-50A Class

| Part | Current | Firmware | Protocol | Notes |
|------|---------|----------|----------|-------|
| SpeedyBee 50A | 50A (55A burst) | BLHeli_32 | DShot600 | Common baseline |
| MAMBA F50 Pro | 50A | BLHeli_32 | DShot600 | Drop-in |
| T-Motor F45A V3 | 45A | BLHeli_32 | DShot600 | Slightly lower current |
| iFlight BLITZ 55A | 55A | BLHeli_32 | DShot600 | Higher headroom |
| Foxeer Reaper F4 50A | 50A | AM32 | DShot600 | Open-source firmware |

**Swap rule:** all 30.5x30.5mm 4-in-1 ESCs with the same voltage rating
(4S or 6S) are physical drop-ins. The motor output pads are in the same
relative positions. The key variable is current rating — match or exceed
the original.

**BLHeli_32 vs AM32:** both support bidirectional DShot and RPM filtering.
They are functionally interchangeable for the pilot. AM32 is open-source.
Swapping between them doesn't require FC firmware changes.

**Connector type:** some ESCs use solder pads for motor wires, some use
JST-SH. If your motors have pre-crimped JST connectors, verify the new
ESC has the same connector.

---

## Motors

Motor swaps are mechanical and electrical.

### Compatibility Checklist

1. **Mounting pattern** — standard FPV motors use 4x M3 holes on a 16x16mm
   or 16x19mm pattern. Verify against frame arm motor mount.
2. **Shaft diameter** — determines which prop adapter fits. Standard is 5mm
   (M5) for 5" motors. T-mount or press-fit varies.
3. **KV rating** — determines RPM per volt. Must match your battery voltage
   and prop. Same KV = same throttle feel and performance.
4. **Stator size** — determines torque and current draw. 2306 and 2207 are
   common for 5". A 2306 draws more current than a 2207 at the same KV.
   Make sure your ESC can handle the new motor's current.
5. **Motor direction** — can be changed in firmware (BLHeli_32/AM32
   configurator or Betaflight DShot commands). No resoldering needed.

**Swap rule:** any motor with the same stator size, KV, mounting pattern,
and shaft diameter is a direct swap. Different stator = verify ESC current
capacity. Different KV = different flight characteristics (may need PID
retune).

---

## Analog VTX

### 20x20mm, 5.8 GHz

| Part | Power | Smart Audio | Connector | Notes |
|------|-------|------------|-----------|-------|
| Rush Tiny Tank | 25-800 mW | Yes (SA) | UFL | Common baseline |
| AKK Race Ranger | 25-1600 mW | Yes (SA) | UFL | More power options |
| Foxeer Reaper | 25-600 mW | Yes (SA) | MMCX | Different antenna connector |
| HGLRC Zeus | 25-800 mW | Yes (SA) | UFL | Drop-in for Rush |

**Swap rule:** any Smart Audio VTX with the same mounting (20x20mm),
connector type (UFL or MMCX), and similar power range is a drop-in. If
switching between UFL and MMCX, you need a different pigtail/antenna.
Smart Audio protocol is universal — no FC firmware changes needed.

**IRC Tramp vs Smart Audio:** if swapping between a Smart Audio VTX and an
IRC Tramp VTX, change the VTX protocol in Betaflight (Configuration tab →
Other Features → VTX control). The wiring is the same (single wire to a
UART TX pad).

---

## GPS Modules

### Standard UART GPS

| Part | Chipset | Constellations | Compass | Notes |
|------|---------|---------------|---------|-------|
| BN-220 | UBlox M8 | GPS+GLONASS | No | Budget baseline |
| BN-880 | UBlox M8 | GPS+GLONASS+BeiDou | HMC5883L | Most common with compass |
| Beitian BE-880 | UBlox M8 | GPS+GLONASS+BeiDou | QMC5883L | BN-880 clone, same pinout |
| GEPRC M10 | UBlox M10 | GPS+GLONASS+Galileo+BeiDou | QMC5883L | Newer chipset, faster lock |
| SpeedyBee SP-M10 | UBlox M10 | All 4 | QMC5883L | Drop-in M10 upgrade |

**Swap rule:** any UART GPS module with the same connector (usually JST-SH
6-pin: VCC, GND, TX, RX, SDA, SCL) is a drop-in. The SDA/SCL lines are
for the compass (I2C). If your old GPS had no compass and the new one does,
enable the compass in firmware. If swapping M8 for M10, update the GPS
protocol in firmware (UBLOX for both, but M10 supports newer messages).

---

## When You Can't Find a Drop-In

If no direct substitute exists:

1. **Check Forge Browse** — filter by category, sort by in-stock retailers
2. **Check the Forge DB schema_data** — pinout, protocol, and mounting
   info is in the part entry where available
3. **Ask Wingman** — describe what you need and what you're replacing,
   Wingman will cross-reference the DB
4. **Community submission** — if you find a working substitute not in the
   DB, submit it at `/submit/` on the handbook site

---

## NDAA / Supply Chain Considerations

Most FPV components (HappyModel, BetaFPV, GEPRC, iFlight, Foxeer) are
manufactured in China. For NDAA-compliant builds:

- **FCs:** Orqa (Croatia), BrainFPV (USA), ARK Electronics (USA)
- **ESCs:** limited NDAA options — check [NDAA Compliance](../components/ndaa-compliance.md)
- **Receivers:** ELRS hardware is open-source — the firmware is uncontrolled,
  but the hardware is Chinese. Currently no NDAA-compliant ELRS receiver
  exists.
- **GPS:** UBlox is Swiss (NDAA compliant). The module PCB may be Chinese.

Supply chain diversification is an active concern for military programs.
PROP UA (Ukrainian propellers) and local FC manufacturing are emerging
to reduce Chinese dependency.

---

## Sources

- Forge parts database (3,596 parts, cross-referenced by schema_data)
- Appendix B: UART Maps for 416 FCs
- ExpressLRS hardware compatibility documentation
- BLHeli_32 / AM32 target compatibility lists
- Community substitution reports
