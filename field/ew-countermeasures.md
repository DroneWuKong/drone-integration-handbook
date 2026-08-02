# RF Interference Recognition and Flight Safety

> **Verified:** July 31, 2026  
> **Scope:** Lawful civilian, commercial, educational, and public-safety UAS troubleshooting in the United States.  
> **Excluded:** Jamming, spoofing, transmitter location, countermeasure evasion, unauthorized frequency or power changes, and offensive electronic-warfare activity.

A degraded control, video, telemetry, or navigation link does **not** by itself prove intentional jamming. The same symptoms can be caused by damaged antennas, poor power, receiver overload, self-interference, congestion, multipath, obstructions, configuration errors, thermal problems, or ordinary range limits.

The safe response is to protect people and aircraft first, follow a tested contingency, preserve evidence, eliminate ordinary causes, and report unresolved suspected harmful interference through the proper channel.

Federal law prohibits ordinary civilian operation, marketing, or sale of signal jammers in the United States. Nothing in this guide authorizes interference with another user's communications or operation outside the frequencies, power levels, equipment authorizations, licenses, and operating rules applicable to the system.

---

## Immediate priorities during a link anomaly

Use the aircraft's approved operating manual, manufacturer guidance, and organization procedures. Do not improvise a new flight mode, frequency, power setting, or mission objective while the aircraft is already degraded.

### 1. Maintain aircraft control if possible

- Reduce pilot workload.
- Avoid aggressive maneuvering unless required to prevent a collision.
- Maintain separation from people, structures, vehicles, and other aircraft.
- Use only a **previously tested and approved** contingency mode.
- If safe control cannot be assured, execute the planned abort, recovery, diversion, or landing procedure.

### 2. Do not diagnose intent in flight

“Jamming” is a conclusion, not an instrument reading. Do not pursue a suspected source, attempt to map it, fly toward it, or continue an operation to collect more evidence when safety margins are shrinking.

### 3. Protect other airspace users

Give way to crewed aircraft. If the operation is near emergency response, a TFR, an airport, a critical facility, or other sensitive airspace, terminate or recover the operation as required by the applicable rules and authorization.

### 4. Preserve data after the aircraft is safe

Save logs, screenshots, controller messages, video, and maintenance observations before rebooting, updating, or changing the configuration.

---

## Symptoms and ordinary causes

### Control-link degradation

Possible indicators include reduced link-quality values, delayed commands, telemetry loss, failsafe warnings, or complete control-link loss.

Common non-malicious causes:

- damaged, detached, shadowed, or incorrectly polarized antennas;
- loose coax or connector damage;
- receiver power instability or brownout;
- transmitter power or antenna fault;
- incorrect region, protocol, rate, or model configuration;
- self-interference from onboard Wi-Fi, video, telemetry, or compute hardware;
- receiver desensitization from a nearby transmitter;
- congested spectrum;
- terrain, structures, foliage, vehicle bodies, or aircraft orientation blocking the path;
- ordinary range limits.

### Video degradation

Possible indicators include breakup, freezing, frame loss, color or synchronization errors, or loss of the image while other links remain normal.

Common non-malicious causes:

- camera or video-transmitter power problems;
- overheated video hardware;
- damaged antenna or feed line;
- incorrect channel or bandwidth configuration;
- multipath near buildings, vehicles, metal surfaces, or the ground;
- blockage by the airframe, battery, payload, terrain, or foliage;
- another authorized user occupying nearby spectrum;
- encoder, cable, connector, display, or network faults.

### GNSS or navigation anomalies

Possible indicators include falling satellite count, inconsistent position, poor accuracy estimates, jumps, drift, unexpected mode changes, or disagreement between navigation sources.

Common non-malicious causes:

