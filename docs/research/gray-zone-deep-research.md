# Gray Zone Deep Research Report — PIE Integration
## Status: INTEGRATED (April 4, 2026)
## Last Updated: 2026-04-04T14:30:00Z

---

## Executive Summary

A new class of drone companies has emerged between trusted Blue UAS platforms and banned adversary technology, exploiting regulatory gaps to sell Chinese-derived drones to U.S. government buyers. PIE tracks 4 gray zone entities across 6 risk dimensions with 35 source URLs and 8 follow-up intelligence flags.

## Entities Tracked

### 1. Anzu Robotics (CRITICAL — 0.782)
- **Status:** Product discontinued Feb 10, 2026. Active TX AG litigation. Zero products.
- **Structure:** Anzu Robotics LLC → XTI Drones Holdings → XTI Aerospace (NASDAQ: XTIA)
- **Key Finding:** DJI Mavic 3 licensed derivative. DJI retains cryptographic signing keys. ~50% Chinese components.
- **Litigation:** TX AG Paxton filed Feb 18, 2026 in Collin County. 7 counts DTPA. No response filed 45+ days.
- **Financial:** XTI acquired for $3.175M (Anzu) + Drone Nerds. $20M JPMorgan ABL facility Feb 2026. 10-K delayed.
- **Sources:** 15 verified URLs (SEC filings, TX AG petition, FCC filings, news, OSINT)

### 2. Cogito Tech / SPECTA (HIGH — 0.537)
- **Status:** Products still listed on retail. Subject to FCC Covered List.
- **Structure:** COGITO TECH COMPANY LIMITED (Hong Kong)
- **Key Finding:** DJI Air 3 clone. Identical PCBs. OcuSync frequency fingerprint confirmed by Konrad Iturbe.
- **Sources:** 5 verified URLs (FCC filings, OSINT trackers)

### 3. SkyRover / Knowact (CRITICAL — 0.850)
- **Status:** Products still available at retailers. Announced vague US manufacturing "exploration."
- **Structure:** SZ Knowact Robot Technology Co., Ltd (Shenzhen) → multiple FCC filing entities (Skyhigh Tech LLC)
- **Key Finding:** DJI Mini 4 Pro clone. Direct DJI cloud connectivity. 9+ shell companies identified. DJI logos visible in FCC antenna diagrams. WaveGo Tech filing included Knowact documentation.
- **Sources:** 10 verified URLs (FCC filings, DroneXL analysis, OSINT trackers, news)

### 4. Autel Robotics (HIGH — 0.525)
- **Status:** Named entity in FY2025 NDAA Section 1709. FCC authorizations quietly revoked.
- **Structure:** Autel Robotics Co., Ltd (Shenzhen) → US operations
- **Key Finding:** Chinese-owned. Entity List. CITIC Corporation investor (Ministry of Finance). "Little Giant" designation. Unlike generic foreign drone ban, Autel cannot bypass via US manufacturing.
- **Sources:** 5 verified URLs (legal analyses, AUVSI, FCC guidance)

## Regulatory Landscape (as of April 2026)

### FCC Covered List (Dec 22, 2025)
- ALL foreign-produced UAS and UAS critical components added
- DJI + Autel specifically named in Section 1709 NDAA — entity-level ban (cannot bypass via US manufacturing/licensing)
- Blue UAS and "Buy American" exemptions until Jan 1, 2027
- First 4 conditional approvals March 18, 2026 (none Chinese-manufactured)
- FCC quietly revoked certain DJI/Autel authorizations issued just before ban
- FCC Oct 2025 vote granted retroactive revocation authority

### DJI v. FCC (Ninth Circuit Case 26-1029)
- Filed Feb 20, 2026. DJI represented by former Solicitor General
- Argues: exceeded statutory authority, failed procedures, violated Fifth Amendment
- FCC moved to dismiss on ripeness (bureau-level, not final Commission order)
- Also filed motion for reconsideration at FCC
- Timeline: 6-18 months for decision. Likely modified approach rather than clean overturn.

### State-Level Enforcement
- **Florida:** Enforced since April 2023. $200M+ grounded. $25M replacement (12.5%). 2-10x cost increase.
- **New York:** S.3259/A.2237 passed 2025. Aligns with federal Section 889.
- **Nevada:** Banned Chinese drones for agencies Jan 2024.
- **Arkansas:** Enacted restrictions.
- **Texas:** DJI on Prohibited Technologies List. 4 CCP-linked company lawsuits filed Feb 2026.

### FY2026 NDAA ($900B)
- Expands to Chinese ground drones and "clones"
- SAFER SKIES Act: C-UAS authority for state/local law enforcement
- US-Taiwan joint drone co-development mandate by March 2026
- $100K/violation penalties for unauthorized C-UAS

## Shell Company Network (OSINT)
Konrad Iturbe's automated OcuSync frequency detection identified 12+ DJI front companies:
Cogito Tech, Spatial Hover, Lyno Dynamics, Fikaxo, Jovistar, WaveGo Tech, Knowact Robot, Skyhigh Tech, Skyany, Skyrover, and others.

Detection method: DJI OcuSync uses specific frequency pairs (5745.5-5829.5 MHz) that act as unmistakable signatures in FCC filings regardless of corporate branding.

Evidence of coordination: WaveGo/Knowact documentation cross-linked, Fikaxo→Spatial Hover product migration, DJI logos in FCC diagrams.

GitHub tracker: https://github.com/KonradIT/dji-front-companies

## Follow-Up Research Flags
See data/grayzone/followup_flags.json for 8 active intelligence flags with sources.

## Data Files
- `data/grayzone/entities.json` — 4 entities with 35 total source URLs and latest_developments
- `data/grayzone/indicators.json` — 14 OSINT indicators with confidence scores
- `data/grayzone/risk_scores.json` — 6-dimension risk scoring engine output
- `data/grayzone/flags.json` — 36 gray zone flags
- `data/grayzone/followup_flags.json` — 8 follow-up intelligence flags (updated April 4, 2026)
