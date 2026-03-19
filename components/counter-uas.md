# Counter-UAS — The Other Side of the Problem

> **Part 6 — Components**
> If you build drones, you need to understand what defeats them.
> Counter-UAS technology defines the threat environment your
> systems must survive in.

---

## Why Drone Operators Need to Understand C-UAS

Every drone operator exists in an environment where someone may
be trying to stop them. Military operators face dedicated EW and
C-UAS systems. Commercial operators face regulations, geofencing,
and increasingly — active detection systems around airports,
prisons, stadiums, and critical infrastructure.

Understanding C-UAS isn't about building countermeasures. It's
about understanding the threat your drone faces and designing
systems that survive it. The Handbook's unsolved-problems chapter
covers the theoretical challenges. This chapter covers the products.

---

## Detection Methods

C-UAS systems detect drones through four primary methods, often
combined in a single system:

| Method | How It Works | Strengths | Weaknesses |
|--------|-------------|-----------|------------|
| **RF Detection** | Scans for known drone control/video frequencies | Passive (no emissions), identifies protocol/manufacturer | Fails against fiber-optic or autonomous drones |
| **Radar** | Active electromagnetic pulses detect flying objects | Works in all weather, long range, 3D tracking | False positives (birds), expensive, active emission |
| **Optical/Thermal** | Cameras with AI identify drone silhouettes | Visual confirmation, works against RF-silent drones | Weather-dependent, range-limited, compute-intensive |
| **Acoustic** | Microphone arrays detect propeller noise | Passive, works in RF-denied environments | Short range, high false positive in noisy environments |

Modern C-UAS systems fuse multiple detection methods to reduce
false positives. DroneShield's SensorFusionAI and D-Fend's
EnforceAir both use multi-sensor fusion as their core approach.

---

## Defeat Methods

| Method | How It Works | Legal Status |
|--------|-------------|-------------|
| **RF Jamming** | Overwhelms drone control/video frequencies | Military/LE only (illegal for civilians in most jurisdictions) |
| **GPS Spoofing** | Sends false GPS signals to confuse navigation | Military only — highly regulated |
| **Protocol Manipulation** | Exploits drone communication protocols to take control | Military/LE only — cyber-attack classification |
| **Kinetic Interceptor** | Physical interception (net guns, interceptor drones, directed energy) | Varies — some commercial options legal |
| **High-Power Microwave** | Directed energy to fry drone electronics | Military only |

**Legal reality:** In most countries, only military and authorized
law enforcement can actively defeat drones. Civilians can detect
and report, but cannot jam, spoof, or intercept. Know your
jurisdiction.

---

## Major C-UAS Manufacturers

### DroneShield (Australia/USA)

The most widely deployed commercial C-UAS company. ASX-listed (DRO).

| Detail | Value |
|--------|-------|
| HQ | Sydney, Australia / Virginia, USA |
| Stock | ASX: DRO |
| Approach | RF detection + AI + optional jamming |
| AI Engine | SensorFusionAI — fuses RF, radar, optical, ADS-B data |
| Contracts | $48M+ cumulative with single Asia-Pacific reseller; NATO eastern flank C2E deployment |

**Product Line:**

| Product | Type | Description |
|---------|------|-------------|
| DroneSentry | Fixed site | Autonomous C-UAS: radar + RF + cameras + optional DroneCannon jamming. Anti-swarming capable. |
| DroneSentry-X Mk2 | Mobile/expeditionary | Vehicle-mounted or pop-up. RFAI detection + RFAI-ATK defeat. First C-UAS with integrated RF attack. |
| DroneSentry-C2 | Software platform | Command and control. SensorFusionAI. Integrates third-party sensors via RESTful API. |
| DroneSentry-C2 Enterprise | Network C2 | Multi-site unified monitoring. Critical infrastructure networks. |
| DroneGun Mk4 | Handheld jammer | Point-and-shoot RF disruption. Military/LE only. |
| DroneGun Tactical | Compact jammer | Smaller form factor handheld. |
| RfPatrol Mk2 | Body-worn detector | Passive RF detection, real-time alerts. Wearable. |
| DroneOptID | AI software | Camera-agnostic computer vision for drone detection/tracking. |

