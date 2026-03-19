# Batteries & Power Systems — The Weight You Carry

> **Part 6 — Components**
> Batteries define flight time, payload capacity, and increasingly,
> procurement eligibility. The NDAA battery ban is coming.

---

## The Approaching Deadline

**NDAA FY2026 prohibits DoD purchase of batteries for weapons and
support systems from foreign entities of concern (China, Russia)
effective January 1, 2028.** This creates an 18-month window where
the entire defense UAS industry must reshore its battery supply chain.

Most drone batteries today use Chinese cells — even packs assembled
in the US typically contain CATL, EVE, or other Chinese cells.
The 2028 deadline will force a transition to allied-nation cell
manufacturers. Understanding who makes cells vs. who assembles
packs is critical.

---

## Cell Manufacturers vs. Pack Assemblers

A "drone battery" is a pack of individual cells wired together
with a balance connector and protection circuit. The cells inside
determine energy density, discharge rate, and cycle life. The pack
integrator adds the BMS, connector, and housing.

Most operators buy packs (Tattu, CNHL, GNB). But the NDAA question
is about the cells inside, not the label on the shrink wrap.

---

## Cell Manufacturers — The Supply Chain Layer

### Amprius Technologies — The NDAA Battery Leader

| Detail | Value |
|--------|-------|
| HQ | Fremont, CA, USA |
| NYSE | AMPX |
| NDAA | Compliant (working with DIU on all 11 cell components) |
| Technology | Silicon anode lithium-ion (100% silicon anode — only commercial source) |
| SiMaxx | **520 Wh/kg**, 1,300 Wh/L (CES 2026 Best of Innovation — 2× conventional) |
| SiCore | **450 Wh/kg**, 1,150 Wh/L, commercially available in volume |
| SA128 Cell | 21700 cylindrical, 6.8 Ah, 320 Wh/kg (Nanotech US production) |
| Fast Charge | 0–80% in under 6 minutes (third-party validated) |
| Revenue | $73M (2025, +202% YoY), guiding $125–135M for 2026 |
| Profitability | First positive adjusted EBITDA Q4 2025 |
| DIU Contracts | $10.5M + $1.5M |
| Production | 2+ GWh capacity: Korea Battery Alliance + Nanotech Energy (first US mfg partner, Feb 2026) |
| Customers | AeroVironment, L3Harris, Teledyne FLIR, BAE Systems, Nokia, ESAero, AALTO/Airbus (67-day stratospheric flight) |

Amprius has near-monopoly positioning on NDAA-compliant high-
performance UAS cells through 2028. Their silicon anode technology
delivers 2× the energy density of conventional lithium-ion — same
flight time at half the battery weight, or double the flight time
at the same weight. The Nanotech Energy partnership (Feb 2026)
establishes the first US-based production of Amprius cells,
critical for NDAA compliance ahead of the Jan 2028 deadline.

### American Lithium Energy (ALE) — SafeCore Safety Pioneer

| Detail | Value |
|--------|-------|
| HQ | Vista, CA, USA |
| NDAA | Compliant — designed and manufactured in USA |
| Technology | Silicon anode lithium-ion with SafeCore+ and ZeroVolt |
| Energy Density | 400 Wh/kg shipping at MW scale |
| Charge Rate | 5C–10C fast charge |
| Operating Temp | -40°C to +70°C |
| Safety | SafeCore+™ prevents thermal runaway via internal electrode delamination |
| ZeroVolt™ | Cells can be shipped and repeatedly discharged to 0V without damage |
| Cycle Life | 15,000+ cycles validated in space applications |
| Applications | Defense (battlefield-tested), aerospace (space-proven), UAV, eVTOL |
| SBIR | Joint work with Pacific Northwest National Laboratory on non-flammable electrolytes |

ALE's key differentiator is safety. SafeCore+ is a patented internal
safety layer that self-decomposes under abuse conditions to interrupt
current flow — preventing thermal runaway at the electrode level,
not just with external protection circuits. This reduces packaging
weight (no bulky fireproofing needed) and passes nail penetration
and overcharge abuse tests. ZeroVolt technology allows cells to be
safely shipped and stored fully discharged — a significant logistics
advantage for military supply chains.

At 400 Wh/kg shipping at scale, ALE bridges the gap between
conventional Li-ion (~260 Wh/kg) and Amprius SiMaxx (520 Wh/kg),
with a stronger safety story than either.

### Wake Energy — US Pack Assembly at Scale

| Detail | Value |
|--------|-------|
| HQ | Los Angeles, CA, USA |
| NDAA | Compliant — assembled in America |
| Compliance | UN38.3 certified |
| Product | THOR 6030 (6S3P, ~324 Wh, 15 Ah, Molicel P50B/P45B cells) |
| Manufacturing | Hundreds of packs per week, CNC micro TIG welding |
| Testing | MIL-STD-810H 516.8 transit drop (5 ft), 65A continuous thermal testing |
| Cells | Molicel P50B / P45B (Taiwanese — non-Chinese) |
| Formats | Custom configurable for FPV, UAS, robotics |

Wake Energy fills a critical gap: US-based pack assembly using
non-Chinese cells (Molicel/Taiwan) at production scale. They don't
make cells — they engineer and assemble packs with quality processes
(CNC welding, pull-tested coupons, individual electrode QA) that
hobby-grade pack assemblers don't match. The THOR 6030 is a
ready-to-buy 6S pack for tactical FPV and UAS applications.

