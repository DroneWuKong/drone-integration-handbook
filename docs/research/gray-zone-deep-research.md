# Gray Zone Deep Research Report — PIE Integration
## Status: ENRICHED (April 4, 2026 — Session 2)
## Last Updated: 2026-04-04T22:00:00Z

---

## Executive Summary

A new class of drone companies has emerged between trusted Blue UAS platforms and banned adversary technology, exploiting regulatory gaps to sell Chinese-derived drones to U.S. government and consumer buyers. PIE tracks 4 gray zone entities across 6 risk dimensions with 47 source URLs, 16 follow-up intelligence flags, and cross-cutting intel on the DJI v. FCC Ninth Circuit litigation.

The December 22, 2025 FCC Covered List expansion fundamentally changed the landscape: it banned ALL foreign-produced UAS and UAS critical components, not just DJI/Autel. This swept in every shell company simultaneously. The Jan 1, 2027 "firmware cliff" creates a triple deadline where exemptions, firmware waivers, and conditional approvals all expire.

## Entities Tracked

### 1. Anzu Robotics (CRITICAL — 0.782)
- **Status:** Product discontinued Feb 10, 2026. Active TX AG litigation. Zero products. No successor timeline.
- **Structure:** Anzu Robotics LLC (DE) → XTI Drones Holdings → XTI Aerospace (NASDAQ: XTIA)
- **Key Finding:** DJI Mavic 3 licensed derivative. DJI retains cryptographic signing keys. ~50% Chinese components.
- **Litigation:** TX AG Paxton filed Feb 18, 2026 in Collin County. 7 counts DTPA. No response filed 45+ days. Part of 4-lawsuit CCP campaign (TP-Link, Lorex, Temu).
- **Financial:** XTIA at ~$2.10, market cap ~$89M. TTM revenue $3.2M, net loss -$35.6M. $20M JPMorgan ABL facility. 47 employees. Next earnings May 19, 2026.
- **Sources:** 16 verified URLs

### 2. Cogito Tech / SPECTA (HIGH — 0.537)
- **Status:** Subject to FCC Covered List. Existing inventory at retail. No pathway to new products.
- **Structure:** COGITO TECH COMPANY LIMITED (Hong Kong)
- **Key Finding:** DJI Air 3 clone. Identical PCBs. OcuSync frequency fingerprint confirmed by Konrad Iturbe.
- **Sources:** 8 verified URLs

### 3. SkyRover / Knowact (CRITICAL — 0.850)
- **Status:** Most active remaining gray zone entity. Still selling S1 ($359) and X1 ($599) inventory.
- **Structure:** SZ Knowact Robot Technology Co., Ltd (Shenzhen, Nanshan District — same as DJI HQ) → Skyhigh Tech LLC (controllers) → SkyRover brand
- **Key Finding:** DJI Mini 4 Pro clone. 9+ shell entities identified. DJI logos in FCC antenna diagrams. March 2026: announced vague 5-year "explore" US manufacturing plan.
- **Corporate Opacity:** Website has zero corporate info — no parent company, no HQ, no country of origin.
- **Sources:** 13 verified URLs

### 4. Autel Robotics (HIGH — 0.624)
- **Status:** Named in Section 1709 FY2025 NDAA alongside DJI. Entity-specific restrictions that extend to US production, JVs, licensing.
- **Structure:** Autel Robotics Co., Ltd (Shenzhen) → Autel Robotics USA
- **Key Finding:** Unlike generic foreign UAS ban, Autel's Section 1709 restrictions cannot be circumvented by onshoring. FCC revoked certain pre-ban authorizations Jan 2026.
- **Sources:** 10 verified URLs

## Cross-Cutting Intelligence

### DJI v. FCC — Ninth Circuit (Case 26-1029)
- Filed Feb 20, 2026. DJI argues FCC exceeded authority, violated Fifth Amendment, never identified specific threat.
- FCC moved to dismiss on ripeness grounds (bureau-level action, not final Commission order). Motion pending.
- DJI also filed motion for reconsideration at FCC. Oppositions and replies invited.
- Analysis: Ninth Circuit unlikely to overturn outright. More likely to require better procedures or get resolved via trade negotiations.

### FCC Covered List Framework (as of April 2026)
- Effective Dec 22, 2025: ALL foreign-produced UAS and UAS critical components on Covered List
- Exemptions (expire Jan 1, 2027): Blue UAS Cleared List, Buy American standard
- Conditional Approvals: 4 granted (non-DJI/Autel), valid until Dec 31, 2026
- FCC has retroactive revocation authority (Oct 2025 vote)
- OET blanket waiver for minor changes to previously authorized Covered List UAS

### State-Level Enforcement
- Texas: 4 CCP lawsuits Feb 2026. Gov Abbott expanded Prohibited Technologies List.
- Florida: Chinese drone ban enforced for state agencies.
- New York: S.3259 passed (7th state-level ban).
- Nevada: Drone restriction enacted.

### January 1, 2027 Firmware Cliff
Three deadlines converge:
1. Firmware waiver for DJI/Autel/covered entities expires
2. Blue UAS exemption expires
3. 65% domestic content exemption expires
This creates maximum disruption unless policy framework is extended or replaced.

### Shell Company Network (Fully Mapped)
12+ entities identified by Konrad Iturbe's OcuSync fingerprinting system:
Anzu, SkyRover/Knowact, Cogito/SPECTA, Skyany, Spatial Hover, Jovistar, Fikaxo, Lyno Dynamics, WaveGo Tech, Skyhigh Tech, Xtra, Talos
Tracking repo: https://github.com/KonradIT/dji-front-companies

---

## Data Quality Notes
- All source URLs verified April 4, 2026
- entities.json now includes `source_urls` and `latest_developments` per entity
- Cross-cutting intel stored at document level in entities.json
- 16 follow-up flags in followup_flags.json
- Risk scores in risk_scores.json (6-dimension model)
