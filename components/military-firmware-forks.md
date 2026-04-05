# Military Firmware Forks — Combat-Adapted Open-Source Drone Firmware

> The Russo-Ukrainian War has produced the fastest firmware innovation cycle in
> aviation history. Open-source drone firmware — originally built for hobbyist
> racing quads — has been forked, hardened, and deployed at industrial scale.
> Both sides now operate custom firmware ecosystems that transform $300
> commercial hardware into EW-resistant strike platforms.

**Cross-references:** [Ch.2 RF Fundamentals](../fundamentals/rf-fundamentals.md) ·
[Ch.5–7 Firmware](../firmware/four-firmwares.md) ·
[Ch.8 UART/Serial](../firmware/uart-layout.md) ·
[MafiaLRS](mafiairs-combat-elrs.md) ·
[Electronic Warfare](electronic-warfare.md)

---

## Landscape Overview

| Firmware | Base | Origin | Layer | Status | Key Capability |
|----------|------|--------|-------|--------|----------------|
| **MILELRS** | ELRS 3.3.2 | Ukraine | Control Link | ACTIVE | Multiband, encrypted, EW scanning, swarm ID |
| **MILBETA** | BF 4.3/4.5 | Ukraine | FC Firmware | ACTIVE | EW OSD overlay, VTX 3–7 GHz, extended failsafe |
| **MafiaLRS** | ELRS | Ukraine | Control Link | ACTIVE | 433–735 MHz non-standard bands, freq hopping |
| **BarvinokLRS** | Custom | Ukraine | Control Link | ACTIVE | Free distro to frontline, EW-resistant |
| **Barvinok-5** | Custom | Ukraine | Video Link | PROTOTYPE | Encrypted digital video, FHSS, replaces analog |
| **"1001"** | DJI OEM | Russia | Platform FW | DISRUPTED | DJI unlock: flight limits, GPS spoof resist |
| **CIAJeepDoors** | DJI OEM | Ukraine | OPSEC Patch | ACTIVE | Disables DJI Remote ID / AeroScope tracking |
| **mLRS** | Custom LoRa | Open Source | Control+Telem | ACTIVE | MAVLink RC+telemetry, 7–87 km, diversity |
| **DroneBridge** | ESP-IDF | Open Source | Telemetry | ACTIVE | ESP32 serial→WiFi/ESP-NOW, AES-256, swarm |

---

## MILELRS

**Base:** ExpressLRS 3.3.2
**Origin:** Ukrainian engineers, first half 2024
**Current version:** v2.30
**Distribution:** Access-controlled via Telegram, unique TX binding key required

MILELRS is the most widely deployed military control link firmware in the
Russo-Ukrainian War. It runs on the same COTS hardware as stock ELRS
(HappyModel, BETAFPV, RadioMaster, etc.) but adds EW-hardening features
that transform hobby receivers into contested-environment comms systems.

### Capabilities

- **Multiband redundancy** — simultaneous operation across 900 MHz and 2.4 GHz
  using diversity receivers. If one band is jammed, the other maintains link.
- **Encrypted binding** — unique per-transmitter key required. Prevents
  unauthorized connection to friendly drones.
- **EW scanning** — real-time spectrum scanning detects jamming sources and
  reports direction/strength to the FC via telemetry.
- **Auto channel switching** — automatic frequency hopping on interference
  detection. Operator can also manually configure frequency ranges.
- **Multi-RX support** — multiple receiver modules connect to a single FC for
  redundant control paths.
- **Swarm ID** — unique drone identification within coordinated multi-unit ops.
- **Failsafe extensions** — extended timers and configurable behaviors for
  signal loss in combat conditions.

### Supported Hardware

**TX modules:** HappyModel ES900/ES24, BETAFPV 900/2.4 GHz, RadioMaster
Bandit/Ranger, EMAX OLED, CYCLONE

**RX modules:** HappyModel ES900/Dual, BETAFPV SuperD, RadioMaster BR1/BR3,
GEPRC, Foxeer, NeutronRC, iFlight, BAYCKRC, HGLRC Hermes, EMAX, AION Mini

### MILBETA Synergy

MILELRS pairs with MILBETA. The RX sends detailed EW telemetry (packet loss
by frequency band, jamming direction, LQ statistics) to the FC, which MILBETA
renders on the pilot's OSD. MILBETA functions 3 (EW direction-finding) and 6
(LQ statistics display) require MILELRS firmware on the receiver.

### Operational Deployment

By summer 2024, MILELRS was among the most common militarized control systems
in Ukraine. Russia gained access to an earlier version by 2025 and adopted it.
TAF Industries ships the Kolibri 10 strike drone with MILELRS pre-installed.
Production-scale deployment confirms this is standard military issue, not
experimental.

---

## MILBETA

