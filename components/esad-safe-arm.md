# Electronic Safe-and-Arm Devices (ESAD)

> **Forge cross-reference:** 12 entries in `esad` category  
> **Related handbook chapters:** Counter-UAS, Electronic Warfare

## What ESADs Do

An Electronic Safe-and-Arm Device is a safety-critical component in munition systems that prevents unintended detonation during handling, transport, and launch, then arms the warhead when commanded during the terminal phase of flight. ESADs are the bridge between a drone platform and an explosive payload — they ensure the weapon is safe until it is supposed to be dangerous.

This is included in the Forge database because the proliferation of FPV strike drones and loitering munitions has created a new market for ESAD components designed for small UAS form factors, distinct from the legacy missile and bomb fuze market.

## The Safety Architecture

MIL-STD-1316 defines the requirements for fuze safety in US munitions. The core principle is multiple independent safety inhibits — at least two physically distinct mechanisms must prevent firing, and they must be removed in sequence by deliberate operator action, not by environmental conditions (vibration, RF, temperature).

Modern ESADs implement this with:

- **Electrical isolation** — The initiator is physically disconnected from the firing circuit until the arm command is received
- **Logic gates** — Multiple independent enable signals must be present simultaneously (arm command, environment sensing, timing)
- **LEEFI (Laser Energy Enhanced Firing Initiator)** — Uses laser light through fiber optic to fire the initiator, providing inherent electrical isolation from stray RF and EMI. This is critical for drones operating in dense RF environments where traditional electrical initiators could be susceptible to unintended firing from strong electromagnetic fields

## The Landscape

### US Manufacturers

- **Kraken Kinetics** — US-manufactured ESAD specifically designed for FPV strike drones and loitering munitions. Multiple safety inhibits with LEEFI technology. Represents the new generation of ESAD designed for the small UAS form factor from the ground up rather than adapted from larger munition programs.
- **EBAD (Ensign-Bickford Aerospace & Defense)** — Heritage initiator and safe-arm device manufacturer. Products include NSI (NASA Standard Initiator) derivatives. Decades of experience across missile and munition programs.
- **PacSci EMC (Pacific Scientific)** — Major US manufacturer of energetic devices. MIL-STD-1316 compliant across multiple defense prime contractor programs. Part of Fortive Corporation.
- **Excelitas Technologies** — Produces both the Blue Chip LEEFI initiator family and complete ESAD modules integrating initiator, safety logic, and arming sequences. The LEEFI technology is their key differentiator.
- **L3Harris Technologies** — Defense-grade safe-and-arm systems with heritage across numerous US munition programs. Full MIL-STD-1316 compliance.
- **Day & Zimmermann Munitions** — Micro-miniature Electronic Safe, Arm and Fire (ESAF) devices for gun-launched weapons. Shock-hardened designs proven to survive high-G launch environments.

### Allied Nation Manufacturers

- **GATE Technologies (Israel)** — ESAD for Israeli defense UAS and munition programs. Part of Israel's indigenous precision munition supply chain.
- **XTEND (Israel)** — ESAD fuse board designed for integration into FPV and loitering munition platforms. Compact form factor for retrofitting existing drone airframes being converted to strike capability.
- **EDGE Group (UAE)** — ESAD-50 from the Abu Dhabi defense conglomerate. Part of UAE's growing indigenous munition electronics capability.
- **Chemring Group (UK)** — UK defense energetics company with heritage in NATO munition programs. Part of UK's sovereign ordnance supply chain.
- **Junghans Defence / Diehl Defence (Germany)** — German precision fuze and ESAD manufacturer. Part of the Diehl Defence Group producing electronic and mechanical fuzes for NATO programs.

## Relevance to Drone Integration

ESADs are not a typical "drone component" in the way a flight controller or ESC is. They appear in the Forge database because:

1. FPV strike drones are the fastest-growing UAS category in active conflict zones
2. The conversion of commercial FPV platforms to strike capability requires ESAD integration as the critical safety layer
3. Defense procurement programs (Drone Dominance, Replicator) are scaling FPV production and need ESAD supply chains to match
4. NDAA compliance applies to ESAD components just as it does to avionics — US programs cannot use Chinese-origin safety devices

This chapter documents the supply landscape for awareness and procurement planning. ESAD integration requires ordnance engineering expertise and is subject to ITAR, EAR, and munition-specific regulations.
