# Chapter 37: Packable Antennas — Range You Can Carry

> The best long-range antenna is worthless if it doesn't fit in the
> bag you actually brought. This chapter is about the antennas that
> give you real range and still pack down — and the one polarization
> mistake that quietly throws away half your signal on a WiFi link.

---

## The Three-Way Trade

Chapter 3 covered the gain-versus-pattern trade. In the field there is
a third axis: **how small it packs and how fast it deploys.** You are
now trading three things against each other, not two:

- **Gain** — range, but only in the direction the antenna points.
- **Beamwidth** — how forgiving it is about aiming (and, on a mesh,
  how many neighbors it can hear).
- **Pack size / deploy time** — whether it rides in a pouch and sets
  up in ten seconds, or needs a mast, a tripod, and a tracker.

There is no antenna that wins all three. A grid dish is 24 dBi and packs
like a trash-can lid. A rubber-duck packs to nothing and gives you 2 dBi.
The useful middle — **flat CP patches and dual-band panels, 8–13 dBi,
that pack flat** — is where a field-portable long-range link actually
lives.

---

## The Polarization Trap on WiFi Links

This is the single most common way to lose 3–20 dB on a WiFi-broadcast
or mesh link (WFB-NG, OpenHD, or a raw ad-hoc/mesh setup on cards like
the MediaTek MT7612U), and almost nobody checks it.

**The antenna sets the polarization, not the radio.** An MT7612U USB
card is fed as a linear (dipole) device, but if you bolt a circularly
polarized antenna onto it, the link radiates circular. What matters is
the *pair* of antennas across the link, not the chipset.

| TX antenna | RX antenna | Loss | Notes |
|---|---|---|---|
| CP (RHCP) | CP (RHCP) — same hand | ~0 dB | Correct. Matched circular. |
| CP (RHCP) | CP (LHCP) — opposite hand | **-20 to -30 dB** | Wrong-hand CP is near-total rejection. The link may not close at all. |
| CP | Linear | **-3 dB** (consistent) | Survivable. Loss is fixed regardless of rotation. |
| Linear (vertical) | Linear (vertical) | ~0 dB | Correct, *if* both stay vertical. |
| Linear (vertical) | Linear (horizontal) | **-20 dB+** | Cross-polarized. Effectively no link. |

Two rules fall out of this table:

1. **If you run CP on one end, run same-hand CP on the other.** A
   3 dBic CP omni on the air side and a CP patch on the ground must be
   the *same handedness* (both RHCP or both LHCP). Opposite hands is not
   a 3 dB penalty — it is a 20–30 dB hole that looks like a dead radio.
2. **Don't mix CP and linear to "save money."** Putting a linear panel
   (e.g. an Alfa APA-M25) against a CP air antenna costs a flat 3 dB.
   It works, but you gave away a quarter of your range for nothing. If
   you want linear panels on the ground, run a linear antenna on the air
   side too.

The CP-to-linear 3 dB is at least *consistent* — it does not swing with
airframe rotation the way linear-to-linear misalignment does (which is
why CP is preferred on things that bank and roll in the first place).
That consistency is the only reason a mixed setup is tolerable.

---

## Mesh Topology Changes the Antenna Choice

If the link is a true mesh — a routing protocol such as **Babel**
(RFC 8966, a loop-avoiding distance-vector protocol built for dynamic
wireless mesh) picking paths across several moving nodes — then a
narrow directional antenna on a node is a liability. The node can only
hear neighbors inside its beam; anything behind it is invisible to the
routing table, and the mesh can't route around a link it can't see.

| Node role | Antenna | Why |
|---|---|---|
| Roaming / airborne node | Omni (CP, 2–5 dBic) | Must hear any neighbor in any attitude. Directional would drop peers on every turn. |
| Fixed gateway to a known sector | Wide directional (patch, 8–13 dBi, 60–120° beam) | Covers an operating area, not a pinpoint. Range without going blind. |
| Point-to-point backhaul leg | Narrow directional both ends | Known, fixed geometry. Highest gain, needs aiming. |