**Base:** Betaflight 4.3.3 / 4.5.1
**Origin:** Ukrainian engineers, paired with MILELRS
**Current version:** v1.23
**Distribution:** Via Telegram, no license required

MILBETA is a Betaflight fork purpose-built to process and display tactical
data from MILELRS receivers. Stock Betaflight handles flight performance;
MILBETA adds a combat information layer turning the pilot's OSD into a
tactical display.

### Capabilities

1. **OSD camouflage** — hides launch/landing site coordinates from OSD to
   prevent intelligence gathering if video feed is intercepted.
2. **Switch position display** — shows current toggle switch positions on OSD.
3. **EW direction finding** — displays jamming source direction and signal
   strength on OSD. *Requires MILELRS.*
4. **Extended failsafe** — all failsafe timers multiplied by 10×. Writing 1 sec
   in Betaflight Configurator = 10 sec actual. Allows drone to continue mission
   through temporary signal loss.
5. **VTX frequency unlock** — removes stock restrictions. Stock BF: 4900–5999
   MHz. MILBETA: 3000–6999 MHz. Enables non-standard video bands enemy EW may
   not cover.
6. **EW + LQ statistics** — real-time EW and link quality across 12 frequency
   bands on OSD. *Requires MILELRS.*
7. **Armed VTX switching** — allows VTX channel changes while motors are armed
   and in flight.

### FC Compatibility

BF 4.3.3 recommended for older FCs (F722). BF 4.5.1 for newer FCs (F435).
All standard Betaflight targets are supported — MILBETA is a firmware-level
modification, not a hardware change.

---

## FPV_VYZOV Ecosystem

**Affiliation:** Russian non-state developer network
**Components:** MILELRS + MILBETA + custom hardware designs
**Distribution:** Telegram channels with weekly "Friday Updates"

FPV_VYZOV ("Challenge") is a Russian-affiliated developer collective that built
a complete tactical FPV ecosystem around MILELRS and MILBETA. They adopted an
earlier Ukrainian version of MILELRS and extended it.

### EW Hunter-Killer Drones

The ecosystem's signature capability is specialized drones that detect, track,
and neutralize enemy EW assets. Using MILELRS's spectrum scanning to locate
jamming sources, the hunter-killer drone flies toward the EW emitter while
MILBETA displays direction-finding data on the pilot's OSD. This creates a
direct counter to conventional drone defenses.

### Supply Chain

Built entirely on COTS hardware from Chinese manufacturers (HappyModel,
BETAFPV) procured through Russian domestic platforms (Ozon, Wildberries).
Combined with open-source firmware and 3D-printed hardware, this model
iterates faster than traditional military acquisition.

---

## MafiaLRS

> **See dedicated article:** [MafiaLRS — Combat-Adapted ELRS Fork](mafiairs-combat-elrs.md)

**Base:** ExpressLRS · **Origin:** Ukrainian FPV community · **Status:**
Active — 254 RX / 122 TX targets in Forge DB

MafiaLRS is a separate Ukrainian ELRS fork (distinct from MILELRS) operating on
non-standard bands: 433 MHz, 490–560 MHz, and modified 868/915 MHz. Most
Russian jammers target standard ELRS bands; MafiaLRS sidesteps by operating
outside that coverage.

Forge has a self-hosted firmware generator on the Tools page with full target
browser. Source: `BUSHA/targets@mafia-targets` (GitHub).

---

## Barvinok-5 / BarvinokLRS

**Origin:** Ukrainian startup (6-person team)
**Products:** BarvinokLRS (control link, free), Barvinok-5 (digital video, prototype)
**Funding:** Defense Builder accelerator grant

### BarvinokLRS (Control Link)

A custom control firmware distributed free to Ukrainian frontline units. Not a
fork of ELRS — independently developed. Operates on multiple frequencies with
different RF parameters. Field reports confirm it maintains link where other
systems fail under EW pressure.

### Barvinok-5 (Video Module)

Digital video system designed to replace analog FPV video while keeping its
advantages (one-directional, low latency). Adds encryption and wide-spectrum
pseudo-random frequency-hopping modulation (FHSS) with very small packets,
making the signal extremely difficult to jam or intercept. Approaching end of
prototype phase, beginning integration with manufacturers and military units.

### Why This Matters

Analog video is the weakest link in FPV operations. It's unencrypted
(interceptable by any receiver) and easy to jam. Video jamming became the most
effective Russian counter-drone tactic starting summer 2024. Barvinok-5 is one
of several Ukrainian solutions — others include HDZero, Walksnail, and
frequency diversification (operators now use 1.2 GHz, 5.8 GHz, and even
7.2 GHz video).

---

## DJI Military Modifications

### "1001" Firmware (Russian)

