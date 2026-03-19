# Thermal / IR Cameras — What Sees in the Dark

> **Part 6 — Components**
> Thermal imaging for ISR, inspection, SAR, and defense.
> Who makes the sensors, what the specs mean, and what's NDAA compliant.

---

## Why This Matters

Thermal cameras detect infrared radiation emitted by objects based
on their temperature. They see heat, not light. This makes them
essential for night operations, search and rescue, industrial
inspection, firefighting, perimeter security, and target acquisition.

Every enterprise and tactical drone platform either ships with
thermal or supports it as a payload option. The parts-db had zero
thermal camera entries. This chapter fixes that.

---

## The Market Structure

Teledyne FLIR dominates. They are the world's largest volume
manufacturer of ITAR-free, NDAA-compliant infrared sensor and
camera modules, delivering thousands of units daily. Their product
line spans from the $200 Lepton OEM module to six-figure defense
gimbals. Most NDAA-compliant drone platforms use FLIR sensors
(Teal 2 ships with Hadron 640R, Skydio uses Boson+).

The rest of the market breaks down by tier:
- **Defense gimbals:** L3Harris WESCAM, Leonardo DRS, Elbit, Rafael
- **OEM modules:** FLIR Boson/Lepton, RPX Technologies EmbIR
- **Drone-specific cameras:** Workswell (EU), DJI Zenmuse (China)
- **Microbolometer cores:** Lynred (France), Guide Sensmart (China)

---

## Teledyne FLIR — The Reference Standard

### Lepton Family (Entry/OEM)

| Product | Resolution | Type | Key Feature | ITAR | NDAA |
|---------|-----------|------|-------------|------|------|
| Lepton 3.5 | 160×120 | LWIR micro-thermal | Radiometric, smallest thermal module | Free | Compliant |
| **Lepton XDS** (NEW Feb 2026) | 160×120 thermal + 5 MP visible | Dual thermal-visible | MSX edge fusion, Prism ISP, RJPEG output | Free | Compliant |

The Lepton XDS is significant — it's the first dual-sensor module
with MSX (visible edges embossed onto thermal imagery) in a
compact OEM form factor. USB output, SWaP-optimized. Classified
6a993.b.4.b — broadly exportable.

6+ million Leptons shipped. Proven supply chain at scale.

### Boson / Boson+ (Mid-Tier)

| Product | Resolution | Pixel Pitch | Key Feature | ITAR | NDAA |
|---------|-----------|-------------|-------------|------|------|
| Boson 640 | 640×512 | 12µm | LWIR, XIR video processing | Free | Compliant |
| Boson+ 640 | 640×512 | 12µm | Enhanced sensitivity, HDR | Free | Compliant |
| Boson 320 | 320×256 | 12µm | Budget 640-class alternative | Free | Compliant |

Boson is the workhorse thermal core for UAS payloads. The 640×512
resolution at 12µm pixel pitch delivers detail sufficient for most
ISR and inspection applications. Used in dozens of drone platforms.

### Hadron 640 Series (Integrated Dual-Sensor)

| Detail | Value |
|--------|-------|
| Thermal | 640×512 Boson or Boson+ (radiometric) |
| Visible | 64 MP |
| Design | Dual-sensor module, SWaP-optimized |
| Software | Prism AI detection/tracking/classification |
| Compatibility | NVIDIA, Qualcomm drivers |
| ITAR | Free |
| NDAA | Compliant |
| Used In | Teal 2 (Hadron 640R) |

Hadron is the go-to for OEMs who want thermal + visible in a single
module without building their own dual-sensor payload.

### Vue Series (Complete Drone Cameras)

- **Vue TZ20-R** — Dual Boson zoom (20×), radiometric. Ready to mount.
- **Vue Pro R** — 640×512 or 336×256, radiometric. Legacy but widely deployed.

### Defense / Long-Range ISR

- **Neutrino SX8 ISR 50-1000** (announced Feb 2026) — Vehicle detection
  at 34 km, identification at 20 km. Longest-range ISR thermal on market.
  Defense-tier pricing and availability.

---

## RPX Technologies — Blue UAS Framework

| Detail | Value |
|--------|-------|
| HQ | USA |
| Blue UAS | Framework component |
| Product | EmbIR UAV-640 thermal camera |
| Resolution | 640×512 |
| Key Feature | Blue UAS listed, compact, drone-optimized |
| Models | A (wide), B, C (13.6mm), D (16.7mm), E (42mm telephoto) |
| Weight | 20g (Model A) to 118g (Model E) |

RPX is one of the few thermal camera manufacturers directly on
the Blue UAS Framework component list. Compact, lightweight
modules designed specifically for small UAS integration.

---

## Workswell — EU-Made, Drone-Specific

