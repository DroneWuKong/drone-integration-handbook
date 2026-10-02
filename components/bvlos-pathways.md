# BVLOS Pathways

The FAA published a proposed Part 108 framework for routine Beyond Visual Line of Sight operations in August 2025. As of October 2, 2026, it remains proposed rulemaking and does not itself authorize an operation. Current authority still comes through an applicable existing certificate, exemption, waiver, or authorization. [claim:reg-part108-proposed]

> **Current-status boundary:** Every Part 108 item below describes the proposal, not an effective operating rule. Check the current Federal Register docket and FAA operating-authority pages before planning an operation.

---

## What BVLOS Means and Why It's Hard

Under standard Part 107, you must maintain visual line of sight with your drone at all times — roughly 1,500 feet in optimal conditions. BVLOS operations remove this constraint, enabling long-range missions: infrastructure corridor inspection, precision agriculture at scale, last-mile delivery, and persistent ISR.

The regulatory difficulty is that VLOS is also the primary safety mechanism. Without it, the burden shifts to technology: detect-and-avoid systems that tell the drone (and operator) whether other aircraft are nearby, reliable command-and-control links that can't be severed beyond radio range, and airspace deconfliction systems that prevent two drones from being in the same place at once.

---

## Current Paths (Pre-Part 108)

### Path 1: Part 107 BVLOS Waiver

The existing mechanism. You apply to the FAA for a waiver to § 107.31 (visual line of sight requirement), demonstrating that your specific operation can be conducted safely without VLOS.

Part 107 operators that cannot comply with § 107.31 may request an operational waiver by showing an equivalent level of safety. The FAA now directs new Part 107 operational-waiver applications through the Aviation Safety Hub. [claim:reg-part107-bvlos-waiver]

**What the application requires:**
- Detailed operational description (location, altitude, corridor, timing)
- Aircraft technical description (remote ID compliance, C2 link architecture, DAA capability)
- Emergency procedures (lost link, pilot incapacitation, aircraft malfunction)
- Risk mitigation narrative addressing ground risk and air risk
- Proof of operational safety (flight test data, simulation, comparable operations)

**Timing:** The FAA says it will do its best to approve or disapprove a Part 107 waiver request within 90 days, while warning that timing varies with complexity and application completeness. Treat 90 days as an agency service target, not a guaranteed minimum or maximum. [claim:reg-part107-waiver-timing]

### Path 2: Certificate of Authorization (COA)

Public-aircraft authority is not created by § 91.203. FAA materials describe COAs for qualifying public-aircraft operations under Part 91, and a separate expedited § 91.113 waiver path for organizations that meet both the statutory Public Aircraft Operator and Public Safety Organization definitions. The exact COA or waiver conditions control the operation. [claim:reg-part91-public-safety]

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

The NPRM proposes an airworthiness-acceptance path based on consensus standards for covered aircraft rather than applying traditional type certification to every design. The eligibility details, accepted standards and final requirements remain proposal-dependent.

### Detect-and-Avoid Requirements

The NPRM proposes right-of-way and detect-and-avoid rules that use ADS-B Out or other approved electronic-conspicuity information in defined circumstances. The practical design questions include:

- The aircraft needs an approved way to receive the relevant cooperative-traffic information
- You need a DAA algorithm that can command avoidance maneuvers or alert the operator
- Equipage and operating limitations must follow the eventual rule and the specific authorization

**For DIY BVLOS platforms:** uAvionix Ping (ADS-B transceiver, ~$800), Sagetech MXS, and mRo ACSP7 are the common hardware options. ArduPilot 4.4+ has native ADS-B In support with avoidance action.

### UTM and ADSP Integration

For some proposed operations, the NPRM would require coordination with an FAA-approved Automated Data Service Provider (ADSP) for services such as deconfliction. The proposal describes services including:

- Pre-flight airspace reservation
- Real-time conflict detection with other BVLOS operators
- ATC integration in controlled airspace

In practice, this means most BVLOS Permit operators will need to subscribe to a UTM service. ANRA Technologies, Airbus UTM, and Wing are among the early ADSP candidates. Pricing and availability are not yet established.

---

## Practical BVLOS Stack for a Custom Platform

For early engineering exploration of a custom ArduPilot fixed-wing or VTOL that might later seek an applicable BVLOS approval:

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

The proposed framework includes Remote ID requirements. Current Remote ID rules and any issued operating approval control today.

Illustrative ArduPilot configuration to evaluate in a non-operational test environment:
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

## Proposed Part 108 Permit Concepts

The NPRM proposes requirements in these areas. This list is an orientation to the proposal and must not be used as a current compliance checklist:

1. **Operating authorization and airspace conditions** appropriate to the operation.
2. **Remote identification and aircraft conspicuity** as specified by any final rule and the operating approval.
3. **Third-party service coordination** where an approved service is required.
4. **C2 monitoring and lost-link response** defined by the approved operating concept.
5. **Detect-and-avoid performance** appropriate to the airspace and operation.
6. **Records and reports** required by the final rule and operating approval.

The proposed reporting and logging concepts can inform Tooth's audit-trail design. A Tooth record has not been evaluated or approved as satisfying FAA recordkeeping requirements.

---

## What Changes Everything: Detect-and-Avoid

The fundamental barrier to scalable BVLOS has always been that operators can't visually scan for conflicting traffic. The regulatory structure compensates for this with technology requirements, but those requirements add cost, weight, and complexity.

The realistic near-term DAA stack for a Group 1 UAS (under 25kg):

- **ADS-B In** (~50–200g, ~$300–800): detects all manned aircraft broadcasting ADS-B Out. Covers most commercial and general aviation traffic.
- **Traffic Advisory System integration**: ArduPilot's native avoidance will command a climb maneuver when an ADS-B target approaches within a configurable range.
- **Gap**: Low-altitude, non-ADS-B aircraft (gliders, ultralights, non-equipped helicopters, other drones). Cooperative receivers do not detect every traffic threat. Do not assume ADS-B In alone satisfies an eventual DAA requirement or an issued authorization.

This gap is the core reason VO-less BVLOS at scale remains difficult. The ADS-B → avoidance system handles the manned aviation threat; the unequipped aircraft threat is still mostly managed by procedural deconfliction (fly at night, fly in low-activity airspace, coordinate with ATC).
