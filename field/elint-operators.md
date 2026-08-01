# Lawful Spectrum Survey for UAS Operations

> **Verified:** July 31, 2026  
> **Scope:** Passive site assessment, self-interference troubleshooting, channel coordination, and recordkeeping for lawful UAS operations.  
> **Excluded:** Communications interception, content decoding, person or transmitter tracking, military-intelligence collection, targeting, evasion, spoofing, jamming, or exploitation.

A spectrum survey helps answer limited engineering questions:

- How busy is the intended operating band at this place and time?
- Is the aircraft interfering with itself?
- Are several authorized systems competing for the same channels?
- Did a hardware or configuration change raise the local noise floor?
- Does the measured environment support the planned link margin?

A spectrum plot does not, by itself, identify a transmitter, operator, protocol, intent, legality, or threat. Peaks and noise changes should be recorded as observations, not converted into unsupported attribution.

---

## Define the survey before collecting data

Write down the purpose and limits.

```text
Survey owner:
Site and authorization:
Date/time window:
Operational bands being assessed:
Aircraft/configuration:
Question being answered:
Equipment being used:
Data-retention period:
Privacy restrictions:
Responsible reviewer:
```

Examples of appropriate questions:

- Compare noise and channel occupancy before and after adding an onboard computer.
- Select among legally available channels for a multi-aircraft event.
- Document ambient conditions before a range or reliability test.
- Determine whether an intermittent problem follows the aircraft or the site.
- Compare antenna placement options on the same aircraft.

Inappropriate purposes include locating an unknown operator, decoding third-party traffic, identifying military or public-safety systems, collecting message content, evading security controls, or supporting a target package.

---

## Passive versus active testing

### Passive survey

A passive survey observes energy already present. It should not transmit merely to provoke or identify another system.

Typical measurements include:

- displayed noise floor;
- channel or band occupancy over time;
- peak and average received power;
- known emissions from your own equipment;
- changes associated with your own payloads or onboard transmitters;
- time-domain patterns without decoding third-party content.

### Active system test

An active test uses your own authorized transmitter and receiver to measure your system.

It requires:

- lawful equipment and frequencies;
- applicable license or rule authority;
- permitted power and bandwidth;
- a controlled test plan;
- coordination with the site and affected users;
- appropriate separation and safety controls;
- documentation of every transmitting device.

A spectrum analyzer, SDR, signal generator, radio, amplifier, or test transmitter should not be assumed legal for over-the-air transmission merely because it can generate the signal.

---

## Equipment and calibration record

Record enough detail for another reviewer to understand the measurement.

| Field | Example content |
|---|---|
| Instrument | Analyzer or SDR manufacturer/model |
| Serial number | Asset identifier |
| Firmware/software | Exact version |
| Antenna | Model, band, polarization, gain if known |
| Feed line | Type and length |
| Reference level | Instrument setting |
| Span | Frequency range displayed |
| Resolution bandwidth | RBW or equivalent |
| Video bandwidth | VBW or equivalent |
| Detector | Peak, RMS, average, sample, or other |
| Sweep/dwell | Time parameters |
| Calibration | Date, method, and status |
| Location | Survey point and antenna height |
| Orientation | Antenna direction/polarization |
| Time source | Local and UTC reference |

Measurements made with different antennas, gain settings, RBW, locations, or reference levels should not be compared as though they were identical.

---

## Baseline survey procedure

### 1. Establish the instrument baseline

Before interpreting the environment:

- verify the instrument and antenna cover the intended band;
- confirm no overload or clipping indication;
- record the instrument settings;
- inspect cables and connectors;
- capture an equipment-off or shielded reference where practical;
- note nearby electronics that may contaminate the measurement.

### 2. Survey with your UAS equipment powered off

Record the ambient environment before introducing your own transmitters.

Collect:

- a broad view of the authorized operating bands;
- representative narrow views of candidate channels;
- occupancy over a useful time window;
- site changes such as event operations, vehicles, Wi-Fi access points, or industrial equipment.

Do not assign a source or intent merely from a waveform shape or center frequency.

### 3. Add your equipment one subsystem at a time

With the aircraft disarmed and in an approved ground-test condition, activate only your own equipment according to the test plan.

A useful sequence may include:

1. aircraft power electronics only;
2. flight controller and sensors;
3. companion computer;
4. navigation receiver;
5. authorized control link;
6. authorized telemetry link;
7. authorized video link;
8. payload electronics;
9. Remote ID equipment;
10. complete intended configuration.

The purpose is to identify emissions and desensitization caused by **your own system**. Record every state change and do not exceed the lawful operating conditions for the equipment.

### 4. Compare the candidate operational configuration

Evaluate:

- whether one onboard transmitter raises the noise floor at another receiver;
- whether antenna placement, cable routing, shielding, or power wiring changes the result;
- whether several authorized links are unnecessarily concentrated in one band;
- whether the site's measured occupancy reduces the planned link margin;
- whether the operation should be moved, rescheduled, reconfigured within legal limits, or canceled.

### 5. Preserve raw and interpreted records separately

Keep:

- original instrument files;
- screenshots with settings visible;
- test notes;
- aircraft/configuration identifier;
- photographs of the measurement setup where appropriate;
- a separate analysis explaining any conclusions.

Do not overwrite raw data with annotations.

---

## Self-interference checks

Common self-interference paths include:

