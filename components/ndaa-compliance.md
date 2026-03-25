# NDAA Compliance â Drones in US Government Work

> If you're doing government work with drones, NDAA compliance is not
> optional. It's not a checkbox. It affects which hardware you can buy,
> which vendors you can use, and which components you can integrate.

---

## The Regulatory Framework

### NDAA Â§848 â The Core Prohibition

Section 848 of the FY2020 National Defense Authorization Act prohibits
Department of Defense procurement of covered foreign-manufactured unmanned
aircraft systems and related components.

**Covered entities (as of March 2026):**
- DJI (Da-Jiang Innovations)
- Autel Robotics
- Dahua Technology
- Hikvision
- Huawei
- ZTE
- Hytera Communications

### NDAA Â§817 â Component-Level Requirements

**11 critical component categories:**
1. Flight controllers
2. Ground control systems
3. Radio communication systems
4. Cameras
5. Gimbals
6. Data transmission/storage systems
7. Operating software
8. Obstacle avoidance systems
9. Sensors
10. Batteries
11. Propulsion systems

### American Security Drone Act (ASDA)

Extends Â§848 to all federal agencies, not just DOD procurement.

### Executive Order 14307

Addresses national security risks from connected vehicle technology.

---

## Blue UAS Program

25+ platforms cleared as of March 2026.

| Platform | Origin | Specialty |
|----------|--------|-----------|
| Skydio X10 | USA | AI autonomous |
| Parrot ANAFI USA | France | Encrypted data |
| Censys Technologies | USA | Fixed-wing BVLOS |
| Impossible Aerospace US-1 | USA | Long endurance |
| Teal Golden Eagle | USA | Defense-focused |

**Blue UAS cleared does not mean automatically NDAA compliant.** Component-level compliance (Â§817) still applies to modifications.

---

## Country of Origin

The test is not where it was assembled but whether the entity is Chinese-owned, Chinese-controlled, or subject to Chinese government influence.

Non-covered origins: Croatia, France, Israel, UK, Germany, most EU, Canada, Australia.

**Orqa - Croatian Pathway:** Not a covered entity. Needs Blue UAS evaluation or program-specific approval for DOD use. FOCI test may apply.

---

## Practical Checklist

```
â¡ Platform not from covered entity (Â§848)
â¡ All 11 components from non-covered entities (Â§817)
â¡ FCC Covered List check for comms hardware
â¡ ASDA applicability (federal agency involved?)
â¡ Blue UAS clearance or program-specific approval
â¡ SAM.gov registration
â DD Form 2345 for ITAR-controlled data
â Document country of origin for all components
```

---

## Common Mistakes

**"It's not a DJI drone, just a DJI camera"** - Wrong. Â§817 covers components regardless of platform.

**"We bought it from a US distributor"** - Irelevant. Origin is the manufacturer.

**"NDAA only applies to DOD"** - ASDA extended it to all federal agencies.

---

## Related

- [Orqa Hardware Guide](orqa-hardware-guide.md)
- [RF Detection Hardware](rf-detection-hardware.md)
- [Forge Compliance Dashboard](https://forgeprole.netlify.app/compliance/)