DroneShield integrates partners including RADA (AESA radar),
FLIR (thermal cameras), Echodyne (metamaterial radar), Bosch,
and Sentrycs (protocol-level cyber takeover).

### Dedrone (Axon)

Acquired by Axon (TASER parent company). RF + radar + acoustic
+ optical sensor fusion. Strong in law enforcement and critical
infrastructure protection. US/German operations.

### D-Fend Solutions (Israel)

| Detail | Value |
|--------|-------|
| HQ | Israel |
| Product | EnforceAir |
| Approach | Cyber C-UAS — protocol manipulation for controlled takeover |
| Key Feature | Takes control of hostile drone, forces controlled landing |
| Advantage | Non-kinetic, non-jamming — doesn't disrupt friendly RF |

EnforceAir is unique in the C-UAS space because it doesn't jam.
It exploits drone communication protocols to take control of the
drone and land it safely. This avoids the collateral damage of
broadband jamming (which disrupts all RF in the area, including
friendly communications).

### Department 13 (USA/Australia)

| Detail | Value |
|--------|-------|
| Product | MESMER |
| Approach | Protocol manipulation — similar to D-Fend |
| Key Feature | Takes over drone control without jamming |

### Citadel Defense (USA)

| Detail | Value |
|--------|-------|
| Product | Titan |
| Approach | AI-powered C-UAS |
| Key Feature | Autonomous threat assessment and response |

### Sentrycs (Israel)

Protocol-level cyber takeover. Integrated into DroneShield's
DroneSentry platform. Controlled landing and forensic capabilities.

### Robotican (Israel)

| Detail | Value |
|--------|-------|
| Product | Goshawk |
| Type | Kinetic interceptor drone |
| Approach | Autonomous aerial intercept — drone catches drone |
| Comms | Uses Elsight Halo for C2 |

Goshawk represents the kinetic interceptor approach — an
autonomous drone designed to physically intercept hostile drones.
This bypasses EW countermeasures entirely since the interceptor
is autonomous.

---

## The Ukrainian C-UAS Laboratory

Ukraine operates the most intense C-UAS environment on earth.
Both sides deploy extensive EW and C-UAS capabilities, creating
a continuous adaptation cycle:

- Russian EW systems jam GPS, spoof navigation, disrupt C2 links
- Ukrainian drones adapt (fiber-optic, FHSS, autonomous terminal guidance)
- Russia adds rear-facing cameras and altitude-change sensors to Shaheds
- Ukrainian interceptor drones (Wild Hornets Sting, Motor-G Vandal-powered)
  evolve to counter evasive maneuvers

This cycle produces more C-UAS innovation per month than any
formal defense program produces per year. The lessons flow
directly into Western C-UAS and counter-counter-UAS development.

---

## Implications for Drone Operators

1. **Consumer RF links are trivially defeated.** DJI, ELRS, CRSF —
   all operate on known frequencies with known protocols. Any
   competent C-UAS system will detect and can disrupt them.

2. **Autonomy is the counter to C-UAS.** A drone that can complete
   its mission without a continuous RF link (autonomous navigation,
   onboard processing) is inherently harder to defeat than one
   that requires constant pilot control.

3. **Fiber-optic is the ultimate C-UAS counter.** No RF to detect,
   jam, or spoof. The C-UAS response to fiber-optic drones must
   be kinetic (interceptor drones, nets, directed energy) or
   optical (visual detection + tracking).

4. **Know the threat environment before you fly.** If you're
   operating near military installations, prisons, airports, or
   large events, assume C-UAS systems are present.

5. **C-UAS drives drone design.** The reason tactical drones need
   EW-resilient comms, GPS-denied navigation, and onboard autonomy
   is specifically because C-UAS systems exist and are improving
   rapidly. Design for the threat, not for the spec sheet.

---

*Last updated: March 2026*