- two transmitters placed too close together;
- inadequate antenna separation;
- receiver antenna shadowing by the battery, frame, payload, or vehicle;
- shared or noisy power rails;
- digital electronics radiating into GNSS or other sensitive receivers;
- damaged shielding, coax, filters, or connectors;
- harmonics or spurious emissions from defective equipment;
- high-power ground transmitters overloading a nearby receiver front end;
- multiple onboard systems using the same band.

A passive survey can show correlation, but correlation is not certification. Formal emissions compliance and equipment authorization require the applicable laboratory methods and authority.

---

## Channel coordination for a lawful operation

A survey supports coordination; it does not create spectrum rights.

For each system, record:

| System | Authority | Band/channel | Bandwidth | Power | Antenna | Operator | Time window |
|---|---|---|---|---:|---|---|---|
| Control | License/rule/equipment authorization | | | | | | |
| Video | | | | | | | |
| Telemetry | | | | | | | |
| Mesh/network | | | | | | | |
| Remote ID | Applicable product authorization | | | | | | |
| Payload link | | | | | | | |

Then:

- avoid unnecessary overlap among your own systems;
- coordinate with other authorized users at the site;
- maintain a power-on sequence;
- prohibit unplanned transmitters;
- retest after substitutions or repairs;
- stop the test if it affects safety or another authorized service.

Do not respond to congestion by using an unauthorized band, bypassing regional settings, exceeding legal power, or interfering with another user.

---

## Privacy and communications limits

A lawful engineering survey should collect the minimum data needed for the stated purpose.

Do not:

- decode message content;
- capture credentials or private communications;
- retain device identifiers without a documented need and authority;
- follow a transmitter to identify a person or location;
- publish raw data that exposes protected facilities or users;
- correlate RF observations with personal information for surveillance;
- use a public handbook as authority for law-enforcement or intelligence collection.

Where a protocol exposes identifiers as part of ordinary operation, document whether collection is necessary, how it is protected, how long it is retained, and who may access it.

---

## Interpreting results without overclaiming

### Appropriate conclusions

- “The measured noise floor was higher at Site A than Site B under the recorded settings.”
- “Activating the onboard computer correlated with a rise near the GNSS receiver band.”
- “The control receiver's reported quality decreased when the nearby authorized video transmitter was enabled.”
- “The planned channels were heavily occupied during the event window.”
- “The source of the observed energy was not identified.”

### Inappropriate conclusions without additional authority and evidence

- “This peak is an illegal jammer.”
- “That waveform belongs to a particular person or organization.”
- “The source is hostile.”
- “The operator intended to disrupt our flight.”
- “The source is located at this coordinate.”
- “Changing to this unauthorized frequency is justified.”

Use evidence labels:

| Label | Meaning |
|---|---|
| **Instrument observation** | Raw measured value under documented settings |
| **Correlation** | Change occurred with a documented system-state change |
| **Reproduced self-interference** | Internal cause repeated under controlled conditions |
| **External interference suspected** | Environmental energy observed; source and intent unknown |
| **Source confirmed by authorized process** | Identity established by regulator, licensee, spectrum manager, or other authorized investigation |

---

## Reporting package

For unresolved harmful-interference concerns, prepare:

```text
Reporter and organization:
Contact information:
Date/time in local and UTC:
Location and operating authority:
Affected service/system:
Equipment and authorization:
Observed symptoms:
Safety effect:
Troubleshooting completed:
Instrument and settings:
Raw data location:
Known authorized site users:
Whether public-safety communications were affected:
Whether the event is ongoing:
```

Route the package to the appropriate party:

- equipment manufacturer or service provider;
- site spectrum coordinator or licensee;
- FCC complaint process;
- FCC public-safety interference process where applicable;
- U.S. Coast Guard Navigation Center and/or FCC for suspected GPS interference, as directed by GPS.gov;
- FAA or local public-safety authority when an aviation-safety issue is involved.

Do not investigate a suspected illegal source by trespassing, following people, transmitting test signals at them, or attempting to disable equipment.

---

## Survey report template

```markdown
# UAS Spectrum Survey Report

## Purpose and scope
## Site authorization
## Date, time, location, and conditions
## Aircraft and configuration
## Instrumentation and calibration
## Measurement settings
## Ambient baseline
## Own-system state tests
## Observations
## Reproduced self-interference
## Unresolved external observations
## Operational decision
## Safety actions
## Data handling and retention
## Reviewer
## Attachments and raw-data hashes
```

---

## Official source record

| Authority | What it supports | Verified |
|---|---|---:|
| [NTIA — Regulating the Use of Spectrum](https://www.ntia.gov/book-page/regulating-use-spectrum) | Interference principles, coordination, and regulated spectrum use | 2026-07-31 |
| [NTIA/ITS — Best Practices for Radio Propagation Measurements](https://www.ntia.gov/blog/its-releases-best-practices-handbook-propagation-measurements) | Calibration, documentation, verification, and measurement uncertainty | 2026-07-31 |
| [GPS.gov — Spectrum and Interference Issues](https://www.gps.gov/spectrum-interference-issues) | GPS interference sources and reporting channels | 2026-07-31 |
| [GPS.gov — Information About GPS Jamming](https://www.gps.gov/information-about-gps-jamming) | Jammer prohibition, troubleshooting, and FCC reporting | 2026-07-31 |
| [FCC Consumer Complaint Center](https://consumercomplaints.fcc.gov/) | Interference complaint intake | 2026-07-31 |
| [FCC Emergency Complaints](https://consumercomplaints.fcc.gov/hc/en-us/articles/115000914506-Emergency-Complaints) | Routing for consumer and public-safety interference | 2026-07-31 |

Questions, corrections, or privacy concerns: [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).
