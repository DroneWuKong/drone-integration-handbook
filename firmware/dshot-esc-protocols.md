# DShot & ESC Protocols

> DShot is the digital protocol between the flight controller and ESC. It
> replaced analog PWM/OneShot protocols and enabled bidirectional
> communication — the FC tells the ESC what throttle to apply, and the ESC
> reports back motor RPM. This bidirectional data is the foundation of RPM
> filtering, which is arguably the single biggest advance in FPV flight
> performance in the last five years.

**Cross-references:** [ESCs](../components/escs.md) ·
[Motors](../components/motors.md) ·
[PID Tuning](../field/pid-tuning.md) ·
[UART Layout](uart-layout.md) ·
[Propulsion Matching](../components/propulsion-system-matching.md) ·
[Appendix B: UART Maps](appendix-b-uart-maps.md)

---

## Protocol Evolution

| Protocol | Year | Type | Resolution | Throttle Rate | Bidirectional |
|----------|------|------|-----------|--------------|---------------|
| Standard PWM | Legacy | Analog | ~1000 steps | 50–490 Hz | No |
| OneShot125 | ~2015 | Analog | ~1000 steps | Up to 4 kHz | No |
| OneShot42 | ~2016 | Analog | ~1000 steps | Up to 12 kHz | No |
| Multishot | ~2016 | Analog | ~1000 steps | Up to 32 kHz | No |
| **DShot150** | ~2017 | Digital | 2000 steps | 150 kbps | Optional |
| **DShot300** | ~2017 | Digital | 2000 steps | 300 kbps | Optional |
| **DShot600** | ~2017 | Digital | 2000 steps | 600 kbps | **Yes** |
| Proshot1000 | ~2018 | Digital | 2000 steps | 1000 kbps | No |

**DShot600 with bidirectional DShot** is the current standard for FPV builds.
Everything before DShot is considered legacy.

---

## How DShot Works

DShot is a digital protocol — it sends binary data (0s and 1s) as different
pulse widths on the motor signal wire. No calibration needed, no analog
noise issues, no ESC drift.

### Packet Structure

Each DShot frame is 16 bits:

```
[11-bit throttle value] [1-bit telemetry request] [4-bit CRC]
```

| Field | Bits | Description |
|-------|------|-------------|
| Throttle | 11 | 0–2047 (0 = disarmed, 48–2047 = throttle range) |
| Telemetry | 1 | Request ESC to send telemetry on next cycle |
| CRC | 4 | Checksum for error detection |

**Throttle values 1–47 are reserved for special commands** (DShot commands):
motor direction change, save settings, ESC info request, LED control, etc.
Value 0 = motor stop. Values 48–2047 = throttle range (2000 steps of
resolution).

### Bit Encoding

DShot uses pulse-width encoding on a single wire:

- **Bit 1:** high for 75% of the bit period
- **Bit 0:** high for 37.5% of the bit period

The bit period depends on the DShot speed:

| DShot | Bit Period | Frame Time |
|-------|-----------|------------|
| DShot150 | 6.67 µs | 106.7 µs |
| DShot300 | 3.33 µs | 53.3 µs |
| DShot600 | 1.67 µs | 26.7 µs |

---

## Bidirectional DShot (RPM Telemetry)

Bidirectional DShot (also called "DShot telemetry" or "RPM filtering DShot")
reuses the same signal wire for both sending throttle commands and receiving
eRPM data back from the ESC.

### How It Works

1. FC sends a DShot frame with the telemetry request bit set
2. FC switches the pin to input mode
3. ESC responds with a 21-bit frame containing eRPM (electrical RPM) data
4. FC processes the eRPM and calculates actual motor RPM
5. FC uses the RPM data for notch filters that track motor harmonics

The ESC response uses GCR (Group Code Recording) encoding — 4 data bits are
encoded as 5 signal bits for DC balance and clock recovery.

### RPM Filtering

This is why bidirectional DShot matters. When the FC knows the exact RPM of
each motor, it can place gyro notch filters precisely on the motor vibration
frequencies and their harmonics. This dramatically reduces noise without
the phase delay of static notch filters.

**Before RPM filtering:** pilots used multiple static notch filters at
estimated frequencies, which added latency and never perfectly matched the
actual vibration frequencies.

**After RPM filtering:** a single dynamic notch per motor tracks the real
fundamental frequency. Less total filtering needed = less latency = better
flight feel and faster reaction times.

**In Betaflight:** enable bidirectional DShot in the Configuration tab, then
enable RPM filtering in the Filter tab. The gyro RPM filter tracks motor
harmonics automatically.

---

## ESC Firmware

The ESC firmware determines which protocols the ESC supports and how it
drives the motor. Three main ESC firmware families:

