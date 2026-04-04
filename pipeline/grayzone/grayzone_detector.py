#!/usr/bin/env python3
"""
PIE Gray Zone Detector — identifies non-Blue UAS platforms marketing
to government/public safety buyers while carrying adversary-nation
supply chain dependencies.

"Gray Zone" = the space between:
  - Blue UAS (cleared, trusted, verified supply chain)
  - Adversary (DJI, banned, known threat)

These entities LOOK compliant but ARE NOT. They exploit the gap between
regulatory intent and enforcement — exactly what Anzu Robotics did.

Detection heuristics:
  1. IDENTITY WASH — licensed/rebranded adversary tech sold under new brand
  2. COMPONENT PASS-THROUGH — adversary components in "American" wrapper
  3. FIRMWARE DEPENDENCY — adversary-signed crypto keys, SDK, or OTA pipeline
  4. DATA ROUTING RISK — data touches adversary infrastructure at any layer
  5. REGULATORY ARBITRAGE — marketed as compliant without actual certification
  6. SUPPLY CHAIN FRAGILITY — single-source adversary dependency for critical BOM items

Inputs:
  - data/grayzone/entities.json       — tracked gray zone entities
  - data/grayzone/indicators.json     — OSINT signals & detection triggers
  - data/parts-db/drone_models.json   — Forge platform DB for cross-ref
  - data/parts-db/*.json              — component DB for BOM analysis

Outputs:
  - data/grayzone/flags.json          — generated gray zone flags
  - data/grayzone/risk_scores.json    — entity risk scoring
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GRAYZONE_DIR = REPO_ROOT / "data" / "grayzone"
PARTS_DB = REPO_ROOT / "data" / "parts-db"
FLAGS_OUT = GRAYZONE_DIR / "flags.json"
RISK_OUT = GRAYZONE_DIR / "risk_scores.json"

now = datetime.now(timezone.utc).isoformat()


def flag_id(seed: str) -> str:
    return "gz-" + hashlib.md5(seed.encode()).hexdigest()[:10]


def load_json(path: Path) -> list | dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


# ──────────────────────────────────────────
# 1. ENTITY LOADING & ENRICHMENT
# ──────────────────────────────────────────

def load_entities() -> list[dict]:
    """Load tracked gray zone entities from the registry."""
    return load_json(GRAYZONE_DIR / "entities.json")


def load_indicators() -> list[dict]:
    """Load OSINT indicators — signals that trigger gray zone scrutiny."""
    return load_json(GRAYZONE_DIR / "indicators.json")


def load_forge_platforms() -> list[dict]:
    """Load Forge platform DB for cross-referencing."""
    return load_json(PARTS_DB / "drone_models.json")


# ──────────────────────────────────────────
# 2. DETECTION HEURISTICS
# ──────────────────────────────────────────

class GrayZoneScorer:
    """
    Scores entities across six risk dimensions.
    Each dimension: 0.0 (clean) to 1.0 (confirmed threat).
    Overall risk = weighted average.
    """

    WEIGHTS = {
        "identity_wash":        0.25,   # Rebranded adversary tech
        "component_passthrough": 0.20,  # Adversary components present
        "firmware_dependency":   0.20,  # Adversary crypto/SDK/OTA control
        "data_routing_risk":     0.15,  # Data touches adversary infra
        "regulatory_arbitrage":  0.10,  # Marketed as compliant w/o cert
        "supply_chain_fragility": 0.10, # Single-source adversary BOM items
    }

    ADVERSARY_NATIONS = {"china", "cn", "russia", "ru", "iran", "ir", "north korea", "kp"}
    ADVERSARY_ENTITIES = {
        "dji", "dajiang", "autel", "yuneec", "fimi", "hubsan",
        "hikvision", "dahua", "huawei", "zte",
    }

    def __init__(self, entity: dict, indicators: list[dict]):
        self.entity = entity
        self.indicators = [i for i in indicators if i.get("entity_id") == entity.get("id")]
        self.scores = {}
        self.flags = []

    def score_identity_wash(self) -> float:
        """
        Detect rebranded/licensed adversary technology.

        Signals:
        - Licensed tech from adversary manufacturer
        - Hardware teardown matches adversary product
        - FCC filing reveals adversary FCC ID or components
        - CEO/founders previously at adversary company
        """
        score = 0.0
        e = self.entity

        # Licensed from adversary?
        license_source = (e.get("technology_license_source") or "").lower()
        if any(adv in license_source for adv in self.ADVERSARY_ENTITIES):
            score = max(score, 0.9)
            self.flags.append({
                "dimension": "identity_wash",
                "signal": f"Technology licensed from adversary entity: {e.get('technology_license_source')}",
                "severity": "critical",
                "confidence": 0.95,
            })

        # Teardown confirms adversary hardware?
        teardowns = [i for i in self.indicators if i.get("type") == "teardown"]
        for td in teardowns:
            if td.get("confirmed_adversary_hardware"):
                score = max(score, 0.95)
                self.flags.append({
                    "dimension": "identity_wash",
                    "signal": f"Teardown confirms adversary hardware: {td.get('detail', '')}",
                    "severity": "critical",
                    "confidence": td.get("confidence", 0.9),
                })

        # FCC filing reveals adversary components?
        fcc = [i for i in self.indicators if i.get("type") == "fcc_filing"]
        for f in fcc:
            if f.get("adversary_components_found"):
                score = max(score, 0.7)
                self.flags.append({
                    "dimension": "identity_wash",
                    "signal": f"FCC filing reveals adversary components: {f.get('detail', '')}",
                    "severity": "warning",
                    "confidence": f.get("confidence", 0.8),
                })

        # Leadership from adversary company?
        leadership = e.get("leadership_history", [])
        for leader in leadership:
            prev = (leader.get("previous_company") or "").lower()
            if any(adv in prev for adv in self.ADVERSARY_ENTITIES):
                score = max(score, 0.3)
                self.flags.append({
                    "dimension": "identity_wash",
                    "signal": f"{leader.get('name', 'Executive')} previously at {leader.get('previous_company', '')}",
                    "severity": "info",
                    "confidence": 0.99,
                })

        self.scores["identity_wash"] = score
        return score

    def score_component_passthrough(self) -> float:
        """
        Detect adversary-nation components in the BOM.

        Signals:
        - % of BOM sourced from adversary nations
        - Specific banned components (Entity List, ITAR)
        - Chinese-sourced thermal sensors, SoCs, radios
        """
        score = 0.0
        e = self.entity

        cn_pct = e.get("china_component_pct", 0)
        if cn_pct > 50:
            score = max(score, 0.9)
            self.flags.append({
                "dimension": "component_passthrough",
                "signal": f"{cn_pct}% of components sourced from adversary nations",
                "severity": "critical",
                "confidence": 0.85,
            })
        elif cn_pct > 25:
            score = max(score, 0.6)
            self.flags.append({
                "dimension": "component_passthrough",
                "signal": f"{cn_pct}% of components from adversary nations — partial pass-through",
                "severity": "warning",
                "confidence": 0.8,
            })
        elif cn_pct > 0:
            score = max(score, 0.3)

        # Specific banned components?
        banned = e.get("banned_components", [])
        for comp in banned:
            score = max(score, 0.8)
            self.flags.append({
                "dimension": "component_passthrough",
                "signal": f"Banned component detected: {comp}",
                "severity": "critical",
                "confidence": 0.9,
            })

        self.scores["component_passthrough"] = score
        return score

    def score_firmware_dependency(self) -> float:
        """
        Detect adversary control of firmware/software layer.

        Signals:
        - Firmware signed with adversary crypto keys
        - SDK from adversary manufacturer
        - OTA update pipeline routed through adversary infra
        - Root certificates controlled by adversary
        """
        score = 0.0
        e = self.entity

        fw_indicators = [i for i in self.indicators if i.get("type") == "firmware_analysis"]
        for fw in fw_indicators:
            if fw.get("adversary_signed"):
                score = max(score, 0.95)
                self.flags.append({
                    "dimension": "firmware_dependency",
                    "signal": f"Firmware signed with adversary crypto keys: {fw.get('detail', '')}",
                    "severity": "critical",
                    "confidence": fw.get("confidence", 0.9),
                })
            if fw.get("adversary_sdk"):
                score = max(score, 0.7)
                self.flags.append({
                    "dimension": "firmware_dependency",
                    "signal": f"SDK from adversary manufacturer embedded: {fw.get('detail', '')}",
                    "severity": "warning",
                    "confidence": fw.get("confidence", 0.85),
                })
            if fw.get("adversary_ota"):
                score = max(score, 0.9)
                self.flags.append({
                    "dimension": "firmware_dependency",
                    "signal": f"OTA update pipeline touches adversary infrastructure",
                    "severity": "critical",
                    "confidence": fw.get("confidence", 0.85),
                })

        self.scores["firmware_dependency"] = score
        return score

    def score_data_routing(self) -> float:
        """
        Detect data exfiltration risk through adversary infrastructure.

        Signals:
        - Telemetry/flight logs routed through adversary servers
        - Cloud platform with adversary backend
        - SDK phone-home to adversary endpoints
        """
        score = 0.0
        e = self.entity

        data_hosting = (e.get("data_hosting_location") or "").lower()
        if data_hosting in ("us", "usa", "united states"):
            pass  # Clean
        elif any(n in data_hosting for n in self.ADVERSARY_NATIONS):
            score = max(score, 0.9)
            self.flags.append({
                "dimension": "data_routing_risk",
                "signal": f"Data hosted in adversary nation: {data_hosting}",
                "severity": "critical",
                "confidence": 0.9,
            })

        # Even if hosted in US, check for SDK phone-home
        sdk_indicators = [i for i in self.indicators if i.get("type") == "network_analysis"]
        for ni in sdk_indicators:
            if ni.get("adversary_endpoints_contacted"):
                score = max(score, 0.7)
                self.flags.append({
                    "dimension": "data_routing_risk",
                    "signal": f"SDK contacts adversary endpoints: {ni.get('detail', '')}",
                    "severity": "warning",
                    "confidence": ni.get("confidence", 0.75),
                })

        self.scores["data_routing_risk"] = score
        return score

    def score_regulatory_arbitrage(self) -> float:
        """
        Detect misleading compliance claims.

        Signals:
        - Markets to gov/public safety WITHOUT Blue UAS
        - Claims "NDAA compliant" with adversary components
        - Avoids FCC disclosure of adversary relationship
        - Uses language like "American-owned" to imply compliance
        """
        score = 0.0
        e = self.entity

        # Markets to gov but not on Blue UAS?
        targets_gov = e.get("targets_government", False)
        on_blue_uas = e.get("blue_uas_listed", False)
        ndaa_compliant = e.get("ndaa_compliant", False)
        claims_ndaa = e.get("claims_ndaa_compliant", False)

        if targets_gov and not on_blue_uas:
            score = max(score, 0.4)
            self.flags.append({
                "dimension": "regulatory_arbitrage",
                "signal": "Markets to government/public safety without Blue UAS clearance",
                "severity": "warning",
                "confidence": 0.9,
            })

        if claims_ndaa and not ndaa_compliant:
            score = max(score, 0.8)
            self.flags.append({
                "dimension": "regulatory_arbitrage",
                "signal": "Claims NDAA compliance but has adversary-nation components",
                "severity": "critical",
                "confidence": 0.85,
            })

        # Uses misleading origin language?
        misleading = e.get("misleading_origin_claims", [])
        for claim in misleading:
            score = max(score, 0.5)
            self.flags.append({
                "dimension": "regulatory_arbitrage",
                "signal": f"Misleading origin claim: \"{claim}\"",
                "severity": "warning",
                "confidence": 0.7,
            })

        self.scores["regulatory_arbitrage"] = score
        return score

    def score_supply_chain_fragility(self) -> float:
        """
        Detect single-source adversary dependencies.

        Signals:
        - Critical BOM item only available from adversary source
        - Manufacturing in adversary-adjacent facility
        - Component shortage caused by adversary dependency
        """
        score = 0.0
        e = self.entity

        mfg_country = (e.get("manufacturing_country") or "").lower()
        # Not adversary per se, but adversary-adjacent?
        if any(n in mfg_country for n in self.ADVERSARY_NATIONS):
            score = max(score, 0.7)
            self.flags.append({
                "dimension": "supply_chain_fragility",
                "signal": f"Manufacturing in adversary nation: {mfg_country}",
                "severity": "critical",
                "confidence": 0.9,
            })

        # Did component shortage kill the product?
        if e.get("discontinued_supply_chain"):
            score = max(score, 0.8)
            self.flags.append({
                "dimension": "supply_chain_fragility",
                "signal": "Product discontinued due to adversary component shortage",
                "severity": "critical",
                "confidence": 0.95,
            })

        self.scores["supply_chain_fragility"] = score
        return score

    def compute_overall(self) -> dict:
        """Run all heuristics and compute weighted risk score."""
        self.score_identity_wash()
        self.score_component_passthrough()
        self.score_firmware_dependency()
        self.score_data_routing()
        self.score_regulatory_arbitrage()
        self.score_supply_chain_fragility()

        overall = sum(
            self.scores.get(dim, 0) * weight
            for dim, weight in self.WEIGHTS.items()
        )

        # Risk tier
        if overall >= 0.75:
            tier = "CRITICAL"
        elif overall >= 0.50:
            tier = "HIGH"
        elif overall >= 0.25:
            tier = "MEDIUM"
        else:
            tier = "LOW"

        return {
            "entity_id": self.entity.get("id"),
            "entity_name": self.entity.get("name"),
            "overall_risk": round(overall, 3),
            "risk_tier": tier,
            "dimension_scores": {k: round(v, 3) for k, v in self.scores.items()},
            "flags": self.flags,
            "scored_at": now,
        }


# ──────────────────────────────────────────
# 3. CROSS-REFERENCE WITH FORGE DB
# ──────────────────────────────────────────

def cross_reference_forge(entities: list[dict], platforms: list[dict]) -> list[dict]:
    """
    Check if any gray zone entity's products overlap with or compete
    against Forge-tracked platforms. Flag government buyers who may
    have purchased gray zone products thinking they were compliant.
    """
    xref_flags = []

    for entity in entities:
        entity_products = entity.get("products", [])
        for product in entity_products:
            product_category = product.get("category", "")
            product_targets = product.get("target_markets", [])

            # Does this product compete in the same space as Blue UAS platforms?
            if any(t in ("public_safety", "government", "defense", "first_responder")
                   for t in product_targets):

                # Find competing Blue UAS platforms in same category
                competing_blue = [
                    p for p in platforms
                    if p.get("compliance", {}).get("blue_uas")
                    and p.get("category", "").lower() == product_category.lower()
                ]

                if competing_blue:
                    xref_flags.append({
                        "id": flag_id(f"xref-{entity['id']}-{product.get('name','')}"),
                        "timestamp": now,
                        "flag_type": "grayzone_xref",
                        "severity": "warning",
                        "title": (
                            f"Gray zone product '{product.get('name','')}' by {entity.get('name','')} "
                            f"competes with {len(competing_blue)} Blue UAS platforms"
                        ),
                        "detail": (
                            f"{entity.get('name','')} markets {product.get('name','')} to "
                            f"{', '.join(product_targets)} buyers. "
                            f"Blue UAS alternatives: {', '.join(p.get('name','') for p in competing_blue[:5])}. "
                            f"Buyers may have purchased gray zone product believing it was compliant."
                        ),
                        "entity_id": entity.get("id"),
                        "confidence": 0.8,
                        "data_sources": ["forge_platforms_db", "grayzone_entities"],
                    })

    return xref_flags


# ──────────────────────────────────────────
# 4. GENERATE BUYER IMPACT ASSESSMENT
# ──────────────────────────────────────────

def assess_buyer_impact(entity: dict) -> Optional[dict]:
    """
    For confirmed gray zone entities, estimate the impact on
    buyers who purchased their products for government use.
    """
    known_buyers = entity.get("known_government_buyers", [])
    if not known_buyers:
        return None

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "affected_buyers": known_buyers,
        "buyer_count": len(known_buyers),
        "impact_assessment": (
            f"{len(known_buyers)} government/public safety agencies purchased "
            f"{entity.get('name', '')} products potentially believing they met "
            f"Blue UAS or NDAA compliance requirements. These agencies may need "
            f"to re-evaluate their procurement and consider replacement platforms "
            f"from the actual Blue UAS Cleared List."
        ),
        "recommended_actions": [
            "Audit current fleet for gray zone platforms",
            "Cross-reference with DCMA Blue UAS Cleared List",
            "Develop transition plan to verified Blue UAS platforms",
            "Review procurement policies for supply chain verification requirements",
        ],
        "assessed_at": now,
    }


# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────

def main():
    print("=" * 60)
    print("PIE Gray Zone Detector")
    print("=" * 60)

    GRAYZONE_DIR.mkdir(parents=True, exist_ok=True)

    entities = load_entities()
    indicators = load_indicators()
    platforms = load_forge_platforms()

    print(f"  Entities tracked: {len(entities)}")
    print(f"  Indicators loaded: {len(indicators)}")
    print(f"  Forge platforms for cross-ref: {len(platforms)}")

    # Score each entity
    all_risk_scores = []
    all_flags = []

    for entity in entities:
        scorer = GrayZoneScorer(entity, indicators)
        result = scorer.compute_overall()
        all_risk_scores.append(result)

        # Convert dimension flags to PIE-format flags
        for df in result["flags"]:
            all_flags.append({
                "id": flag_id(f"gz-{entity['id']}-{df['dimension']}-{df['signal'][:30]}"),
                "timestamp": now,
                "flag_type": "grayzone",
                "severity": df["severity"],
                "title": f"[GRAY ZONE] {entity.get('name', '')}: {df['signal'][:80]}",
                "detail": df["signal"],
                "entity_id": entity.get("id"),
                "dimension": df["dimension"],
                "confidence": df.get("confidence", 0.5),
                "data_sources": ["grayzone_detector"],
            })

        tier = result["risk_tier"]
        print(f"  {entity.get('name', ''):30s} → {tier:8s} (score: {result['overall_risk']:.3f})")

    # Cross-reference with Forge
    print("\nCross-referencing with Forge platforms...")
    xref_flags = cross_reference_forge(entities, platforms)
    all_flags.extend(xref_flags)
    print(f"  Cross-ref flags: {len(xref_flags)}")

    # Buyer impact assessments
    print("\nAssessing buyer impact...")
    impacts = []
    for entity in entities:
        impact = assess_buyer_impact(entity)
        if impact:
            impacts.append(impact)
            print(f"  {entity.get('name', '')}: {impact['buyer_count']} affected agencies")

    # Write outputs
    with open(FLAGS_OUT, "w") as f:
        json.dump(all_flags, f, indent=2)
    with open(RISK_OUT, "w") as f:
        json.dump({
            "risk_scores": all_risk_scores,
            "buyer_impacts": impacts,
            "generated_at": now,
            "entity_count": len(entities),
            "total_flags": len(all_flags),
        }, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Gray Zone Detection — Complete")
    print(f"  Entities scored: {len(all_risk_scores)}")
    print(f"  Flags generated: {len(all_flags)}")
    print(f"  Buyer impacts: {len(impacts)}")
    print(f"  Output: {FLAGS_OUT}")
    print(f"  Output: {RISK_OUT}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
