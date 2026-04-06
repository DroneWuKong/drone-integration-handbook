# Frequency Planning Worksheet

> You have 6 drones, each with a control link, video link, and GPS. That's
> 18 RF links sharing the same airspace. If you don't plan your frequencies,
> your own fleet will jam itself before the enemy gets a chance to. This
> guide is the practical worksheet for deconflicting multi-drone operations.

**Format:** Print the assignment table. Fill it in before every multi-drone op.
**Cross-references:** [Frequency Bands](../fundamentals/frequency-bands.md) ·
[Link Budgets](../fundamentals/link-budgets.md) ·
[Antennas](../fundamentals/antennas.md) ·
[CRSF & ELRS Protocol](../firmware/crsf-elrs-protocol.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[EW Countermeasures](ew-countermeasures.md) ·
[Comms & Datalinks](../components/comms-datalinks.md)

---

## The Three Links Per Drone

Every FPV drone has at minimum two active RF links, sometimes three:

| Link | Direction | Typical Band | Purpose |
|------|-----------|-------------|---------|
| Control (RC) | Ground → Air | 900 MHz or 2.4 GHz | Stick commands, arming, mode switching |
| Video (VTX) | Air → Ground | 5.8 GHz (or 1.2/2.4/7.2 GHz) | Camera feed to pilot goggles |
| GPS/GNSS | Satellite → Air | 1.575 GHz (L1), 1.227 GHz (L2) | Navigation, RTH, position hold |

GPS is receive-only and shared across all drones — it doesn't need
deconfliction. Control and video are the two links you must plan.

**Telemetry** rides on the control link (CRSF/ELRS telemetry is bidirectional
on the same channel). It does not need a separate frequency assignment.

**MAVLink telemetry over a separate radio** (SiK, mLRS, DroneBridge) is a
fourth link that DOES need its own frequency assignment.

---

## Frequency Band Map

### 900 MHz Band (ELRS 900 / MafiaLRS / mLRS)

| Use | Frequency Range | Notes |
|-----|----------------|-------|
| ELRS 900 MHz | 863–928 MHz | Region-dependent: EU 868 MHz, US/AU 915 MHz |
| MafiaLRS | 433–560 MHz + modified 868/915 | Non-standard bands for EW evasion |
| mLRS 900 | 863–928 MHz | LoRa modulation, longer frame times |
| MILELRS 900 | 863–928 MHz | Same hardware as ELRS, encrypted |

**Self-interference risk:** Low for control links because ELRS uses frequency
hopping (FHSS). Two ELRS transmitters on different binding phrases will
hop independently and rarely collide. However, if you run 6+ drones on 900 MHz
ELRS simultaneously, aggregate interference increases. Monitor LQ.

### 2.4 GHz Band (ELRS 2.4 / Ghost / WiFi)

| Use | Frequency Range | Notes |
|-----|----------------|-------|
| ELRS 2.4 GHz | 2400–2483 MHz | ISM band, shared with WiFi and Bluetooth |
| Ghost (GHST) | 2400–2483 MHz | Orqa/ImmersionRC protocol |
| WiFi (DroneBridge) | 2400–2483 MHz | Telemetry only |
| Bluetooth | 2400–2483 MHz | Short range, ground station |

**Self-interference risk:** HIGH. This band is crowded. WiFi from ground
stations, Bluetooth from phones, and multiple ELRS transmitters all compete.
ELRS FHSS helps but doesn't eliminate the problem. If running 4+ drones on
2.4 GHz ELRS, expect LQ degradation.

**WiFi conflict:** if using a DroneBridge ESP32 or companion computer with
WiFi (Raspberry Pi, VOXL 2) on the same drone, the WiFi radio can interfere
with a 2.4 GHz ELRS receiver. Use 900 MHz ELRS with 2.4 GHz WiFi, or
vice versa. Never stack same-band RC and WiFi on the same drone.

### 5.8 GHz Band (Video)

This is where frequency planning matters most. Analog VTX channels are
narrowband and can easily interfere with each other.

| Band | Channels | Range (MHz) | Channel Spacing |
|------|----------|-------------|----------------|
| R (Raceband) | R1–R8 | 5658–5917 | ~37 MHz apart |
| F (FatShark) | F1–F8 | 5740–5880 | ~20 MHz apart |
| A (Boscam A) | A1–A8 | 5865–5725 | ~20 MHz apart |
| E (DJI/Lumenier) | E1–E8 | 5705–5880 | ~25 MHz apart |

**Critical rule:** adjacent Raceband channels (e.g., R1 and R2) have
enough spacing for 2 drones. Adjacent channels on other bands may NOT —
some overlap. When mixing bands, use a frequency chart to verify no
channel is within 30 MHz of another active channel.

**Raceband is the standard for multi-pilot operations** because its channels
are deliberately spaced to minimize adjacent-channel bleed. Use Raceband
unless you have a specific reason not to.

### Non-Standard Video Bands

| Band | Notes |
|------|-------|
| 1.2 / 1.3 GHz | Long range, good penetration, fewer jammers. Large antennas. Harmonics can interfere with GPS L1 (1.575 GHz) — check with a spectrum analyzer. |
| 2.4 GHz video | Shared with RC band — **never use 2.4 GHz for both RC and video.** |
| 7.2 GHz | Very short wavelength, needs line of sight. Compact antennas. Not covered by most jammers (as of mid-2025). |

---

## The Assignment Table

Print this and fill it in before every multi-drone operation.

```
┌──────────────────────────────────────────────────────────────────┐
│              FREQUENCY ASSIGNMENT — DATE: ________              │
├──────┬───────────┬──────────┬──────────┬──────────┬─────────────┤
│ Drone│ Callsign  │ RC Band  │ RC Notes │ VTX Chan │ VTX Power   │
├──────┼───────────┼──────────┼──────────┼──────────┼─────────────┤
│  1   │ _________ │ ________ │ ________ │ ________ │ ________    │
│  2   │ _________ │ ________ │ ________ │ ________ │ ________    │
│  3   │ _________ │ ________ │ ________ │ ________ │ ________    │
│  4   │ _________ │ ________ │ ________ │ ________ │ ________    │
│  5   │ _________ │ ________ │ ________ │ ________ │ ________    │
│  6   │ _________ │ ________ │ ________ │ ________ │ ________    │
├──────┴───────────┴──────────┴──────────┴──────────┴─────────────┤
│ Telem radio (if separate): Band ________ Chan ________          │
│ GCS WiFi: Band ________ Chan ________                           │
│ Mesh radio (if used): Band ________ Chan ________               │
│ Notes: ________________________________________________________ │
└──────────────────────────────────────────────────────────────────┘
```

---

## Assignment Rules

### Rule 1: Separate RC and Video Bands

Never put control and video on the same frequency band on the same drone.
Standard pattern:

- **RC on 900 MHz + Video on 5.8 GHz** — the most common and safest combo
- **RC on 2.4 GHz + Video on 5.8 GHz** — also safe, but 2.4 GHz is crowded
- **RC on 900 MHz + Video on 1.2 GHz** — long range combo, check for GPS
  harmonic interference
- **RC on 433 MHz + Video on 5.8 GHz** — MafiaLRS config, maximum separation

**Never:** RC on 2.4 GHz + Video on 2.4 GHz. Never.

### Rule 2: ELRS Binding Phrases Are Your Friend

ELRS frequency hopping means two drones on the same band won't directly
interfere — they hop independently. But they share the same spectral space.
The binding phrase ensures each TX only talks to its paired RX.

For multi-drone ops, use unique binding phrases per drone (or use model
match IDs if sharing a binding phrase across a fleet).

### Rule 3: VTX Channel Spacing

For analog video, minimum 30 MHz between any two active VTX channels.
Raceband channels are pre-spaced for this:

**6 drones on Raceband (maximum safe assignment):**

| Drone | Channel | Frequency |
|-------|---------|-----------|
| 1 | R1 | 5658 MHz |
| 2 | R2 | 5695 MHz |
| 3 | R4 | 5769 MHz |
| 4 | R5 | 5806 MHz |
| 5 | R7 | 5880 MHz |
| 6 | R8 | 5917 MHz |

Note: R3 (5732) and R6 (5843) skipped to maintain wider spacing. With 8
Raceband channels, 6 drones is the practical maximum for simultaneous
analog video without interference.

**Digital video (DJI, Walksnail, HDZero)** handles channel management
internally with wider bandwidth per channel. Maximum simultaneous drones
varies by system — check manufacturer documentation. Generally 4–8
simultaneous digital feeds per band.

### Rule 4: Telem and Mesh on Their Own Channels

If running a separate telemetry radio (SiK 915 MHz, mLRS, DroneBridge):

- Don't put it on the same band as your RC link
- If both are 900 MHz, ensure different channel/frequency settings and
  verify they don't overlap using the manufacturer's channel plan
- mLRS and ELRS 900 MHz can coexist if on different LoRa channels, but
  test before trusting in the field

Mesh radios (Silvus, Doodle Labs, Rajant) typically operate on their own
managed spectrum and self-deconflict within the mesh. But they can still
interfere with RC or video if in the same band. Check the mesh radio's
operating frequency before assignment.

### Rule 5: Ground Station RF Discipline

Your ground station emits RF too:

- **Laptop/tablet WiFi** — 2.4 GHz and 5 GHz. If parked next to your
  goggle patch antenna, the 5 GHz WiFi can interfere with 5.8 GHz video.
  Disable 5 GHz WiFi on ground devices or position them away from
  antennas.
- **Phone hotspot** — same issue. Keep phones away from receiver antennas.
- **Mesh radio ground node** — ensure its antenna isn't pointed at your
  video receiver antenna.

---

## Scenario Templates

### Scenario A: 2 Drone FPV Team (Standard)

```
Drone 1: ELRS 900 MHz / R1 (5658 MHz) / 400 mW
Drone 2: ELRS 900 MHz / R4 (5769 MHz) / 400 mW
```

Simple. Maximum VTX channel separation. Both on 900 MHz ELRS with
different binding phrases — no RC conflict.

### Scenario B: 4 Drone Squad (Mixed Recon + Strike)

```
Recon 1:  ELRS 900 MHz / R1 (5658 MHz) / 200 mW (low signature)
Recon 2:  ELRS 900 MHz / R4 (5769 MHz) / 200 mW
Strike 1: ELRS 900 MHz / R6 (5843 MHz) / 600 mW
Strike 2: ELRS 900 MHz / R8 (5917 MHz) / 600 mW
```

Recon drones run lower VTX power to reduce detectability. Strike drones
run higher power for better video at speed. All on 900 MHz ELRS with
unique binding phrases.

### Scenario C: 6 Drone Max Density + GCS

```
Drone 1-3: ELRS 900 MHz / R1, R2, R4 / 400 mW each
Drone 4-6: ELRS 2.4 GHz / R5, R7, R8 / 400 mW each
GCS telem: mLRS 900 MHz (separate LoRa channel from ELRS)
GCS WiFi:  5 GHz only (disabled 2.4 GHz)
```

Split RC across bands to reduce aggregate spectral load. GCS WiFi on
5 GHz only to avoid 2.4 GHz interference. Telem radio on different LoRa
channel than the 900 MHz ELRS units.

### Scenario D: Contested Environment (EW Threat)

```
Drone 1-2: MafiaLRS 433 MHz / 1.2 GHz video / 1 W
Drone 3-4: MILELRS 900+2.4 multiband / R1, R4 (5.8 GHz) / 600 mW
Drone 5:   Fiber optic (no RF video/control)
Drone 6:   ELRS 900 MHz / 7.2 GHz video / 200 mW
```

Maximum frequency diversity. No two drones share the same link stack.
Fiber optic drone is immune to all RF jamming. 7.2 GHz video is outside
most jammer coverage. MafiaLRS on 433 MHz is below standard jammer bands.
MILELRS multiband provides failover if one band is jammed.

---

## Harmonics and Interference Gotchas

### 1.2 GHz Video ↔ GPS L1

1.2 GHz VTX 2nd harmonic = 2.4 GHz (interferes with 2.4 GHz RC).
1.2 GHz VTX at high power can also desense the GPS L1 receiver (1.575 GHz)
if the VTX antenna is near the GPS module. Use physical separation (GPS on
top, VTX antenna on bottom) and a bandpass filter on the GPS if available.

### 5.8 GHz Video ↔ WiFi 5 GHz

5 GHz WiFi (5150–5825 MHz) overlaps with low 5.8 GHz video channels.
If running a companion computer with 5 GHz WiFi, avoid VTX channels below
5800 MHz, or disable 5 GHz WiFi and use 2.4 GHz WiFi instead.

### Motor Noise ↔ Everything

ESC switching noise generates broadband EMI. On poorly shielded builds,
this can raise the noise floor across all bands. Countermeasures: capacitors
on ESC power leads, twisted signal wires, physical separation between
power wiring and RF components, ferrite beads on USB and signal cables.

---

## Spectrum Analyzer: What to Look For

If you have a spectrum analyzer (even a cheap RTL-SDR works for basic
analysis), sweep the operating area before launch:

- **Existing transmitters** — are there other operators, WiFi APs, or known
  jammers active? Avoid their frequencies.
- **Noise floor** — how loud is the ambient RF? A high noise floor on a
  specific band means poor performance on that band regardless of jamming.
- **Your own emissions** — power up one drone at a time and check for
  spurs, harmonics, and unintended emissions.

**See:** [ELINT for Drone Operators](elint-operators.md) (planned) for
advanced spectrum analysis techniques.

---

## Sources

- ExpressLRS frequency hopping documentation
- Oscar Liang, multi-pilot frequency planning guides
- Forge troubleshooting database (video interference entries)
- FPV community race frequency coordination practices
- Field experience from multi-drone training operations
