# Chapter 3: Antennas for People Who Aren't RF Engineers

> The antenna is the most important and least understood component
> on your drone. A $200 radio with a bad antenna loses to a $30
> radio with a good one.

---

## The One Rule

**Match your antenna to your link.**

That's it. Everything else in this chapter is explaining what
that means and how to do it.

---

## What an Antenna Does

An antenna converts electrical signal into radio waves (transmit)
and radio waves back into electrical signal (receive). It doesn't
amplify — it shapes. An antenna with "5 dBi gain" isn't creating
energy. It's focusing the energy that's already there into a
narrower pattern, the same way a flashlight focuses light from
a bulb into a beam.

More gain = narrower beam = longer range in one direction,
shorter range in every other direction.

This is the fundamental trade-off in antenna selection. There is
no antenna that's better in all directions. There are only antennas
that trade coverage pattern for range.

---

## Antenna Types You'll Actually Use

### Dipole / Whip

**What it is:** A straight stick. The stock antenna on most
receivers, telemetry radios, and mesh radios.

**Pattern:** Donut-shaped. Good coverage in all horizontal
directions, weak directly above and below the antenna axis.

**Gain:** 2–5 dBi

**When to use it:** Default choice for anything where you don't
know which direction the other radio will be. RC receivers,
telemetry, mesh nodes on drones that fly in all orientations.

**Orientation matters:** A vertical dipole radiates horizontally.
A horizontal dipole radiates vertically. On a drone, the receiver
antenna should point down or sideways — NOT parallel to the
frame. Two antennas at 90 degrees to each other (antenna diversity)
covers all orientations.

---

### Patch Antenna

**What it is:** A flat rectangle. Common on GPS modules, some
directional links, and video receivers.

**Pattern:** Directional — strong in front, weak behind.
Like holding up a book and only hearing what's in front of it.

**Gain:** 6–14 dBi depending on size

**When to use it:** On the ground station pointing at the drone.
GPS antennas (patch facing sky). Video receiver antennas in
goggles (facing forward). NOT on the drone itself unless you
know exactly where the ground station will be.

**The goggle antenna mistake:** Many pilots fly with stock goggle
antennas (usually small omnis) and wonder why they get video
breakup at 500m. Replacing one goggle antenna with a directional
patch that points toward the flying area can double or triple
video range with no change to the drone.

---

### Helical Antenna

**What it is:** A coil of wire. Comes in two types: normal-mode
(small, used as compact omni) and axial-mode (larger, highly
directional, used for long range).

**Pattern:** Axial-mode helix is a focused beam — high gain,
narrow coverage. Normal-mode is similar to a dipole.

**Gain:** 8–15+ dBi (axial mode)

**When to use it:** Ground-station tracking antenna for long-range
operations. Paired with an antenna tracker that points it at the
drone. Not practical on the drone itself (too large, too directional).

---

### Pagoda / Lollipop / Stubby

**What it is:** Compact circular-polarized antenna. The standard
FPV video antenna on both the drone and the goggles.

**Pattern:** Roughly omnidirectional with circular polarization.

**Gain:** 1–3 dBi

**When to use it:** 5.8 GHz FPV video. Both the VTX antenna on the
drone and the receiver antenna on the goggles should be circular
polarized and the same handedness (both RHCP or both LHCP). Mixing
handedness costs you ~3 dB (half your signal).

**Why circular polarization for video:** When a linearly polarized
signal bounces off a surface (multipath), its polarization can
rotate. If your receive antenna is linear and the signal arrives
at the wrong angle, you lose it. Circular polarization doesn't
have this problem — it receives equally regardless of rotation.
The trade-off is ~3 dB less gain than an equivalent linear antenna.

---

### PCB / Ceramic Chip Antenna

**What it is:** A tiny antenna printed on the circuit board or
bonded as a ceramic chip. Found inside ESP32 modules, Bluetooth
devices, GPS modules, and small receivers.

**Pattern:** Roughly omnidirectional but with significant nulls
depending on PCB ground plane and nearby components.

**Gain:** -2 to 2 dBi (often negative gain compared to an ideal
isotropic radiator)

**When to use it:** When size and cost matter more than range.
The ESP32-C6 on a Tooth uses its built-in PCB antenna for mesh
communication at short range. For anything beyond 100m, use an
external antenna via the U.FL/IPEX connector if available.

---

## Polarization

Radio waves vibrate in a specific orientation. If the transmit
antenna sends vertically polarized waves and the receive antenna
is oriented horizontally, you lose ~20 dB of signal. That's the
difference between a clear link and no link.

