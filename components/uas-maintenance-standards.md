# UAS Maintenance Standards

## Overview

The aerospace industry has converged on **ASTM F3600-22** as the foundational qualification guide for UAS maintenance technicians. Published January 2023 by ASTM Committee F46 (Aerospace Personnel), it defines the knowledge, skills, and abilities (KSAs) required to maintain UAS across three complexity classes — from hobby-grade multirotor to turbine-powered aircraft.

The standard is significant because it treats the **entire UAS as the unit of maintenance** — not just the airframe. A UAS Technician is responsible for the aircraft, ground control station, data links, and all peripheral equipment. This mirrors how operational teams actually maintain systems and is why fleet-level tooling like Tooth and Hangar tracks configuration across all subsystems, not just the FC.

**Companion standards:**
- **ASTM F2909** — Continued Airworthiness of Lightweight UAS (the task baseline F3600 draws from)
- **ASTM F3376** — Core Competencies for Aviation Maintenance Personnel (prerequisite for F3600)
- **ASTM F3366** — General Maintenance Manual (GMM) specification for sUAS

---

## The Three-Class System

F3600-22 classifies UAS by equipage complexity. The classification of the full system is determined by the **highest class of any individual component**.

### Class 1 — Consumer/Tactical Multirotor
**Voltage:** <60V electric or fuel cell  
**Typical examples:** Sub-250g hobby quads, tactical ISR multirotor (MRM2, H7 WingCore builds), DJI Mavic class

| Subsystem | Class 1 Characteristics |
|---|---|
| Landing gear | Fixed or electronically retracted |
| Engine | <60V electric |
| Structure | Remove/replace, foam gluing, composite taping |
| Maintenance model | Line-replaceable unit swap only — no structural repair |
| GCS | Consumer device (phone/tablet app) |
| Software | Open-system app with high configuration variability |
| Networking | Not required for flight |
| Data link | Radio line-of-sight only |
| Launch/recovery | Hand launch or bungee; no dedicated recovery system |
| Manuals required | Operations manual only |

**Technician KSA scope:** Basic electronics, LRU swap procedures, propulsion and battery fundamentals, firmware update procedures, operational safety.

---

### Class 2 — Mid-Complexity Fixed-Wing / Larger Multirotor
**Voltage:** 60–599V electric, piston, or fuel cell  
**Typical examples:** 6S+ fixed-wing ISR platforms, Group 1 UAS, VTOL survey aircraft, fuel cell endurance platforms

| Subsystem | Class 2 Characteristics |
|---|---|
| Landing gear | Fixed or retractable (hydraulic/pneumatic/electronic) |
| Engine | 60–599V electric, piston, rotary, or modular turbine |
| Structure | Advanced composites/metal — sanding, grinding, potting, elevated cure, riveting |
| Maintenance model | LRU swap for most components; structural repair common |
| GCS | Portable or fixed multi-user workstation; open+closed software mix |
| Networking | Simple networking (hubs, switches, routers) required |
| Data link | LOS + cellular + satellite relay possible; complex handover events possible |
| Launch/recovery | Pneumatic/hydraulic launcher; parachute, VTOL, arresting gear |
| Support equipment | Ground power unit; fuel/defuel devices; external engine start equipment |
| Manuals required | CMM + engine maintenance manual + AMM + IPC |

**Technician KSA scope:** All Class 1 plus: composites repair, hydraulic systems, complex avionics, networking, multi-link data architectures, launcher/recovery systems.

---

### Class 3 — High-Complexity / MALE / HALE
**Voltage:** >599V electric or turbine/piston comparable to manned aircraft  
**Typical examples:** Group 3–5 UAS, turbine-powered platforms, high-altitude long-endurance systems

Maintenance is functionally equivalent to manned aircraft, with the addition of UAS-specific systems (autonomy stack, ground data terminal, datalink redundancy). Full manned aviation manual set required.

---

## Airworthiness Definition

F3600-22 defines airworthiness specifically in the UAS context:

> **Airworthiness** — within this guide, refers to a state of readiness whereby the system meets all manufacturer specifications for safe operations.

This is deliberately narrower than the FAA's manned aviation definition. For UAS, airworthiness is manufacturer-spec compliance, not regulatory certification. This means the maintenance standard's authority is the **component manufacturer's documentation**, not a type certificate. For open-source platforms (ArduPilot, Betaflight), the flight controller firmware + vehicle configuration parameters collectively constitute the "manufacturer specification."

This is the direct justification for Tooth's audit trail design: every parameter change that moves the vehicle away from a known-good AMC configuration is a potential airworthiness event.

---

## Knowledge Area Taxonomy

F3600-22 Tables 2–4 define KSAs per class across these subject areas (drawn from the companion AAM standard WK88720 which shares the same taxonomy):

