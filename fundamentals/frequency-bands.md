# Chapter 2: Frequency Bands and Regulatory Reality

> The regulations tell you what you're allowed to do.
> The physics tell you what will actually work.
> They don't always agree.

---

## The Bands That Matter

Drone operations live in a handful of frequency bands. Here's where
everything sits and why.

### 900 MHz (902–928 MHz in the US, 868 MHz in EU)

**What lives here:** Long-range RC links (ELRS 900, TBS Crossfire),
telemetry radios (RFD900x, SiK, MicroHard P900), some mesh radios,
LoRa, and a surprising amount of industrial IoT.

**Why it matters:** Sub-GHz propagation is king. 900 MHz bends around
obstacles, penetrates foliage, and reaches farther per milliwatt
than any other band you'll use. A 100 mW ELRS 900 link will
outrange a 1 W 2.4 GHz link in most real-world environments.

**Regulatory:**
- US: ISM 902–928 MHz, up to 1 W conducted + antenna gain (FCC Part 15.247)
- EU: 868 MHz band, 25 mW ERP with duty cycle limits (ETSI EN 300 220)
- The EU/US split is the single biggest cross-border problem in
  drone operations. 900 MHz hardware built for the US market
  doesn't work in Europe, and vice versa. ELRS handles this with
  region-specific firmware builds. Many other systems don't.

**What the regulations don't tell you:** The 900 MHz ISM band
is shared with utility meters (smart grid AMI), industrial SCADA,
agricultural sensors, and LoRaWAN gateways. In urban environments,
the noise floor at 900 MHz can be 20+ dB higher than rural. Your
range will be shorter in the city.

---

### 2.4 GHz (2400–2483.5 MHz)

**What lives here:** Most RC links (ELRS 2.4, Ghost, ACCST, IBUS),
WiFi (802.11b/g/n/ax), Bluetooth, ZigBee, microwave ovens, baby
monitors, wireless cameras, mesh radios, and roughly half of all
wireless devices ever manufactured.

**Why it matters:** 2.4 GHz is the default for everything. It's
globally harmonized (same band everywhere), license-free, and
supported by every chip on the market. If you don't know what
frequency to use, you use 2.4 GHz. So does everyone else.

**Regulatory:**
- Global ISM band, generally 100 mW–1 W EIRP depending on jurisdiction
- FCC: up to 1 W conducted, 4 W EIRP with directional antennas (Part 15.247)
- EU: 100 mW EIRP (ETSI EN 300 328)
- Japan: 10 mW/MHz (effectively limits wideband signals)

**What the regulations don't tell you:** 2.4 GHz is a war zone.
At any given moment at a race event, fly-in, or urban deployment
site, you're sharing spectrum with:
- Every phone's WiFi and Bluetooth
- Every laptop's WiFi
- Every smart home device
- Other pilots' RC links
- Nearby mesh radios
- The microwave in the food truck

The saving grace is that modern protocols (ELRS, Ghost, CRSF) use
frequency hopping, which spreads the signal across the entire band
and makes them resilient to narrowband interference. But when the
entire band is congested, even FHSS degrades.

**The 2.4 GHz deconfliction problem:** If your RC link is 2.4 GHz
AND your mesh radio is 2.4 GHz AND your companion computer's WiFi
is 2.4 GHz, you have three transmitters on the same band in the
same airframe. Even with different channels and different protocols,
the front-end receivers will desense each other. The fix is simple:
put at least one of them on a different band.

---

### 5.8 GHz (5725–5875 MHz)

**What lives here:** Analog FPV video, digital FPV video (DJI, HDZero,
Walksnail), 5 GHz WiFi (802.11a/n/ac/ax), some mesh radios, radar,
and weather services.

**Why it matters:** 5.8 GHz is the FPV video band. Virtually every
drone with a camera transmits video on 5.8 GHz. The band has enough
bandwidth for analog and digital video, and the higher frequency
means smaller antennas.

**Regulatory:**
- ISM 5.725–5.875 GHz in most jurisdictions
- FCC: 1 W conducted (Part 15.247)
- EU: 25 mW EIRP (yes, really — ETSI EN 300 440). Most VTX
  modules shipped into the EU are technically non-compliant
  at any setting above 25 mW.
- The broader 5 GHz UNII bands (5.15–5.35, 5.47–5.725 GHz) are
  used by WiFi but have DFS (Dynamic Frequency Selection)
  requirements due to radar coexistence. DFS can force your
  radio to change channels mid-flight. Not ideal.

**What the regulations don't tell you:**
- 5.8 GHz has significantly higher path loss than 2.4 GHz. In
  free space, 5.8 GHz loses ~7.7 dB more than 2.4 GHz at the
  same distance. In practice this means roughly half the range
  per milliwatt. You compensate with power and antenna gain.
- 5.8 GHz does not penetrate foliage, buildings, or terrain well.
  If you fly behind a tree, your video will break before your
  RC link does (assuming RC is on 2.4 GHz or 900 MHz).
- At FPV race events, analog 5.8 GHz channel management is
  critical. 40 channels sounds like a lot until 8 pilots are
  in the air and their harmonics are stepping on each other.
  Digital systems (DJI, HDZero) are wideband and harder to
  deconflict — they don't fit neatly into the 40-channel system.