- antenna placement or damage;
- airframe or payload masking;
- multipath near buildings, cliffs, metal roofs, or vehicles;
- electromagnetic noise from onboard electronics;
- inadequate sky view;
- ionospheric or space-weather effects;
- stale corrections, base-station, network, or datum problems;
- compass interference or calibration error;
- software, sensor, or estimation faults.

### Several links degrade together

Simultaneous symptoms can be caused by:

- common power failure;
- damaged wiring or connector assemblies;
- processor overload;
- thermal shutdown;
- a shared antenna or network path;
- nearby high-power authorized transmitters;
- severe site congestion;
- airframe orientation or terrain masking.

Do not skip the common-cause check merely because intentional interference seems plausible.

---

## Safe troubleshooting sequence

### Step 1 — Record the event before changing anything

Capture:

```text
Date and local/UTC time:
Location and operating area:
Aircraft and serial/configuration ID:
Pilot and observer:
Mission phase:
Altitude and approximate position:
Control/video/telemetry/GNSS symptoms:
Warnings and displayed values:
Weather and visibility:
Known nearby transmitters or events:
Recovery action:
Outcome:
```

Export the original logs and preserve an unmodified copy.

### Step 2 — Inspect power and physical hardware

With the aircraft disarmed and made safe:

- inspect batteries, regulators, connectors, cables, and grounds;
- inspect all RF connectors and antennas;
- check for impact, heat, water, contamination, or abrasion;
- verify antennas are the correct type and attached to the intended port;
- inspect payload and accessory wiring added since the last known-good flight;
- review brownout, reset, thermal, and fault logs.

### Step 3 — Compare against the last known-good configuration

Record changes to:

- firmware and configuration;
- receiver or transmitter settings;
- antennas or mounting;
- payloads and onboard computers;
- radio, video, network, or navigation hardware;
- battery and power architecture;
- site, altitude, and flight profile.

Revert only through an approved configuration-control process.

### Step 4 — Isolate self-interference on the ground

In a lawful controlled test area, use the organization's test procedure to compare the aircraft with optional onboard transmitters and payload systems enabled or disabled one at a time.

The objective is to identify interference **generated by your own system**, not to locate or characterize another party's communications.

Record:

- aircraft state;
- which subsystems were active;
- measured link or noise indicators;
- test distance and geometry;
- power source;
- instrument and software versions;
- result.

Do not transmit outside authorized frequencies, power, or test conditions.

### Step 5 — Compare locations and times

If the problem cannot be reproduced at a known-clean test site, document the difference rather than declaring intentional interference.

Useful comparisons include:

- same aircraft at another lawful site;
- same site at another time;
- a known-good aircraft of the same configuration;
- a known-good antenna, cable, battery, or receiver;
- manufacturer diagnostic tools;
- approved passive spectrum measurements.

### Step 6 — Escalate to the manufacturer or service provider

Provide the evidence package and ask for review of:

- hardware faults;
- firmware defects;
- known coexistence issues;
- approved configuration limits;
- status-code interpretation;
- repair or replacement procedures.

### Step 7 — Report unresolved suspected harmful interference

After ordinary equipment and connectivity causes have been investigated:

