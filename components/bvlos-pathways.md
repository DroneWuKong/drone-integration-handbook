# BVLOS Pathways

Beyond Visual Line of Sight operations entered a new phase in August 2025 when the FAA published its long-awaited Part 108 Notice of Proposed Rulemaking. For the first time, there's a clear statutory framework for routine BVLOS operations — not just individual waivers. This guide covers the current compliance paths and what's changing.

> **Note:** Part 108 is still proposed rulemaking as of early 2026. The FAA is reviewing public comments. What exists today are the Part 107 waiver and COA pathways. Part 108 is described here as the expected near-term framework.

---

## What BVLOS Means and Why It's Hard

Under standard Part 107, you must maintain visual line of sight with your drone at all times — roughly 1,500 feet in optimal conditions. BVLOS operations remove this constraint, enabling long-range missions: infrastructure corridor inspection, precision agriculture at scale, last-mile delivery, and persistent ISR.

The regulatory difficulty is that VLOS is also the primary safety mechanism. Without it, the burden shifts to technology: detect-and-avoid systems that tell the drone (and operator) whether other aircraft are nearby, reliable command-and-control links that can't be severed beyond radio range, and airspace deconfliction systems that prevent two drones from being in the same place at once.

---

## Current Paths (Pre-Part 108)

### Path 1: Part 107 BVLOS Waiver

The existing mechanism. You apply to the FAA for a waiver to § 107.31 (visual line of sight requirement), demonstrating that your specific operation can be conducted safely without VLOS.

**Reality check:** BVLOS waivers increased from ~1,200 in 2020 to ~27,000 by 2023, but the vast majority of approved operations still use visual observers. Of 44,000+ BVLOS flights logged under the FAA's BEYOND program through 2025, fewer than 800 (~2%) were flown without a visual observer. The safety case for VO-less operations remains the hardest part of any waiver application.

**What the application requires:**
- Detailed operational description (location, altitude, corridor, timing)
- Aircraft technical description (remote ID compliance, C2 link architecture, DAA capability)
- Emergency procedures (lost link, pilot incapacitation, aircraft malfunction)
- Risk mitigation narrative addressing ground risk and air risk
- Proof of operational safety (flight test data, simulation, comparable operations)

**Timeline:** 90 days minimum. In practice 6–18 months. Applies only to the specific described operation — a new location or aircraft requires a new application.

### Path 2: Certificate of Authorization (COA)

COAs are issued to public agencies (law enforcement, fire, government entities) under 14 CFR § 91.203. They allow more flexible operations than Part 107, including BVLOS, at the cost of ongoing reporting and oversight requirements.

Public safety agencies often find COA amendments faster to process than commercial waivers because there's an established relationship with the FAA and a clear public benefit case.

### Path 3: Part 135 Air Carrier Certificate

Amazon Prime Air, UPS Flight Forward, and Wing operate under Part 135 certificates. This gives them authority for routine BVLOS operations at scale but requires FAA oversight comparable to a small airline: operations specifications, airworthiness data, crew training programs.

Not a realistic path for most operators — it's the endpoint for mature commercial delivery networks, not a starting point for an inspection company.

---

## Part 108: The Proposed BVLOS Framework (August 2025 NPRM)

Part 108 proposes to replace the waiver-by-waiver approach with a risk-tiered authorization framework. The core structure:

### Two Authorization Types

**Permit (lower-risk):**
- Faster issuance (targeted at days, not months)
- Restricted to specific operation types: corridor surveys, infrastructure inspection, precision agriculture
- Operations over sparse population in uncontrolled airspace
- Remote ID required
- DAA via ADS-B In required or equivalent
- Flight below 400ft AGL in shielded areas

**Certificate (higher-risk):**
- Full operations specification review — comparable to Part 135 light
- Allows operations over people, in controlled airspace, and at higher operational complexity
- Requires a designated Operations Supervisor and Flight Coordinator
- Safety Management System (SMS) required
- The path for package delivery, urban ISR, and complex corridor operations

### Airworthiness

Under Part 108, aircraft up to 1,320 lbs including payload do not need traditional FAA type certification. Instead, manufacturers self-certify compliance with consensus standards (ASTM F3003, F2909, etc.) — the same approach used for Light Sport Aircraft. This is a significant reduction in friction for UAS manufacturers.

### Detect-and-Avoid Requirements

Part 108 requires UAS to detect and yield right-of-way to any aircraft broadcasting ADS-B Out or other electronic conspicuity technology. The practical implication:

- Your aircraft needs **ADS-B In** (receiver) to detect manned traffic
- You need a DAA algorithm that can command avoidance maneuvers or alert the operator
- ADS-B Out is not required for UAS under 1,320 lbs but is strongly encouraged (and may be required in controlled airspace)

**For DIY BVLOS platforms:** uAvionix Ping (ADS-B transceiver, ~$800), Sagetech MXS, and mRo ACSP7 are the common hardware options. ArduPilot 4.4+ has native ADS-B In support with avoidance action.