**The rules:**
- Linear antennas (dipole, whip): orient both the same way.
  Both vertical, or both horizontal. On a drone that changes
  orientation constantly, this is hard — which is why diversity
  (two antennas at 90 degrees) helps.
- Circular polarized antennas (pagoda, lollipop): match handedness.
  Both RHCP or both LHCP. Don't mix.
- Cross-polarization loss: linear TX → circular RX (or vice versa)
  costs ~3 dB. Not ideal but survivable.

---

## Connectors

The small connectors used in drone antennas are fragile. Know them.

| Connector | Size | Common Use | Durability |
|-----------|------|-----------|------------|
| SMA | Medium | VTX, telemetry radio, ground station | Good — threaded, secure |
| RP-SMA | Medium | Same as SMA, reversed polarity | Good — check male/female |
| U.FL / IPEX | Tiny | On-board connections, GPS, receiver | Fragile — 30 mate cycles rated |
| MMCX | Small | Some receivers, compact VTX | Fair — snap-on, better than U.FL |

**The U.FL problem:** U.FL (also called IPEX or MHF) connectors are
rated for about 30 connect/disconnect cycles. After that, the spring
contact weakens and the connection becomes intermittent. Every time
you unplug and replug a U.FL antenna, you're using one of those
30 cycles. On a racing drone that gets rebuilt weekly, this matters.

**Fix:** Don't disconnect U.FL antennas unless you have to. Route
the antenna wire so it stays connected during maintenance. If a
U.FL connection becomes intermittent (video cuts out when you flex
the cable), replace the pigtail — the connector is worn out.

---

## Antenna Placement on a Drone

Where you put the antenna matters as much as which antenna you choose.

### Do

- Mount RC receiver antennas pointing away from the frame at
  90 degrees to each other (diversity). The classic "V" shape
  with antenna tubes works.
- Mount GPS antenna on top of the frame with a clear view of
  the sky. No carbon fiber between the GPS patch and the
  satellites.
- Mount the VTX antenna where it won't get hit in a crash.
  Rear-facing on a standoff is common.
- Keep transmit antennas (VTX, mesh radio) as far from receive
  antennas (RC receiver, GPS) as physically possible on the frame.

### Don't

- Don't run antenna wires parallel to power wires. Motor current
  creates magnetic fields that induce noise in antenna cables.
- Don't let antenna wires cross each other at sharp angles.
- Don't fold or kink antenna wires. The coax impedance changes
  at the bend and reflects signal back instead of radiating it.
- Don't mount antennas inside a carbon fiber enclosure. CF
  attenuates RF. If the antenna is inside a CF tube, you're
  losing signal.
- Don't forget the ground plane. A 900 MHz dipole needs a ground
  plane (the FC, the frame, or a dedicated ground plane element)
  to radiate properly. Hanging in free space with no ground
  reference, it underperforms.

---

## Range Estimation (Quick and Dirty)

You don't need to calculate a full link budget to estimate range.
Here's the shortcut.

**Start with the manufacturer's claimed range.** Divide by 3.
That's your real-world range with obstacles, interference, and
non-ideal antenna placement.

**If you're doing better than 1/3 of claimed range,** your setup
is good. If you're doing worse, check antenna orientation,
connections, and interference from other on-board transmitters.

**If you need more range:**
1. Better antenna on the ground station (cheapest improvement)
2. Higher VTX/radio power (easy but wastes battery)
3. Better antenna on the drone (limited by weight/size)
4. Lower frequency band (900 MHz instead of 2.4 GHz)
5. Higher gain directional antenna with tracker (most effective,
   most complex)

The order above is also the order of cost-effectiveness. A $15
directional antenna on your goggles does more for range than a
$50 amplifier on the drone.

---

## The Antenna You Already Have

Before buying new antennas, check the ones you have:

- **Is it the right band?** A 5.8 GHz antenna on a 2.4 GHz
  radio is a $0 dummy load. It will not work. At all. This
  sounds obvious but it happens.
- **Is it connected?** Flex the cable gently at the connector.
  If the signal changes, the connection is bad.
- **Is it damaged?** A cracked antenna element, kinked coax,
  or corroded connector all kill performance.
- **Is it oriented correctly?** Rotating an antenna 90 degrees
  can cost 20 dB. Try different orientations before buying
  a new antenna.

---

## Next

- **Chapter 4: Link Budgets Without the Math** — estimating
  range from specs without a calculator.
- **Chapter 1: The Five Link Types** — which antenna goes
  with which link.

---

*The best antenna is the one that's pointed the right way,
connected properly, and on the correct frequency.
Everything else is optimization.*
