# ELRS Airport Mode — Transparent Serial Bridge

> The most common ELRS mistake: trying to use a SkyGuy or generic TX module
> as an external CRSF input. It won't work. Airport mode is the solution you
> actually want.

---

## The Problem Airport Mode Solves

Standard ELRS modules on generic TX targets reject external CRSF input. If
you're trying to build a wireless serial bridge — relaying MAVLink telemetry,
triggering a servo remotely, connecting two systems over RF — you'll hit a wall
with the standard approach.

Airport mode bypasses this entirely by turning both modules into a **transparent
serial bridge**: whatever bytes go in one end come out the other. No RC frames,
no CRSF protocol overhead. Just bytes.

---

## How It Works

Both modules stay on **RX firmware**. Neither runs TX firmware. One module is
connected to your serial source; the other is connected to your serial
destination. The RF link between them is completely transparent.

```
[Device A] <-> UART <-> [ELRS RX module A] <-> RF <-> [ELRS RX module B] <-> UART <-> [Device B]
```

Both modules run RX firmware. Airport mode is configured via the ELRS
Configurator on each module independently.

---

## Configuration

### Requirements
- Two ELRS modules (same frequency band — both 900MHz or both 2.4GHz)
- Both flashed with **RX firmware** (not TX)
- ELRS Configurator 3.x+

### Steps

1. Flash both modules with RX firmware for your target
2. Connect each module to your PC via USB or UART passthrough
3. Open ELRS Configurator and connect to the module
4. Navigate to the **Airport** tab
5. Set baud rate to **115200** on both modules
6. Set the same **UID/binding phrase** on both modules
7. Power both modules — they will link automatically
8. Verify with a loopback test: bytes sent into module A appear at module B

### Baud Rate

115200 is the standard for most use cases (MAVLink, CRSF passthrough, servo
triggers). The link is bidirectional and full-duplex at this rate.

---

## Real-World Applications

### Wireless Servo Trigger
Connect XIAO ESP32-C6 to ELRS RX module A on the transmitting end.
Connect ELRS RX module B to a servo driver on the receiving end.
The ESP32 sends a byte; the servo fires. No RC transmitter involved.

**Hardware used in testing:**
- XIAO ESP32-C6 + DroneBridge carrier board
- Two ELRS modules on 2.4GHz RX firmware
- Airport mode at 115200 baud

### MAVLink Telemetry Bridge
Relay MAVLink packets between a companion computer and a ground station
over an ELRS RF link, without using the RC control channel.

### Serial Data Relay
Any UART serial data — sensor output, debug logs, command streams — can be
relayed wirelessly between two points within ELRS RF range.

---

## What Doesn't Work

| Approach | Why It Fails |
|----------|-------------|
| External CRSF input on generic TX targets | SkyGuy and most generic modules reject external CRSF |
| TX firmware with Airport mode | Airport mode requires RX firmware on both ends |
| Mixed frequency bands | 900MHz and 2.4GHz modules cannot link |
| Mixing UID/binding phrases | Modules must share the same binding phrase |

---

## Troubleshooting

**Modules won't link:** Verify same frequency band, same firmware version,
same UID. Try re-flashing both to the same firmware build.

**Data corruption at high baud rates:** Drop to 57600 or 38400. ELRS Airport
mode is reliable at 115200 for most payloads but RF conditions affect
throughput.

**One-way only:** Airport mode is bidirectional. If only seeing data
one way, check UART wiring — TX/RX may be swapped on one side.

**Latency spikes:** Expected on packet loss. Design your protocol to tolerate
10-50ms latency and occasional gaps.

---

## Related

- [ELRS Binding and Configuration](../field/ghost-config.md)
- [Companion Computer Integration](../integration/companion.md)
- [ESP32 Wireless Projects](../components/companion-computers.md)