### UTM and ADSP Integration

For Permit-level operations, Part 108 requires coordination with an FAA-approved Automated Data Service Provider (ADSP) for airspace deconfliction. ADSPs are the commercial entities (currently in development / early certification) that will handle:

- Pre-flight airspace reservation
- Real-time conflict detection with other BVLOS operators
- ATC integration in controlled airspace

In practice, this means most BVLOS Permit operators will need to subscribe to a UTM service. ANRA Technologies, Airbus UTM, and Wing are among the early ADSP candidates. Pricing and availability are not yet established.

---

## Practical BVLOS Stack for a Custom Platform

Assuming a DIY ArduPilot fixed-wing or VTOL targeting Part 108 Permit operations:

### Command & Control Link

The C2 link must be reliable beyond visual range. Options ranked by practicality:

| Link Type | Range | Latency | Cost | Notes |
|---|---|---|---|---|
| Cellular (LTE/5G) | Nationwide where coverage exists | 50–200ms | $30–80/mo | DroneEngage, SIYI, Herelink cellular |
| Satellite (Iridium) | Global | 270–400ms | $150–500/mo | Too high latency for active control; OK for telemetry + failsafe |
| Satellite (Starlink) | Near-global | 20–40ms | $120–200/mo + terminal | Promising but terminal weight is significant |
| 900MHz LoRa (MANET) | 10–30km LOS | 100–300ms | Low | Mesh relay extends range; Meshtastic for backup C2 |
| 1.4GHz licensed | 100+ km | <50ms | High (license) | Best for long-range fixed-wing ISR |

The most practical setup for low-cost BVLOS: **primary C2 via LTE (DroneEngage)**, **backup telemetry via LoRa mesh** (Meshtastic), with a 900MHz or 1.4GHz direct link for short-range departure and approach phases.

### ADS-B In

Required under Part 108. ArduPilot configuration:
```
ADSB_ENABLE = 1
ADSB_TYPE = 1 (MAVLink) or 2 (uAvionix Ping)
AVD_ENABLE = 1  (Airborne Vehicle Detection — ArduPilot avoidance)
AVD_F_ACTION = 2 (Climb on threat detection)
```

### Remote ID

Required at all times. See the Remote ID for Custom Builds guide for wiring and configuration details.

### GCS Software

QGroundControl and Mission Planner both support BVLOS workflows: corridor planning, altitude limits, geofence setup, and multi-link C2. Mission Planner has better ArduPilot integration; QGC has better cross-platform support and MAVLink 2 telemetry handling.

For cellular BVLOS via DroneEngage: the DroneEngage companion computer (Raspberry Pi) connects to your FC via USB serial and handles MAVLink forwarding over the cellular link transparently. You fly with QGC or Mission Planner on any internet-connected device.

---

## Operational Requirements Under Part 108 Permit

The operational requirements for a Permit are manageable for a serious operator:

1. **Pre-flight NOTAM:** File a UAS-specific NOTAM via DroneZone for the planned operating area. Required before each BVLOS operation.
2. **Remote ID active:** Broadcast module powered and transmitting from the moment of departure.
3. **ADSP coordination:** File flight intent with an approved ADSP (once the infrastructure is in place; currently in development).
4. **C2 link monitoring:** Maintain and log C2 link quality throughout the flight. Lost link action (defined in operations manual) must execute automatically.
5. **ADS-B monitoring:** Active ADS-B In monitoring with DAA capability operative.
6. **Post-flight reporting:** Log flight data including any conflicts detected, C2 link outages, or operational deviations.

The reporting and logging requirements directly motivate Tooth's audit trail design — a complete Tooth record satisfies most of the Part 108 recordkeeping burden automatically.

---

## What Changes Everything: Detect-and-Avoid

The fundamental barrier to scalable BVLOS has always been that operators can't visually scan for conflicting traffic. The regulatory structure compensates for this with technology requirements, but those requirements add cost, weight, and complexity.

The realistic near-term DAA stack for a Group 1 UAS (under 25kg):

- **ADS-B In** (~50–200g, ~$300–800): detects all manned aircraft broadcasting ADS-B Out. Covers most commercial and general aviation traffic.
- **Traffic Advisory System integration**: ArduPilot's native avoidance will command a climb maneuver when an ADS-B target approaches within a configurable range.
- **Gap**: Low-altitude, non-ADS-B aircraft (gliders, ultralights, non-equipped helicopters, other drones). No affordable solution yet. The FAA acknowledges this gap and Part 108 does not require detection of non-equipped aircraft — the risk mitigation is procedural (fly at appropriate times and locations).

This gap is the core reason VO-less BVLOS at scale remains difficult. The ADS-B → avoidance system handles the manned aviation threat; the unequipped aircraft threat is still mostly managed by procedural deconfliction (fly at night, fly in low-activity airspace, coordinate with ATC).