- use the [FCC Consumer Complaint Center](https://consumercomplaints.fcc.gov/) for applicable interference complaints;
- use the FCC public-safety interference process when public-safety communications are affected;
- report suspected GPS interference through the channels identified by [GPS.gov](https://www.gps.gov/information-about-gps-jamming), including the FCC and U.S. Coast Guard Navigation Center where applicable;
- notify the organization's spectrum manager, site authority, or license coordinator;
- report related aviation-safety issues through the appropriate FAA channel.

An emergency or immediate threat should be reported to the appropriate emergency or public-safety authority rather than investigated by the operator.

---

## Preflight interference-resilience checklist

### Configuration

- [ ] Exact approved firmware and configuration identified
- [ ] Correct region, frequencies, channels, bandwidths, and legal power settings confirmed
- [ ] Antenna type, connector, orientation, and polarization confirmed
- [ ] Control, video, telemetry, Wi-Fi, payload, and Remote ID transmitters inventoried
- [ ] Self-interference assessment completed after any hardware change

### Safety behavior

- [ ] Lost-link behavior tested in a controlled environment
- [ ] Navigation-degradation behavior understood
- [ ] Manual or independent recovery mode tested where supported
- [ ] Alternate landing or recovery area identified
- [ ] Pilot and observer know the abort criteria
- [ ] Return, land, or other contingency does not depend on a subsystem already known to be unreliable

### Evidence readiness

- [ ] Logging enabled and storage available
- [ ] Aircraft/configuration identifier recorded
- [ ] Time synchronized where practical
- [ ] Contact information for manufacturer, spectrum manager, site authority, and regulator available

---

## PNT resilience without spoofing claims

A position anomaly should be handled as an **untrusted navigation estimate** until the cause is known.

Safer system design includes:

- independent position or velocity sources where justified;
- integrity and confidence monitoring;
- clear operator indication when estimates disagree;
- a documented operating envelope for GPS-denied modes;
- tested fallback behavior;
- protection against a low-confidence estimate silently commanding the aircraft.

Do not rely on satellite count alone to distinguish obstruction, interference, spoofing, antenna failure, multipath, or estimator problems.

---

## What this guide does not authorize

Do not use this guide to:

- operate, acquire, advertise, sell, or distribute a jammer;
- transmit false navigation signals;
- interfere with control, video, telemetry, GNSS, cellular, public-safety, or other authorized communications;
- change to unauthorized frequencies or exceed permitted power;
- locate, follow, identify, or attack a suspected transmitter;
- decode or exploit another party's communications;
- evade a lawful counter-UAS, security, or spectrum-enforcement system;
- continue an unsafe mission merely to collect data.

Authorized federal activity, licensed testing, and government spectrum operations have their own written authorities and procedures. They should not be inferred from a public handbook.

---

## Evidence-quality labels

Use these labels in incident reports:

| Label | Meaning |
|---|---|
| **Observed symptom** | Directly recorded behavior, warning, log, or measurement |
| **Reproduced fault** | Symptom repeated under documented controlled conditions |
| **Probable equipment cause** | Evidence strongly supports an internal hardware/configuration cause |
| **Environmental interference suspected** | Ordinary internal causes were investigated; source and intent remain unknown |
| **Harmful interference confirmed by authority** | Determination made by the responsible regulator, spectrum manager, or authorized investigator |
| **Intentional jamming confirmed by authority** | Intentional source confirmed by an authorized investigative process |

Operators should ordinarily stop at the evidence level they can actually support.

---

## Official source record

| Authority | What it supports | Verified |
|---|---|---:|
| [GPS.gov — Information About GPS Jamming](https://www.gps.gov/information-about-gps-jamming) | Federal jammer prohibition, ordinary troubleshooting first, FCC reporting | 2026-07-31 |
| [GPS.gov — Spectrum and Interference Issues](https://www.gps.gov/spectrum-interference-issues) | Interference sources and GPS reporting context | 2026-07-31 |
| [FCC Consumer Complaint Center](https://consumercomplaints.fcc.gov/) | Interference complaint intake | 2026-07-31 |
| [FCC Emergency Complaints](https://consumercomplaints.fcc.gov/hc/en-us/articles/115000914506-Emergency-Complaints) | Consumer/non-public-safety and public-safety interference routing | 2026-07-31 |
| [FAA Hotline](https://www.faa.gov/about/office_org/headquarters_offices/aae/programs_services/faa_hotlines) | Aviation-safety and regulatory reporting | 2026-07-31 |
| [NTIA — Regulating the Use of Spectrum](https://www.ntia.gov/book-page/regulating-use-spectrum) | Why uncoordinated transmissions create interference and require regulation | 2026-07-31 |

Questions or corrections: [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).
