# MafiaLRS — Combat-Adapted ELRS Fork

> MafiaLRS is a Ukrainian fork of ExpressLRS adapted for contested RF
> environments. It operates outside standard ELRS frequency bands to
> evade electronic warfare coverage. Actively maintained and battle-tested in Ukraine.

---

## What MafiaLRS Is

MafiaLRS is a fork of ELRS maintained by the Ukrainian developer community (BUSHA/targets@mafia-targets).

**Status:** Actively maintained as of March 2026
**Targets:** 376 RX targets, 122 TX targets

---

## Key Differences from Stock ELRS

| Parameter | Stock ELRS | MafiaLRS |
|-----------|------------|----------|
| 900MHz band | 868/915MHz | 433-735MHz modified |
| 490-560MHz | Not supported | Supported |
| Frequency hopping | Standard ELRS pattern | Modified for EW evasion |
| Compatibility | Standard ELRS | Requires MafiaLRS on both ends |

The core modification is frequency hopping outside the bands that standard EW jamming systems cover.

---

## Operational Context

Developed in response to active RF jamming of standard drone control frequencies in Ukraine. Standard ELRS, Crossfire, and DJI links are vulnerable to broadband jamming. MafiaLRS operates in the gaps.

---

## Identifying Your Target

The [Forge MafiaLRS tool](https://uas-forge.com/tools/#mafialrs) is a **target
selector, not a compiler**. It does not produce a firmware binary — a static
site cannot run the build toolchain. What it does:

- Browse 376 RX / 122 TX target definitions
- Filter by manufacturer
- Copy the **target ID** for the hardware you have

That target ID is the input to the build below. If you came here expecting the
tool to hand you a `.bin`, it never did: it tells you *which* target to build,
not the firmware itself.

---

## Building the Firmware

MafiaLRS is an ExpressLRS fork distributed as a targets overlay
(`BUSHA/targets@mafia-targets`). It builds exactly like stock ELRS — the fork
changes the target definitions, the regulatory/frequency-domain tables, and the
FHSS hopping sequence, not the build process. Two routes:

### Route 1 — ExpressLRS Configurator (GUI)

1. Install the ExpressLRS Configurator.
2. Point it at the fork source / `mafia-targets` branch instead of the official
   release channel.
3. Select the **target** matching the ID you copied from Forge.
4. Set build options: binding phrase, regulatory/frequency domain, telemetry
   ratio.
5. Build. The Configurator drives PlatformIO underneath and emits the binary.

### Route 2 — PlatformIO / CLI (reproducible / CI)

1. Clone the ELRS source plus the `mafia-targets` overlay.
2. Set build flags in `user_defines.txt` (binding phrase, domain, features).
3. `pio run -e <environment>` for the environment matching your target
   (for example, an ESP32 2.4 GHz RX environment).
4. The output `.bin` lands in `.pio/build/<environment>/`.

### Flashing

| Method | Use for | Notes |
|--------|---------|-------|
| WiFi OTA | RX/TX already running ELRS | Join the module's AP, upload via the web UI |
| Betaflight passthrough | RX wired to a flight controller | Flash through the FC's UART |
| UART / FTDI | Bare or bricked chip | Manual boot-mode wiring |

---

## Failure Modes

- **Both ends must match.** A MafiaLRS RX will not bind to a stock-ELRS TX, or
  vice versa — the FHSS sequence and domain tables differ. A mismatch looks
  like a dead link with no telemetry, not an obvious error message.
- **Wrong target = no boot or no RF.** Flashing a definition that does not match
  your radio chip (for example SX1280 vs SX1276) leaves the link dead until you
  reflash the correct target over UART.
- **Binding phrase mismatch fails silently.** The phrase is hashed locally and
  never transmitted, so a typo on one end simply never binds — there is no
  on-air error to observe.

---

## Legal Notes

MafiaLRS operates on frequencies not licensed for unlicensed use in many jurisdictions. For US operators: not appropriate for routine commercial or recreational use. Defense and public safety contexts only.

---

## Related

- [ELRS Airport Mode](../field/elrs-airport-mode.md)
- [RF Detection Hardware](rf-detection-hardware.md)
- [Forge MafiaLRS Generator](https://uas-forge.com/tools/)
