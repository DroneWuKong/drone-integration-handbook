# ELINT for Drone Operators

> Serhii "Flash" Beskrestnov drives a black VW van bristling with antennas
> across Ukraine, teaching military units to read the electromagnetic
> spectrum. He created the "Military Signalmen" Signal group that became
> a 24-hour support service for communications specialists across every
> sector of the frontline. The knowledge he teaches informally has never
> been written down in a consolidated, operator-accessible format.
> This guide is an attempt to fill that gap.

**What this is:** a practical introduction to reading RF spectrum data
as a drone operator — understanding what you're seeing, what it means
for your mission, and what to do about it.

**What this is not:** a signals intelligence (SIGINT) manual. This is
the 20% of ELINT knowledge that covers 80% of what a drone operator
needs to know.

**Cross-references:** [Frequency Bands](../fundamentals/frequency-bands.md) ·
[EW Countermeasures](ew-countermeasures.md) ·
[Frequency Planning](frequency-planning.md) ·
[Electronic Warfare](../components/electronic-warfare.md) ·
[Military Firmware Forks](../components/military-firmware-forks.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md)

---

## The Electromagnetic Spectrum Is a Battlefield

Every drone emits RF energy. Every jammer emits RF energy. Every radio,
WiFi access point, and cell tower emits RF energy. A spectrum analyzer
shows you all of it — who's transmitting, on what frequency, how strong,
and often from what direction.

For a drone operator, this means:

- **Before launch:** is the spectrum clear? Are there jammers active?
  Are friendly drones already on your planned channels?
- **During ops:** is interference increasing? Has a new jammer appeared?
  Is someone intercepting your video feed?
- **After ops:** what did the enemy's RF signature look like? What
  frequencies were they using? This is intelligence for the next mission.

---

## Equipment

### Minimum: RTL-SDR ($25-40)

A USB software-defined radio dongle. Receives (listen only, does not
transmit) from about 24 MHz to 1.7 GHz. Paired with free software,
it's a basic spectrum analyzer.

| Parameter | RTL-SDR v3/v4 |
|-----------|--------------|
| Frequency range | 24 MHz – 1.766 GHz |
| Bandwidth | ~2.4 MHz visible at once |
| Dynamic range | ~50 dB |
| Cost | $25-40 |
| Software | SDR#, GQRX, SDR++, rtl_power |
| Power | USB powered |

**Limitation:** cannot see 2.4 GHz or 5.8 GHz — the two most
important FPV bands. For those you need a different receiver.

### Better: RTL-SDR + HackRF + Downconverter

| Tool | Frequency Range | Notes |
|------|----------------|-------|
| RTL-SDR v3/v4 | 24 MHz – 1.7 GHz | 433, 868, 915 MHz coverage |
| HackRF One | 1 MHz – 6 GHz | Covers 2.4 GHz and 5.8 GHz |
| Ham-It-Up downconverter | HF (0-30 MHz) with RTL-SDR | Not needed for drone ops |

HackRF One ($300-350) covers the full drone spectrum including 2.4 GHz
(ELRS, Ghost) and 5.8 GHz (video). Combined with RTL-SDR for sub-GHz,
you have full coverage.

### Purpose-Built: Handheld Spectrum Analyzers

| Tool | Range | Notes |
|------|-------|-------|
| TinySA Ultra | 100 kHz – 5.3 GHz | Handheld, $130, good enough for field use |
| RF Explorer | 240 MHz – 6.1 GHz | More accurate, ~$300 |
| Kvertus spectrum tools | Custom | Ukrainian-made, battle-optimized |

TinySA Ultra is the sweet spot for most operators — covers 433 MHz
through 5.3 GHz in a pocket-sized device. Doesn't quite reach 5.8 GHz
but covers the control link bands and most of the video band.

### Antenna Matters

The SDR is only as good as its antenna. The included telescoping whip
is adequate for strong nearby signals. For useful ELINT:

- **Wideband discone** — omnidirectional, covers 25 MHz – 6 GHz. Mount
  on a mast for best results. Good for general spectrum survey.
- **Directional Yagi or log-periodic** — for direction-finding. Narrow
  beamwidth lets you sweep and find the bearing to a specific signal.
- **2.4 GHz patch or Yagi** — dedicated to the ELRS/Ghost band.
- **5.8 GHz patch** — dedicated to the video band.

---

## What to Look For

### Pre-Mission Spectrum Sweep

Before launching, do a 60-second sweep across your operating bands.
You're looking for:

**1. Active jammers**

Jammers appear as broadband noise — a raised noise floor across a
wide frequency range rather than a narrow signal on a specific
channel. A jammer on 5.8 GHz raises the noise floor across the
entire 5.6-6.0 GHz range. A GPS jammer raises the floor around
1.575 GHz.

What it looks like on a spectrum display:
```
Normal:     ____|_____|____    (narrow spikes = individual signals)
Jammed:     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾    (elevated floor = broadband noise)
```

**2. Enemy control links**

Enemy drone control links appear as narrow signals hopping across a
band. ELRS hops rapidly (dozens of channels per second) and appears
as a faint smear across the band rather than a fixed signal. DJI
OcuSync appears as a wider OFDM signal (~20 MHz wide) that's easier
to spot.

**3. Enemy video transmitters**

Analog VTX signals are the easiest to detect. They're narrowband
(6-8 MHz), fixed frequency (not hopping), and continuous. A 5.8 GHz
analog VTX on Raceband R1 appears as a strong, steady signal at
5658 MHz.