The practical read: put the gain on the **fixed end pointed at the
operating area**, keep the **moving ends omni**, and prefer a
*wide-beam* patch (like the TrueRC X-Air's ~120° pattern) over a narrow
yagi so the mesh keeps discovering neighbors across a sector instead of
a pencil line. A tracker only earns its complexity once the beam gets
narrow enough (below ~15–20°) that a human can't keep it pointed.

**Babel doesn't change RF range** — it changes what the link needs to
*stay routed*: a healthy path in *both* directions. A big patch on the
gateway does nothing if the moving node's little omni can't be heard on
the way back. Budget the weaker direction, not the stronger one.

---

## The Packable Menu

Gains and pack characteristics below are from manufacturer specs and
field use. Treat gain as a comparison guide, not a guarantee — axial
ratio and real pattern vary.

### Air / moving side — stay omni, stay light

| Antenna | Gain | Pol | Pack | Notes |
|---|---|---|---|---|
| CP omni stub (Singularity-class) | 2–3 dBic | CP | Trivial | Direct upgrade from a stock 3 dBic. Better pattern, still tiny. |
| Cloverleaf / skew-planar | 2–3 dBic | CP | Trivial | Good multipath rejection. Fragile elements. |
| Linear dipole / whip | 2–5 dBi | Linear | Trivial | Only if the ground end is also linear. |

Don't chase gain on the moving end — a directional antenna there loses
link every time the airframe turns away.

### Ground / fixed side — this is where range is won

| Antenna | Gain | Beam (−3 dB) | Pol | Pack | Needs aiming? |
|---|---|---|---|---|---|
| CP omni stub | 2–3 dBic | 360° | CP | Trivial | No — but no range gain either |
| **TrueRC X-Air (5.8 / 2.4)** | **~9.5–10.5 dBic** | **~68°** | CP | **Flat, pocketable** | Point at the sector; no tracker |
| TrueRC X²-Air (5.8) | ~13 dBic | ~62° | CP | Flat, slightly larger | Point at the sector |
| Alfa APA-M25 (dual-band 2.4/5) | 8 dBi (2.4) / 10 dBi (5) | ~66° | **Linear** | Flat panel, ~167×66×18 mm | Point at the sector |
| Folding yagi | 10–14 dBi | 30–50° | Linear | Folds, longer | Recommended |
| Panel array (2×2 / 4×4) | 14–18 dBi | 20–30° | Linear/CP | Bulkier, still flat | Tracker recommended |
| Grid / dish | 18–24 dBi | 10–15° | Linear | **Does not pack** | Must track |

The sweet spot for "range you can carry" is the **flat CP patch
(X-Air / X²-Air) or the dual-band linear panel (APA-M25)** — 8–13 dBi,
rides flat in a pouch, wide enough beam to cover a sector by hand. That
band of the table is the whole point of the chapter.

---

## Worked Example: MT7612U Mesh, CP Both Ends

The setup that prompted this chapter, run through the Chapter 4 method
so the numbers are honest:

- **Radios:** MT7612U USB cards both ends. Box says 23 dBm; the Linux
  driver caps these at **~18 dBm** and they famously ignore higher
  power settings — budget 18 dBm, not 23.
- **Air antenna:** 3 dBic CP omni.
- **Ground antenna:** TrueRC X-Air, ~10 dBic CP directional patch,
  same handedness as the air antenna (this is not optional — see the
  polarization trap above).
- **Polarization loss:** 0 dB (matched CP-CP). **Cable/connector:** ~1 dB.
- **Effective one-way budget:** 18 + 3 + 10 − 1 = **30 dB** of power +
  gain to spend against path loss.
- **RX sensitivity (WFB-NG-style, MCS0/1, long GI):** ~−91 dBm at the
  raw decode edge.

Two range numbers, both assuming clear line of sight *and* a clear
first Fresnel zone:

| Band | Theoretical (0 dB margin, decode edge) | Expected (10 dB link margin) |
|---|---|---|
| **2.4 GHz** (X-Air 2.4, ~10 dBic) | **~11 km** | **~3.5 km** |
| **5.8 GHz** (X-Air 5.8, ~10 dBic) | **~4.5 km** | **~1.5 km** |

Read those two columns as the envelope, not a promise. "Theoretical" is
the distance where the signal just reaches the decode threshold with
nothing held back — one gust of multipath and it drops. "Expected" holds
back 10 dB for fading, imperfect aiming, and Fresnel intrusion, which is
what you actually plan around. Reality lands between them and drifts
toward the left column only in a clean rural RF environment.

Three things move these numbers more than anything else:

1. **Band.** 2.4 GHz buys ~3× the range of 5.8 GHz for the same gear
   (13 dB less free-space loss at the same distance). If regulations and
   spectrum congestion allow it, run the link on 2.4.
2. **The MT7612U's real 18 dBm.** That's ~5 dB under the box number —
   about a 45% range haircut baked in before you leave the truck.
   Measure your card's actual output; don't trust the label.
3. **Fresnel, not just line of sight.** At 4 km on 2.4 GHz the first
   Fresnel zone is ~11 m in radius at midpoint. Ground clutter eating
   the bottom of it is most of the gap between the two columns above.

---

## Anatomy of a Range Record

The packable setup above lands in single-digit kilometres. WiFi-broadcast
systems like OpenHD have flown **60–75 km** on the same physics. The
record is not one exotic component — it is the discipline of stacking
every lever at once. Free-space loss at 60 km on 5.8 GHz is **~143 dB**;
closing that with margin takes roughly **58 dB of TX power + antenna gain
combined**. Here is where that comes from, in order of contribution:

| Lever | Buys you | How |
|---|---|---|
| Tracked directional ground antenna | **~30 dB** | 20–30 dBi panel/dish on a GPS antenna tracker. The beam is ~10–15° wide — a human can't hold it, so the tracker is the enabling piece, not an accessory. |
| Altitude + terrain | Makes 60 km *exist* | Ground station on a ridge, aircraft at altitude. Radio horizon ≈ 4.12·(√h_tx + √h_rx) km — a 500 m ridge + 1500 m aircraft reaches ~250 km of horizon. Mountain-to-air, never a field. |
| Narrow channel (5/10 MHz) | **~3–6 dB** | Halving bandwidth halves integrated noise: ~3 dB per halving of receiver sensitivity. Trades video bitrate for reach. |
| Lowest MCS + FEC | Graceful edge | MCS0 (BPSK) is the most robust rate; WFB-NG forward error correction softens loss instead of cliff-diving, so you can operate at the ragged edge of the budget. |
| Card + (last) power | A few dB | RTL8812AU/EU over MT7612U — proven injection, 5/10 MHz support, and it *honors* higher power settings. A PA to ~30 dBm is the least efficient lever: 6 dB (4× power) only doubles range, versus 30 dB from an antenna. |
| RX diversity + clean spectrum | Protects the margin | Multiple ground RX cards combined per-packet; flown in rural terrain where the noise floor sits near −100 dBm. An urban −85 dBm floor would erase 15 dB instantly. |

The air side stays **omni** through all of this — the aircraft banks and
turns and can't point anything. Every one of these knobs lives on the
**ground** or in the **flight profile**. That is the whole lesson of this
chapter at its extreme: put the gain on the end that isn't moving, give
the signal a clean path to fly across, and never rely on a single trick.

**The failure mode of chasing records:** each lever narrows your
operating envelope. A 15° beam that loses tracking lock drops the link.
A 5 MHz channel gives you a slideshow, not video. MCS0 at the margin
means one terrain intrusion is a dropout, not a blur. Records are flown
by people who accept those constraints deliberately — they are not a
config you leave on for everyday flying.

---

## Recommendations

**If you keep CP (your air antenna is CP):**
Ground end → **TrueRC X-Air** (matched hand, ~10 dBic, flat, no
tracker for a sector). Air end → keep the 3 dBic CP omni or step to a
Singularity-class stub. This is the smallest-bag, no-mismatch path and
needs zero changes to your polarization scheme.

**If you'll commit the whole link to linear:**
Ground end → **Alfa APA-M25** (dual-band, 8/10 dBi, packs flat, native
RP-SMA for the Alfa cards). Air end → linear dipole. Slightly cheaper,
dual-band in one panel, but only correct if *both* ends are linear.

**Either way:**
- Run **2.4 GHz** for range unless the band is unusable.
- Point the fixed patch at the operating **sector**, not a pinpoint —
  the wide beam is doing you a favor on a moving target and on a mesh.
- Add a tracker only when the ground gain climbs past ~15 dBi and the
  beam gets too narrow to hold by hand.

---

## Failure Modes

- **Wrong-hand CP.** RHCP against LHCP looks exactly like a dead radio
  or a broken cable. Before you tear the build apart, confirm both CP
  antennas are the same handedness. This costs 20–30 dB.
- **Trusting the box power.** "23 dBm" on an MT7612U is ~18 dBm in
  practice. Every downstream range estimate inherits that 5 dB error.
- **Directional antenna on a mesh node.** Narrow-beam gain on a moving
  or peer-facing node blinds the routing table to neighbors outside the
  beam. Keep gain on the fixed end.
- **One-way budgeting.** A big ground patch that the air node can't be
  heard back through gives you a downlink and no uplink. Babel needs the
  return path; budget the weaker direction.
- **Ignoring the Fresnel zone.** "I have line of sight" is necessary,
  not sufficient. Clutter in the bottom of the first Fresnel zone pulls
  you off the theoretical number long before the geometry says it should.

---

## Next

- **Chapter 3: Antennas for People Who Aren't RF Engineers** — gain,
  pattern, and polarization from the ground up.
- **Chapter 4: Link Budgets Without the Math** — the method behind the
  worked example above.
- **Chapter 2: Frequency Bands & Regulatory Reality** — before you
  "just run 2.4 GHz for range," check what you're allowed to transmit.

---

*Range you can't carry to the field is range you don't have. Pick the
antenna that packs, match your polarization, and put the gain on the end
that isn't moving.*