**Platform:** DJI Mavic series and similar consumer drones
**Distribution:** Closed network of "terminals" (pre-configured laptops)
**Scale:** ~200,000 drones flashed as of March 2025
**Status:** Distribution infrastructure compromised by cyberattack (July 2025)

Removes manufacturer-imposed flight limits, improves GPS spoofing resistance,
and enables high-capacity battery support. The firmware itself was reportedly
not compromised in the attack, but the terminal-based update system was
disabled, preventing new drones from being flashed.

### CIAJeepDoors (Ukrainian)

**Platform:** DJI drones with Remote ID
**Delivery:** USB device called "Olga"

Activates a command in DJI firmware that disables Remote ID broadcasting.
Remote ID allows Russian AeroScope terminals to identify both the drone's
position and the operator's position — enabling artillery targeting of
operators. CIAJeepDoors closes this vulnerability. DJI has since released
firmware on newer models that prevents Remote ID from being disabled.

---

## Open-Source Building Blocks

### mLRS

**Base:** Custom LoRa firmware (SX126x / SX128x / STM32WLE5)
**Bands:** 433 MHz, 868/915 MHz, 2.4 GHz
**Range:** 7–87 km depending on mode and power
**Protocol:** Integrated RC + full MAVLink telemetry
**Hardware:** MatekSys mR900-30, mR24-30 (purpose-built), also FrSky R9 and ELRS hardware

Not a military fork, but its combined RC and MAVLink telemetry over LoRa with
full diversity makes it directly relevant to BVLOS and contested environments.
Supported natively by ArduPilot.

### DroneBridge ESP32

**Base:** ESP-IDF (pure C)
**Protocols:** MAVLink, MSP, LTM, transparent serial
**Encryption:** AES-256-GCM in all modes including ESP-NOW broadcasts
**Range:** ~1 km (ESP-NOW LR with external antenna)
**Cost:** $3–5 per board

Ultra-low-cost serial-to-WiFi/ESP-NOW telemetry bridge. Supports swarm
networking via ESP-NOW with encrypted broadcasts. Useful as a cheap telemetry
fallback or local mesh relay. Not a combat system, but a building block for
low-cost telemetry architectures.

---

## The EW Arms Race Context

The firmware fork ecosystem exists because of the escalating EW arms race:

Standard frequencies → enemy deploys jammers → firmware moves to non-standard
bands → enemy expands jamming → firmware adds FHSS and encryption → enemy
develops wideband jammers → firmware adds multiband redundancy → video jamming
emerges as the new weak point → encrypted digital video develops → fiber-optic
drones bypass RF entirely.

By summer 2025, Ukraine deployed video on the 7.2 GHz band — causing
significant disruption because Russian jammers weren't covering it. Both sides
now compile and share statistics on enemy video frequencies detected by ELINT
forces.

### Production Scale

Ukraine's defense industry can produce 8+ million FPV drones per year across
160+ manufacturers. FPV drones account for 60% of Russian combat losses. TAF
Industries alone produces 80,000 drones/month. Russia's fiber-optic FPV
production reached 50,000+/month by September 2025. These firmware forks
aren't experimental — they're production firmware for industrial-scale warfare.

### Fiber-Optic: The EW Endgame

Fiber-optic FPV drones are immune to all RF-based EW because the control
signal travels through a physical cable. Both sides are mass-producing them.
Fiber-optic makes all RF-layer firmware hardening irrelevant — but range and
weight limitations mean RF-based systems remain necessary for many mission
profiles.

---

## Sources

- Armada International, "The Curran Papers No. 5: Jamming UAV Video Signals" (Feb 2026)
- Cyber Shafarat / Treadstone 71, "Russian FPV Drone Tactical Ecosystem" (Oct 2025)
- Cyber Shafarat, "MILELRS v2.30 firmware upgrades" (Apr 2025)
- Cyber Shafarat, "MILBETA v1.23 firmware flashing" (Nov 2024)
- IEEE Spectrum, "Ukraine Is the First Hackers' War" (Mar 2025)
- IEEE Spectrum, "Ukraine Weapons Tech Thrives Amid Conflict" (Nov 2025)
- Ukraine's Arms Monitor, "TAF Industries: 150,000 FPVs per Month" (Oct 2025)
- The Record, "Cyberattack deals blow to Russian firmware" (Jul 2025)
- dev.ua, "Barvinok-5 video module developer interview" (Oct 2025)
- C4ISRNet, "How Ukraine learned to cloak its drones" (Oct 2022)
- NSDC Ukraine, "Results of Ukraine's Defense Industry in 2025: FPV Drones" (Jan 2026)
- ArduPilot Docs, mLRS integration guide
- GitHub: olliw42/mLRS, DroneBridge/ESP32, BUSHA/targets@mafia-targets
