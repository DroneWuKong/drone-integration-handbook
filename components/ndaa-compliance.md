# NDAA Compliance — Drones in US Government Work

> If you're doing government work with drones, NDAA compliance is not
> optional. It's not a checkbox. It affects which hardware you can buy,
> which vendors you can use, and which components you can integrate.

---

## The Regulatory Framework

### NDAA §848 — The Core Prohibition

Section 848 of the FY2020 National Defense Authorization Act prohibits
Department of Defense procurement of covered foreign-manufactured unmanned
aircraft systems and related components.

**Covered entities (as of April 2026):**
- DJI (Da-Jiang Innovations) — also on FCC Covered List
- Autel Robotics — §1709 FY2025 NDAA named entity; FCC Covered List
- SZ DJI Technology Co.
- Dahua Technology
- Hikvision
- Huawei
- ZTE
- Hytera Communications
- Anzu Robotics — DJI-derived, status under active review
- SkyRover / Knowact — gray zone, DJI cloud architecture

### NDAA §817 — Component-Level Requirements

**11 critical component categories — all must be non-covered:**
1. Flight controllers
2. Ground control systems
3. Radio communication systems
4. Cameras
5. Gimbals
6. Data transmission and storage systems
7. Operating software
8. Obstacle avoidance systems
9. Sensors
10. Batteries
11. Propulsion systems

### American Security Drone Act (ASDA)

Extends §848 to **all federal agencies**, not just DoD procurement.
State/local agencies receiving federal grants (DHS BRIC, HMGP, COPS)
are bound when using federal funds.

### FCC Covered List

Separate from NDAA — applies to any communications equipment connected
to US government networks. DJI and Autel are both on this list.
FCC Blue UAS Exemption for existing DJI/Autel fleets **expires January 1, 2027**.
Agencies currently operating under exemption must complete platform
transition or apply for individual exemption before that date.

### NDAA FY2025 §1709

Specifically named Autel Robotics as a covered entity for DoD purposes,
closing a gap where some procurement offices were treating Autel as compliant.

---

## Blue UAS Program

Managed by DCMA (transitioned from DIU, December 2025).
**30+ platforms cleared as of April 2026.**

| Platform | Cleared | Origin | Specialty |
|----------|---------|--------|-----------|
| Skydio X10D | Yes | USA | AI autonomous, FLIR Boson+ |
| Freefly Astro / Astro Map | Yes | USA | PX4, payload-agnostic |
| Teal 2 / Black Widow | Yes | USA | Defense-focused |
| Parrot ANAFI USA | Yes | France | Encrypted data |
| Draganfly Apex / Commander | Yes | Canada | Multi-mission |
| American Robotics Scout | Yes | USA | Autonomous dock system |
| AgEagle eBee VISION / TAC | Yes | USA/Swiss | Fixed-wing BVLOS |
| WingtraOne GEN II | Yes | Switzerland | Survey/mapping |
| Ascent Aerosystems Spirit | Yes | USA | Coaxial BVLOS |
| Red Cat Black Widow | Yes | USA | SRR Tranche 2 |
| Anduril Ghost X | Yes | USA | Lattice AI integration |
| Fat Shark Aura | Yes (Aug 2025) | USA | FPV camera |

**Removed from Blue UAS list (March 2025):** Inspired Flight IF1200A,
Parrot removed temporarily (Parrot ANAFI USA subsequently re-cleared).
Always verify current status at bluelist.dcma.mil before procurement.

**Blue UAS cleared ≠ automatically NDAA compliant.** Component-level
compliance (§817) still applies to modifications and third-party payloads.

---

## Country of Origin

The test is not where it was assembled — it's whether the entity is
Chinese-owned, Chinese-controlled, or subject to Chinese government influence.

**Non-covered origins (generally safe):** Croatia, France, Israel, UK,
Germany, Switzerland, Canada, Australia, Netherlands, Sweden.

**Gray zone:** Companies with Chinese investment, Chinese-born founders,
or manufacturing in China even if HQ is elsewhere. FOCI (Foreign Ownership,
Control, or Influence) test applies for sensitive programs.

**Orqa — Croatian Pathway:** Not a covered entity. Croatian manufacture,
EU supply chain. Needs Blue UAS evaluation or program-specific approval
for DoD use. FOCI test clean. Viable pathway for defense FPV builds.

---

## Practical Procurement Checklist

```
☐ Platform not from covered entity (§848)
☐ All 11 component categories from non-covered entities (§817)
☐ FCC Covered List check for all comms hardware
☐ ASDA applicability (federal agency or federal funds involved?)
☐ Blue UAS clearance OR program-specific approval
☐ NDAA §1709 check (Autel specifically named FY2025)
☐ FCC Blue UAS Exemption status (expires Jan 1, 2027)
☐ SAM.gov / DHS AEL eligibility for grant-funded purchases
☐ DD Form 2345 for ITAR-controlled data/components
☐ Document country of origin for all 11 component categories
```

---

## Common Mistakes

**"It's not a DJI drone, just a DJI camera"** — Wrong. §817 covers
components regardless of platform origin.

**"We bought it from a US distributor"** — Irrelevant. Origin is the
manufacturer, not the reseller.

**"NDAA only applies to DoD"** — ASDA extended it to all federal agencies.
State/local agencies using federal grant funds are also bound.

**"Autel is fine, only DJI is covered"** — Wrong as of FY2025 NDAA §1709.

**"Our DJI fleet has the FCC exemption"** — The exemption expires
January 1, 2027. Begin transition planning now.

**"Anzu Robotics is US-based, so it's compliant"** — Under active review.
Anzu is DJI-derived hardware with US entity status. Do not assume compliant
for federal procurement without independent legal review.

---

## Related

- [Orqa Hardware Guide](orqa-hardware-guide.md)
- [RF Detection Hardware](rf-detection-hardware.md)
- [Forge Compliance Dashboard](https://uas-forge.com/compliance/)
- [DFR Regulatory Brief](../patterns/dfr-regulatory.md)
