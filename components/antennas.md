# Antennas

> **Forge cross-reference:** 394 entries in `antennas` category  
> **Related handbook chapters:** Video Transmitters (VTX), RC Receivers, Mesh Radios, RF Tools

## Antennas Are Not Accessories

Antennas are frequently treated as afterthoughts — "I'll just use whatever came in the box." This is wrong. The antenna is the last element in your RF chain and the one most operators never think about. A bad antenna placement or mismatch can reduce your effective video range by 60% or cause unexpected video breakup at ranges where your link budget says you should be fine.

The good news: you don't need to be an RF engineer to make good antenna decisions. You need to understand four concepts — gain, polarization, radiation pattern, and impedance matching. Everything else is detail.

## Core Concepts

### Gain
Antenna gain is measured in dBi (decibels relative to an isotropic radiator). A 0 dBi antenna radiates equally in all directions — a perfect sphere. A 3 dBi antenna focuses that energy into a flatter "donut" shape, doubling the power in the horizontal plane at the cost of the vertical. A 9 dBi patch antenna focuses into a narrow cone.

**Rule:** Gain is not free energy. It's redistribution. More gain in one direction means less in others.

For FPV video antennas:
- 0–2 dBi omnidirectional: standard for short-range freestyle and racing
- 3–5 dBi omnidirectional: medium range, slightly flattened pattern
- 7–14 dBi patch/directional: long-range, requires aiming

### Polarization
Polarization describes the orientation of the electromagnetic wave. Antennas can be linearly polarized (horizontal or vertical) or circularly polarized (RHCP or LHCP).

**Circular polarization** (CP) is the standard for FPV video. Why: a circularly polarized wave maintains polarization as the drone rolls and pitches. A linearly polarized signal fades when the transmit and receive antenna orientations mismatch. LHCP and RHCP should be matched — mixing them causes ~30dB loss.

**Linear polarization** is standard for RC control links (ELRS, Crossfire, FrSky). The control link's receiver diversity and frequency hopping compensate for the polarization variation.

**Rule for video:** Match polarity. VTX antenna and goggles antenna should both be RHCP or both LHCP. DJI uses RHCP as standard.

### Radiation Pattern
The 3D shape of where the antenna transmits and receives. For an omnidirectional antenna, this is a torus (donut) — strong around the equator, nulls at the poles.

**Practical implication:** When the drone is directly above or below you, an omni antenna has a null. For high-altitude operations, a patch antenna pointed up or a diversity system is needed.

### Impedance Matching
All drone RF systems run at 50 ohm impedance. Antennas, cables, and connectors must all be 50 ohm. Mismatched impedance causes standing wave reflections that waste power and can damage transmitters.

In practice: use proper SMA/RP-SMA connectors, avoid exceeding manufacturer cable length recommendations, and never kink coaxial cable.

## Antenna Types

### Stub / Whip (Omni, Linear, 0–3 dBi)
The simplest antenna — a piece of wire cut to quarter-wave length. The "rubber duck" antenna on most receivers is a loaded stub. Very small, adequate for short range. Not used for video in any serious application.

### Dipole / Cloverleaf (Omni, RHCP/LHCP, 0–3 dBi)
The workhorse FPV antenna. A cloverleaf or skew-planar wheel antenna consists of 3–4 angled elements that create circular polarization. RHCP cloverleafs are the standard drone-side video antenna for analog systems.

Examples: TrueRC Singularity, Pagoda series, generic cloverleaf sets.

### Lollipop / Mushroom (Omni, CP, 1–3 dBi)
A compact circularly polarized design that outperforms cloverleafs in size/performance ratio. Standard for DJI digital systems. Very common — included with most DJI VTX products.

Examples: GEPRC Stable V2, Foxeer Lollipop 4.

### Pagoda (Omni, CP, 0–2 dBi)
A printed circuit board antenna design that became popular for its flat radiation pattern and excellent CP purity. Very durable (PCB construction), excellent for goggle antennas. Less common now as lollipops improved.

