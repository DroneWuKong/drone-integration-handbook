# Fiber-Optic FPV Integration

> Fiber-optic FPV drones are immune to all RF-based electronic warfare.
> The control signal and video travel through a physical cable, not over
> the air. Both Russia and Ukraine are mass-producing them. Russia's
> fiber-optic FPV production exceeded 50,000 units/month by September 2025.
> Ukraine codified and scaled fiber-optic variants throughout 2025.
> This is the least documented area in drone technology. This guide covers
> what's publicly known about integration.

**Cross-references:** [EW Countermeasures](ew-countermeasures.md) ·
[Electronic Warfare](../components/electronic-warfare.md) ·
[Military Firmware Forks](../components/military-firmware-forks.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[Frames](../components/frames-airframe-selection.md) ·
[ESCs](../components/escs.md)

---

## Why Fiber-Optic

Every other countermeasure in the EW arms race is a software or frequency
fix — move to a different band, encrypt the signal, hop frequencies. The
jammer responds by covering more spectrum. It's an escalating cycle.

Fiber-optic breaks the cycle entirely. There is no RF emission to jam,
spoof, intercept, or direction-find. The drone is electromagnetically
silent on both the control and video links. The only RF emission is from
the motors (broadband EMI) and any onboard GPS receiver.

**The tradeoff:** you're physically tethered to the launch point by a
cable. Range is limited by spool capacity. Weight increases with range.
The cable can snag, break, or be cut. These are real limitations — which
is why RF-based systems remain necessary for many mission profiles. Fiber
is not a universal replacement. It's a specific tool for specific
situations.

---

## How It Works

### Architecture

```
Ground Station                         Drone
┌──────────┐    fiber cable    ┌──────────────┐
│ TX Module │ ──────────────── │ RX Module    │
│ (control  │    (1-25 km)     │ (converts to │
│  + video  │                  │  UART/CRSF + │
│  receive) │                  │  video out)  │
└──────────┘                   └──────────────┘
     │                               │
  Goggles                        FC (UART)
  + Radio                        + Camera
```

The fiber cable carries bidirectional data:

- **Ground → Drone:** RC channel data (same as CRSF/SBUS over UART)
- **Drone → Ground:** video feed (analog composite or digital stream)

The ground-side module converts the pilot's stick inputs to optical
signals. The drone-side module converts optical signals back to electrical
UART for the FC and outputs video to the goggles.

### What Travels Through the Fiber

| Signal | Direction | Encoding | Notes |
|--------|-----------|----------|-------|
| RC channels | Ground → Drone | Serial (CRSF/SBUS/PPM) | Same as wireless RC, just over fiber |
| Video | Drone → Ground | Analog composite or digital | Depends on system |
| Telemetry | Drone → Ground | Serial (MAVLink/MSP) | Optional, bandwidth permitting |

The FC doesn't know or care that its control input comes from fiber instead
of a wireless receiver. It sees CRSF or SBUS on its UART, same as always.
This is why fiber integration doesn't require FC firmware changes.

---

## The Spool

The fiber spool is the defining component. It contains the fiber-optic
cable wound on a reel with a motor-driven feed system.

### Spool Placement

Two approaches in current use:

**Drone-mounted spool (most common):** the spool is on the drone. Cable
pays out as the drone flies away from the anchor point. The ground end of
the cable is anchored at the launch site.

- **Advantage:** simpler ground station. Just anchor the cable end.
- **Disadvantage:** spool weight is on the drone, reducing payload capacity
  and flight time. Spool motor draws power from the flight battery.

**Ground-mounted spool:** the spool stays on the ground. Cable pays out
as the drone flies.

- **Advantage:** spool weight isn't on the drone.
- **Disadvantage:** cable tension management is harder. The cable must
  feed cleanly as the drone maneuvers. Snag risk is higher.

Most production systems (Ukrainian and Russian) use drone-mounted spools
because the cable management is more predictable.

### Cable Specifications

| Parameter | Typical Value | Notes |
|-----------|--------------|-------|
| Fiber type | Single-mode 9/125 | Standard telecom fiber |
| Cable diameter | 0.25 – 0.9 mm | Thinner = lighter but more fragile |
| Weight per km | 30 – 200 g/km | Depends on diameter and coating |
| Breaking strength | 1 – 5 N | Enough for flight tension, not snag resistance |
| Bend radius (min) | 5 – 15 mm | Tighter bends = signal loss or breakage |
| Operating range | 1 – 25 km | Limited by spool capacity and cable weight |
| Signal loss | 0.35 dB/km @ 1310nm | Negligible for FPV distances |

**Cable weight is the primary range limiter.** A 10 km spool of 0.25 mm
fiber weighs roughly 300–500 g including the spool and motor. A 25 km
spool may weigh 1+ kg. This weight comes directly out of the drone's
payload budget.

### Spool Motor

The spool motor maintains constant tension on the cable as it pays out.
Too much tension = cable snaps. Too little = cable loops and tangles.

- **Motor type:** small brushed or brushless DC motor with slip clutch
  or electronic tension control
- **Power:** typically 1–3W, powered from the flight battery or a
  dedicated BEC
- **Control:** constant-torque (simplest) or closed-loop tension feedback

The spool motor wiring connects to a spare BEC output or directly to
the battery through a regulator. It does NOT connect to the FC's motor
outputs — it's an auxiliary system.

---

## FC Integration

### Wiring

The fiber RX module on the drone outputs standard serial:

```
Fiber RX Module          Flight Controller
─────────────────────    ─────────────────
  UART TX  ──────────── FC UART RX (Serial RX pad)
  UART RX  ──────────── FC UART TX (Telemetry)
  5V       ──────────── 5V BEC
  GND      ──────────── GND
```

Configure the FC UART for Serial RX with the appropriate protocol
(CRSF, SBUS, or PPM depending on the fiber system). From the FC's
perspective, this is identical to a wireless receiver.

### Firmware Configuration

**No firmware changes are needed.** The FC doesn't know or care that
the signal comes from fiber. Configure the UART exactly as you would
for a wireless ELRS/Crossfire receiver:

- Betaflight: Serial RX on the connected UART, provider = CRSF (or SBUS)
- iNav: same configuration
- ArduPilot: serial protocol = RCInput on the appropriate SERIAL port

### Video Connection

The camera connects to the fiber TX module on the drone (not to a VTX):

```
Camera ──[composite video]──> Fiber TX Module ──[fiber]──> Ground RX ──> Goggles
```

For analog systems, this is a standard composite video connection (the
same yellow wire you'd run to an analog VTX). The fiber system replaces
the VTX entirely — there is no VTX on a fiber drone.

For digital systems, the integration is more complex and depends on the
specific fiber module. Some accept HDMI or MIPI CSI input.

### OSD

OSD overlay (battery voltage, flight mode, etc.) must be mixed into the
video signal BEFORE it enters the fiber TX module. Two approaches:

- **FC with OSD chip (standard):** the FC's OSD chip overlays data onto
  the composite video signal. Wire camera → FC video-in, FC video-out →
  fiber TX module. This is the normal analog OSD wiring.
- **External OSD board:** if the FC doesn't have an OSD chip, use an
  external OSD board between camera and fiber TX.

---

## Weight Budget

Fiber adds weight that RF systems don't have. Plan accordingly.

| Component | Typical Weight | Notes |
|-----------|---------------|-------|
| Fiber RX module (drone side) | 5 – 15 g | Varies by manufacturer |
| Spool (5 km) | 150 – 300 g | Cable + reel + motor |
| Spool (10 km) | 300 – 600 g | Significant payload impact |
| Spool (25 km) | 800 – 1500 g | Only on larger platforms (7"+) |
| Spool motor + driver | 10 – 30 g | Constant-torque system |

**Impact on platform selection:**

- **5" quad:** 5 km spool is practical. 10 km is marginal (heavy).
- **7" quad:** 10 km spool is practical. This is the sweet spot.
- **10" quad / heavy lift:** 25 km spool is feasible.

Flight time reduction from spool weight: roughly 10–20% for a 5 km spool
on a 5" build, 25–40% for a 10 km spool. Plan battery capacity accordingly.

---

## Operational Considerations

### Launch Procedure

1. Anchor the cable end (ground-spool) or pre-tension the spool (drone-spool)
2. Verify cable feed path is clear of obstacles, props, and antenna masts
3. Launch vertically — the cable must pay out cleanly without tangling
4. Maintain positive altitude — slack cable near ground = snag risk

### Flight Envelope

- **No return path:** the cable is one-way. The drone flies out and the
  cable pays out. You cannot reel it back in during flight (most systems).
  The drone is committed to its outbound path.
- **No orbiting:** circular flight patterns wrap the cable around itself
  or around obstacles. Fly outbound in a straight line or gentle arc.
- **Altitude management:** cable sag between drone and anchor point must
  be above terrain and obstacles. Higher altitude = more cable needed for
  the same ground distance.
- **Wind:** crosswind pushes the cable laterally, increasing effective
  cable length needed and snag risk. Strong wind = shorter practical range.

### Cable Management

- **Snag = mission kill.** Cable caught on a tree, building, or antenna
  mast stops the drone. At FPV speeds, this can snap the cable or
  crash the drone.
- **Route planning:** before launch, identify the cable path. Clear of
  vertical obstacles. Ideally over open terrain.
- **Cable recovery:** after the mission, the cable is either recovered
  (reeled back in) or abandoned. For one-way strike missions, the cable
  is expendable.

### Failure Modes

| Failure | Symptom | Result |
|---------|---------|--------|
| Cable break (tension) | Instant loss of all links | Drone enters failsafe |
| Cable snag | Control lag then break | Same as above |
| Spool jam | Cable stops paying out, drone pulls against anchor | Drone decelerates, may snap cable |
| Fiber bend too tight | Signal degradation, video noise | Reduced video quality, then total loss |
| Spool motor failure | Cable pays out uncontrolled | Slack cable, high snag risk |

**Critical point:** when the cable breaks, the drone has NO control link
and NO video. Unlike RF systems, there is no degraded mode — it's all or
nothing. Failsafe configuration is even more important on fiber drones
than on RF drones.

---

## Fiber vs RF: When to Use Which

| Factor | Fiber | RF |
|--------|-------|-----|
| EW immunity | Total | Depends on firmware/frequency |
| Detection signature | Electromagnetically silent | Detectable by ELINT |
| Range flexibility | Fixed by spool capacity | Adjustable (power, rate, antenna) |
| Flight pattern | Outbound line only | Unrestricted |
| Reusability | Cable may be expendable | Fully reusable |
| Weight penalty | 150–1500 g (spool) | Minimal (receiver only) |
| Setup time | Cable routing required | Power on and go |
| Cost per mission | Cable cost if not recovered | Zero (reusable hardware) |

**Use fiber when:**
- Operating in a known high-EW environment where RF links will be jammed
- The mission profile is outbound-only (strike, one-way recon)
- Electromagnetically silent approach is required (no RF signature)
- The target is within spool range and on a clear cable path

**Use RF when:**
- Mission requires orbiting, return trips, or complex flight patterns
- Range exceeds spool capacity
- Weight budget is tight
- Rapid deployment (no cable routing setup time)
- Reusability is important

---

## Production Scale Context

As of late 2025:

- **Russia:** 50,000+ fiber-optic FPVs per month. Domestic fiber cable
  production at the Saransk plant. Chinese spool cooperation.
- **Ukraine:** codified and scaled all available fiber-optic variants in
  2025. TAF Industries Kolibri 13 O is one example (fiber-optic variant).
  Multiple manufacturers producing at scale.
- **Tactics:** Russia uses fiber FPV drones as ground mines (drone waits on
  road, detonates on contact). Ukraine launched fiber FPVs from naval
  drone motherships (USV-launched, sea-based strikes on ports).

This is no longer experimental technology. It's production-scale
industrial warfare equipment.

---

## Sources

- Advances in Military Technology Vol. 20 No. 2, fiber-optic FPV counter-tactics
- Ukraine's Arms Monitor, fiber-optic production reporting
- Defense Advancement, "Evolving Countermeasures for Fiber-Controlled Drones"
- NSDC Ukraine, "Results of Ukraine's Defense Industry in 2025: FPV Drones"
- Defense News, "Of fiber-optics and FPVs" (Nov 2025)
- Telecom fiber-optic cable specifications (ITU-T G.652)
