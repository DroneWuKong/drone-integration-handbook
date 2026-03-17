# Chapter 8: UART Layout and Why It Matters

> You will run out of UARTs before you run out of ideas.
> Planning the layout before you build saves hours of rewiring later.

---

## What a UART Is

A UART (Universal Asynchronous Receiver/Transmitter) is a serial
port. Two wires: TX (transmit) and RX (receive). Every device that
talks to the flight controller — RC receiver, GPS, telemetry radio,
companion computer, ESC telemetry, Bluetooth module, mesh radio —
needs a UART.

The flight controller has a fixed number of UARTs. Once they're
allocated, they're gone. Adding another device means either freeing
a UART or getting a different FC.

---

## How Many UARTs You Actually Get

| MCU | Typical FC | Hardware UARTs | Usable UARTs | Notes |
|-----|-----------|---------------|-------------- |-------|
| STM32F405 | Most 30x30 FCs | 6 | 3–5 | UART1 often hardwired to USB/VCP |
| STM32F722 | Budget FCs | 4 | 3 | Fewer UARTs, fewer features |
| STM32F745/F765 | Mid-range | 8 | 5–6 | More headroom |
| STM32H743/H750 | Premium FCs | 8+ | 6–8 | Best for complex builds |
| RP2040 | Pico-based FCs | 2 | 2 | Very limited |
| ESP32-C6 | Tooth/Seed | 2 | 1–2 | One for FC bridge, one for debug |

"Usable" is lower than "hardware" because:
- One UART is typically dedicated to USB (VCP/CDC) for configurator access
- Some UARTs share pins with SPI (used for gyro, OSD, flash) and can't be used
- Some UARTs have inverted-only pads on the PCB (for SBUS) and can't be
  repurposed without hardware modification

**Check your FC's documentation for which UARTs are actually available
on pads.** The schematic may show 6 UARTs, but if only 4 have TX/RX
pads on the board, you have 4 usable UARTs.

---

## The Standard Allocation

For a typical FPV quad with GPS and telemetry:

| UART | Assignment | Protocol | Baud Rate |
|------|-----------|----------|-----------|
| UART1 | RC Receiver | CRSF (ELRS/Crossfire/Ghost) | 420000 |
| UART2 | GPS | NMEA or UBX | 38400 or 115200 |
| UART3 | Telemetry / MSP Bridge | MSP, MAVLink, or SmartPort | 115200 |
| UART4 | ESC Telemetry | BLHeli/AM32 telemetry | 115200 |

That uses 4 of your ~5 usable UARTs and you haven't added a
companion computer, mesh radio, or Bluetooth module yet.

---

## What Eats UARTs

Every peripheral that communicates over serial needs its own UART.
Here's the complete list of things that might want one:

| Device | Protocol | Required? | Notes |
|--------|----------|-----------|-------|
| RC Receiver | CRSF/SBUS/IBUS | Yes | Non-negotiable. No UART = no control. |
| GPS | NMEA/UBX | For navigation | Required for RTH, GPS modes, position logging |
| Telemetry radio | MSP/MAVLink/LTM | For GCS link | Can share with RC if receiver supports it (CRSF telemetry) |
| ESC Telemetry | Serial telemetry | For RPM filter | Only needed if using bidirectional DShot or ESC temp monitoring |
| OSD (analog) | MSP DisplayPort | For on-screen display | Only if using DJI OSD or analog OSD with MSP |
| Companion computer | MAVLink/MSP | For AI/autonomy | The big UART consumer — wants high baud rate |
| Bluetooth module | SPP/BLE | For wireless config | Can use MSP-over-BT instead of USB |
| Mesh radio | Serial/Ethernet | For swarm | If the mesh radio uses serial (some use Ethernet instead) |
| LED controller | Serial LED | For prop LEDs | Rarely needs a full UART — can use soft serial |
| Rangefinder | Serial | For altitude hold | Some rangefinders use I2C instead (saves a UART) |
| Optical flow | Serial/I2C | For position hold | Prefer I2C version to save UARTs |

---

## Strategies When You Run Out

### 1. CRSF Telemetry Passthrough

If your RC receiver uses CRSF protocol (ELRS, Crossfire, Ghost),
it already has a bidirectional link to the transmitter. You can
send telemetry data (battery, GPS, attitude) through the RC link
instead of using a separate telemetry radio.

**Saves:** 1 UART (the one that would have gone to a telemetry radio)

**Trade-off:** Telemetry bandwidth is limited to what CRSF can carry
(basic flight data, not full MAVLink). If you need full MAVLink
telemetry (parameter editing, mission upload), you still need a
separate radio.

### 2. Soft Serial

Betaflight and iNav support "soft serial" — bit-banging a UART
on any GPIO pin. It works for low-baud-rate devices.

**Saves:** 1 hardware UART

**Trade-off:** Limited to ~19200 baud reliably. Not suitable for
CRSF (420000), GPS at high rate, or MAVLink. Good for: SmartPort
telemetry, serial LED, low-rate telemetry.