### Patch (Directional, CP or Linear, 9–13 dBi)
A flat PCB antenna with high gain in a forward hemisphere. The standard ground station antenna for long-range FPV and video downlink. Paired with an omni antenna in a diversity receiver setup (Rapidfire, DJI Goggles 2 diversity, antenna tracker systems).

**Usage:** Mount on a tripod or antenna tracker pointed at the expected flight zone. Provides dramatic range extension for long-range flights but requires accurate aiming.

Examples: TrueRC X-Air, ImmersionRC SpiroNET, generic patches.

### Helical (Directional, RHCP, 10–15 dBi)
A coiled conductor around a central axis that produces very high-gain circular polarization. More directional than patch, excellent axial ratio. Used in long-distance UAV video links and sometimes in GPS reception. Expensive to manufacture at quality.

### Panel / Yagi (Directional, Linear, 14–20 dBi)
Very high gain, very narrow beam. Used in some FPV long-range antenna tracker setups and fixed-link video infrastructure. Not practical for handheld use.

## System Design Decisions

### For FPV Racing / Freestyle (Short Range, <400m)
Both TX (VTX antenna) and RX (goggle antenna) should be omni RHCP. Typical: Lollipop 4 on drone, Rapidfire diversity receiver with two omnis on goggles. Total system weight: 5–10g. No aiming required.

### For Long-Range FPV / Cinematic (400m–10km)
Omni RHCP on drone. Diversity system on goggles: one omni + one patch. The omni provides coverage when close or overhead, the patch provides gain when far. An antenna tracker that keeps the patch aimed at the drone extends range to the link budget limit.

### For Fixed-Wing BVLOS (10km+)
Patch or helical on a dedicated antenna tracker. Diversity diversity omni for backup. Ensure you have the correct antenna gain for your link budget — at 50km you cannot rely on an omni VTX antenna and a patch goggle antenna. You need a high-gain antenna on both sides, or a relay drone.

### Control Link Antennas
ELRS/Crossfire antennas are linear and typically dipole whips. The TX module antenna should be positioned upright (vertical polarization standard). Receiver antennas on the drone should be routed at approximately 90° to each other for diversity (one horizontal, one vertical, or angled apart) with antennas mounted clear of carbon fiber frame arms.

## Connectors

The FPV antenna connector ecosystem is fragmented and a source of real frustration:

- **SMA** — The sensible standard. Secure threaded connection. Used on most VTX, some goggles, and higher-end receivers.
- **RP-SMA** (Reverse Polarity SMA) — The center pin and outer thread are swapped relative to SMA. Used extensively by DJI, some FrSky products, and many goggles. SMA and RP-SMA are mechanically compatible but electrically incompatible — they connect but don't pass signal. This is a common and invisible failure mode.
- **U.FL / IPEX** — Tiny board-level connector used on receivers and some FCs for direct antenna attachment. Very low power handling. A U.FL-to-SMA pigtail is required for external antennas.
- **MMCX** — Similar to U.FL but slightly larger and more robust. Used by some TBS products.

**Rule:** Check connector type before ordering. A mismatched connector can silently kill your RF performance.

## NDAA

Antennas themselves are passive RF devices — the NDAA concern is manufacturing origin. Most high-performance FPV antennas come from: TrueRC (Canada ✓), ImmersionRC (Ireland ✓), AKK (China ✗), Foxeer antennas (China ✗), GEPRC (China ✗).

For non-critical use, Chinese-made antennas are functionally adequate. For federated procurement, TrueRC and ImmersionRC are the primary NDAA-compliant high-performance options.

## Forge Cross-Reference

394 antenna entries spanning every category above. Use the `USA` and `NDAA ✓` filter pills to narrow to compliant options. The antennas category currently shows manufacturer_country as the primary compliance indicator — sort by price to find budget omni options vs. premium directional systems.
