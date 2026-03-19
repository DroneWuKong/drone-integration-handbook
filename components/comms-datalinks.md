# EW-Resilient Communications — Keeping the Link Alive

> **Part 6 — Components**
> The radio link between operator and drone is the single point of
> failure that electronic warfare exploits. This chapter covers
> who builds the links that survive jamming.

---

## The EW Reality

GPS-denied, spectrum-contested environments are the new baseline.
Ukraine proved this at scale — Russian EW systems routinely jam
GPS, spoof navigation, and disrupt C2 links. The average lifespan
of a commercial drone on the Ukrainian front is days, not months,
largely because consumer-grade links fail under EW pressure.

Any drone system intended for contested environments needs
communications that degrade gracefully rather than failing
catastrophically. This means frequency hopping, spread spectrum,
mesh networking, and ultimately — for complete EW immunity —
fiber-optic links.

The Handbook's RF Fundamentals (Part 1) covers the physics.
This chapter covers the products and manufacturers.

---

## Sine Engineering — Combat-Proven from Day One

The most important communications company most people have never
heard of. Founded in Lviv, Ukraine in 2022 as a counter-UAS team.
After realizing that resilient connectivity is both the most critical
enabler and the most vulnerable aspect of UAS operations, they
pivoted to building their own solutions.

| Detail | Value |
|--------|-------|
| HQ | Lviv, Ukraine (European office planned) |
| Founded | 2022 |
| Employees | 150 |
| Customers | 150+ UAV development teams, 70+ drone manufacturers worldwide |
| Notable Client | Vyriy Drone (100% Ukrainian-sourced FPV) |
| NATO | Innovation Range winner (Dec 2025, communications category) |
| Production | Scaling 5× in 2026 |
| Funding | Bootstrapped through 2025, first investment round in progress |

### Pasika Platform

Pasika ("Apiary") is Sine Engineering's integrated platform for
multi-drone operations in contested environments. Four core pillars:

1. **Resilient C2 Datalinks** — Secure command and control with
   Smart FHSS (frequency hopping spread spectrum), jamming detect
   and avoid. Hardware-agnostic.
2. **Digital Video Datalinks** — HD video transmission optimized
   for EW-contested environments.
3. **GPS-Independent Navigation** — Satellite-free positioning
   using time-of-flight signals from nearby Sine.Links (inspired
   by legacy aviation navigation). Not centimeter-accurate, but
   maintains operational continuity when GPS is denied.
4. **Swarm Capability** — One operator controls multiple drones
   via single interface. Assign mission zones, launch sequentially,
   switch between drone feeds, deconflict paths automatically.

