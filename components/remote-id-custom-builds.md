# Remote ID Decision Guide for Custom UAS — United States

> **Verified:** July 31, 2026  
> **Scope:** Civil operations in the United States, primarily under 14 CFR Part 107 or the Exception for Limited Recreational Operations of Unmanned Aircraft.  
> **Use:** Preliminary operational screening—not an FAA authorization, Declaration of Compliance, or substitute for operation-specific advice.

Remote ID obligations depend first on **why and how the aircraft is being operated**, then on registration status and the exact aircraft or broadcast module being used. A custom build is not exempt merely because it was assembled by the operator, uses open-source flight-control firmware, or weighs less than 250 grams.

The governing rule is [14 CFR Part 89](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-89). The FAA states that drones **required to be registered or actually registered** must comply with Remote ID unless an authorized exception or deviation applies.

---

## The decision tree

### Step 1 — Identify the operating rule

Use the rule for the actual flight, not the aircraft's marketing category.

| Operation | Starting point |
|---|---|
| Work, business, inspection, mapping, paid or unpaid service, most organizational use | Part 107 unless another authority applies |
| Purely personal recreation meeting every requirement of 49 U.S.C. § 44809 | Limited recreational exception |
| Public aircraft, complex Part 91, waiver-based, research, or other special operation | Confirm the specific authorization with the FAA |

The FAA advises operators who are unsure whether a flight is recreational to assume Part 107 and satisfy Part 107 requirements.

### Step 2 — Determine whether registration is required

| Operating rule | Registration result |
|---|---|
| Part 107 | Each aircraft/device must be registered, including aircraft under 250 g |
| Limited recreation, aircraft 250 g or more | Registration required |
| Limited recreation, aircraft under 250 g | Registration is generally not required if the flight qualifies fully for the recreational exception |
| Aircraft voluntarily registered even though not otherwise required | Remote ID requirements generally apply because the aircraft is registered |

Weigh the complete aircraft in its normal flight configuration, including its battery and permanently or routinely installed equipment.

### Step 3 — If registered or required to be registered, select a compliance path

The FAA identifies three ordinary operating paths:

1. Operate a **Standard Remote ID drone**.
2. Operate a drone fitted with an FAA-accepted **Remote ID broadcast module**.
3. Operate a drone without Remote ID equipment **inside a FRIA**, within the FRIA boundary and visual line of sight.

A separate FAA Letter of Authorization may permit an eligible operator to deviate from Remote ID requirements for a defined purpose. Do not assume that a waiver, research project, government customer, or event automatically creates that authorization.

---

## Path A — Standard Remote ID drone

A Standard Remote ID drone is produced with built-in Remote ID capability and broadcasts required identification and location information about the aircraft and control station.

Before treating an aircraft as Standard Remote ID compliant:

- Find the **exact manufacturer and model** in the FAA's [Declaration of Compliance system](https://uasdoc.faa.gov/listDocs).
- Confirm the listing is for **Standard Remote ID**, not only a broadcast module with a similar product name.
- Use the Remote ID serial number supplied or displayed by the manufacturer.
- Enter that Remote ID serial number in the appropriate FAA registration record.
- Follow the manufacturer's current operating and update instructions.

A flight-controller setting, Wi-Fi beacon, open-source package, or serial number entered by the user does not by itself convert a custom aircraft into a Standard Remote ID aircraft. The FAA accepts Declarations of Compliance from manufacturers, not individual operators attempting to certify an improvised configuration.

---

## Path B — Remote ID broadcast module

A broadcast module can retrofit an aircraft that was not produced as a Standard Remote ID drone. It broadcasts identification and location information about the aircraft and its **takeoff location**.

### Verify the module before purchase or use