| Knowledge Domain | Class 1 | Class 2 | Class 3 |
|---|---|---|---|
| Structure / Airframe | Awareness | Proficient | Expert |
| Propulsion (electric) | Proficient | Expert | Expert |
| Propulsion (combustion) | Awareness | Proficient | Expert |
| Avionics / FC | Proficient | Expert | Expert |
| Information Technology / Software | Proficient | Expert | Expert |
| Data Links / RF | Awareness | Proficient | Expert |
| GCS / Control Station | Proficient | Proficient | Expert |
| Operations / Safety | Proficient | Proficient | Expert |
| Regulatory | Awareness | Proficient | Proficient |
| Human Factors | Awareness | Proficient | Proficient |
| Documentation / Manuals | Awareness | Proficient | Expert |

*Awareness = can identify and describe. Proficient = can perform with guidance. Expert = can perform independently and train others.*

---

## Relevance to the Wingman Ecosystem

The F3600-22 framework maps directly to Wingman's tooling layer:

| F3600-22 Requirement | Wingman Implementation |
|---|---|
| Airworthiness = manufacturer spec compliance | Hangar derives params from AMC vehicle_components.json; every step references manufacturer source |
| Full audit trail of configuration changes | Tooth — SHA-256 audit chain, before/after state per parameter, technician ID, timestamp |
| GCS maintenance includes software reinstall | Hangar param diff engine — compare current directory vs proposed, approve/reject per param |
| Documentation requirement (CMM/AMM/IPC) | Forge platform profiles link to manufacturer datasheets per component |
| Class 1 LRU swap with component records | Tooth component swap events — install/remove per serial/batch, flight hours at swap |
| Firmware version tracking | Tooth records firmware version at every param change event |
| Pre-flight airworthiness verification | Hangar preflight checklist module (see below) |

### The Tooth Audit Trail as Maintenance Record

Under F3600-22, any change to a Class 1 UAS that affects its configuration relative to manufacturer specifications is a maintenance event. For software-configurable platforms, this includes:

- Flight controller firmware updates
- Parameter changes (any change from the baseline AMC vehicle directory)
- Component swaps (ESC, motor, FC, receiver, battery)
- Blackbox log entries that document in-flight anomalies

Tooth records all of these. A complete Tooth record constitutes a maintenance logbook compliant with F3600-22's intent for Class 1 systems.

---

## Pre-Flight Airworthiness Checklist

The standard's airworthiness definition implies a pre-flight verification process. The following structure is used in Hangar's preflight checklist (see Hangar documentation):

**Software/Configuration**
- [ ] Firmware version matches last known-good Tooth record
- [ ] All parameters within Tooth-approved baseline (no untracked diffs)
- [ ] Blackbox logging enabled and storage available

**Propulsion**
- [ ] All motors spin up cleanly — no grinding, vibration, or asymmetric noise
- [ ] Propellers secure, no cracks or chips, pitch/diameter matches build spec
- [ ] Battery voltage at or above pre-flight minimum (BATT_ARM_VOLT threshold)
- [ ] Battery connector secure, no damage to leads

**Structure**
- [ ] Frame arms secure — no cracks at motor mounts or arm joints
- [ ] All screws present and tight (vibration inspection)
- [ ] No foam delamination or composite delamination visible

**Electronics**
- [ ] FC LED indicators normal
- [ ] RC link established and RSSI above mission minimum
- [ ] GPS lock acquired (if required for flight mode)
- [ ] OSD or telemetry feed live

**Data Links / GCS**
- [ ] GCS connected and showing live telemetry
- [ ] RC channel outputs verified (control surfaces or motor response correct)
- [ ] Failsafe tested — RC signal loss → expected FS action

---

## Standards Ecosystem Context

F3600-22 sits within a broader ASTM UAS standards family (Committee F38 and F46):

- **F3002** — Design of the Command and Control Link for sUAS
- **F3003** — Quality Assurance Specification for Small Unmanned Aircraft
- **F3178** — Operational Risk Assessment for sUAS Operations
- **F3269** — Methods for Bounding Flight Behavior of UAS
- **F3322** — Small Unmanned Aircraft Systems (sUAS) Parachutes
- **F3366** — General Maintenance Manual Specification for sUAS
- **F3376** — Core Competencies for Aviation Maintenance Personnel *(prerequisite for F3600)*
- **F3600** — **UAS Maintenance Technician Qualification** *(this standard)*

The FAA has been moving toward accepting ASTM standards as means of compliance for UAS operations under 14 CFR Part 107 and the forthcoming Part 108 (BVLOS). Organizations with F3600-aligned maintenance programs are better positioned for Part 108 compliance as those rules mature.
