# CRSF & ELRS Protocol Deep Dive

> CRSF (Crossfire) is the serial protocol that carries RC channel data and
> telemetry between the receiver and flight controller. ExpressLRS uses CRSF
> as its wire protocol. Understanding CRSF at the protocol level matters
> because it's the foundation for ELRS, MafiaLRS, MILELRS, and every military
> fork in the ecosystem.

**Cross-references:** [UART Layout](../firmware/uart-layout.md) ·
[Five Link Types](../fundamentals/five-link-types.md) ·
[ELRS Airport Mode](../field/elrs-airport-mode.md) ·
[MafiaLRS](mafiairs-combat-elrs.md) ·
[Military Firmware Forks](military-firmware-forks.md) ·
[Comms & Datalinks](comms-datalinks.md)

---

## What CRSF Is

CRSF is a bidirectional serial protocol designed by TBS (Team BlackSheep) for
their Crossfire system. When ExpressLRS was developed, it adopted CRSF as the
wire-side protocol between the receiver and the flight controller rather than
inventing a new one. This means every ELRS receiver speaks CRSF over its UART
connection.

CRSF carries two data streams in opposite directions:

- **Downlink (RX → FC):** RC channel data (stick positions, switches, aux
  channels)
- **Uplink (FC → RX → TX → GCS):** Telemetry (battery voltage, GPS position,
  attitude, RSSI, link quality, custom sensors)

---

## CRSF Packet Structure

Every CRSF frame follows the same structure:

```
[Address] [Length] [Type] [Payload...] [CRC8]
```

| Field | Size | Description |
|-------|------|-------------|
| Address | 1 byte | Destination device (0xC8 = FC, 0xEA = TX module, 0xEC = RX) |
| Length | 1 byte | Payload + type + CRC (everything after this byte) |
| Type | 1 byte | Frame type identifier |
| Payload | variable | Frame-type-specific data |
| CRC8 | 1 byte | CRC8 with poly 0xD5 (DVB-S2 standard) |

Maximum frame size is 64 bytes total.

### Key Frame Types

| Type ID | Name | Direction | Purpose |
|---------|------|-----------|---------|
| 0x16 | RC Channels Packed | RX → FC | 16 channels of RC data, 11 bits each |
| 0x14 | Link Statistics | RX → FC | RSSI, LQ, SNR, TX power, RF mode |
| 0x08 | Battery Sensor | FC → TX | Voltage, current, capacity, remaining |
| 0x02 | GPS | FC → TX | Lat, lon, groundspeed, heading, altitude, sats |
| 0x07 | Vario | FC → TX | Vertical speed |
| 0x21 | Flight Mode | FC → TX | Current flight mode as string |
| 0x29 | Device Info | Both | Device name, serial number, hardware/firmware version |
| 0x2D | Parameter Entry | TX ↔ RX | Lua configuration parameters |
| 0x32 | Command | TX → RX | Model match, binding commands |

### RC Channel Encoding

The 0x16 frame packs 16 channels into 22 bytes using 11-bit resolution per
channel (0–2047). Channel values map to:

- **172** = 988 µs (minimum)
- **992** = 1500 µs (center)
- **1811** = 2012 µs (maximum)

This gives 1624 discrete steps per channel — significantly better resolution
than SBUS (which also uses 11 bits but has lower effective resolution due to
its encoding).

---

## CRSF Baud Rate

CRSF runs at **420000 baud** by default. This is hardcoded in Betaflight,
iNav, and ArduPilot. The baud rate must match between the FC UART
configuration and the receiver.

In Betaflight, set the UART to "Serial RX" with provider "CRSF":

```
serial 1 64 115200 57600 0 115200
set serialrx_provider = CRSF
```

The 420000 baud rate allows up to 500 Hz packet rate, which is the maximum
ELRS supports.

---

## ExpressLRS Packet Rates

ELRS uses CRSF on the wire but has its own over-the-air protocol. The
packet rate determines how often the transmitter sends an update to the
receiver:

| Rate | Modulation | Range | Latency | Use Case |
|------|-----------|-------|---------|----------|
| 50 Hz | LoRa | Maximum | 20 ms | Long range, telemetry |
| 100 Hz | LoRa | Very long | 10 ms | Long range |
| 150 Hz | LoRa | Long | 6.7 ms | Balanced |
| 250 Hz | LoRa | Medium | 4 ms | General FPV |
| 333 Hz | LoRa/FLRC | Medium-short | 3 ms | Freestyle |
| 500 Hz | FLRC | Short | 2 ms | Racing |

**Lower rates = longer range** because the receiver has more time to
accumulate signal energy. This is a fundamental LoRa tradeoff.

**FLRC (Fast Long Range Communication)** is a Semtech mode available on
SX1280/SX1281 chips (2.4 GHz only). It's faster than LoRa but shorter range.
Used for the 333/500 Hz modes.

---

## Telemetry