- Confirm the **exact module manufacturer and model** appears in the FAA [Declaration of Compliance system](https://uasdoc.faa.gov/listDocs).
- Confirm the listing identifies it as a Remote ID broadcast module.
- Obtain the module's Remote ID serial number from the device or manufacturer documentation.
- Register the module and aircraft information using the FAA's current DroneZone process.
- Follow the module manufacturer's installation, power, placement, firmware, and status-indication instructions.

### Operational limitation

The FAA states that a pilot using a broadcast module must be able to see the drone at all times during flight. A broadcast module is therefore not a general solution for BVLOS operation.

### Recreational inventory versus Part 107

The registration treatment differs:

- **Recreational:** A recreational operator may use one registration number for the devices in the recreational inventory. The FAA permits a broadcast module to be moved among listed non-Standard-Remote-ID drones when the module's Remote ID serial number and each aircraft make/model are entered as instructed in DroneZone.
- **Part 107:** Each individual Standard Remote ID drone or broadcast module is registered separately and receives a unique registration number. Do not reuse the recreational inventory procedure for Part 107 devices.

The registration number marked on the aircraft and the **Remote ID serial number** are different fields. Do not substitute the FAA registration number for the manufacturer-assigned Remote ID serial number.

---

## Path C — FAA-Recognized Identification Area

A FRIA is a defined location where an aircraft without Remote ID equipment may be operated.

For an aircraft relying on the FRIA path:

- the aircraft must remain inside the FRIA boundary;
- the aircraft must remain within visual line of sight;
- the operator must comply with every other rule applicable to the flight;
- the operator should verify that the FRIA is current before the flight.

A FRIA does not make an aircraft compliant everywhere else and is not a portable exemption that follows a club, school, or operator to another location.

---

## Custom-build guidance

For most one-off Betaflight, iNav, ArduPilot, PX4, or independently assembled aircraft, the lowest-ambiguity path is:

1. Determine the actual operating rule.
2. Register the aircraft/device under the correct dashboard when required.
3. Select a broadcast module listed under an FAA-accepted Declaration of Compliance.
4. Install it exactly as the manufacturer specifies.
5. Enter the module's Remote ID serial number in DroneZone.
6. Verify the module reports normal status before flight.
7. Maintain visual line of sight when relying on the broadcast-module path.

Do not assume that generic firmware support is a compliance approval. Firmware may provide position data or transport to a module, but compliance depends on the complete declared product/configuration and the operator's registration and operating practices.

### No firmware commands are prescribed here

Remote ID implementation details change across firmware, hardware targets, modules, and releases. A command should appear in this handbook only after it is verified against:

- the official documentation for the exact firmware version;
- the exact aircraft and flight-controller target;
- the exact FAA-accepted module or Standard Remote ID product;
- a documented bench and flight-status test;
- the current FAA registration workflow.

Until those conditions are met, use the module or aircraft manufacturer's instructions rather than an unverified CLI recipe.

---

## Registration and serial-number checklist

Before submitting or editing a registration:

- [ ] Confirm whether the operation is Part 107, limited recreation, or another authority.
- [ ] Confirm whether the aircraft is required to be registered.
- [ ] Confirm whether the selected product is Standard Remote ID or a broadcast module.
- [ ] Confirm the exact product in the FAA Declaration of Compliance system.
- [ ] Record the manufacturer-assigned **Remote ID serial number**.
- [ ] Use the correct DroneZone dashboard: Part 107 or Recreational Flyer.
- [ ] For Part 107, register each individual device separately.
- [ ] For recreational use, follow the FAA inventory procedure for every aircraft/module combination.
- [ ] Mark the aircraft with the FAA registration number as required.
- [ ] Carry proof of registration during the operation.

---

## Preflight verification

Remote ID should be treated as a required aircraft system when the operation depends on it.

Before flight:

- [ ] Confirm the aircraft or module matches the registration record.
- [ ] Confirm the Remote ID serial number is correct.
- [ ] Confirm the module or aircraft has the required position source and indicates normal operation.
- [ ] Confirm the module is installed and powered according to manufacturer instructions.
- [ ] Confirm the planned operation is compatible with the selected path, including VLOS for a broadcast module.
- [ ] Confirm any FRIA boundary or FAA authorization relied upon is current.
- [ ] Resolve abnormal status before takeoff; do not assume a receiver app's failure alone proves the aircraft is noncompliant or that a visible app entry alone proves full compliance.

Keep the registration record, product documentation, Declaration of Compliance reference, firmware/module version, and maintenance record with the aircraft's configuration documentation.

---

## Common errors

**"It is under 250 g, so Remote ID never applies."**  
Incorrect. All Part 107 aircraft must be registered. A sub-250-g exception generally matters only for an aircraft flown exclusively under the limited recreational exception and not otherwise registered.

**"My FAA registration number is the Remote ID serial number."**  
Incorrect. The registration number and the manufacturer-assigned Remote ID serial number are separate.

**"The firmware has a Remote ID menu, so the build is compliant."**  
Not necessarily. Verify an FAA-accepted Declaration of Compliance for the complete Standard Remote ID product or broadcast module being used.

**"I can use one recreational registration procedure for my Part 107 fleet."**  
Incorrect. Part 107 devices are registered individually.

**"A broadcast module makes BVLOS legal."**  
Incorrect. The FAA's ordinary broadcast-module path requires the pilot to be able to see the drone throughout the flight.

**"A FRIA means the aircraft can fly without Remote ID anywhere."**  
Incorrect. The aircraft must remain within the recognized FRIA and visual line of sight.

---

## Source hierarchy and verification record

| Authority | What it supports | Verified |
|---|---|---:|
| [14 CFR Part 89](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-89) | Controlling Remote ID operating and production requirements | 2026-07-31 |
| [FAA Remote Identification of Drones](https://www.faa.gov/uas/getting_started/remote_id) | Applicability, three compliance paths, registration workflow, VLOS limitation, DoC lookup, LOA process | 2026-07-31 |
| [FAA Drone Registration](https://www.faa.gov/uas/getting_started/register_drone) | Registration requirements and DroneZone process | 2026-07-31 |
| [FAA Recreational Flyers](https://www.faa.gov/uas/recreational_flyers) | 250-g recreational registration threshold and recreational operating rule | 2026-07-31 |
| [FAA Commercial Operators](https://www.faa.gov/uas/commercial_operators) | Part 107 registration requirement | 2026-07-31 |
| [FAA Remote ID Declaration of Compliance system](https://uasdoc.faa.gov/listDocs) | Current accepted Standard Remote ID and broadcast-module declarations | Check at time of purchase and registration |
| [FAA Remote ID for Industry](https://www.faa.gov/uas/getting_started/remote_id/industry) | Manufacturer responsibility for Declarations of Compliance | 2026-07-31 |

Regulatory and product status can change. Recheck the official sources before using this guide for a new aircraft, registration, firmware change, or operation.

Questions or corrections: [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).
