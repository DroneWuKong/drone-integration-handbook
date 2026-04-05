# Video Transmitters (VTX)

> The VTX broadcasts the camera feed from the drone to the pilot's goggles.
> It's the most RF-sensitive component on the quad — power level, frequency,
> antenna choice, and placement directly determine video range and quality.
> In contested environments, the VTX is also the most vulnerable component:
> video jamming is now the primary counter-drone tactic.

**Forge DB:** 116 video transmitters
**Cross-references:** [FPV Cameras](fpv-cameras.md) ·
[Antennas](../fundamentals/antennas.md) ·
[Frequency Bands](../fundamentals/frequency-bands.md) ·
[Link Budgets](../fundamentals/link-budgets.md) ·
[Electronic Warfare](electronic-warfare.md) ·
[Military Firmware Forks](military-firmware-forks.md) ·
[OpenHD](openhd-implementation-guide.md)

---

## VTX Systems Overview

| System | Type | Resolution | Latency | Encryption | Ecosystem |
|--------|------|-----------|---------|------------|-----------|
| Analog 5.8 GHz | Analog | ~700 TVL | <1 ms | None | Open (any goggles) |
| DJI O3 / O4 Pro | Digital | 1080p+ | ~30–50 ms | Yes | DJI goggles only |
| Walksnail Avatar | Digital | 1080p | ~30–50 ms | Yes | Walksnail/compatible |
| HDZero | Digital | 720p | <4 ms | No | Multi-goggle |
| OpenHD / OpenIPC | Digital | Variable | 80–150 ms | Configurable | Open source |

---

## Analog VTX

### How It Works

The camera outputs a composite video signal. The VTX modulates this onto an RF
carrier (typically 5.8 GHz) and broadcasts it. The receiver in the goggles
demodulates it back to video. Simple, fast, proven.

### Power Levels

| Power | Range (typical) | Use Case |
|-------|----------------|----------|
| 25 mW | 200–500 m | Indoor, proximity, pit mode |
| 200 mW | 500 m – 1 km | Park flying, freestyle |
| 400 mW | 1–2 km | General FPV |
| 600 mW | 2–4 km | Long range, penetration |
| 1–2 W | 4–10+ km | Extended long range |
| 5 W | 10+ km | Maximum range (military) |

Higher power = more range but also more heat, more current draw, and more
detectable by enemy RF sensors. Military use favors minimum necessary power
to reduce electronic signature.

### Frequency Bands (5.8 GHz)

Standard analog VTX operates across several band groups within 5.8 GHz:

| Band | Channels | Range | Notes |
|------|----------|-------|-------|
| A (Boscam) | 8 | 5865–5725 MHz | Legacy |
| B (Boscam) | 8 | 5733–5866 MHz | Legacy |
| E (DJI/Lumenier) | 8 | 5705–5880 MHz | Common |
| F (ImmersionRC/FatShark) | 8 | 5740–5880 MHz | Common |
| R (Raceband) | 8 | 5658–5917 MHz | Racing standard |
| L (Low) | 8 | 5362–5614 MHz | Less common |

**Raceband** is the standard for multi-pilot flying because its channels are
spaced to minimize adjacent-channel interference.

### Non-Standard Frequencies

In contested environments, operators move away from 5.8 GHz to bands that
enemy jammers don't cover:

- **1.2 / 1.3 GHz** — longer wavelength, better obstacle penetration, fewer
  jammers targeting this band. Requires larger antennas. Gaining popularity
  in Ukrainian military use.
- **2.4 GHz** — shared with control links (ELRS, etc.), which creates
  self-interference risk. Some operators use it for video when 5.8 GHz is
  jammed.
- **7.2 GHz** — first deployed by Ukraine summer 2025. Caused significant
  disruption because Russian jammers weren't covering it. Very short
  wavelength = needs line of sight but compact antennas.

