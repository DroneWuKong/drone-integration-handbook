# The Drone Integration Handbook

> **Free. Open. No login required.**
> An industry reference for drone RF, integration, and field operations.
> Built by operators, for operators.

---

## What This Is

A practical reference for anyone integrating, operating, or troubleshooting
multi-platform drone systems. Not a product manual. Not a sales pitch.
A handbook you keep open on your bench.

Covers RF communications, flight controller firmware, field diagnostics,
fleet operations, and the real-world problems that don't show up in
manufacturer documentation.

---

## Table of Contents

### Part 1 — RF Fundamentals

1. [The Five Link Types](fundamentals/five-link-types.md)
   Every drone has up to five simultaneous RF links. What they are,
   why they exist, how they interact, and what happens when they fight.

2. [Frequency Bands and Regulatory Reality](fundamentals/frequency-bands.md)
   2.4 GHz, 900 MHz, 5.8 GHz, sub-GHz — what lives where, what the
   regulations actually say, and what the regulations don't cover.

3. [Antennas for People Who Aren't RF Engineers](fundamentals/antennas.md)
   Omni vs. directional, polarization, gain, and the one rule that
   matters: match your antenna to your link, not to your ego.

4. [Link Budgets Without the Math](fundamentals/link-budgets.md)
   How to estimate range, why your range is always less than advertised,
   and the three things that actually kill links in the field.

### Part 2 — Flight Controller Firmware

5. [The Four Firmwares](firmware/four-firmwares.md)
   Betaflight, iNav, ArduPilot, PX4 — what each does well, what each
   does poorly, and when to use which. No religious wars.

6. [MSP Protocol — The Betaflight/iNav Language](firmware/msp-protocol.md)
   How MSP works, the messages that matter, and how to talk to an FC
   from anything with a serial port.

7. [MAVLink Protocol — The ArduPilot/PX4 Language](firmware/mavlink-protocol.md)
   MAVLink v2, system/component IDs, heartbeats, parameter pull,
   and the difference between ArduPilot and PX4's MAVLink dialects.

8. [UART Layout and Why It Matters](firmware/uart-layout.md)
   Every FC has a finite number of UARTs. How to allocate them,
   what happens when you run out, and the common mistakes.

### Part 3 — Field Operations

9. [Pre-Flight Checklist That Actually Works](field/preflight.md)
   Not the manufacturer's marketing checklist. The one that catches
   the problems that ground you.

10. [Blackbox Logs — What They Tell You](field/blackbox.md)
    How to pull logs, what the traces mean, and the five patterns
    that indicate real problems vs. normal noise.

11. [PID Tuning for People Who Fly, Not Simulate](field/pid-tuning.md)
    What P, I, and D actually do to your quad, how to read the
    symptoms, and a tuning workflow that works at the field.

12. [When Things Go Wrong](field/troubleshooting.md)
    The diagnostic tree. Start here when something breaks.
    Covers: no arm, flyaway, oscillation, video loss, failsafe,
    motor desync, GPS glitch, compass interference.

### Part 4 — Integration

13. [Adding a Companion Computer](integration/companion.md)
    When you need more than an FC. VOXL 2, Jetson, Pi — what
    connects where, what protocols to use, and power budgeting.

14. [Mesh Radios for Multi-Vehicle](integration/mesh-radios.md)
    Doodle Labs, Silvus, Persistent Systems — what they actually are
    (hint: OpenWRT + batman-adv), how to configure them, and the
    real-world range you'll get.

15. [TAK Integration](integration/tak.md)
    Cursor-on-Target, ATAK, WinTAK — how to get your drone onto
    the common operating picture without a defense contractor.

### Part 5 — [Platform References](platforms/README.md)

Full integration profiles — RF links, firmware, payloads, SDKs, and gotchas.

**Commercial Off-the-Shelf:**
- [DJI Matrice 350 RTK](platforms/cots/dji-m350-rtk.md) — Enterprise flagship. 55 min, triple gimbal. Not NDAA.
- [DJI Matrice 30T](platforms/cots/dji-m30t.md) — Mid-tier enterprise, integrated quad-sensor. Not NDAA.
- [DJI Mavic 4 Pro](platforms/cots/dji-mavic4-pro.md) — Prosumer/light commercial. Not NDAA.
- [Autel EVO MAX 4T V2](platforms/cots/autel-evo-max-4t.md) — Quad-sensor, GPS-denied, A-Mesh. XE is NDAA.
- [Autel EVO II Enterprise V3](platforms/cots/autel-evo2-enterprise.md) — Dual-sensor workhorse.
- [DJI Agras T50](platforms/cots/dji-agras-t50.md) — Ag spraying/spreading, 40 kg payload, 52 acres/hr.
- [DJI FlyCart 30](platforms/cots/dji-flycart-30.md) — Heavy-lift delivery, 30–40 kg payload.
- [Flyability Elios 3](platforms/cots/flyability-elios-3.md) — Confined space, collision-tolerant cage, LiDAR SLAM.

**NDAA / Blue UAS / Green UAS:**
- [Skydio X10 / X10D](platforms/blue-uas/skydio-x10.md) — Best-in-class autonomy. X10D is Blue UAS.
- [Freefly Astro](platforms/blue-uas/freefly-astro.md) — PX4, MAVLink, Blue UAS. Open architecture.
- [Inspired Flight IF1200A](platforms/blue-uas/inspired-flight-if1200a.md) — Heavy-lift hex, ArduPilot, Blue UAS.
- [Teal 2](platforms/blue-uas/teal-2.md) — Night ISR, FLIR Hadron 640R, Blue UAS.
- [Parrot ANAFI USA](platforms/blue-uas/parrot-anafi-usa.md) — Ultra-light, Blue UAS.
- [WingtraOne / WingtraRAY](platforms/blue-uas/wingtra-wingtraone.md) — Fixed-wing VTOL mapping, 59 min, Blue UAS.

**Open-Source / Custom Build:**
- [Holybro X500 V2 + Pixhawk 6X](platforms/open-source/holybro-x500-pixhawk6x.md) — Reference PX4 dev kit.
- [ArduPilot / PX4 General Reference](platforms/open-source/ardupilot-px4-reference.md) — Integration guide for custom builds.

**Tactical / Defense:**
- [Anduril Ghost X](platforms/tactical/anduril-ghost-x.md) — 80-min endurance, Lattice AI. Govt/mil only.
- [Teal Black Widow](platforms/tactical/teal-black-widow.md) — SRR Tranche 2 winner. Army procurement.
- [Skyfish Osprey](platforms/tactical/skyfish-osprey.md) — Precision mapping, NDAA.
- [SiFly Q12](platforms/tactical/sifly-q12.md) — Endurance-focused, NDAA.

---

## How to Use This Handbook

**At the bench:** Look up the specific topic. Each chapter is self-contained.
Cross-references point to related chapters when context helps.

**In the field:** The troubleshooting chapter (12) is your starting point.
The pre-flight checklist (9) is your ending point.

**Learning:** Read Part 1 first. Then pick the firmware chapter (Part 2)
that matches your platform. Then read the field chapters (Part 3) in
any order.

---

## Contributing

This handbook is open. If you have platform experience, field data,
or corrections, contributions are welcome. File an issue or PR on the
GitHub repo.

The only rules:
- Be accurate. If you're not sure, say so.
- Be practical. Theory is fine, but show how it applies in the field.
- No marketing. This is a reference, not a product pitch.
- "Safety" is in quotes. Systems mitigate danger. They don't eliminate it.

---

## License

Content is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
unless otherwise noted. Platform-specific content may have additional
restrictions from the platform manufacturer.

---

*Built in the field. With real data. On real hardware.*