Digital video (DJI, Walksnail) is wider bandwidth (~20 MHz) and
more complex, but still identifiable by its characteristic shape
on the spectrum.

**4. Your own emissions**

Power up your own drone and check what it looks like on the spectrum
analyzer. Know your own RF fingerprint. Verify your VTX is on the
right channel and not putting out harmonics or spurs on other bands.

**5. Ambient interference**

WiFi access points, cell towers, industrial equipment, power lines,
and other non-drone sources. These are permanent features of the RF
landscape. Note them so you don't mistake them for threats.

---

## Reading the Waterfall Display

Most SDR software shows two views:

**Spectrum view (top):** real-time power vs frequency. X-axis =
frequency, Y-axis = signal strength (dBm or dB). Spikes are
transmitters.

**Waterfall view (bottom):** time vs frequency with color = power.
X-axis = frequency, Y-axis = time (scrolling), color = signal
strength. This shows how signals change over time.

### Pattern Recognition

| Pattern | What It Is |
|---------|-----------|
| Thin vertical line (waterfall) | Fixed-frequency transmitter (analog VTX, FM radio) |
| Rapid horizontal dashes | Frequency-hopping signal (ELRS, FHSS) |
| Wide colored band | Broadband signal (jammer, WiFi, DJI OFDM) |
| Pulsing signal | Intermittent transmitter (radar, pulsed jammer) |
| Signal that moves frequency | Scanning jammer or chirp |
| Sudden noise floor elevation | Jammer activated |
| Narrow signal appearing/disappearing | Drone launching/landing |

---

## Direction Finding (Basic)

With a directional antenna (Yagi, log-periodic, or even a patch
antenna), you can estimate the bearing to a signal:

1. Tune the SDR to the target signal's frequency
2. Slowly rotate the directional antenna 360°
3. Note the bearing where the signal is strongest — that's the
   approximate direction to the transmitter
4. Note the bearing where the signal is weakest (null) — this is
   180° from the transmitter (on a Yagi) or 90° (on some antennas)

**Accuracy:** ±10-30° with a handheld Yagi, depending on multipath
and reflections. Good enough to determine general direction — is the
jammer to the north or to the east? Good enough to vector an
interceptor drone.

**MILELRS EW overlay** does this automatically at the drone level —
the receiver's antenna diversity and signal processing estimates the
EW source direction and displays it on the pilot's OSD. Manual DF
with a ground-based SDR complements this by providing ground-level
data.

---

## Video Frequency Intelligence

Both sides compile and share statistics on enemy video frequencies
detected by ELINT forces. This data drives tactical adaptation:

- If 80% of enemy video is on 5.8 GHz band F, concentrate jamming
  resources on those specific channels
- If enemy starts appearing on 1.2 GHz, alert EW units to cover
  that band
- If enemy deploys 7.2 GHz video (as Ukraine did in summer 2025),
  this reveals a gap in current jamming coverage

**As a drone operator, the inverse applies:** check what frequencies
the enemy's ELINT is detecting. If they're publishing statistics
showing your video frequencies, you need to move to a band they're
not monitoring.

---

## Practical ELINT Workflow

### Before Mission

1. **Spectrum sweep** — 30-60 seconds across 400 MHz – 6 GHz
2. **Document the noise floor** — photograph or save a screenshot
   of the baseline spectrum. This is your reference.
3. **Identify known signals** — WiFi, cell, friendly radio nets.
   Anything you can account for is not a threat.
4. **Identify unknown signals** — anything you can't account for
   is potentially enemy or jammer. Note frequency and bearing.
5. **Adjust frequency plan** — if a band is noisy or has jammer
   activity, move your planned channels to a clear band.

### During Mission

1. **Monitor your operating bands** — if the noise floor rises on
   your control or video band, a jammer may have activated.
2. **Watch for new signals** — a new narrowband signal appearing on
   5.8 GHz while you're operating may be an enemy video feed, which
   means an enemy drone is nearby.
3. **Correlate with link quality** — if your OSD shows LQ dropping
   and the spectrum shows increased noise on your band, that confirms
   jamming (vs a range issue or hardware problem).

### After Mission

1. **Save spectrum recordings** — most SDR software can record
   I/Q data for later analysis.
2. **Report findings** — frequencies detected, signal types,
   jammer activity, bearing estimates. This intelligence feeds
   into the next mission's frequency plan and EW response.
3. **Update the team** — share what you found with other operators.
   The "Military Signalmen" model of shared intelligence is the
   most effective pattern.

---

## Safety and Legal

- **An SDR receives only.** It does not transmit. Receiving is legal
  in virtually all jurisdictions. Transmitting on frequencies you
  don't hold a license for is not.
- **Do not transmit on enemy frequencies** unless you have specific
  authorization (EW operations, military authority). Receiving and
  analyzing is intelligence. Transmitting is electronic attack,
  which is a different authority level.
- **Encrypt your own signals** where possible (MILELRS, digital video).
  Assume the enemy has the same ELINT capability you do.

---

## Sources

- MIT Technology Review, "Meet the radio-obsessed civilian shaping
  Ukraine's drone defense" (Sep 2024) — profile of Flash
- IEEE Spectrum, "Ukraine Is the First Hackers' War" (Mar 2025)
- Armada International, "Jamming UAV Video Signals" (Feb 2026) —
  video frequency ELINT statistics
- RTL-SDR project documentation
- HackRF One documentation
- TinySA Ultra user community
- Ukrainian Military Signalmen community practices (public)
