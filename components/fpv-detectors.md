# FPV Detectors & RF Detection Hardware

> **Forge cross-reference:** 30 entries in `fpv_detectors` category  
> **Related handbook chapters:** Electronic Warfare, Counter-UAS, ELINT for Drone Operators

## What FPV Detectors Do

FPV detectors are passive RF monitoring devices that detect the presence of FPV drone video and control link transmissions. They answer the question: "Is there a drone operating near me right now?" without requiring active transmission or expensive radar infrastructure.

The use cases divide into two groups:

**Operator use:** Frequency planning, channel conflict detection, and pre-flight spectrum checks. A pilot at a race event uses an RF detector to see which channels are already in use before powering up.

**Security/counter-UAS use:** Perimeter monitoring to detect unauthorized drone activity. A security guard carries a handheld detector to identify when someone is flying an FPV drone near a facility. The detector identifies the transmission without needing to locate or interdict the drone.

FPV detectors are a component of a C-UAS stack — they provide detection but not identification, geolocation, or interdiction. See `components/counter-uas.md` for the full counter-drone picture.

## Detection Targets

FPV detectors target the RF signatures of:

**Analog video (5.8GHz):** The 5.725–5.875GHz band. FM modulated video signal. Very easy to detect — high power (25–600mW), always-on transmission. Characteristic bandwidth of 20–30MHz. Most legacy FPV systems.

**Digital video (2.4/5.8GHz):** DJI O3/O4, Walksnail Avatar, HDZero all use modulated digital signals. Harder to detect than analog — more burst-like, lower power, spread-spectrum. Requires dedicated digital detection signatures.

**Control links (900MHz/2.4GHz):** ELRS, Crossfire, FrSky. Frequency-hopping spread spectrum. Significantly harder to detect than video — designed to be RF-resilient. Specialist detectors can identify FHSS patterns.

**DJI OcuSync/DragonFly:** DJI's proprietary control+video links. Specific RF signatures that some commercial detectors include in their signature libraries.

## Product Categories

### Handheld RF Detectors (SpyFinder, RF Scout)
Simple wide-spectrum RF detectors that alert when they detect RF energy above a threshold. Not FPV-specific — they detect any RF source (WiFi, cellular, RF bugs, FPV). Very inexpensive ($30–150). High false-positive rate in RF-dense environments. Directional variants point toward the signal source.

**Use case:** Quick "is there any FPV transmission here" check. Not suitable for professional security applications.

### FPV-Specific Spectrum Analyzers (Veyron ISDS, RF Explorer)
Portable spectrum analyzers that display a real-time spectrum sweep across FPV bands. The operator can see the 5.8GHz spectrum and identify occupied channels. Some include frequency identification libraries that match observed signals to known systems.

**RF Explorer:** The de facto standard. Compact USB-connected spectrum analyzer, ~$130–200 depending on frequency range. RFExplorer software shows waterfall displays. Used by race event organizers, frequency coordinators, and operators doing pre-flight checks.

**ISDS204B:** 2.4GHz + 5.8GHz dual-band portable analyzer. Standalone operation (no laptop required). Popular for field use.

### Professional RF Monitoring (DJI AeroScope compatible, DroneTracker)
Commercial counter-UAS platforms that include passive RF monitoring as one layer of detection. DJI AeroScope listens for DJI's OcuSync broadcast and extracts drone ID, GPS position, and operator location from the signal — a remote ID function before Remote ID was regulated.

**Limitation:** AeroScope only covers DJI platforms broadcasting over DJI's protocol. Custom FPV drones using ELRS/Crossfire are invisible to it.

### SDR-Based Detection (RTL-SDR + Software)
Software-Defined Radio dongles ($25–50) combined with open-source software (SDR#, GQRX, DragonOS) can perform spectrum analysis across virtually any frequency band. With appropriate antennas and signal processing software, an experienced operator can detect and classify most FPV transmissions.

**Ceiling:** SDR-based detection requires expertise to use effectively. The hardware is cheap; the knowledge isn't.

## NDAA Status

FPV detectors are primarily passive consumer electronics. Most are either US-manufactured or European. The Chinese presence is limited compared to other FPV categories. Specific high-end professional detection systems (DJI AeroScope) are Chinese but used in specific counter-UAS contexts where Chinese-manufactured equipment may be excluded — verify per program.

## Integration in Operations

### Pre-Flight Frequency Check Protocol
1. Power on RF Explorer or equivalent before powering any drone
2. Scan 5.725–5.875GHz and 2.400–2.485GHz
3. Identify occupied channels — look for peaks above noise floor
4. Select channels with cleanest spectrum (lowest noise floor)
5. Document selected channels for the flight crew

### Security Monitoring Deployment
For perimeter RF monitoring:
- Mount multiple antennas at elevated positions around the perimeter
- Use spectrum analyzers with logging capability for post-event review
- Establish baseline spectrum (what normal RF looks like) before monitoring
- Set threshold alerts for anomalous 5.8GHz energy
- Integrate with camera system for visual cuing when RF detected

**Critical limitation:** RF detection alone does not locate a drone. It confirms transmission is occurring in a frequency band consistent with drone operation. Combining with direction-finding antennas or multi-receiver TDOA systems enables geolocation.