---

### Sub-GHz Below 900 (433, 315, 169 MHz)

**What lives here:** LoRa long-range, some RC systems (FrSky R9
at 433 MHz in some regions), key fobs, garage door openers,
tire pressure monitors, and very long-range telemetry.

**Why it matters:** Lower frequency = better propagation = longer range.
433 MHz LoRa links can reach 10+ km with tiny antennas and milliwatts
of power. But bandwidth is measured in kilobits, not megabits.

**Regulatory:**
- 433 MHz ISM: 10 mW in EU, not ISM in the US (amateur band,
  requires ham license for non-ISM use)
- 315 MHz: US ISM for low-power devices
- 169 MHz: EU smart meter band, very restricted

**When you'd use it:** Very long-range telemetry (LoRa), sub-floor
FHSS detection (listening, not transmitting), or interoperability
with existing infrastructure on these bands.

---

### Military and Licensed Bands

**L-band (1–2 GHz):** Some tactical mesh radios (Doodle Labs HelixL+S).
Military satellite. GPS (L1 at 1575.42 MHz, L2 at 1227.60 MHz).
No ISM access — requires licensing or government authorization.

**S-band (2–4 GHz):** Overlaps 2.4 GHz ISM. Some military radar.
Weather radar. Tactical links.

**C-band (4–8 GHz):** Doodle Labs C-Band radios, satellite downlinks,
some military comms. Requires licensing in most jurisdictions.

**You don't need to operate on these bands** unless you're working
with military or government platforms. But you do need to know they
exist because: (a) military radar on S-band and C-band can overwhelm
your receivers, and (b) GPS signals on L-band can be jammed or
spoofed, affecting your drone's navigation.

---

## The Gap Between Rules and Reality

### What Operators Actually Do

The regulatory framework assumes static, ground-based transmitters
in controlled environments. Drone operations are none of those things.

In practice:
- FPV pilots routinely fly 600–800 mW VTX power despite EU limits of 25 mW
- Long-range operators use 900 MHz at full power in countries where
  the band allocation is ambiguous
- "1 W EIRP" limits are rarely enforced at hobby flying fields
- Military operators have blanket spectrum authority in their
  operational areas and don't worry about ISM band rules

This handbook doesn't tell you to break the rules. It tells you
the rules exist, what they are, and acknowledges that the
enforcement reality differs from the regulatory text. Know your
jurisdiction's rules. Make your own informed decisions.

### Frequency Coordination at Events

At any gathering of more than 4-5 pilots:

1. **Assign video channels before anyone powers up.** Analog 5.8 GHz
   has 40 channels across 6 bands (A, B, E, F, R, L). Use non-adjacent
   channels. Band F (Fatshark / IRC) and Band R (RaceBand) are the
   most common for events.

2. **Separate RC bands.** If half the pilots are on 2.4 GHz ELRS and
   half are on 900 MHz Crossfire, that's actually ideal — no RC
   interference between the two groups.

3. **Power down when not flying.** A VTX broadcasting 800 mW on the
   ground creates more interference than one in the air at 200m,
   because ground-level signals have direct paths to every other
   receiver in the pit area.

4. **Know your VTX table.** Betaflight's VTX table maps power levels
   and channels for your specific VTX hardware. Verify it matches
   reality — misconfigured VTX tables can put you on the wrong
   channel or the wrong power level.

### Frequency Coordination for Fleet Operations

At a commercial or tactical deployment with multiple drones:

1. **Map all five links for each platform.** Build a frequency plan
   before the operation, not during it.

2. **Separate bands where possible.** RC on 900, telemetry on 2.4,
   video on 5.8, mesh on a different 5 GHz channel. The more band
   separation, the less self-interference.

3. **Document what's transmitting.** If you're operating near other
   teams, other companies, or military assets, knowing exactly what
   frequencies you're using — and at what power — prevents problems
   and demonstrates professionalism.

4. **Plan for interference.** If your operation is near an airport,
   military base, or large venue (stadiums use a LOT of 2.4 and 5 GHz),
   your range predictions from a clean test site are optimistic.
   Budget a 50% range reduction in congested spectrum environments.

---

## Quick Reference: Band Comparison

| Band | Range (per mW) | Penetration | Bandwidth | Congestion | Typical Use |
|------|---------------|-------------|-----------|------------|-------------|
| 433 MHz | Excellent | Best | Very low | Low | LoRa telemetry |
| 900 MHz | Very good | Good | Low-medium | Medium | Long-range RC, telemetry |
| 2.4 GHz | Good | Fair | High | Severe | RC, WiFi, mesh, BLE |
| 5.8 GHz | Fair | Poor | Very high | High | FPV video, WiFi |

The universal trade-off: **lower frequency = longer range and better
penetration but less bandwidth. Higher frequency = more bandwidth
but shorter range and worse penetration.** Everything in RF engineering
is a version of this trade-off.

---

## Next

- **Chapter 3: Antennas for People Who Aren't RF Engineers** — how to
  choose, orient, and not break your antennas.
- **Chapter 1: The Five Link Types** — frequency deconfliction in
  the context of a complete drone system.

---

*The spectrum is a shared resource. Know what you're transmitting,
where, and at what power. The drone next to you is sharing the
same resource.*