Czech manufacturer building thermal cameras purpose-designed for
drone use. Non-Chinese manufacturing. Full SDK and MAVLink
integration. Compatible with DJI Matrice 300/350 and any platform
via standard interfaces.

### Product Line

| Product | Thermal | Visible | Weight | Key Feature |
|---------|---------|---------|--------|-------------|
| WIRIS Pro | 640×512 (Super-Res 1266×1010) | FHD 10× optical zoom | <430g | Radiometric, SSD recording, 50 mK (30 mK option) |
| WIRIS Pro SC | 640×512 (Super-Res 1266×1010) | FHD 10× optical zoom | <450g | Scientific-grade 30 mK, interchangeable lenses |
| WIRIS Enterprise | 640×512 (Super-Res 1266×1010) | 16 MP + rangefinder | — | Multi-sensor, IP66, thermal+RGB+rangefinder |
| WIRIS Enterprise G | — | — | — | Gas detection variant |
| WIRIS Agro | 640×512 | — | — | Agriculture/NDVI water stress mapping |
| GIS-320 | Specialized | — | — | Gas leak detection, 400+ gases detectable |

**All models:** Temp range up to 1,500°C, radiometric video,
individually calibrated with certificate, WIRIS OS, SDK available
(Data SDK + Stream SDK + MAVLink interface + CANbus/UART SDK).

### Why Workswell Matters

EU-manufactured thermal cameras for drones are rare. Most European
brands resell Chinese-made sensors. Workswell manufactures in
Prague and provides full SDK access — making them the primary
EU-sourced alternative to FLIR for operators who need non-Chinese,
non-US thermal imaging.

---

## Israeli Manufacturers (Defense Tier)

### Elbit Systems

Mini-POP, Micro-POP — defense-grade EO/IR payloads for tactical
UAS. Stabilized gimbals with thermal, visible, and laser designator.
Widely deployed on Israeli and export military platforms.

### Controp

iSky series — stabilized EO/IR payloads. Focus on small UAS and
maritime applications. Israeli defense export controlled.

### Rafael

TOPLITE EOS — heritage from Litening targeting pod. Defense-tier
multi-sensor gimbals. Not available for commercial purchase.

Israeli thermal/EO payloads are among the most combat-proven in
the world but are typically available only through government-to-
government sales or defense export channels.

---

## Microbolometer Core Manufacturers

Most thermal cameras use uncooled microbolometer detector cores
from a handful of OEMs. Understanding this layer matters because
the core determines the fundamental capability of any camera
built on it.

| Manufacturer | HQ | Status | Notes |
|-------------|-----|--------|-------|
| Lynred (formerly ULIS) | Grenoble, France | EU-made | Major European IR detector OEM. Supplies cores to many camera manufacturers including European defense |
| Guide Sensmart | Wuhan, China | NOT NDAA | Chinese OEM cores. Aggressive pricing. Used in many third-party thermal cameras |
| InfiRay | Yantai, China | NOT NDAA | Competing Chinese OEM modules |
| Teledyne FLIR | USA | NDAA compliant | Vertically integrated — makes own cores for Boson/Lepton |

**Lynred** is the key non-Chinese, non-US microbolometer source.
Any European defense program requiring thermal imaging without
US ITAR or Chinese supply chain dependency will likely use Lynred
cores.

---

## DJI Thermal (Context — NOT NDAA)

DJI's Zenmuse H20T and H30T are the best-integrated drone thermal
cameras on the market — quad-sensor (wide, zoom, thermal, laser
rangefinder) with seamless software integration. The H30T's thermal
is 640×512 with 1280×1024 super-resolution.

**NOT NDAA compliant.** Excluded from any government or defense
use. But for commercial operators without compliance requirements,
DJI thermal payloads offer the best out-of-box experience.

---

## Choosing Thermal for Your Drone

1. **Resolution matters less than you think.** 640×512 is the
   sweet spot. 320×256 is adequate for many applications. 160×120
   (Lepton) works for detection but not identification.

2. **Radiometric vs. non-radiometric.** Radiometric cameras
   measure actual temperatures (critical for inspection). Non-
   radiometric only show relative temperature differences (adequate
   for SAR and ISR).

3. **NETD (sensitivity) matters more than resolution.** ≤50 mK
   is standard. ≤30 mK is scientific-grade. Lower NETD = better
   ability to see small temperature differences.

4. **Integration complexity.** FLIR modules have the best driver
   support (NVIDIA, Qualcomm). Workswell provides full SDK. DJI
   is plug-and-play but closed ecosystem. Israeli payloads require
   defense procurement channels.

5. **ITAR vs. ITAR-free.** FLIR OEM modules are ITAR-free (EAR
   6a993.b.4.b). Defense gimbals from L3Harris, Elbit, Rafael are
   typically ITAR-controlled and require export licenses.

---

*Last updated: March 2026*