### 3. Companion Computer as Hub

Instead of connecting multiple devices to the FC, connect them to
a companion computer and use one UART between the companion and FC.

```
Before (4 UARTs on FC):
  FC UART1 ← RC receiver
  FC UART2 ← GPS
  FC UART3 ← Telemetry radio
  FC UART4 ← Mesh radio

After (2 UARTs on FC):
  FC UART1 ← RC receiver
  FC UART2 ← Companion computer (MAVLink)
  
  Companion ← GPS (USB)
  Companion ← Telemetry radio (USB or Ethernet)
  Companion ← Mesh radio (Ethernet)
```

**Saves:** 2+ UARTs on the FC

**Trade-off:** Adds weight, power consumption, and complexity.
The companion computer becomes a single point of failure for
everything except manual RC control.

### 4. I2C Instead of Serial

Some peripherals (compass, barometer, rangefinder, optical flow)
are available in both serial and I2C versions. I2C uses a shared
bus — multiple devices on the same two wires (SDA, SCL).

**Saves:** 1 UART per device moved to I2C

**Trade-off:** I2C is slower than serial and can have bus contention
issues with multiple devices. But for low-bandwidth sensors, it's fine.

### 5. DMA and UART Sharing (Advanced)

On STM32H7 FCs, DMA (Direct Memory Access) allows the CPU to
handle UART traffic more efficiently. Some advanced configurations
use UART inversion and protocol detection to share a single UART
between two devices that take turns.

This is fragile, FC-specific, and not recommended unless you
know exactly what you're doing.

---

## The UART Planning Template

Before building, fill this out:

```
Platform: _______________
FC: _______________
MCU: _______________
Available UARTs: _______________

| UART | Device | Protocol | Baud Rate | Required? |
|------|--------|----------|-----------|-----------|
| 1    |        |          |           |           |
| 2    |        |          |           |           |
| 3    |        |          |           |           |
| 4    |        |          |           |           |
| 5    |        |          |           |           |
| 6    |        |          |           |           |

Devices that didn't get a UART:
  _______________ → moved to I2C / soft serial / companion / dropped

UARTs remaining after allocation: ___
```

If you fill this out and you're already at zero remaining UARTs
before adding the companion computer you wanted, you need a
different FC or a companion-as-hub architecture.

---

## Platform-Specific UART Maps

### Typical F405 (4 usable UARTs)

```
UART1 → USB VCP (configurator) — not available for peripherals
UART2 → RC Receiver (CRSF @ 420000)
UART3 → GPS (UBX @ 115200)
UART4 → Available
UART5 → Available
UART6 → ESC Telemetry (if DShot bidirectional)
```

Two free UARTs (4 and 5) for telemetry radio, companion, mesh,
or Bluetooth.

### Orqa H7 QuadCore (6+ usable UARTs)

```
USART1 → USB VCP
USART2 → Available
USART3 → RC (GHST/IRONghost @ 420000)
UART4  → Available
USART6 → MAVLink telemetry (ATAK/TAK @ 115200)
UART7  → GPS (UBX @ 115200)
UART8  → ESC telemetry
```

Three free UARTs (2, 4, plus potential soft serial). The H7's
extra UARTs are why it supports more complex integrations than F4.

### PX4 on Pixhawk 6X

```
TELEM1 → MAVLink GCS (115200 or 57600)
TELEM2 → MAVLink companion computer (921600)
GPS 1  → GPS (auto-detect)
GPS 2  → Second GPS or compass
RC IN  → RC receiver (SBUS/CRSF)
DEBUG  → Console / NSH shell
```

PX4 labels its ports by function rather than UART number.
The mapping to hardware UARTs is in the board configuration.

---

## Common Mistakes

**1. Wrong baud rate.** CRSF is 420000. Many people set 115200
because that's the "default" they're used to. The receiver will
not connect. Always check the protocol's required baud rate.

**2. TX/RX swap.** FC TX connects to device RX, and vice versa.
This is wrong more often than any other wiring mistake. If a
serial device doesn't respond, swap TX and RX as the first
diagnostic step.

**3. Voltage mismatch.** Most FCs output 3.3V serial. Most
peripherals accept 3.3V. But some older devices are 5V serial
and can damage 3.3V inputs. Check before connecting.

**4. Two devices on one UART.** You can't connect a GPS and a
telemetry radio to the same UART and expect both to work.
Serial is point-to-point. Use a companion computer or
multiplexer if you need to share.

**5. Forgetting the configurator UART.** If you reassign the
USB/VCP UART to a peripheral, you may lose the ability to
connect Betaflight Configurator. Always keep at least one
path to the configurator available (USB or MSP-over-other-UART).

---

## Next

- **Chapter 6: MSP Protocol** — the protocol that rides on these UARTs
  when talking to Betaflight and iNav.
- **Chapter 13: Adding a Companion Computer** — the architecture
  that solves the "not enough UARTs" problem.

---

*Plan your UARTs before you solder. Desoldering a GPS module
because you need that UART for a companion computer is not
how you want to spend a Saturday.*
