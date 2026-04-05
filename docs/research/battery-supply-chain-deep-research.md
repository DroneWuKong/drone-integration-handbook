# Lithium Battery Supply Chain Intelligence for the UAS/Drone Industry

**Deep Research Report — April 2026**
**Source:** Deep research session, 67 sources cited
**PIE Database:** data/battery-supply-chain/cell_manufacturers.json (v2.0)

---

## Executive Summary

China controls over 90% of drone-grade pouch cell production and 70–98% of every upstream battery material, making the entire Western drone industry dependent on a supply chain Beijing has demonstrated willingness to weaponize. The October 2024 Skydio sanctions proved this is not theoretical risk. With NDAA battery procurement bans taking effect in October 2027 and January 2028, Blue UAS manufacturers face a 2–4 year critical gap where compliance mandates exist without sufficient allied supply. The most viable near-term path runs through Molicel (Taiwan) cylindrical cells and Amprius (US) silicon-anode cells, but neither can replace Chinese pouch cells at scale today.

---

## Key Findings

### Three Structural Realities

1. **Molicel is a single point of failure** — the only allied high-drain cylindrical cell source, with the July 2025 Kaohsiung factory fire halving capacity from ~3.3 GWh to ~1.5 GWh. Demand exceeds 2x production.

2. **No non-Chinese pouch cell supply exists at scale** — most multirotor drones (Skydio, DJI-class, military quadrotors) use LiPo pouch cells. Zero commercial-scale US production. 90%+ from Shenzhen/Dongguan/Huizhou.

3. **China controls 70–98% of every upstream battery material** — even "NDAA-compliant" cells carry residual Chinese raw material exposure.

### Supply Chain Weaponization: The Skydio Case

On October 11, 2024, China sanctioned Skydio after the US approved $567M in Taiwan defense assistance. Skydio's sole battery supplier — Dongguan Poweramp (a Japanese TDK subsidiary on Chinese soil) — was ordered to halt all operations. The strategic lesson: **ownership origin ≠ production jurisdiction**. Even Japanese-owned factories are subject to Chinese government orders.

### The Pouch Cell Gap

This is the fundamental unsolved problem. Most multirotors use LiPo pouch cells. The only paths to closing the gap:
- Amprius: pouch cells at pilot scale (<10 MWh/year)
- Badland Batteries: $50M DoD-funded factory in Fargo targeting 2026
- CRG Defense: claims US manufacturing, limited public specs

Timeline to parity: 2029–2030 minimum with dramatically increased investment.

### NDAA Compliance Timeline

| Date | Event |
|------|-------|
| 2020 | FY2020 NDAA Sec 848 — batteries NOT explicitly listed (loophole) |
| Dec 2023 | FY2024 NDAA Sec 154 — names 6 Chinese companies |
| Dec 2025 | FY2026 NDAA — extends to all Foreign Entities of Concern |
| **Oct 1, 2027** | **Sec 154 takes effect — 6 named companies banned** |
| **Jan 1, 2028** | **FEOC ban takes effect — all Chinese battery companies** |

---

## US Cell Manufacturers (NDAA-Compliant)

| Company | Chemistry | Best Cell | Wh/kg | Status |
|---------|-----------|-----------|-------|--------|
| **Amprius** (AMPX) | Si-anode NMC | SA08 pouch | 338–500 | Shipping. $53.3M backlog. |
| **Lyten** | Li-S | Drone pouch | 400 | 3+ hr demo. 0.5–2C only. |
| **American Lithium Energy** | Nano-Si | 18650 4.0Ah | 330 | Shipping. 5M cells/yr. |
| **EaglePicher** | Custom defense | Custom | — | Defense-only. No commercial cells. |
| **CRG Defense** | Li-ion | — | — | US cells/packs/motors. Limited specs. |
| **Enovix** (ENVX) | 3D Si-anode | Defense cell | 341.8 | Korean ops shipping. $100M pipeline. |

## Allied Cell Manufacturers

| Company | Country | Best Drone Cell | Key Spec | Status |
|---------|---------|-----------------|----------|--------|
| **Molicel** | Taiwan | P60C 21700 | 6000mAh/100A/286 Wh/kg | Factory fire halved capacity |
| **Samsung SDI** | S. Korea | 40T 21700 | 4000mAh/35A | Secondary option, inferior to Molicel |
| **Murata** | Japan | VTC6A 18650 | 3000mAh/30A | 18650 only, stock-outs |
| **LG Energy** | S. Korea | M50LT 21700 | 5000mAh/14.4A | Too low-drain for drones |
| **Panasonic** | Japan | NCR21700A | 5000mAh/15A | Too low-drain, Tesla-committed |

## Chinese Manufacturers Tracked

| Company | Key Risk |
|---------|----------|
| **Grepow** (Tattu/Gens Ace) | Dominant LiPo force. 1M Ah/day. Not sanctioned. |
| **EVE Energy** | Named in NDAA Sec 154. DoD ban Oct 2027. |
| **Dongguan Poweramp** (TDK) | Skydio crisis. Canonical weaponization case. |

## White Label Map (14 brands traced)

Most FPV/drone battery brands (Tattu, GNB, DOGCOM, Ovonic, NewBeeDrone, Turnigy, CNHL, Lumenier LiPo, XILO, iFlight/GEPRC/Flywoo/BETAFPV, Thunder Power) trace to Chinese OEM manufacturers, primarily Grepow. DJI batteries source from ATL (TDK) + SunWoda. Skydio pre-sanctions sourced from Dongguan Poweramp (TDK).

Exception: Lumenier NAV Li-ion packs use Molicel cells (confirmed NDAA-compliant).

## Raw Material Chokepoints (11 tracked)

China controls 65–98% of every battery material layer. Top critical dependencies:
- LFP cathode: 98%
- Graphite processing: 95%
- Anode materials: 90%
- Cobalt refining: 80%

## Emerging Technologies (5 assessed)

| Technology | TRL | Drone Fit | China Independence | Timeline |
|-----------|-----|-----------|-------------------|----------|
| **Silicon-anode** | 7–8 | HIGH (5–8C) | Partial | Now (defense) |
| **Li-S** | 5–6 | Fixed-wing only | Complete | 2025–2028 |
| **Solid-state** | 4–6 | TBD | TBD | 2028–2030 |
| **H2 fuel cells** | 7–8 | Large only | High | Available now |
| **Na-ion** | 3–8 | Not viable | Theoretical | N/A |

## Cost Analysis

- NDAA cylindrical vs Chinese LiPo: **3–6x premium**
- US pouch vs Chinese pouch: **10–20x at pilot scale**
- Molicel 6S2P pack (cells only): $60–72 vs Chinese LiPo equivalent: $15–25

---

*Data structured for PIE database at data/battery-supply-chain/cell_manufacturers.json*
*67 sources cited in structured JSON*