MILBETA firmware unlocks VTX frequency control from 3000–6999 MHz (vs stock
Betaflight's 4900–5999 MHz), enabling operation on these non-standard bands.

---

## Digital VTX Systems

### DJI O3 / O4 Pro

DJI's FPV video system dominates the consumer digital market. The O4 Pro is
the current generation.

**Architecture:** integrated air unit (camera + VTX + processor in one module).
Video is encoded on the drone, transmitted digitally, and decoded in DJI
goggles. Supports recording onboard.

**Strengths:** best image quality, established ecosystem, reliable link.
**Weaknesses:** heaviest option, most expensive, locked to DJI goggles,
closed-source firmware, DJI Remote ID concerns in military contexts.

### Walksnail Avatar

Caddx/Walksnail's competing digital system.

**Architecture:** separate camera and VTX board, connected by ribbon cable.
More modular than DJI — you can choose different cameras.

**Strengths:** modular, good image quality, competitive pricing, supports
gyro data passthrough for stabilized HD recording.
**Weaknesses:** smaller ecosystem than DJI, fewer goggle options.

### HDZero

The racer's digital system. Fundamentally different architecture from
DJI/Walksnail.

**Architecture:** digital transmission optimized for minimum latency rather
than maximum resolution. Sub-4ms glass-to-glass latency — comparable to
analog.

**Strengths:** lowest latency of any digital system, lightweight modules
(Whoop VTX is extremely compact), open protocol supporting multiple goggle
brands, community-driven development.
**Weaknesses:** 720p maximum resolution (lower than competitors), smaller
ecosystem.

### OpenHD / OpenIPC

Open-source digital video. Two approaches:

**OpenHD** — runs on Raspberry Pi hardware. Uses WiFi chipsets for
wifibroadcast-style unidirectional streaming. Higher latency (100–150ms)
but fully configurable frequencies and parameters.

**OpenIPC** — reflashes IP camera board firmware. The camera SoC's hardware
video encoder provides 1080p60 at ~80ms latency and only 1.7W power draw.
Cheaper and lower power than OpenHD but harder to set up. License explicitly
prohibits military use.

**See:** [OpenHD Implementation Guide](openhd-implementation-guide.md)

---

## VTX Control

### SmartAudio / IRC Tramp

Protocols that allow the FC to control the VTX (power level, channel,
frequency) via a serial connection. Betaflight, iNav, and ArduPilot all
support VTX control tables. This enables:

- **Pit mode** — low power on the ground to avoid interfering with others
- **In-flight channel switching** — change frequency without landing
- **Power ramping** — automatic power increase after takeoff

MILBETA extends this with armed VTX switching (normally locked in stock
Betaflight) and the expanded 3000–6999 MHz frequency range.

### VTX Tables

Betaflight uses VTX tables to define available bands, channels, and power
levels for each VTX model. The table must match your hardware — wrong table
= wrong frequencies. Custom VTX tables can be created for non-standard
frequency operation.

---

## Antenna Considerations

VTX antenna choice is as important as the VTX itself. Key factors:

**Polarization** — circular polarization (RHCP or LHCP) is standard for FPV.
Rejects multipath reflections. Both the VTX antenna and goggle antenna must
match polarization.

**Gain vs coverage** — omnidirectional antennas (dipole, pagoda, lollipop)
provide coverage in all directions but limited range. Directional antennas
(patch, helical) on the receiver side extend range but require tracking.

**Connector type** — SMA, RP-SMA, MMCX, UFL/IPEX. Smaller connectors
(MMCX, UFL) are lighter but more fragile. Pigtail adapters add weight but
protect the VTX connector.

**Mounting** — the antenna must be above and clear of the carbon fiber frame.
Carbon attenuates RF. A VTX antenna sandwiched between carbon plates will
have severely reduced range.

---

## VTX Selection Criteria

1. **Which video system are your goggles?** — this narrows the field
   immediately. Analog goggles need analog VTX, DJI goggles need DJI air
   units, etc.
2. **Power level needed?** — determined by range requirements and legal
   limits (if applicable).
3. **Size and weight?** — micro builds need micro VTX. Weight matters for
   racing and small quads.
4. **Frequency flexibility?** — for contested environments, ability to
   operate on non-standard frequencies is critical.
5. **Smart Audio / control protocol?** — needed for FC-based VTX management.
6. **Stack compatibility?** — 20×20 or 30.5×30.5 mounting.

---

## Contested Environment VTX Strategy

The video link is now the primary target for counter-drone EW. A layered
approach to video survivability:

**Layer 1 — frequency diversification.** Don't use standard 5.8 GHz Raceband
channels. Move to less-targeted bands (1.2 GHz, off-band 5.8 GHz channels,
7.2 GHz).

**Layer 2 — power management.** Use minimum necessary power to reduce
detectability. Higher power = easier to detect and direction-find. Increase
power only when range demands it.

**Layer 3 — digital encryption.** Digital systems (DJI, Walksnail) encrypt
the video feed, preventing interception. Analog feeds are fully open —
anyone on the frequency sees what you see.

**Layer 4 — FHSS / spread spectrum.** Systems like Barvinok-5 use frequency-
hopping spread spectrum to make jamming extremely difficult. The signal hops
across a wide band in a pseudo-random pattern that the jammer can't predict.

**Layer 5 — fiber optic.** Eliminates the RF video link entirely. The video
signal travels through a physical fiber cable, immune to all RF-based
jamming. Limited by cable weight and range. Both sides are mass-producing
fiber-optic FPV drones.

---

## VTX Systems in Forge

| System | Count | Notes |
|--------|-------|-------|
| Walksnail Avatar | 23 | Most modular digital option |
| DJI O3/O4 | 18 | Integrated air units |
| Analog | 14 | Legacy + budget builds |
| HDZero | 10 | Low-latency digital |
| Herelink | 4 | Enterprise/commercial |
| Other | 47 | Specialty, long-range, custom |

---

## Sources

- Forge parts database (116 video transmitters)
- Oscar Liang, VTX and video system guides
- Armada International, "Jamming UAV Video Signals" (Feb 2026)
- Cybershafarat, MILBETA VTX frequency unlock documentation
- dev.ua, Barvinok-5 FHSS video system
- OpenHD project documentation
- OpenIPC project (note: license prohibits military use)