CRSF telemetry is bidirectional — the FC sends sensor data to the RX, which
relays it over the air to the TX module, which passes it to the radio via
CRSF. The radio (EdgeTX/OpenTX) can display this data on screen or pass it
to Lua scripts (like Yaapu Telemetry).

### Link Statistics (0x14)

The most important telemetry frame. Sent by the RX on every packet:

| Field | Bits | Description |
|-------|------|-------------|
| Uplink RSSI Ant 1 | 8 | Signal strength on antenna 1 (dBm, negated) |
| Uplink RSSI Ant 2 | 8 | Signal strength on antenna 2 (diversity) |
| Uplink Link Quality | 8 | Percentage of packets received (0–100) |
| Uplink SNR | 8 | Signal-to-noise ratio (dB, signed) |
| Active Antenna | 8 | Which antenna is currently selected |
| RF Mode | 8 | Current packet rate index |
| Uplink TX Power | 8 | Transmitter power level index |
| Downlink RSSI | 8 | Signal strength of telemetry downlink |
| Downlink LQ | 8 | Telemetry link quality |
| Downlink SNR | 8 | Telemetry signal-to-noise |

**Link Quality (LQ)** is the single most important metric for control link
health. It represents the percentage of expected packets that actually arrived.
LQ of 100 = every packet received. LQ below 70 indicates a stressed link.
Below 50 is dangerous. At 0, failsafe triggers.

**This is the data that MILELRS extends** — adding per-frequency-band LQ
breakdown, EW signal detection, and direction-finding data into extended
telemetry frames that MILBETA renders on the OSD.

---

## Binding

ELRS binding establishes a unique association between a TX module and an RX.
The binding phrase (set during firmware compilation or via Lua script) is
hashed into a UID that both sides must share.

**Stock ELRS:** binding phrase is a human-readable string hashed into a 6-byte
UID. Anyone who knows the phrase can bind to your receiver.

**MILELRS:** adds encrypted per-transmitter keys. Each TX module gets a unique
cryptographic key that must be generated and paired. This prevents an adversary
who captures a receiver from binding their own transmitter to it.

---

## Model Match

CRSF supports model matching — the TX sends a model ID, and the receiver only
responds if the ID matches. This prevents accidentally controlling the wrong
drone if you have multiple quads on the same binding phrase.

In EdgeTX/OpenTX, each model slot has a model match ID. The receiver stores
the expected ID. Mismatch = no arm.

---

## Airport Mode (ELRS Backpack)

ELRS Airport mode repurposes the CRSF serial link for general-purpose serial
data passthrough. Instead of RC channels, the link carries arbitrary serial
data between two endpoints. This enables:

- MAVLink telemetry relay over ELRS
- Serial device bridging (GPS, sensors)
- Wireless servo control

**See:** [ELRS Airport Mode](../field/elrs-airport-mode.md)

---

## CRSF vs SBUS vs Other Protocols

| Protocol | Baud | Channels | Resolution | Inverted | Telemetry |
|----------|------|----------|-----------|----------|-----------|
| CRSF | 420000 | 16 | 11-bit (1624 steps) | No | Bidirectional |
| SBUS | 100000 | 16 | 11-bit (2048 steps) | Yes (needs inverter) | None (separate) |
| GHST (Ghost) | 420000 | 16 | 12-bit | No | Bidirectional |
| IBUS | 115200 | 14 | 10-bit | No | Optional |
| PPM | Analog | 8–12 | ~1000 steps | N/A | None |

**CRSF advantages over SBUS:**
- No signal inversion needed (SBUS requires an inverter or a hardware UART
  that supports inverted signal, which is why some FC pads are labeled
  "SBUS" specifically)
- Built-in bidirectional telemetry (SBUS is one-way; telemetry needs a
  separate wire/protocol like S.Port)
- Higher baud rate supports faster packet rates
- More extensible frame format

**Why CRSF dominates:** ExpressLRS adopted it, and ELRS is now the dominant
open-source RC system. Every ELRS receiver speaks CRSF. TBS Crossfire
receivers speak CRSF. Orqa Ghost uses GHST (similar to CRSF). This means
the majority of modern builds use CRSF or a close variant.

---

## Wiring

CRSF needs only 4 wires between the receiver and FC:

| Wire | Purpose |
|------|---------|
| TX (from RX) | RC data from receiver to FC |
| RX (from RX) | Telemetry from FC to receiver |
| 5V | Power (most RX accept 5V from FC) |
| GND | Ground |

Connect RX TX → FC RX pad, and RX RX → FC TX pad (crossed). The UART must
be configured for Serial RX with CRSF provider in the firmware.

**See:** [UART Layout](../firmware/uart-layout.md) and
[Appendix B: UART Maps](../firmware/appendix-b-uart-maps.md) for FC-specific
wiring.

---

## Sources

- TBS CRSF protocol specification (github.com/crsf-wg/crsf)
- ExpressLRS documentation (expresslrs.org)
- Betaflight serial RX implementation
- EdgeTX CRSF telemetry documentation
- Oscar Liang, ELRS setup guides