### BLHeli_S

Legacy 8-bit firmware for older ESCs. Supports DShot150/300/600 but does
NOT support bidirectional DShot or RPM filtering. No longer actively
developed. If your ESC runs BLHeli_S, you're missing RPM filtering — the
single biggest performance improvement available.

### BLHeli_32

32-bit commercial firmware. Full DShot support including bidirectional.
RPM filtering works. Supports advanced features like variable PWM frequency,
LED control, and comprehensive ESC telemetry via a separate telemetry wire
(voltage, current, temperature, RPM per motor).

BLHeli_32 is the incumbent standard. Closed-source but well-supported.

### AM32

Open-source 32-bit ESC firmware. Full feature parity with BLHeli_32
including bidirectional DShot. Growing in popularity because it's free and
community-developed. The Orqa 3030 70A ESC runs AM32.

**Key advantage:** AM32 can be flashed onto many BLHeli_32-compatible ESCs,
giving you open-source firmware on existing hardware.

### Bluejay

Open-source firmware for 8-bit ESC hardware (the same chips that run
BLHeli_S). Adds bidirectional DShot support to hardware that BLHeli_S
doesn't support it on. If you have a BLHeli_S ESC and can't replace it,
flashing Bluejay gives you RPM filtering.

---

## ESC Telemetry (Separate Wire)

In addition to bidirectional DShot (which only carries RPM), some ESCs
provide full telemetry over a separate serial connection:

| Data | Source | Protocol |
|------|--------|----------|
| Voltage per ESC | ESC ADC | Serial telemetry |
| Current per ESC | Shunt resistor | Serial telemetry |
| Temperature | Onboard thermistor | Serial telemetry |
| RPM per motor | Back-EMF / DShot | Either method |

This telemetry wire connects to a spare FC UART. Betaflight can display
per-ESC data on the OSD (individual ESC temps, voltages). Useful for
diagnosing motor or ESC issues — one hot ESC indicates a motor problem
on that arm.

---

## Configuration in Betaflight

### Enabling DShot600 + Bidirectional

In Betaflight Configurator → Configuration tab:

1. **ESC/Motor Protocol:** DShot600
2. **Bidirectional DShot:** Enable
3. **Motor Poles:** set to your motor's actual pole count (typically 14 for
   most FPV motors — count the magnets and divide by 2)

Motor pole count must be correct for accurate RPM calculation. Wrong pole
count = RPM filter on wrong frequencies = worse performance than no filter.

### Enabling RPM Filtering

In Betaflight Configurator → Filters tab:

1. **Gyro RPM Filter:** Enable
2. **Harmonics:** 3 (tracks fundamental + 2 harmonics per motor)
3. **Min Frequency:** 100 Hz (below this RPM filtering disengages)

With RPM filtering active, you can typically reduce or remove static notch
filters, lowering total filter delay.

---

## DShot Commands

The reserved throttle values (1–47) are used for special commands:

| Value | Command |
|-------|---------|
| 1–5 | Beep patterns (ESC locator) |
| 6 | ESC info request (firmware version, etc.) |
| 7 | Spin direction 1 (normal) |
| 8 | Spin direction 2 (reversed) |
| 9 | 3D mode off |
| 10 | 3D mode on |
| 12 | Save settings |
| 20 | Spin direction normal |
| 21 | Spin direction reversed |

These commands are sent by the FC firmware — pilots don't interact with them
directly. Betaflight uses them for motor direction configuration (reversible
via CLI/Configurator without re-soldering motor wires).

---

## Troubleshooting

### RPM Filtering Not Working

1. **Bidirectional DShot not enabled** — must be toggled on in Configuration
2. **Wrong motor pole count** — count magnets, divide by 2
3. **ESC firmware doesn't support it** — BLHeli_S does not. Flash Bluejay or
   upgrade to BLHeli_32/AM32 hardware.
4. **Wiring too long** — long signal wires between FC and ESC can corrupt
   the high-speed bidirectional signal. Keep wires short.

### Motor Desync

Symptoms: motor stutters, stops mid-flight, or makes grinding noise.

Causes: DShot timing issues, ESC timing too aggressive, motor KV too high
for battery voltage, damaged motor winding.

Fix: lower ESC timing (via BLHeli_32/AM32 configurator), check motor for
physical damage, try DShot300 instead of DShot600 if desync persists.

---

## Sources

- Betaflight DShot implementation (github.com/betaflight/betaflight)
- BLHeli_32 documentation
- AM32 project (github.com/am32-firmware/AM32)
- Bluejay project (github.com/mathiasvr/bluejay)
- Oscar Liang, DShot and RPM filtering guides