**Combat record:** Missions exceeding 200+ km in active EW
conditions. Deployed across multiple Ukrainian drone types
including strike FPVs, fiber-optic drones, and interceptors
(Wild Hornets' Sting).

### Why Sine Engineering Matters

Pasika allows $300–500 FPV drones to complete missions that would
typically require more expensive platforms — because they maintain
comms longer, avoid jamming more often, and deliver telemetry for
continuous improvement. The system evolves weekly from direct
battlefield feedback. As Sine puts it: "We don't bet on stability.
We design for instability."

Their approach — "operator-scaled deployment" that extends human
capability rather than replacing it — maps directly to the AI
Wingman "Jarvis not Ultron" philosophy.

**FPGA-based modules** are in development for next-generation
hardware. European branch opening for NATO-aligned manufacturing
partnerships, including targeting US defense manufacturers
supplying the Pentagon.

---

## Western Mesh Radio Manufacturers

### Doodle Labs

| Detail | Value |
|--------|-------|
| HQ | USA / Singapore |
| Blue UAS | Framework component (Mesh Rider Radios) |
| Technology | OpenWRT + batman-adv mesh networking |
| Products | Mesh Rider series in Helix configuration |
| Key Feature | Wi-Fi-based mesh with ruggedized form factor |
| NDAA | Compliant (Blue UAS Framework listed) |

Doodle Labs Mesh Rider radios are the most commonly integrated
mesh networking solution in commercial and defense small UAS.
Under the hood, they run OpenWRT Linux with batman-adv mesh
protocol — which means they're configurable Linux devices, not
black boxes. This is both a strength (flexible, hackable) and
a vulnerability (software complexity increases attack surface).

See the Handbook's mesh radios chapter (Chapter 14) for
configuration details and real-world range expectations.

### Silvus Technologies

| Detail | Value |
|--------|-------|
| HQ | Los Angeles, CA, USA |
| Technology | StreamCaster MIMO radios |
| Key Feature | MN-MIMO (Mobile Networked MIMO) — highest throughput mesh |
| Products | SC-4200, SC-4400 series |
| Weight | 100–300g depending on model |
| Power | 5–15W |
| NDAA | US manufacturer — compliant |

Silvus provides the highest-throughput mesh radios in the market.
Their MN-MIMO technology uses multiple-input multiple-output
antenna configurations with mesh networking for combined
throughput and resilience. Premium pricing — positioned for
high-value platforms where bandwidth justifies the SWaP cost.

### Persistent Systems

| Detail | Value |
|--------|-------|
| HQ | New York, NY, USA |
| Technology | MPU5 MANET radio |
| Key Feature | Android-based radio with integrated compute |
| Products | MPU5 series |
| NDAA | US manufacturer — compliant |

Persistent Systems MPU5 is unique in running Android OS natively
on the radio, enabling onboard application hosting. Wave Relay
MANET protocol. Used extensively by US SOF and DoD.

### TrellisWare Technologies

| Detail | Value |
|--------|-------|
| HQ | San Diego, CA, USA |
| Technology | TSM (TrellisWare Scalable MANET) waveform |
| Key Feature | Barrage Relay — patented non-routing mesh, 800+ nodes tested |
| Waveforms | TSM (wideband MANET), Katana (anti-jam ECCM), NB LOS |
| Encryption | AES-256 built-in |
| Bands | UHF + L-band + S-band (225–2600 MHz) in single radio |
| NDAA | US manufacturer — compliant |
| New (2025) | Anti-jam C2 waveform for uncrewed systems, Barrage Beamforming |

**Product Line:**

| Radio | Form Factor | Key Feature |
|-------|-------------|-------------|
| TW Shadow 950 | Handheld SDR | Flagship. Multi-band, HD video multicast, 32 talk-groups |
| TW Shadow 750 | Compact handheld | Mission-critical voice/data/PLI, simplified operation |
| TW Shadow 135 HPR | High Power (20W) | Vehicular/airborne/relay. Extended range |
| TW Ghost 875 | Small relay | Built-in battery, deploy as network node |
| TW Ghost 870 | OEM module | Embeddable into drones, robotics, platforms |
| TW Spirit 860 | Next-gen soldier | Public safety, first responder compatible |

TrellisWare's Barrage Relay technology eliminates traditional
routing — all nodes collaboratively relay all traffic using
cooperative combining. This means the network self-heals
instantly when nodes join, leave, or are destroyed. Tested
with 800+ nodes. Network formation in under 5 seconds.

**Anti-jam C2 for UAS (2025):** New waveform specifically for
drone command and control with anti-jam uplink alongside high-
throughput video/sensor downlink. Lowest latency in the industry.
This directly addresses the DDG Phase II EW requirement.

### Mobilicom

| Detail | Value |
|--------|-------|
| HQ | Israel / USA |
| Blue UAS | Framework component (SkyHopper) |
| Products | SkyHopper PRO, PRO Lite, PRO Micro |
| Key Feature | Encrypted, cybersecure drone datalinks |
| Partnership | ARK Electronics — affordable AI drone solutions |
| NDAA | Blue UAS Framework listed |

---

## Turkish Manufacturers

### Aselsan

Turkey's largest defense electronics company. Produces military-
grade communications, EW systems, and radar. Supplies datalinks
for Baykar TB2/TB3 and TAI ANKA platforms. Export-controlled.

### TUALCOM

Stackable data acquisition and telemetry suites for UAS.
Integrated with Turkish military platforms.

### Meteksan

AKSON C-Band datalink (announced Nov 2025). Turkish defense
communications.

---

## Fiber-Optic — The EW-Immune Option

Fiber-optic FPV eliminates RF entirely. Video and control signals
travel through a thin optical fiber trailed behind the drone.
Zero RF emissions means zero detectability and complete immunity
to electronic warfare jamming.

**Key players:**
- **Kela Technologies** (Israel, In-Q-Tel backed) — fiber-optic
  technology partner for Neros Archer Fiber. World's first
  NDAA-compliant fiber-optic FPV.
- **SkyFall** (Ukraine) — Fiber-optic FPV drones. Partnered with
  Skycutter for DDG Phase I (Shrike 10 Fiber won with 99.3 points).
- **3DTech** (Ukraine) — 3D-prints their own fiber spool casings.
- **Hasta** (Ukraine) — Optically-guided FPV, 20–50 km range.

**Tradeoff:** Range is limited by spool length (physical fiber
must trail behind the drone). The fiber can snag on obstacles.
But for missions where EW immunity is paramount and range is
known, fiber-optic is unbeatable.

DDG Phase I validated this: the fiber-optic Shrike dominated
the competition. DDG Phase II's full EW environment will likely
further advantage fiber-optic platforms.

---

## Choosing Communications

1. **Consumer FPV links (ELRS, CRSF, DJI) are NOT EW-resilient.**
   They work in benign environments. They fail under deliberate
   jamming. Don't pretend otherwise.

2. **Mesh radios add resilience but add SWaP.** A Doodle Labs or
   Silvus radio is 100–300g and 5–15W. That's your biggest payload
   hit after the camera. Budget it.

3. **Frequency diversity matters.** A single-band radio can be
   jammed with a single jammer. Multi-band radios (TrellisWare
   UHF+L+S in one device) are harder to deny.

4. **Non-routing mesh > traditional routing.** TrellisWare's
   Barrage Relay and batman-adv (Doodle Labs) both eliminate
   single-point-of-failure routing tables. The network heals
   when nodes die.

5. **For DDG Phase II / contested environments:** TrellisWare
   anti-jam C2 or Sine Engineering Pasika are the purpose-built
   solutions. Fiber-optic for maximum EW immunity at the cost
   of range flexibility.

6. **Combat-proven > spec sheet.** Sine Engineering's Pasika has
   been tested against Russian EW daily for years. That validation
   data doesn't appear on any data sheet.

---

*Last updated: March 2026*