For operators who need NDAA-compliant battery packs without
designing custom solutions, Wake Energy is the most accessible
option — production-ready, tested to military standards, and
shipping now.

### Molicel (Taiwan)

| Detail | Value |
|--------|-------|
| HQ | Taiwan (subsidiary of Taiwan Cement Corp) |
| Key Cells | P42A (21700, 4200mAh, 45A), P50B (21700, 5000mAh, high-power) |
| NDAA | Likely compliant (Taiwanese, NOT Chinese) — verify per program |
| Partners | KULR Technology for K1A drone battery systems |
| Status | Already referenced in AI Wingman Power Systems Architecture doc |

Molicel P42A and P50B are the reference 21700 cells for high-
performance drone applications. Taiwanese manufacturing makes
them the most accessible non-Chinese high-discharge cells.

### Samsung SDI (South Korea)

| Detail | Value |
|--------|-------|
| HQ | South Korea |
| Key Cells | 40T (21700, 4000mAh, 35A), 50E (21700, 5000mAh), 50S (21700, 5000mAh, 25A) |
| NDAA | Allied nation — likely compliant |

### LG Energy Solution (South Korea)

| Detail | Value |
|--------|-------|
| HQ | South Korea |
| Key Cells | M50T (21700, 5000mAh), HG2 (18650, 3000mAh, 20A) |
| NDAA | Allied nation — likely compliant |

### Chinese Cell Manufacturers (Context — NOT NDAA)

- **CATL** — World's largest battery manufacturer. NOT NDAA.
- **EVE Energy** — Major Li-ion cell OEM. NOT NDAA.
- **Most hobby LiPo packs** (Tattu, CNHL, GNB) use Chinese cells.

---

## Battery System Integrators

### KULR Technology

| Detail | Value |
|--------|-------|
| HQ | Houston, TX, USA |
| Product | KULR ONE Air (K1A) — advanced UAS battery system |
| Cells | Amprius SiCore + Molicel P50B |
| Key Feature | Thermal management expertise, standard + custom OEM configs |
| Partners | Hylio (Texas-manufactured ag drone batteries) |
| Production | Volume production Q4 2025 |

KULR is the bridge between cell manufacturers and drone OEMs.
They handle thermal management, BMS design, and pack engineering
so that drone companies don't have to become battery companies.

### Tattu / Gens Ace (Context — NOT NDAA)

In the parts-db for some products. Dominant hobby LiPo brand.
Chinese-manufactured. **NOT NDAA compliant.** Needs compliance
flags added to all existing entries.

---

## LiPo vs. Li-Ion for Drones

| | LiPo | Li-Ion (21700) |
|---|------|---------------|
| Energy Density | ~150-200 Wh/kg | ~200-260 Wh/kg (450+ with Amprius) |
| Discharge Rate | High (75-100C burst) | Moderate (8-15C typical) |
| Cycle Life | 200-300 cycles | 500-1000+ cycles |
| Weight | Heavier for given energy | Lighter per Wh |
| Best For | FPV racing, aggressive flight | Endurance, commercial ops |
| NDAA Risk | Cells almost always Chinese | Allied options exist (Molicel, Samsung, LG) |

The industry is moving from LiPo to 21700 Li-Ion for everything
except extreme-discharge FPV applications. 21700 packs offer
better energy density, longer cycle life, and a path to NDAA
compliance through Molicel/Samsung/LG cells.

---

## The Price Reality

| Cell Source | $/Wh (approx.) | NDAA Status |
|------------|----------------|-------------|
| Chinese LiPo (Tattu, CNHL) | $0.10-0.20 | NOT compliant |
| Chinese Li-Ion (EVE, CATL) | $0.08-0.15 | NOT compliant |
| Korean Li-Ion (Samsung, LG) | $0.15-0.25 | Allied — likely compliant |
| Taiwan Li-Ion (Molicel) | $0.15-0.25 | Likely compliant |
| US Silicon Anode (Amprius) | $0.50-1.00+ | Compliant |

The 2028 NDAA battery deadline will create a 3-5× cost increase
for defense UAS battery systems unless allied-nation (Korea, Taiwan)
cell production scales to meet demand.

---

## Choosing Batteries

1. **Match voltage to your ESCs and motors.** 4S (14.8V nominal)
   is standard for 5" FPV. 6S (22.2V) is standard for larger builds.
   8S and above for heavy-lift.

2. **Capacity determines flight time.** More mAh = more flight time
   but more weight. There's a sweet spot for every airframe.

3. **Discharge rate determines power.** "C rating" = max safe
   current draw as a multiple of capacity. A 1500mAh 100C pack
   can deliver 150A. LiPo C ratings are often inflated by manufacturers.

4. **Storage charge matters.** LiPo storage voltage is 3.8V/cell.
   Never store LiPo at full charge or fully depleted. Storage charge
   the same day you fly.

5. **For NDAA builds:** Molicel P42A/P50B 21700 packs are the
   pragmatic choice today. Amprius SiCore is the premium path
   with 2× energy density. KULR K1A provides engineered pack
   solutions.

---

*Last updated: March 2026*
