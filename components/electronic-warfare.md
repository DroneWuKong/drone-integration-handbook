# Electronic Warfare Systems

> **Forge cross-reference:** 14 entries in `ew_systems` category  
> **Related handbook chapters:** Counter-UAS, Navigation & PNT, Frequency Bands  
> **Handbook Roadmap:** Aligns with planned Chapter 16 (Electronic Warfare Awareness)

## Scope

This chapter covers electronic warfare (EW) hardware tracked in the Forge database — primarily counter-UAS jammers and GNSS protection devices. It is written from the drone operator's perspective: what these systems do, how they affect your platform, and what to know when your drone operates near them.

This is not a guide for building or operating EW systems. It is a guide for understanding the EW environment your drone will encounter.

## How EW Affects Drones

Electronic warfare against drones targets three subsystems:

1. **Command link** — Jamming the RC/C2 frequency forces failsafe (RTL, land, or hover). Effective against manually-piloted platforms; less effective against autonomous platforms with pre-programmed missions.
2. **GNSS** — Jamming removes position data, causing position-hold failures and navigation degradation. Spoofing is worse: it feeds false position data that can redirect or crash the drone without triggering a failsafe.
3. **Video link** — Jamming the FPV downlink blinds the operator but does not directly affect the drone's autonomous capabilities. Less commonly targeted because it does not create an immediate safety effect.

## Counter-UAS EW Systems in the Database

### Handheld Jammers

Directional devices aimed at a target drone. Effective range typically 500m–2km depending on power and antenna gain.

- **DroneShield DroneGun Tactical** — Rifle-form handheld jammer covering common ISM bands (2.4 GHz, 5.8 GHz) plus GNSS frequencies. Directional antennas in a shouldered design. The most recognizable C-UAS jammer in media coverage. Effective against consumer drones; less effective against frequency-hopping military links.
- **DroneShield DroneGun Mk4** — Lighter pistol-grip version with wider environmental operating range. Same principle, smaller package.
- **Flex Force Dronebuster** — The only handheld electronic attack system authorized for DoD use. Compact design, field-proven across multiple theaters. If you are flying near US military installations, this is the device most likely to be pointed at you.
- **NT Service EDM4S SkyWiper** — Ukrainian-manufactured portable EW device. Disrupts both communication and GNSS simultaneously. Battle-tested in the Ukraine conflict.

### Fixed/Vehicle-Mounted Systems

Area-denial systems that protect facilities or convoys.

- **DroneShield DroneSentry** — Integrated detect-and-defeat system combining RF detection, radar, and camera tracking with electronic countermeasures. Deployed at airports, military bases, and critical infrastructure.
- **DroneShield RfPatrol** — Wearable RF detection sensor (not a jammer). Detects drone control signals and alerts the operator. Included here because detection and jamming are typically deployed together.
- **D-Fend Solutions EnforceAir2** — RF cyber takeover system. Unlike jammers, EnforceAir2 does not disrupt the signal — it takes control of the drone's command link and forces a controlled landing. This is significantly more sophisticated than jamming and works against drones that have jam-resistant links.

### GNSS Protection

- **infiniDome GPSdome** — Lightweight GNSS anti-jam module designed for UAS. Fits inline between the GNSS antenna and receiver. Detects and mitigates jamming in real-time. This is a defensive system — it protects your drone's GNSS from attack rather than attacking another drone.
- **Aselsan KORAL** — Turkish-manufactured mobile EW system. Primarily for larger platforms and ground-based defense. Included for awareness of the threat environment.

### Strategic/Theater-Level Systems

These are not C-UAS specific — they are area-denial EW systems that happen to affect drones along with everything else in the electromagnetic spectrum.

- **Raytheon NGJ-MB (Next Generation Jammer Mid-Band)** — Airborne EW pod for fighter aircraft. If operating in a theater where NGJ-equipped aircraft are present, expect degraded or denied GNSS and communications across wide areas.
- **Krasukha-4** — Russian mobile electronic warfare complex. Documented use in Ukraine and Syria. Affects GNSS, radar, and communications over large areas. Relevant for any drone operations in or near conflict zones.
- **Murmansk-BN** — Russian HF jamming system with extreme range (5,000+ km claimed). Primarily targets HF communications but the EW environment it creates affects nearby systems.
- **Pole-21** — Russian GNSS denial system deployed around military installations.
- **GIDS Spider-AD** — Pakistani C-UAS system combining detection, tracking, and electronic countermeasures.

## Operating in EW Environments

### What to Expect

If your drone enters an active EW environment:

- **GNSS degradation** — Position accuracy drops, then position is lost entirely. ArduPilot/PX4 will fall back to non-GPS flight modes if configured. Betaflight does not have this fallback — FPV drones lose GPS rescue and position hold.
- **Link loss** — Failsafe triggers on RC link. If using ELRS, the low-rate fallback may maintain link longer than the jamming expects. Crossfire/Tracer have different resilience profiles.
- **Compass interference** — Strong RF sources can corrupt magnetometer readings, causing toilet-bowl oscillations or fly-aways in GPS-aided modes.

### Defensive Measures

1. **Pre-programmed missions** — Drones executing autonomous waypoint missions are inherently resistant to C2 jamming (they do not need the command link to continue the mission). This is why military doctrine is shifting toward autonomy.
2. **GPS-denied navigation** — See the Navigation & PNT chapter. INS, VIO, and SLAM provide position when GNSS is jammed.
3. **Anti-jam GNSS** — CRPA antennas (Inertial Labs M-AJ-QUATRO) and inline protection modules (infiniDome GPSdome) can maintain GNSS lock through moderate jamming.
4. **Frequency agility** — Links that hop across wide bands (FHSS) are harder to jam than fixed-frequency links. ELRS and MANET radios both use frequency hopping.
5. **Redundant navigation** — Fuse multiple independent sources: GNSS + INS + VIO + barometer. No single point of failure.

## Regulatory and Legal Notes

EW equipment is heavily regulated. In the US, intentionally jamming radio signals violates the Communications Act (47 USC § 333) with limited exceptions for federal agencies. Counter-UAS jammers are only legal for authorized federal entities. Private use of jammers — even to protect your own property from drones — is illegal.

For drone operators, the practical implication is that you will encounter EW effects near military installations, prisons, stadiums (during major events), and critical infrastructure. Plan for link loss and GNSS degradation in these areas even if no TFR or NOTAM explicitly mentions electronic countermeasures.
