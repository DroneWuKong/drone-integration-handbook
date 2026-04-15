#!/usr/bin/env python3
"""
PIE Live Pipeline — reads real Forge DB, generates real flags.
Run from the repo root: python pipeline/pie_pipeline_live.py
"""

import json
import os
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# Import supplemental analysis modules
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pie_supplemental import (
    analyze_rf_comms, analyze_ew, analyze_sof, analyze_nav_pnt,
    analyze_propulsion, analyze_test_infra, analyze_financial,
    analyze_gray_zone,
    analyze_battery_supply_chain, analyze_thermal_supply_chain,
    analyze_control_link_supply_chain,
    analyze_stack_supply_chain,
    analyze_vtx_supply_chain,
    analyze_esc_supply_chain,
    analyze_allied_manufacturers,
    analyze_fpv_camera_supply_chain,
    analyze_frame_supply_chain,
    analyze_receiver_supply_chain,
    analyze_antenna_supply_chain,
    analyze_propeller_supply_chain,
    analyze_live_pricing,
    analyze_battery_partsdb,
    SUPPLEMENTAL_SOURCES,
)
from pie_advanced import (
    analyze_dependency_graph, analyze_lead_times, analyze_contract_demand,
    analyze_conflict_consumption, analyze_alternatives, analyze_price_elasticity,
    analyze_sanctions_evasion, analyze_what_if, analyze_temporal_patterns,
    analyze_sentiment_signals, ADVANCED_SOURCES,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PARTS_DB = REPO_ROOT / "data" / "parts-db"
FORGE_DB = REPO_ROOT / "data" / "forge_database.json"
FLAGS_OUT = REPO_ROOT / "data" / "flags.json"
PREDS_OUT = REPO_ROOT / "data" / "predictions.json"

now = datetime.now(timezone.utc).isoformat()


# ──────────────────────────────────────────
# SOURCE REGISTRY — every data source with URL, description, validation
# ──────────────────────────────────────────

SOURCES = {
    # ── Forge Ecosystem ──
    "forge_parts_db": {
        "name": "Forge Parts Database",
        "url": "https://uas-forge.com/",
        "description": "3,008 vetted drone components across 20 categories. Curated by the Drone Integration Handbook project.",
        "validation": "Hand-verified specs. Pricing cross-referenced with distributors. Updated on each Forge release.",
        "type": "primary",
    },
    "forge_compliance": {
        "name": "Forge Compliance Dashboard",
        "url": "https://uas-forge.com/compliance/",
        "description": "Blue UAS, NDAA §848, ITAR, and country-of-origin status for 219 platforms.",
        "validation": "Compliance tiers verified against DIU Blue UAS Cleared List and NDAA text.",
        "type": "primary",
    },
    "forge_industry_intel": {
        "name": "Forge Industry Intelligence",
        "url": "https://uas-forge.com/industry/",
        "description": "Curated funding rounds, defense contracts, grants & market data from the Forge data pipeline.",
        "validation": "Hand-verified from primary sources (SAM.gov, SEC filings, press releases).",
        "type": "primary",
    },
    "forge_bom": {
        "name": "Forge BOM Graph",
        "url": "https://uas-forge.com/builder/",
        "description": "Bill of Materials mapping: which platforms use which components. Derived from platform profiles + parts-db.",
        "validation": "BOM data from manufacturer specs, teardowns, and Handbook platform profiles.",
        "type": "derived",
    },
    # ── GUR / Ukraine Intelligence ──
    "opensanctions_gur": {
        "name": "OpenSanctions — Ukraine War & Sanctions (GUR)",
        "url": "https://data.opensanctions.org/datasets/latest/ua_war_sanctions/targets.simple.csv",
        "description": "OpenSanctions daily bulk export of GUR War & Sanctions portal data. Structured CSV/JSON, no auth required, free for non-commercial use. Updated daily.",
        "validation": "OpenSanctions crawls war-sanctions.gur.gov.ua and publishes structured data daily. Cross-referenced with GUR portal primary sources.",
    },
    "gur_war_sanctions": {
        "name": "GUR War & Sanctions Portal",
        "url": "https://war-sanctions.gur.gov.ua",
        "description": "Ukraine's military intelligence (GUR) database of foreign components in captured Russian weapons. 5,534 components across 190 weapon systems.",
        "validation": "Physical teardowns of captured/downed weapons. Component photos, manufacturer IDs, and PCB analysis published publicly.",
        "type": "primary",
    },
    "euromaidanpress": {
        "name": "Euromaidan Press",
        "url": "https://euromaidanpress.com/2025/12/22/new-russian-reconnaissance-drone-uses-british-raspberry-pi-microcomputer-and-licensed-windows-11/",
        "description": "Independent Ukrainian English-language media. Reported on RPi 5 in Molniya-2R and RPi in Geran-5.",
        "validation": "Cites GUR primary sources directly. Cross-referenced with GUR portal data.",
        "type": "reporting",
    },
    "united24media": {
        "name": "United24 Media",
        "url": "https://united24media.com/latest-news/british-raspberry-pi-found-powering-russias-geran-strike-drone-despite-santions-15841",
        "description": "Official Ukrainian fundraising platform media arm. Reported 40,000+ RPi units procured for Geran drones.",
        "validation": "Cites Polkovnik GSh Telegram channel (linked to Ukraine's Armed Forces) and GUR disclosures.",
        "type": "reporting",
    },
    "heise": {
        "name": "Heise Online (Germany)",
        "url": "https://www.heise.de/en/news/Russian-jet-kamikaze-drone-with-Raspberry-Pi-4-10669801.html",
        "description": "German tech publication. Reported on RPi 4 found in Geran-3 jet drone teardown by Ukrainian intelligence.",
        "validation": "Independent German reporting based on GUR HUR published analysis.",
        "type": "reporting",
    },
    "dronexl_gur": {
        "name": "DroneXL — GUR Teardown Analysis",
        "url": "https://dronexl.co/2026/03/02/ukraine-gur-russian-drones-foreign-parts/",
        "description": "Detailed walkthrough of GUR War & Sanctions portal. Documents 5,534 components, 190 weapon systems, interactive 3D models.",
        "validation": "Primary reporting from the GUR portal with component-level detail.",
        "type": "reporting",
    },
    # ── Government / Policy ──
    "gov_programs": {
        "name": "DoD Program Tracking",
        "url": "https://defensescoop.com/2025/12/02/hegseth-drone-dominance-program-ddp-gauntlets-website-rfi/",
        "description": "Pentagon drone program tracking — Drone Dominance, Replicator/DAWG, SRR, CCA, FTUAS.",
        "validation": "Sourced from DoD RFIs, DefenseScoop, Breaking Defense, Congressional Research Service.",
        "type": "aggregated",
    },
    "congress_gov": {
        "name": "Congressional Research Service (CRS)",
        "url": "https://www.congress.gov/crs-product/IF12668",
        "description": "CRS reports on Army sUAS programs, NDAA provisions, and DoD drone procurement.",
        "validation": "Official nonpartisan congressional research. Primary source for legislative analysis.",
        "type": "primary",
    },
    "defensescoop": {
        "name": "DefenseScoop",
        "url": "https://defensescoop.com/2026/03/05/dod-drone-dominance-program-orders-deliveries-military-units/",
        "description": "Defense technology news. Primary reporting on Drone Dominance orders, Blue UAS updates.",
        "validation": "Cited by DoD officials. Primary source for Gauntlet results and delivery timelines.",
        "type": "reporting",
    },
    "sam_gov": {
        "name": "SAM.gov (Federal Contract Database)",
        "url": "https://sam.gov",
        "description": "Official US federal contract awards database. Source for contract values, awardees, timelines.",
        "validation": "Official government procurement data. Primary source.",
        "type": "primary",
    },
    "congress": {
        "name": "US Congress / NDAA",
        "url": "https://www.congress.gov",
        "description": "National Defense Authorization Act text, appropriations bills, committee reports.",
        "validation": "Official legislative text. Primary source for policy analysis.",
        "type": "primary",
    },
    "fcc": {
        "name": "Federal Communications Commission",
        "url": "https://www.fcc.gov",
        "description": "FCC equipment authorization data. Source for foreign drone import restrictions (NDAA §1709).",
        "validation": "Official regulatory data. Primary source.",
        "type": "primary",
    },
    "policy_tracker": {
        "name": "Policy Signal Aggregation",
        "url": "https://www.govconwire.com/articles/drones-unmanned-systems-war-dept-initiatives-dawg",
        "description": "Aggregated policy signals from executive orders, congressional actions, and agency memos.",
        "validation": "Cross-referenced across multiple reporting sources and official government documents.",
        "type": "aggregated",
    },
    # ── Market / Financial ──
    "trendforce": {
        "name": "TrendForce DRAM Pricing",
        "url": "https://www.trendforce.com/prices/dram",
        "description": "Semiconductor market research. DRAM contract pricing, quarterly forecasts.",
        "validation": "Industry-standard pricing source. Cited by RPi, Samsung, SK Hynix in earnings.",
        "type": "primary",
    },
    "rpi_earnings": {
        "name": "Raspberry Pi FY2025 Earnings",
        "url": "https://www.theregister.com/2026/03/31/raspberry_pi_fy_2025/",
        "description": "RPi Holdings (LON:RPI) annual results. Revenue $323.5M, DRAM impact, diversion acknowledgment.",
        "validation": "Public company financial disclosure. Audited results. CEO statements on drone diversion.",
        "type": "primary",
    },
    "morgan_stanley": {
        "name": "Morgan Stanley AI Infrastructure Forecast",
        "url": "https://www.techspot.com/news/110770-analysts-warn-ai-demand-could-push-consumer-tech.html",
        "description": "$620B AI infrastructure spend in 2026 (up from $470B in 2025). DRAM supply impact analysis.",
        "validation": "Institutional research. Cited alongside Citi, Macquarie, Nomura analyst reports.",
        "type": "reporting",
    },
    "distributor_pricing": {
        "name": "Distributor Pricing (Mouser/DigiKey/Arrow)",
        "url": "https://www.mouser.com",
        "description": "Real-time component pricing and lead times from major electronic distributors.",
        "validation": "Live API data (when API keys configured). Currently using published MSRP and known pricing.",
        "type": "primary",
    },
    # ── Defense Contracts ──
    "defense_contracts": {
        "name": "Defense Contract Tracking",
        "url": "https://breakingdefense.com",
        "description": "Contract awards, program milestones, and acquisition signals from defense reporting.",
        "validation": "Cross-referenced across DefenseScoop, Breaking Defense, Defense Daily, and SAM.gov.",
        "type": "aggregated",
    },
    # ── DIU / DCMA ──
    "diu_blue_uas": {
        "name": "DIU/DCMA Blue UAS Cleared List",
        "url": "https://www.diu.mil/blue-uas-cleared-list",
        "description": "Official DoD Blue UAS Cleared List. 50+ platforms vetted for cybersecurity and supply chain trust.",
        "validation": "Official DoD certification. Primary source. Transitioned to DCMA per Jul 2025 SecDef memo.",
        "type": "primary",
    },
    # ── Supply Chain / Geopolitical ──
    "supply_chain_mapping": {
        "name": "Supply Chain Geographic Mapping",
        "url": "https://uas-forge.com/compliance/",
        "description": "Component origin tracking mapped to allied nation risk levels. Based on manufacturer HQ and fab locations.",
        "validation": "Manufacturer data from Forge DB. Fab locations from public disclosures and industry reporting.",
        "type": "derived",
    },
    "geopolitical_risk": {
        "name": "Geopolitical Risk Assessment",
        "url": "https://uas-forge.com/platforms/",
        "description": "Allied nation stability and supply chain concentration risk. Taiwan/TSMC, S.Korea/DRAM focus.",
        "validation": "Based on published geopolitical analysis, TSMC concentration data, and DRAM market reports.",
        "type": "derived",
    },
    # ── Software / Autonomy ──
    "software_ecosystem": {
        "name": "UAS Software Ecosystem Tracking",
        "url": "https://uas-forge.com/platforms/",
        "description": "Maps autonomy software (Hivemind, Gambit, Lattice, Swarmer) to hardware dependencies and contracts.",
        "validation": "Company announcements, partnership press releases, contract awards, and platform integration disclosures.",
        "type": "aggregated",
    },
    # ── C-UAS ──
    "cuas_tracking": {
        "name": "Counter-UAS Industry Tracking",
        "url": "https://uas-handbook.com/#c605",
        "description": "C-UAS companies, products, contracts. Tracks shared component demand between C-UAS and UAS.",
        "validation": "Company disclosures, contract awards, Handbook Ch. Counter-UAS reference.",
        "type": "aggregated",
    },
    # ── Workforce ──
    "workforce_analysis": {
        "name": "Manufacturer Workforce & Capacity Estimates",
        "url": "https://uas-forge.com/industry/",
        "description": "Employee counts, facility locations, production rate estimates for UAS manufacturers.",
        "validation": "LinkedIn data, company disclosures, press releases, job posting analysis. Estimates marked as such.",
        "type": "estimated",
    },
    "capacity_estimate": {
        "name": "Production Capacity Estimates",
        "url": "https://uas-forge.com/industry/",
        "description": "Monthly production capacity estimates based on contract deliverables, company statements, and facility size.",
        "validation": "Derived from contract volumes, delivery timelines, and company disclosures. Marked as estimates.",
        "type": "estimated",
    },
    # ── BOM ──
    "bom_analysis": {
        "name": "BOM Cost Index Analysis",
        "url": "https://uas-forge.com/cost/",
        "description": "Reference Blue UAS BOM costed from Forge parts-db pricing. Compared to non-compliant equivalent.",
        "validation": "Component prices from Forge DB (distributor-sourced). BOM composition from platform profiles.",
        "type": "derived",
    },
    # ── Foreign Intel ──
    "foreign_intel": {
        "name": "Foreign UAS Program Intelligence",
        "url": "https://uas-forge.com/platforms/",
        "description": "Tracks foreign drone programs (China, Turkey, Iran, Ukraine, EU, India, etc.) and their supply chain implications.",
        "validation": "Aggregated from defense reporting, Forge platform DB (42 countries), and open-source intelligence.",
        "type": "aggregated",
    },
    "fpv_market": {
        "name": "FPV Component Market Tracking",
        "url": "https://www.getfpv.com",
        "description": "Commercial FPV component pricing and availability. GetFPV, RaceDayQuads, Pyrodrone.",
        "validation": "Live retailer pricing. Monitored for anomalies against 90-day moving averages.",
        "type": "primary",
    },
}


# Merge supplemental + advanced sources
SOURCES.update(SUPPLEMENTAL_SOURCES)
SOURCES.update(ADVANCED_SOURCES)


def resolve_sources(source_ids):
    """Convert a list of source ID strings into rich source objects with URLs."""
    resolved = []
    for sid in source_ids:
        if sid in SOURCES:
            s = SOURCES[sid].copy()
            s["id"] = sid
            resolved.append(s)
        else:
            resolved.append({
                "id": sid,
                "name": sid.replace("_", " ").title(),
                "url": "",
                "description": "",
                "validation": "",
                "type": "unknown",
            })
    return resolved


def load_json(path):
    with open(path) as f:
        return json.load(f)


def flag_id(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:12]


# ──────────────────────────────────────────
# 1. LOAD FORGE DB
# ──────────────────────────────────────────

def load_forge():
    """Load Forge data — prefer forge_database.json (219 platforms), fall back to parts-db."""
    db = {}
    total = 0

    # Try the master forge_database.json first (has all 219 platforms)
    if FORGE_DB.exists():
        master = load_json(FORGE_DB)
        if isinstance(master, dict):
            if "drone_models" in master:
                db["drone_models"] = master["drone_models"]
                total += len(master["drone_models"])
                print(f"  forge_database.json: {len(master['drone_models'])} platforms (master)")
            if "components" in master:
                # components here is category metadata, not individual parts
                pass
            if "industry" in master:
                db["industry"] = master.get("industry", [])

    # Always load parts-db for component-level data
    for f in sorted(PARTS_DB.glob("*.json")):
        data = load_json(f)
        if isinstance(data, list):
            key = f.stem
            # Don't overwrite drone_models if we got them from forge_database.json
            if key == "drone_models" and "drone_models" in db and len(db["drone_models"]) >= len(data):
                print(f"  parts-db/{f.name}: {len(data)} entries (skipped — master has {len(db['drone_models'])})")
                continue
            db[key] = data
            total += len(data)

    print(f"  Total: {total} entries across {len(db)} categories")
    return db


# ──────────────────────────────────────────
# 2. ANALYZE PLATFORMS
# ──────────────────────────────────────────

def analyze_platforms(db):
    """Analyze drone_models for Blue UAS / compliance patterns."""
    flags = []
    models = db.get("drone_models", [])

    blue = [m for m in models if isinstance(m, dict) and m.get("compliance", {}).get("blue_uas")]
    ndaa = [m for m in models if isinstance(m, dict) and m.get("compliance", {}).get("ndaa_compliant")]
    adversary = [m for m in models if isinstance(m, dict) and
                 m.get("country", "").lower() in ("china", "cn", "russia", "ru", "iran", "ir")]

    print(f"  Platforms: {len(models)} total | {len(blue)} Blue UAS | {len(ndaa)} NDAA | {len(adversary)} adversary-nation")

    # Flag: Blue UAS list growth
    if len(blue) >= 20:
        flags.append({
            "id": flag_id("blue-uas-growth"),
            "timestamp": now,
            "flag_type": "correlation",
            "severity": "info",
            "title": f"Blue UAS Cleared List at {len(blue)} platforms — procurement demand expanding",
            "detail": (
                f"Forge DB tracks {len(blue)} Blue UAS platforms across {len(set(m.get('manufacturer','') for m in blue))} manufacturers. "
                f"Each platform requires trusted SBC/SoM, MCU, thermal, GNSS, and radio components. "
                f"Scaling across {len(blue)} platforms creates compound demand on shared component supply chains."
            ),
            "confidence": 0.95,
            "prediction": "Component demand proportional to fleet-wide production volume. Monitor distributor lead times for Jetson, QRB5165, STM32H7.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["forge_parts_db"],
        })

    # Flag each Blue UAS platform with known high-demand SBC
    sbc_demand = {}
    for m in blue:
        name = m.get("name", "")
        mfr = m.get("manufacturer", "")
        desc = (m.get("description") or "").lower()

        # Extract SBC signals from description
        for sbc, sbc_id in [
            ("jetson", "jetson-orin"),
            ("voxl", "qrb5165"),
            ("qrb5165", "qrb5165"),
            ("raspberry pi", "rpi"),
            ("rpi", "rpi"),
            ("stm32h7", "stm32h7"),
            ("pixhawk", "stm32h7"),
        ]:
            if sbc in desc:
                sbc_demand.setdefault(sbc_id, []).append(name)

    for sbc_id, platforms in sbc_demand.items():
        if len(platforms) >= 2:
            flags.append({
                "id": flag_id(f"multi-platform-{sbc_id}"),
                "timestamp": now,
                "flag_type": "correlation",
                "severity": "warning" if len(platforms) >= 3 else "info",
                "title": f"{len(platforms)} Blue UAS platforms share {sbc_id.upper()} dependency",
                "detail": (
                    f"Forge BOM analysis: {', '.join(platforms[:5])} all depend on {sbc_id.upper()} SBC/SoM. "
                    f"Simultaneous production scaling creates compound demand on a single component supply chain. "
                    f"If one program spikes orders, others face allocation pressure."
                ),
                "confidence": 0.88,
                "prediction": f"Lead time sensitivity: any single program's production ramp will impact availability for the other {len(platforms)-1} platforms.",
                "platform_id": None,
                "component_id": sbc_id,
                "data_sources": ["forge_parts_db", "forge_compliance"],
            })

    return flags, blue, ndaa, adversary


# ──────────────────────────────────────────
# 3. ANALYZE COMPANION COMPUTERS (SBCs)
# ──────────────────────────────────────────

def analyze_sbcs(db):
    """Analyze companion_computers for pricing anomalies and supply signals."""
    flags = []
    cc = db.get("companion_computers", [])
    print(f"  Companion computers: {len(cc)}")

    # Track processors used
    processor_counts = {}
    for c in cc:
        proc = (c.get("processor") or "").lower()
        name = c.get("name", "")
        price_str = c.get("approx_price", "")

        # Parse price — handle string, int, float
        price = 0
        if isinstance(price_str, (int, float)):
            price = float(price_str)
        elif isinstance(price_str, str) and price_str:
            nums = re.findall(r'[\d,]+\.?\d*', price_str.replace(",", ""))
            if nums:
                price = float(nums[0])

        # Track processor families
        for family, label in [
            ("qrb5165", "Qualcomm QRB5165"),
            ("jetson orin", "NVIDIA Jetson Orin"),
            ("jetson agx", "NVIDIA Jetson AGX"),
            ("rk3588", "Rockchip RK3588"),
            ("bcm2712", "Broadcom BCM2712 (RPi 5)"),
            ("stm32h7", "STM32H7"),
            ("ambarella", "Ambarella"),
        ]:
            if family in proc:
                processor_counts.setdefault(label, []).append({"name": name, "price": price})

    for proc_label, boards in processor_counts.items():
        if len(boards) >= 2:
            avg_price = sum(b["price"] for b in boards if b["price"] > 0) / max(1, sum(1 for b in boards if b["price"] > 0))
            flags.append({
                "id": flag_id(f"sbc-cluster-{proc_label}"),
                "timestamp": now,
                "flag_type": "correlation",
                "severity": "info",
                "title": f"{len(boards)} companion boards use {proc_label} — supply chain cluster",
                "detail": (
                    f"Forge DB: {', '.join(b['name'][:30] for b in boards[:4])} all use {proc_label}. "
                    f"Avg price: ${avg_price:.0f}. Same silicon dependency means a shortage at the chip level "
                    f"impacts all boards in this cluster simultaneously."
                ),
                "confidence": 0.85,
                "prediction": f"Monitor {proc_label} chip availability. Any fab disruption or allocation shift cascades to {len(boards)} companion computer products.",
                "platform_id": None,
                "component_id": proc_label.lower().replace(" ", "-"),
                "data_sources": ["forge_parts_db"],
            })

    return flags


# ──────────────────────────────────────────
# 4. ANALYZE MESH RADIOS
# ──────────────────────────────────────────

def analyze_mesh(db):
    """Analyze mesh radio supply — critical for multi-vehicle Blue UAS."""
    flags = []
    mesh = db.get("mesh_radios", [])
    print(f"  Mesh radios: {len(mesh)}")

    us_mesh = [m for m in mesh if "usa" in (m.get("manufacturer_hq") or "").lower() or "us" in (m.get("manufacturer_hq") or "").lower()]
    non_us = [m for m in mesh if m not in us_mesh]

    # Flag: limited US mesh radio supply
    if len(us_mesh) <= len(mesh) * 0.6:
        flags.append({
            "id": flag_id("mesh-us-supply"),
            "timestamp": now,
            "flag_type": "supply_constraint",
            "severity": "warning",
            "title": f"US-manufactured mesh radios: {len(us_mesh)} of {len(mesh)} options — NDAA bottleneck",
            "detail": (
                f"Forge DB tracks {len(mesh)} mesh radios. Only {len(us_mesh)} from US manufacturers. "
                f"Blue UAS platforms require NDAA-compliant mesh for multi-vehicle ops. "
                f"Doodle Labs and Silvus dominate the Blue UAS mesh market — "
                f"limited supplier diversity creates concentration risk."
            ),
            "confidence": 0.82,
            "prediction": "Mesh radio becomes supply bottleneck as multi-drone programs (Lattice, Replicator) scale. Limited alternatives at MANET performance tier.",
            "platform_id": None,
            "component_id": "mesh-radios",
            "data_sources": ["forge_parts_db"],
        })

    return flags


# ──────────────────────────────────────────
# 5. ANALYZE FLIGHT CONTROLLERS
# ──────────────────────────────────────────

def analyze_fcs(db):
    """Analyze FC MCU concentration — STM32 dependency."""
    flags = []
    fcs = db.get("flight_controllers", [])
    print(f"  Flight controllers: {len(fcs)}")

    # Count MCU families
    mcu_counts = {"STM32F405": 0, "STM32F722": 0, "STM32H743": 0, "STM32H750": 0, "other": 0}
    for fc in fcs:
        name = fc.get("name", "").lower()
        desc = (fc.get("description") or "").lower()
        text = name + " " + desc
        matched = False
        for mcu in ["stm32h743", "stm32h750", "stm32f405", "stm32f722"]:
            if mcu.lower() in text:
                key = mcu.upper()[:9] + mcu[9:].upper() if len(mcu) > 9 else mcu.upper()
                for k in mcu_counts:
                    if mcu.upper().startswith(k[:8]):
                        mcu_counts[k] += 1
                        matched = True
                        break
        if not matched:
            mcu_counts["other"] += 1

    h7_count = mcu_counts.get("STM32H743", 0) + mcu_counts.get("STM32H750", 0)
    total_stm = sum(v for k, v in mcu_counts.items() if k != "other")

    if total_stm > len(fcs) * 0.5:
        flags.append({
            "id": flag_id("fc-stm32-concentration"),
            "timestamp": now,
            "flag_type": "supply_constraint",
            "severity": "warning",
            "title": f"STM32 concentration: {total_stm}/{len(fcs)} flight controllers depend on STMicroelectronics",
            "detail": (
                f"Forge DB: {len(fcs)} FCs tracked. ~{total_stm} use STM32 MCUs (F4/H7 families). "
                f"H7-class (H743/H750) used by ~{h7_count} premium FCs including defense FPV platforms. "
                f"Drone Dominance FPV scaling drives STM32H7 demand alongside existing commercial FPV market."
            ),
            "confidence": 0.90,
            "prediction": "STM32H7 allocation pressure increases as Drone Dominance program scales FPV production. FPV industry and defense share the same MCU supply.",
            "platform_id": None,
            "component_id": "stm32h7",
            "data_sources": ["forge_parts_db"],
        })

    return flags


# ──────────────────────────────────────────
# 6. GUR DIVERSION CROSS-REFERENCE
# ──────────────────────────────────────────

def fetch_gur_live():
    """
    Fetch GUR War & Sanctions component diversion data.

    Primary source: OpenSanctions ua_war_sanctions bulk download (free, no auth,
    daily updated). URL: https://data.opensanctions.org/datasets/latest/ua_war_sanctions/
    OpenSanctions crawls the GUR portal and publishes structured JSON/CSV daily.

    Falls back to: cached data → verified static dataset.
    Returns list of {weapon, component, role, units, manufacturer, country} dicts.
    """
    import urllib.request, urllib.error, ssl, json as _json, csv, io

    GUR_CACHE = REPO_ROOT / "data" / "procurement" / "gur_components_cache.json"

    # ── Primary: OpenSanctions ua_war_sanctions CSV (free, no auth, daily) ──
    # CSV is lighter than the full FTM JSON and has the fields we need.
    OPENSANCTIONS_URL = (
        "https://data.opensanctions.org/datasets/latest"
        "/ua_war_sanctions/targets.simple.csv"
    )

    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            OPENSANCTIONS_URL,
            headers={"User-Agent": "PIE-Intelligence/1.0 (non-commercial research)"},
        )
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            raw = r.read().decode("utf-8")

        reader = csv.DictReader(io.StringIO(raw))
        findings = []
        uas_keywords = [
            "uav", "drone", "shahed", "geran", "lancet", "orion",
            "fpv", "unmanned", "loitering", "missile", "geranium",
        ]
        for row in reader:
            # Filter to UAS/weapons-relevant entities
            caption = (row.get("caption") or "").lower()
            schema  = (row.get("schema") or "").lower()
            topics  = (row.get("topics") or "").lower()
            countries = row.get("countries") or ""

            is_uas_relevant = (
                any(kw in caption for kw in uas_keywords)
                or "weapons.manufacture" in topics
                or "sanction" in topics
            )
            if not is_uas_relevant:
                continue

            findings.append({
                "weapon":       row.get("caption", "Unknown"),
                "component":    row.get("name", row.get("caption", "")),
                "role":         row.get("topics", ""),
                "manufacturer": row.get("caption", ""),
                "country":      countries.split(";")[0].strip() if countries else "",
                "units":        "",
                "source":       "opensanctions_gur",
                "opensanctions_id": row.get("id", ""),
                "datasets":     row.get("datasets", ""),
            })

        if findings:
            print(f"  ✓ GUR/OpenSanctions: {len(findings)} UAS-relevant entities")
            GUR_CACHE.parent.mkdir(parents=True, exist_ok=True)
            GUR_CACHE.write_text(_json.dumps({
                "fetched_at": now,
                "source": "opensanctions_ua_war_sanctions",
                "count": len(findings),
                "components": findings,
            }, indent=2))
            return findings
        else:
            print("  ⚠ OpenSanctions returned data but no UAS-relevant entries — falling back")

    except Exception as e:
        print(f"  ⚠ GUR/OpenSanctions fetch failed ({type(e).__name__}): {e} — trying cache")

    # ── Fallback 1: cached data from last successful fetch ──
    if GUR_CACHE.exists():
        try:
            cache = _json.loads(GUR_CACHE.read_text())
            findings = cache.get("components", [])
            fetched  = cache.get("fetched_at", "unknown")
            source   = cache.get("source", "cache")
            print(f"  ℹ GUR using cached data ({len(findings)} entries, {source}, fetched {fetched[:10]})")
            return findings
        except Exception:
            pass

    # ── Fallback 2: verified static dataset (hand-curated from GUR research) ──
    print("  ℹ GUR using verified static dataset (all fetches failed)")
    return [
        {"weapon": "Geran-2/3 (Shahed-136/238)", "component": "Raspberry Pi 4B",
         "role": "Borscht Tracker V3", "units": "40,000+",
         "manufacturer": "Raspberry Pi Ltd", "country": "UK", "source": "static"},
        {"weapon": "Geran-5", "component": "Raspberry Pi",
         "role": "Tracker + 3G/4G modem", "units": "",
         "manufacturer": "Raspberry Pi Ltd", "country": "UK", "source": "static"},
        {"weapon": "Molniya-2R", "component": "Raspberry Pi 5",
         "role": "Reconnaissance computer", "units": "",
         "manufacturer": "Raspberry Pi Ltd", "country": "UK", "source": "static"},
        {"weapon": "FPV (various)", "component": "Allwinner H616",
         "role": "Grape Pi 1 (machine vision)", "units": "",
         "manufacturer": "Allwinner Technology", "country": "China", "source": "static"},
        {"weapon": "Shahed-136 (Geran-2)", "component": "STM32 MCU",
         "role": "Flight controller", "units": "",
         "manufacturer": "STMicroelectronics", "country": "Switzerland", "source": "static"},
        {"weapon": "Lancet-3", "component": "Sony IMX camera sensor",
         "role": "Target acquisition", "units": "",
         "manufacturer": "Sony", "country": "Japan", "source": "static"},
        {"weapon": "Shahed-107", "component": "Chinese FPV motor (XV 540 KV)",
         "role": "Propulsion", "units": "",
         "manufacturer": "Telefly Telecommunications", "country": "China", "source": "static"},
        {"weapon": "Feniks UAV", "component": "QIR50T gyro-stabilized system",
         "role": "Stabilization/targeting", "units": "",
         "manufacturer": "Unknown Chinese OEM", "country": "China", "source": "static"},
        {"weapon": "Geran-3", "component": "Telefly JT80 turbojet engine",
         "role": "Propulsion", "units": "",
         "manufacturer": "Telefly Telecommunications Equipment Co.", "country": "China", "source": "static"},
    ]


def analyze_diversion(db):
    """Cross-reference Forge components against known GUR teardown findings."""
    flags = []

    # Fetch GUR data — live if available, cached or static as fallback
    gur_findings = fetch_gur_live()

    # Check if any Forge companion computers share silicon with diverted components
    cc = db.get("companion_computers", [])
    for finding in gur_findings:
        comp = finding["component"].lower()
        for board in cc:
            board_name = (board.get("name") or "").lower()
            board_proc = (board.get("processor") or "").lower()
            if ("raspberry" in comp and "raspberry" in board_name) or \
               ("raspberry" in comp and "rpi" in board_proc) or \
               ("allwinner" in comp and "allwinner" in board_proc):
                flags.append({
                    "id": flag_id(f"diversion-{finding['weapon']}-{board.get('name','')}"),
                    "timestamp": now,
                    "flag_type": "diversion_risk",
                    "severity": "critical",
                    "title": f"Diversion risk: {finding['component']} found in {finding['weapon']}",
                    "detail": (
                        f"GUR teardown confirmed {finding['component']} used as '{finding['role']}' in {finding['weapon']}. "
                        f"{finding.get('units', 'Unknown quantity')} units reportedly diverted. "
                        f"Forge DB contains '{board.get('name', '')}' using same silicon family — "
                        f"shared supply chain with verified diversion pipeline."
                    ),
                    "confidence": 0.93,
                    "prediction": "Gray market premium persists. DRAM-driven price hikes may slow diversion as cost-benefit shifts, but active procurement pipelines remain.",
                    "platform_id": None,
                    "component_id": finding["component"].lower().replace(" ", "-"),
                    "data_sources": ["gur_war_sanctions", "forge_parts_db"],
                })
                break  # One flag per GUR finding

    # Always add the primary GUR diversion flags — these are verified intelligence
    # regardless of whether Forge DB has matching boards
    verified_diversions = [
        {
            "title": "RPi 4B confirmed in Geran-2/3 'Borscht' tracker — 40,000+ units diverted",
            "detail": (
                "GUR War & Sanctions portal and Ukrainian military intelligence confirmed "
                "Raspberry Pi 4B as the core of the 'Borscht Tracker V3' in Geran-2 (Shahed-136) "
                "and Geran-3 (Shahed-238) attack drones. Reports indicate 40,000+ units procured "
                "via gray market channels. RPi CEO Eben Upton acknowledged use in Russian drones "
                "and tightened end-use requirements for China sales. "
                "Cross-reference: RPi CM4 used by Freefly Astro (Blue UAS) and custom ArduPilot builds."
            ),
            "component_id": "raspberry-pi-4b",
        },
        {
            "title": "RPi 5 confirmed in Molniya-2R reconnaissance drone",
            "detail": (
                "GUR documented RPi 5 integrated alongside Chinese Mini PC F8 (rebranded as 'Raskat') "
                "running Windows 11 in the Molniya-2R reconnaissance UAV. The Molniya-2R is the "
                "recon variant of the kamikaze FPV drone, used for monitoring Ukrainian positions "
                "and strike adjustment. Confirms active, ongoing procurement of latest-gen RPi hardware "
                "despite tightened export controls."
            ),
            "component_id": "raspberry-pi-5",
        },
        {
            "title": "RPi tracker with mesh networking in Geran-5 jet drone",
            "detail": (
                "Russia's Geran-5 (6m wingspan, jet-powered, 90kg warhead, 1000km range) uses "
                "a 12-channel Kometa satellite navigation system and a tracker based on RPi "
                "with 3G/4G modems. The Geran-5 also features XK-F358 mesh network modems "
                "enabling 'chain control' — multiple drones in a salvo maintaining comms. "
                "This represents escalation from simple GPS-guided to mesh-networked swarm capability, "
                "all built on commercially available SBCs."
            ),
            "component_id": "raspberry-pi",
        },
    ]
    for vd in verified_diversions:
        fid = flag_id(f"gur-verified-{vd['component_id']}")
        if not any(f["id"] == fid for f in flags):
            flags.append({
                "id": fid,
                "timestamp": now,
                "flag_type": "diversion_risk",
                "severity": "critical",
                "title": vd["title"],
                "detail": vd["detail"],
                "confidence": 0.94,
                "prediction": "RPi gray market premium in China remains elevated (30-50% above MSRP). Active procurement pipeline confirmed by multiple intelligence sources.",
                "platform_id": None,
                "component_id": vd["component_id"],
                "data_sources": ["gur_war_sanctions", "euromaidanpress", "united24media", "heise"],
            })

    return flags


# ──────────────────────────────────────────
# 7. GENERATE PREDICTIONS
# ──────────────────────────────────────────

def generate_predictions(blue_count, ndaa_count, db):
    """Generate supply chain predictions based on real Forge data."""
    preds = []
    cc = db.get("companion_computers", [])
    mesh = db.get("mesh_radios", [])

    # Count Jetson boards
    jetson_boards = [c for c in cc if "jetson" in (c.get("processor") or "").lower()]
    qrb_boards = [c for c in cc if "qrb5165" in (c.get("processor") or "").lower()]

    preds.append({
        "timeframe": "Q3 2026",
        "event": f"Jetson Orin NX allocation-only for defense ({len(jetson_boards)} boards in Forge DB depend on Jetson)",
        "probability": 0.65,
        "impact": "critical",
        "drivers": [
            f"{blue_count} Blue UAS platforms scaling simultaneously",
            f"{len(jetson_boards)} companion boards use Jetson silicon",
            "DRAM pricing pressure (AI datacenter competition)",
            "NVIDIA AI priority over embedded/edge",
        ],
        "model": "forge_bom_analysis + supply_extrapolation",
        "last_updated": now,
    })

    preds.append({
        "timeframe": "Q2-Q3 2026",
        "event": "STM32H7 becomes allocated for defense FPV production",
        "probability": 0.72,
        "impact": "high",
        "drivers": [
            "Drone Dominance FPV program scaling (Neros Archer 2,200+/mo)",
            f"{db.get('flight_controllers', []).__len__()} FCs in Forge DB — majority STM32",
            "FPV commercial + defense demand on same MCU supply",
        ],
        "model": "forge_bom_analysis",
        "last_updated": now,
    })

    preds.append({
        "timeframe": "Q3 2026",
        "event": f"Mesh radio supply bottleneck — only {len(mesh)} options tracked, limited NDAA-compliant sources",
        "probability": 0.71,
        "impact": "high",
        "drivers": [
            "Multi-vehicle Blue UAS programs (Lattice Mesh, Replicator)",
            f"Only {len(mesh)} mesh radios in Forge DB",
            "Doodle Labs + Silvus dominate Blue UAS mesh — concentration risk",
        ],
        "model": "forge_bom_analysis + concentration_risk",
        "last_updated": now,
    })

    preds.append({
        "timeframe": "Q4 2026",
        "event": "RPi gray market premium exceeds 50% in China",
        "probability": 0.58,
        "impact": "medium",
        "drivers": [
            "DRAM crunch continues through 2027",
            "Active diversion pipeline (GUR confirmed 40K+ units)",
            "RPi price hikes cascade (Pi 5 8GB now $95)",
        ],
        "model": "price_anomaly + diversion_tracking",
        "last_updated": now,
    })

    preds.append({
        "timeframe": "H2 2026",
        "event": "FLIR Boson 640 allocation tightens following next Ukraine USAI package",
        "probability": 0.84,
        "impact": "high",
        "drivers": [
            "AeroVironment Switchblade 600 production ramp",
            "Ukraine USAI packages (6-week lag correlation with Boson lead times)",
            "Limited 640-resolution thermal alternatives",
        ],
        "model": "cross_correlation + contract_signal",
        "last_updated": now,
    })

    preds.append({
        "timeframe": "2027",
        "event": f"QRB5165 successor enters Blue UAS Framework ({len(qrb_boards)} boards currently depend on QRB5165)",
        "probability": 0.82,
        "impact": "medium",
        "drivers": [
            "ModalAI next-gen roadmap",
            f"{len(qrb_boards)} companion boards use QRB5165 in Forge DB",
            "Edge AI performance requirements increasing",
        ],
        "model": "product_lifecycle",
        "last_updated": now,
    })

    return preds


# ──────────────────────────────────────────
# 7. SOFTWARE ECOSYSTEM TRACKING
# ──────────────────────────────────────────

# Maps software platforms → hardware dependencies → manufacturers
# When a software company wins a contract, the hardware they run on gets demand pressure

SOFTWARE_ECOSYSTEM = [
    {
        "name": "Shield AI Hivemind",
        "company": "Shield AI",
        "type": "autonomy_os",
        "description": "AI pilot + swarm coordination. EdgeOS middleware, Hivemind Pilot, Commander C2. GPS/comms-denied capable.",
        "hardware_deps": ["NVIDIA Jetson Orin", "Hivemind ASIC"],
        "platforms_integrated": ["Shield AI V-BAT", "Anduril YFQ-44A (Fury CCA)", "MQ-20 Avenger", "Destinus Hornet", "Destinus Ruta", "NGC Talon IQ"],
        "contracts": ["USAF CCA Increment 1 (YFQ-44A)", "AFSOC STRATFI", "Ukraine Brave1", "Taiwan NCSIST", "ST Engineering Singapore"],
        "combat_deployed": True,
        "combat_note": "200+ flights in Ukraine on V-BAT, 200+ Russian targets identified",
    },
    {
        "name": "Gambit Autonomy",
        "company": "Gambit",
        "type": "autonomy_orchestration",
        "description": "Hardware-agnostic autonomy orchestration. Multi-robot coordination, adaptive intelligence, cross-platform (air/land/sea).",
        "hardware_deps": ["Qualcomm QRB5165 (via VOXL 2)", "ModalAI VOXL SDK"],
        "platforms_integrated": ["ModalAI Seeker", "ModalAI VOXL 2 ecosystem", "third-party VOXL SDK vehicles"],
        "contracts": ["USAF contract (>$500 combined)", "CENTCOM multi-sensor fusion", "ModalAI partnership (Mar 2026)"],
        "combat_deployed": False,
        "combat_note": "",
    },
    {
        "name": "Swarmer",
        "company": "Swarmer (getswarmer.com)",
        "type": "swarm_autonomy",
        "description": "Combat-proven collaborative autonomy. Single operator → hundreds of drones. AI-driven navigation, scalable swarm ops.",
        "hardware_deps": ["Various FPV/tactical FCs", "Companion computers"],
        "platforms_integrated": ["Multiple tactical platforms"],
        "contracts": ["Combat-deployed (details classified)"],
        "combat_deployed": True,
        "combat_note": "Combat-proven collaborative autonomy software",
    },
    {
        "name": "Anduril Lattice",
        "company": "Anduril Industries",
        "type": "c2_mesh",
        "description": "AI-powered C2 and sensor fusion platform. Connects autonomous systems into unified kill chain. Mesh networking, threat detection.",
        "hardware_deps": ["NVIDIA Jetson AGX Orin", "Lattice CertusPro-NX FPGA", "Doodle Labs mesh radios"],
        "platforms_integrated": ["Anduril Ghost-X", "Anduril Altius", "Anduril Anvil (C-UAS)", "Sentry Tower"],
        "contracts": ["Replicator Phase 2", "USSOCOM MFWS", "Lattice Mesh network", "Taiwan integration"],
        "combat_deployed": True,
        "combat_note": "Deployed in USCENTCOM, USINDOPACOM theaters",
    },
    {
        "name": "Skydio Autonomy Engine",
        "company": "Skydio",
        "type": "visual_autonomy",
        "description": "Visual SLAM + obstacle avoidance + 3D scanning. Computer vision-first autonomy. Edge AI on Jetson.",
        "hardware_deps": ["NVIDIA Jetson Orin NX", "Custom Skydio ASIC", "Sony IMX sensors"],
        "platforms_integrated": ["Skydio X10D", "Skydio X2D"],
        "contracts": ["USSOCOM", "CBP Replicator", "DOI fleet", "US Army SRR"],
        "combat_deployed": False,
        "combat_note": "",
    },
    {
        "name": "Auterion / PX4",
        "company": "Auterion",
        "type": "flight_os",
        "description": "Enterprise PX4-based flight OS. Skynode hardware + AuterionOS. Open standards, MAVLink native.",
        "hardware_deps": ["Qualcomm QRB5165", "STM32H7 (Pixhawk)"],
        "platforms_integrated": ["Quantum Systems Trinity", "Freefly Astro", "Various Blue UAS Framework integrators"],
        "contracts": ["Blue UAS Framework component", "NATO interop"],
        "combat_deployed": True,
        "combat_note": "PX4 ecosystem deployed on multiple platforms in Ukraine",
    },
    {
        "name": "Palladyne AI",
        "company": "Palladyne AI (formerly Sarcos)",
        "type": "autonomy_middleware",
        "description": "Platform-agnostic autonomy for heterogeneous robot fleets. Swarm integration, multi-domain coordination.",
        "hardware_deps": ["Various companion computers"],
        "platforms_integrated": ["Draganfly drones", "Various ground/air platforms"],
        "contracts": ["Draganfly swarm integration (Mar 2026)"],
        "combat_deployed": False,
        "combat_note": "",
    },
]


def analyze_software(db):
    """Analyze software ecosystem — map software to hardware dependencies and manufacturers."""
    flags = []
    models = db.get("drone_models", [])

    # Build manufacturer → platforms map from Forge DB
    mfr_platforms = {}
    for m in models:
        mfr = (m.get("manufacturer") or "").strip()
        if mfr:
            mfr_platforms.setdefault(mfr, []).append(m)

    print(f"  Software platforms tracked: {len(SOFTWARE_ECOSYSTEM)}")
    print(f"  Manufacturers in Forge DB: {len(mfr_platforms)}")

    # Track hardware demand driven by software contracts
    hw_demand_from_sw = {}  # hardware_dep → [software platforms driving demand]

    for sw in SOFTWARE_ECOSYSTEM:
        for hw in sw["hardware_deps"]:
            hw_demand_from_sw.setdefault(hw, []).append(sw["name"])

        # Flag combat-deployed software with active scaling
        if sw["combat_deployed"] and sw["contracts"]:
            flags.append({
                "id": flag_id(f"sw-combat-{sw['name']}"),
                "timestamp": now,
                "flag_type": "contract_signal",
                "severity": "warning" if len(sw["contracts"]) >= 3 else "info",
                "title": f"{sw['name']} ({sw['company']}) — combat-deployed, {len(sw['contracts'])} active contracts",
                "detail": (
                    f"{sw['name']}: {sw['description']} "
                    f"Combat status: {sw['combat_note']}. "
                    f"Contracts: {', '.join(sw['contracts'][:4])}. "
                    f"Hardware dependencies: {', '.join(sw['hardware_deps'])}. "
                    f"Integrated on: {', '.join(sw['platforms_integrated'][:4])}."
                ),
                "confidence": 0.92,
                "prediction": f"Contract wins for {sw['company']} drive hardware demand for {', '.join(sw['hardware_deps'][:2])}. Monitor distributor lead times.",
                "platform_id": None,
                "component_id": sw["hardware_deps"][0].lower().replace(" ", "-") if sw["hardware_deps"] else None,
                "data_sources": ["forge_industry_intel", "defense_contracts", "software_ecosystem"],
            })

    # Flag hardware with multiple software stacks competing for it
    for hw, sw_list in hw_demand_from_sw.items():
        if len(sw_list) >= 2:
            flags.append({
                "id": flag_id(f"sw-hw-convergence-{hw}"),
                "timestamp": now,
                "flag_type": "correlation",
                "severity": "warning" if len(sw_list) >= 3 else "info",
                "title": f"{len(sw_list)} autonomy stacks depend on {hw} — compound demand",
                "detail": (
                    f"Software convergence on {hw}: {', '.join(sw_list)}. "
                    f"Each software platform winning new contracts drives additional hardware demand. "
                    f"When Shield AI wins a CCA contract, Anduril wins Replicator, and Skydio wins SRR — "
                    f"they all pull from the same {hw} supply."
                ),
                "confidence": 0.87,
                "prediction": f"{hw} supply chain feels compound pressure from multiple software-driven scaling programs.",
                "platform_id": None,
                "component_id": hw.lower().replace(" ", "-"),
                "data_sources": ["software_ecosystem", "forge_bom"],
            })

    return flags, hw_demand_from_sw


# ──────────────────────────────────────────
# 7b. MANUFACTURER-SPECIFIC ANALYSIS
# ──────────────────────────────────────────

def analyze_manufacturers(db, sw_hw_demand):
    """Map specific UAS manufacturers to their component dependencies and software stacks."""
    flags = []
    models = db.get("drone_models", [])

    # Key manufacturers to track — map to their known SBC/software stacks
    MFR_INTEL = {
        "Skydio": {
            "software": ["Skydio Autonomy Engine"],
            "key_hw": ["NVIDIA Jetson Orin NX", "Sony IMX sensors"],
            "note": "Visual autonomy leader. X10D is Blue UAS. Largest enterprise drone fleet in US Gov.",
        },
        "Shield AI": {
            "software": ["Shield AI Hivemind"],
            "key_hw": ["NVIDIA Jetson Orin", "Hivemind ASIC"],
            "note": "Hivemind on V-BAT, CCA YFQ-44A, Ukraine. $2.7B+ valuation.",
        },
        "Anduril Industries": {
            "software": ["Anduril Lattice"],
            "key_hw": ["NVIDIA Jetson AGX Orin", "Lattice FPGA", "Doodle Labs mesh"],
            "note": "Ghost-X, Altius, Anvil. Replicator Phase 2. Lattice C2 platform.",
        },
        "Teal Drones / Red Cat Holdings": {
            "software": ["ModalAI VOXL SDK", "Gambit (via ModalAI)"],
            "key_hw": ["Qualcomm QRB5165", "FLIR Lepton/Hadron"],
            "note": "Teal 2, Black Widow (SRR Tranche 2). FPV + ISR. Drone Dominance.",
        },
        "ModalAI": {
            "software": ["ModalAI VOXL SDK", "Gambit Autonomy"],
            "key_hw": ["Qualcomm QRB5165"],
            "note": "VOXL 2 is Blue UAS Framework autopilot. Seeker/Stinger for SRR.",
        },
        "Neros Technologies": {
            "software": ["Custom (ELRS + Betaflight/ArduPilot)"],
            "key_hw": ["STM32H7", "ESP32-S3", "ELRS 900MHz"],
            "note": "Archer FPV. Drone Dominance at scale — 2,200+/mo production.",
        },
        "AeroVironment": {
            "software": ["Proprietary AV autonomy"],
            "key_hw": ["Custom AV SoC", "Xilinx FPGA", "FLIR Boson 640"],
            "note": "Switchblade 600. Major Ukraine supplier. USSOCOM contracts.",
        },
        "Freefly Systems": {
            "software": ["PX4 + Herelink"],
            "key_hw": ["RPi CM4", "Herelink v2"],
            "note": "Astro is Blue UAS. Open architecture. DOI/USGS mapping.",
        },
        "Parrot": {
            "software": ["Parrot FreeFlight SDK"],
            "key_hw": ["Parrot P7 SoC", "FLIR Boson 320"],
            "note": "ANAFI USA. Blue UAS. French-made. Army SRR legacy.",
        },
    }

    for mfr_name, intel in MFR_INTEL.items():
        # Find this manufacturer's platforms in Forge DB
        mfr_models = [m for m in models if mfr_name.lower() in (m.get("manufacturer") or "").lower()]
        blue_models = [m for m in mfr_models if m.get("compliance", {}).get("blue_uas")]
        ndaa_models = [m for m in mfr_models if m.get("compliance", {}).get("ndaa_compliant")]

        if not mfr_models:
            continue

        platform_names = [m.get("name", "") for m in mfr_models[:5]]

        flags.append({
            "id": flag_id(f"mfr-{mfr_name}"),
            "timestamp": now,
            "flag_type": "contract_signal",
            "severity": "info",
            "title": f"{mfr_name}: {len(mfr_models)} platforms in Forge DB ({len(blue_models)} Blue UAS)",
            "detail": (
                f"Manufacturer: {mfr_name}. {intel['note']} "
                f"Platforms: {', '.join(platform_names)}. "
                f"Software: {', '.join(intel['software'])}. "
                f"Key hardware dependencies: {', '.join(intel['key_hw'])}. "
                f"Forge DB: {len(mfr_models)} total, {len(blue_models)} Blue UAS, {len(ndaa_models)} NDAA."
            ),
            "confidence": 0.95,
            "prediction": f"Production scaling at {mfr_name} directly impacts demand for {', '.join(intel['key_hw'][:2])}.",
            "platform_id": mfr_models[0].get("pid") if mfr_models else None,
            "component_id": intel["key_hw"][0].lower().replace(" ", "-") if intel["key_hw"] else None,
            "data_sources": ["forge_parts_db", "forge_compliance", "software_ecosystem"],
        })

    return flags


# ──────────────────────────────────────────
# 8. COUNTER-UAS TRACKING
# ──────────────────────────────────────────

CUAS_COMPANIES = [
    {"name": "DroneShield", "hq": "Australia/US", "products": ["RfPatrol", "DroneGun", "DroneSentry"],
     "hw_deps": ["SDR modules", "NVIDIA Jetson (AI detection)", "FPGA signal processing"],
     "contracts": ["$6.2M Asia-Pacific military (Mar 2026)", "FEMA $250M C-UAS grant program", "US Army fixed-site"],
     "note": "Largest C-UAS customer base globally, 955+ protected sites"},
    {"name": "Dedrone (Axon)", "hq": "US", "products": ["DedroneTracker.AI", "DedroneRapidResponse"],
     "hw_deps": ["RF sensors", "Radar modules", "GPU compute (AI classification)"],
     "contracts": ["Axon acquisition", "FAA integration", "Fortune 500 sites"],
     "note": "300-drone identification database. Sensor fusion platform."},
    {"name": "Epirus", "hq": "US", "products": ["Leonidas HPM", "SmartPower"],
     "hw_deps": ["GaN amplifiers", "Custom power electronics", "FPGA"],
     "contracts": ["JIATF C-UAS contract (Mar 2026)", "GDLS/Kodiak autonomous HPM integration"],
     "note": "High-power microwave directed energy. Defeats drone swarms."},
    {"name": "D-Fend Solutions", "hq": "Israel/US", "products": ["EnforceAir"],
     "hw_deps": ["SDR modules", "RF analysis compute"],
     "contracts": ["US federal agencies", "Airport protection"],
     "note": "Cyber-takeover approach — hijacks drone control link."},
    {"name": "Anduril (Anvil/Sentry)", "hq": "US", "products": ["Anvil interceptor", "Sentry Tower"],
     "hw_deps": ["NVIDIA Jetson AGX Orin", "Lattice FPGA", "Doodle Labs mesh"],
     "contracts": ["Replicator", "USCENTCOM", "USINDOPACOM"],
     "note": "Kinetic C-UAS interceptor + AI sensor tower. Lattice C2 backbone."},
    {"name": "L3Harris", "hq": "US", "products": ["Counter-UAS systems", "MANET radios"],
     "hw_deps": ["Custom RF", "FPGA", "Signal processing ASICs"],
     "contracts": ["C-UAS production ramp (Mar 2026)", "JIATF"],
     "note": "Major defense prime ramping C-UAS production."},
]


def analyze_cuas(db):
    """Track Counter-UAS companies — they compete for the same components as drone makers."""
    flags = []
    print(f"  C-UAS companies tracked: {len(CUAS_COMPANIES)}")

    # Shared hardware between C-UAS and UAS
    shared_hw = {}
    for c in CUAS_COMPANIES:
        for hw in c["hw_deps"]:
            if any(k in hw.lower() for k in ["jetson", "fpga", "sdr", "nvidia"]):
                shared_hw.setdefault(hw, []).append(c["name"])

    for hw, companies in shared_hw.items():
        if len(companies) >= 2:
            flags.append({
                "id": flag_id(f"cuas-shared-{hw}"),
                "timestamp": now,
                "flag_type": "correlation",
                "severity": "info",
                "title": f"C-UAS and UAS share {hw} supply — {len(companies)} C-UAS companies competing",
                "detail": (
                    f"Counter-UAS companies ({', '.join(companies)}) use {hw}, "
                    f"same silicon as Blue UAS platforms. C-UAS scaling (FEMA $250M grant, "
                    f"JIATF contracts, FIFA World Cup security) adds demand to shared supply chain."
                ),
                "confidence": 0.80,
                "prediction": f"C-UAS + UAS compound demand on {hw}. Monitor as C-UAS contracts scale in 2026.",
                "platform_id": None,
                "component_id": hw.lower().replace(" ", "-"),
                "data_sources": ["cuas_tracking", "defense_contracts"],
            })

    # Flag major C-UAS contract awards
    for c in CUAS_COMPANIES:
        if len(c["contracts"]) >= 2:
            flags.append({
                "id": flag_id(f"cuas-{c['name']}"),
                "timestamp": now,
                "flag_type": "contract_signal",
                "severity": "info",
                "title": f"C-UAS: {c['name']} — {len(c['contracts'])} contracts, competes for drone supply chain",
                "detail": (
                    f"{c['name']} ({c['hq']}): {c['note']} "
                    f"Products: {', '.join(c['products'])}. "
                    f"Hardware deps: {', '.join(c['hw_deps'])}. "
                    f"Contracts: {', '.join(c['contracts'][:3])}."
                ),
                "confidence": 0.85,
                "prediction": f"{c['name']} scaling drives demand for {', '.join(c['hw_deps'][:2])}.",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["cuas_tracking", "defense_contracts"],
            })

    return flags


# ──────────────────────────────────────────
# 9. TARIFF & TRADE POLICY SIGNALS
# ──────────────────────────────────────────

POLICY_SIGNALS = [
    {
        "date": "2025-12",
        "event": "FCC blocks new foreign drone imports (equipment authorization freeze)",
        "impact": "Domestic Blue UAS demand spike — no new Chinese drone models can enter market",
        "affected": ["All Blue UAS manufacturers (positive)", "DJI/Autel (negative)"],
        "component_pressure": ["Jetson Orin NX", "QRB5165", "STM32H7"],
        "severity": "warning",
    },
    {
        "date": "2025-07",
        "event": "Drone Dominance executive order — 'Unleashing U.S. Military Drone Dominance'",
        "impact": "Massive defense FPV procurement acceleration. Blue UAS list transitions to DCMA.",
        "affected": ["Neros", "Teal", "ModalAI", "All FPV component suppliers"],
        "component_pressure": ["STM32H7", "ESP32-S3", "ELRS modules", "FLIR thermals"],
        "severity": "warning",
    },
    {
        "date": "2024",
        "event": "American Security Drone Act (ASDA) — bans DJI for federal use",
        "impact": "Federal agencies must transition to Blue UAS. Creates demand cliff for DJI, ramp for domestic.",
        "affected": ["DJI (banned)", "All Blue UAS manufacturers (demand surge)"],
        "component_pressure": ["All Blue UAS companion computers", "NDAA-compliant radios"],
        "severity": "info",
    },
    {
        "date": "2025-2026",
        "event": "DRAM tariff & AI datacenter priority — memory allocation shift",
        "impact": "AI datacenters get DRAM priority. SBC makers (RPi, embedded) pay more, wait longer.",
        "affected": ["RPi", "All SBC manufacturers", "Embedded system builders"],
        "component_pressure": ["RPi CM4/CM5", "Jetson modules", "LPDDR4X"],
        "severity": "warning",
    },
    {
        "date": "2026",
        "event": "US tariff escalation — 25%+ on Chinese electronics components",
        "impact": "Components sourced from China cost more. NDAA compliance pressure increases.",
        "affected": ["Any platform with Chinese-origin components", "Autel (CN/US hybrid)"],
        "component_pressure": ["Motors (many CN-made)", "ESCs", "Frames", "Batteries"],
        "severity": "warning",
    },
]


def analyze_policy():
    """Track tariff and trade policy signals that shift component demand."""
    flags = []
    print(f"  Policy signals tracked: {len(POLICY_SIGNALS)}")

    for p in POLICY_SIGNALS:
        flags.append({
            "id": flag_id(f"policy-{p['event'][:30]}"),
            "timestamp": now,
            "flag_type": "contract_signal",
            "severity": p["severity"],
            "title": f"Policy: {p['event'][:70]}",
            "detail": (
                f"Date: {p['date']}. {p['impact']} "
                f"Affected manufacturers: {', '.join(p['affected'][:4])}. "
                f"Component pressure: {', '.join(p['component_pressure'][:4])}."
            ),
            "confidence": 0.95,
            "prediction": f"Demand shift toward domestic/allied components. Monitor lead times for {', '.join(p['component_pressure'][:2])}.",
            "platform_id": None,
            "component_id": p["component_pressure"][0].lower().replace(" ", "-") if p["component_pressure"] else None,
            "data_sources": ["policy_tracker", "fcc", "congress"],
        })

    return flags


# ──────────────────────────────────────────
# 10. BOM COST INDEX
# ──────────────────────────────────────────

def analyze_bom_cost(db):
    """
    Track the total cost to build a reference Blue UAS-compliant drone.
    Uses Forge parts-db pricing to compute a BOM cost index.
    """
    flags = []

    # Reference Blue UAS BOM — what you'd need to build a compliant ISR quad
    reference_bom = {
        "Companion Computer (Jetson Orin NX)": 599,
        "Flight Controller (Pixhawk 6X / H7)": 300,
        "Thermal Camera (FLIR Lepton 3.5)": 250,
        "GNSS/RTK (u-blox ZED-F9P)": 189,
        "Mesh Radio (Doodle Labs entry)": 1800,
        "RC Link (NDAA-compliant)": 120,
        "Frame (US-manufactured)": 400,
        "Motors x4 (US/allied)": 280,
        "ESCs x4 (NDAA)": 200,
        "Battery (6S LiPo)": 120,
        "Propellers": 40,
        "Wiring/connectors": 50,
    }
    total = sum(reference_bom.values())

    # Compare to what a non-compliant (Chinese) build would cost
    non_compliant_bom = {
        "Companion (RPi/Orange Pi)": 80,
        "FC (Chinese F405)": 35,
        "Camera (generic)": 60,
        "GPS (BN-880)": 15,
        "Radio (ELRS standard)": 28,
        "RC Link (standard)": 40,
        "Frame (Chinese carbon)": 45,
        "Motors x4 (Chinese)": 80,
        "ESCs x4 (Chinese)": 60,
        "Battery": 60,
        "Props": 12,
        "Wiring": 15,
    }
    non_compliant_total = sum(non_compliant_bom.values())
    premium_pct = ((total - non_compliant_total) / non_compliant_total) * 100

    print(f"  Blue UAS BOM index: ${total:,} ({premium_pct:.0f}% premium over non-compliant)")

    flags.append({
        "id": flag_id("bom-index-blue-uas"),
        "timestamp": now,
        "flag_type": "price_anomaly",
        "severity": "warning",
        "title": f"Blue UAS BOM cost index: ${total:,} — {premium_pct:.0f}% premium over non-compliant build",
        "detail": (
            f"Reference Blue UAS ISR quad BOM: ${total:,}. "
            f"Equivalent non-compliant build: ${non_compliant_total:,}. "
            f"Compliance premium: {premium_pct:.0f}%. "
            f"Largest cost drivers: mesh radio (${reference_bom['Mesh Radio (Doodle Labs entry)']:,}), "
            f"companion computer (${reference_bom['Companion Computer (Jetson Orin NX)']:,}), "
            f"frame (${reference_bom['Frame (US-manufactured)']:,}). "
            f"DRAM pricing and tariffs push this index higher each quarter."
        ),
        "confidence": 0.90,
        "prediction": f"BOM index trending up. DRAM + tariffs add ~8-15% YoY. At ${total:,}, cost barrier limits Blue UAS adoption by smaller agencies.",
        "platform_id": None,
        "component_id": "bom-index",
        "data_sources": ["forge_parts_db", "distributor_pricing"],
    })

    # Flag the mesh radio as the single biggest cost driver
    mesh_pct = (reference_bom["Mesh Radio (Doodle Labs entry)"] / total) * 100
    flags.append({
        "id": flag_id("bom-mesh-cost"),
        "timestamp": now,
        "flag_type": "price_anomaly",
        "severity": "info",
        "title": f"Mesh radio is {mesh_pct:.0f}% of Blue UAS BOM — single largest cost driver",
        "detail": (
            f"Doodle Labs entry-level mesh: ${reference_bom['Mesh Radio (Doodle Labs entry)']:,}. "
            f"Silvus MN Micro: $4,500-5,200. "
            f"This single component is {mesh_pct:.0f}% of the total ${total:,} BOM. "
            f"No low-cost NDAA-compliant alternative exists at MANET performance tier."
        ),
        "confidence": 0.92,
        "prediction": "Mesh radio cost is the biggest barrier to Blue UAS fleet scaling. Market opportunity for lower-cost NDAA mesh entrants.",
        "platform_id": None,
        "component_id": "mesh-radios",
        "data_sources": ["forge_parts_db", "bom_analysis"],
    })

    return flags


# ──────────────────────────────────────────
# 11. WORKFORCE & PRODUCTION CAPACITY
# ──────────────────────────────────────────

MFR_CAPACITY = [
    {"name": "Skydio", "employees": 800, "hq": "San Mateo, CA", "facilities": ["San Mateo HQ", "Manufacturing facility"],
     "est_monthly_capacity": 500, "recent_signal": "Raised $230M Series E. Scaling X10D production."},
    {"name": "Shield AI", "employees": 900, "hq": "San Diego, CA", "facilities": ["San Diego HQ", "Engineering center"],
     "est_monthly_capacity": 150, "recent_signal": "$2.7B+ valuation. Hivemind licensing to multiple platforms."},
    {"name": "Anduril", "employees": 3000, "hq": "Costa Mesa, CA", "facilities": ["Costa Mesa HQ", "Multiple manufacturing"],
     "est_monthly_capacity": 300, "recent_signal": "$14B+ valuation. Arsenal-1 factory planned. Replicator Phase 2."},
    {"name": "Red Cat / Teal", "employees": 200, "hq": "Salt Lake City, UT", "facilities": ["SLC manufacturing"],
     "est_monthly_capacity": 600, "recent_signal": "SRR Tranche 2 winner. Drone Dominance. Scaling FPV production."},
    {"name": "Neros Technologies", "employees": 50, "hq": "Los Angeles, CA", "facilities": ["LA manufacturing"],
     "est_monthly_capacity": 2500, "recent_signal": "Drone Dominance FPV at scale. 2,200+/mo claimed."},
    {"name": "AeroVironment", "employees": 6000, "hq": "Arlington, VA", "facilities": ["Multiple US facilities", "Pocomoke City MD"],
     "est_monthly_capacity": 800, "recent_signal": "Switchblade 600 production ramp. Major Ukraine supplier."},
    {"name": "ModalAI", "employees": 150, "hq": "San Diego, CA", "facilities": ["San Diego assembly (USA)"],
     "est_monthly_capacity": 400, "recent_signal": "VOXL 2 Blue UAS Framework. Seeker for SRR. Gambit partnership."},
    {"name": "Freefly Systems", "employees": 80, "hq": "Woodinville, WA", "facilities": ["Woodinville HQ"],
     "est_monthly_capacity": 150, "recent_signal": "Astro Blue UAS. DOI/USGS fleet contracts."},
]


def analyze_capacity():
    """Assess manufacturer production capacity vs contract demands."""
    flags = []
    print(f"  Manufacturers with capacity data: {len(MFR_CAPACITY)}")

    for mfr in MFR_CAPACITY:
        # Flag capacity risk: small team + large contracts
        units_per_employee = mfr["est_monthly_capacity"] / max(mfr["employees"], 1)
        if units_per_employee > 20:  # High output per employee = lean/risky
            flags.append({
                "id": flag_id(f"capacity-lean-{mfr['name']}"),
                "timestamp": now,
                "flag_type": "supply_constraint",
                "severity": "warning",
                "title": f"{mfr['name']}: {mfr['est_monthly_capacity']}/mo capacity with {mfr['employees']} employees — lean operation",
                "detail": (
                    f"{mfr['name']} ({mfr['hq']}): ~{mfr['est_monthly_capacity']} units/mo with "
                    f"{mfr['employees']} employees ({units_per_employee:.0f} units/employee/mo). "
                    f"Facilities: {', '.join(mfr['facilities'])}. "
                    f"Signal: {mfr['recent_signal']} "
                    f"High output-per-employee ratio suggests limited surge capacity."
                ),
                "confidence": 0.72,
                "prediction": f"Production scaling risk if contract demand exceeds capacity. Workforce expansion or second shift needed.",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["workforce_analysis", "capacity_estimate"],
            })

    return flags


# ──────────────────────────────────────────
# 12. DRAM PRICING SIGNAL
# ──────────────────────────────────────────

def analyze_dram():
    """
    Track DRAM pricing impact on SBC/companion computer costs.
    In production: scrape TrendForce weekly data.
    For now: use known data points from RPi earnings + research.
    """
    flags = []

    # Known DRAM data points from research
    dram_data = {
        "ddr4_8gb_contract": 3.25,      # $/unit, Q1 2026
        "lpddr4x_contract": 3.80,       # $/unit
        "qoq_increase": 8.5,            # % Q/Q
        "yoy_increase": 22,             # % Y/Y approx
        "forecast": "Elevated through 2027, possible easing 2028",
        "driver": "AI datacenter demand consuming production capacity",
        "rpi_impact": "RPi 5 8GB: $80→$95, 16GB: $120→$145",
        "jetson_impact": "Orin NX 16GB: $599→$649",
    }

    print(f"  DRAM: DDR4 ${dram_data['ddr4_8gb_contract']}/unit, +{dram_data['qoq_increase']}% QoQ")

    flags.append({
        "id": flag_id("dram-pricing-q1-2026"),
        "timestamp": now,
        "flag_type": "price_anomaly",
        "severity": "warning",
        "title": f"DRAM pricing: +{dram_data['qoq_increase']}% QoQ, +{dram_data['yoy_increase']}% YoY — cascading to SBC costs",
        "detail": (
            f"DDR4 8Gb contract: ${dram_data['ddr4_8gb_contract']}/unit. "
            f"LPDDR4X: ${dram_data['lpddr4x_contract']}/unit. "
            f"QoQ increase: {dram_data['qoq_increase']}%. "
            f"Driver: {dram_data['driver']}. "
            f"Impact: {dram_data['rpi_impact']}. {dram_data['jetson_impact']}. "
            f"Forecast: {dram_data['forecast']}. "
            f"Morgan Stanley projects $620B AI infrastructure spend in 2026 (up from $470B in 2025)."
        ),
        "confidence": 0.93,
        "prediction": "DRAM pressure continues through 2027. Every SBC and companion computer in the Forge DB is affected. No relief until new fab capacity comes online ~2028.",
        "platform_id": None,
        "component_id": "dram-lpddr4x",
        "data_sources": ["trendforce", "rpi_earnings", "morgan_stanley"],
    })

    return flags, dram_data


# ──────────────────────────────────────────
# 13. ALLIED NATION SUPPLY CHAIN
# ──────────────────────────────────────────

ALLIED_SUPPLY = {
    "Taiwan": {
        "critical_components": ["Qualcomm QRB5165 (fab)", "TSMC node for Jetson", "Ambarella SoCs"],
        "risk_level": "high",
        "risk_factor": "Cross-strait tensions. TSMC concentration. Single point of failure for all advanced chips.",
        "blue_uas_platforms": ["All Jetson-based", "All QRB5165-based", "All Ambarella-based"],
    },
    "France": {
        "critical_components": ["Parrot P7 SoC", "Parrot platforms", "Safran sensors"],
        "risk_level": "low",
        "risk_factor": "NATO ally. Stable supply. EU export controls may tighten on dual-use.",
        "blue_uas_platforms": ["Parrot ANAFI USA"],
    },
    "Switzerland": {
        "critical_components": ["Wingtra platforms", "u-blox GNSS modules", "STMicroelectronics"],
        "risk_level": "low",
        "risk_factor": "Neutral nation. u-blox is critical GNSS supplier for many Blue UAS platforms.",
        "blue_uas_platforms": ["WingtraOne/WingtraRAY"],
    },
    "Germany": {
        "critical_components": ["Quantum Systems platforms", "STMicroelectronics (EU fabs)", "Bosch sensors"],
        "risk_level": "low",
        "risk_factor": "NATO ally. EU export controls. Strong manufacturing base.",
        "blue_uas_platforms": ["Quantum Systems Trinity"],
    },
    "Israel": {
        "critical_components": ["Hailo AI accelerators", "D-Fend C-UAS", "Various defense components"],
        "risk_level": "medium",
        "risk_factor": "Strong ally but regional instability. Hailo-8/10H AI chips used in drone vision systems.",
        "blue_uas_platforms": [],
    },
    "South Korea": {
        "critical_components": ["Samsung DRAM", "SK Hynix memory", "Samsung foundry"],
        "risk_level": "medium",
        "risk_factor": "Major DRAM supplier. Samsung/SK Hynix produce majority of global DRAM. North Korea tensions.",
        "blue_uas_platforms": ["Indirect — DRAM in all SBCs"],
    },
    "UK": {
        "critical_components": ["Raspberry Pi (design + Sony Wales fab)", "ARM architecture licenses"],
        "risk_level": "low",
        "risk_factor": "Five Eyes ally. RPi designed in Cambridge, manufactured in Wales. ARM (SoftBank-owned) licenses cores for all mobile SoCs.",
        "blue_uas_platforms": ["Freefly Astro (RPi CM4)", "Custom builds"],
    },
    "Japan": {
        "critical_components": ["Sony image sensors", "Renesas MCUs", "Sony RPi manufacturing (Wales)"],
        "risk_level": "low",
        "risk_factor": "Close ally. Sony IMX sensors dominate drone cameras. Renesas automotive MCUs.",
        "blue_uas_platforms": ["Skydio (Sony IMX)", "Most camera-equipped platforms"],
    },
}


def analyze_allied_supply(db):
    """Map geographic risk in the Blue UAS supply chain."""
    flags = []
    print(f"  Allied nations tracked: {len(ALLIED_SUPPLY)}")

    high_risk = {k: v for k, v in ALLIED_SUPPLY.items() if v["risk_level"] == "high"}
    medium_risk = {k: v for k, v in ALLIED_SUPPLY.items() if v["risk_level"] == "medium"}

    for nation, data in high_risk.items():
        flags.append({
            "id": flag_id(f"geo-risk-{nation}"),
            "timestamp": now,
            "flag_type": "supply_constraint",
            "severity": "critical",
            "title": f"Geographic risk: {nation} — {data['risk_level']} risk, critical to Blue UAS supply chain",
            "detail": (
                f"{nation}: {data['risk_factor']} "
                f"Critical components: {', '.join(data['critical_components'][:4])}. "
                f"Affected Blue UAS platforms: {', '.join(data['blue_uas_platforms'][:4])}."
            ),
            "confidence": 0.88,
            "prediction": f"Any disruption in {nation} cascades to {', '.join(data['critical_components'][:2])} supply for all Blue UAS programs.",
            "platform_id": None,
            "component_id": data["critical_components"][0].lower().replace(" ", "-") if data["critical_components"] else None,
            "data_sources": ["geopolitical_risk", "supply_chain_mapping"],
        })

    for nation, data in medium_risk.items():
        flags.append({
            "id": flag_id(f"geo-risk-{nation}"),
            "timestamp": now,
            "flag_type": "supply_constraint",
            "severity": "warning",
            "title": f"Geographic risk: {nation} — {data['risk_level']} risk ({', '.join(data['critical_components'][:2])})",
            "detail": (
                f"{nation}: {data['risk_factor']} "
                f"Critical components: {', '.join(data['critical_components'][:4])}."
            ),
            "confidence": 0.78,
            "prediction": f"Monitor {nation} stability. Component sourcing diversification recommended.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["geopolitical_risk", "supply_chain_mapping"],
        })

    return flags


# ──────────────────────────────────────────
# 13b. GOVERNMENT & DOD PROGRAMS
# ──────────────────────────────────────────

GOV_PROGRAMS = [
    # ── DoD Drone Programs ──
    {
        "name": "Drone Dominance Program (DDP)",
        "agency": "DoD / Under Secretary R&E",
        "status": "active — Phase 1 orders placed Mar 2026",
        "budget": "$1.4B congressional appropriation (FY25 reconciliation) + ongoing",
        "scope": "200,000+ small UAS by 2027. 30,000 by Jul 2026. Gauntlet competitive trials.",
        "platforms": ["Neros Archer", "PDW C100", "Multiple FPV vendors"],
        "component_demand": ["STM32H7", "ESP32-S3", "ELRS 900MHz", "FPV cameras", "LiPo batteries"],
        "category": "procurement",
        "impact": "critical",
    },
    {
        "name": "Replicator → DAWG (Defense Autonomous Warfare Group)",
        "agency": "DoD / SecDef",
        "status": "active — renamed from Replicator. Focus on larger autonomous systems.",
        "budget": "$500M+ (Replicator 1). Additional funding through Replicator 2.",
        "scope": "Thousands of attritable autonomous systems. All-domain. Replicator 2 focused on C-UAS.",
        "platforms": ["Anduril Ghost-X", "Anduril Altius", "Switchblade 600", "Dive-LD UUV"],
        "component_demand": ["Jetson AGX Orin", "FLIR Boson 640", "Doodle Labs mesh", "Lattice FPGA"],
        "category": "procurement",
        "impact": "critical",
    },
    {
        "name": "Army SRR (Short Range Reconnaissance)",
        "agency": "U.S. Army",
        "status": "active — Tranche 2 selection pending. 5,880 systems over 5 years.",
        "budget": "Program of record. Multi-year acquisition.",
        "scope": "Platoon-level ISR quad. <5 lbs. 30 min endurance. Selected: Skydio X10D, Teal Black Widow.",
        "platforms": ["Skydio X10D", "Teal Black Widow"],
        "component_demand": ["NVIDIA Jetson Orin NX", "Qualcomm QRB5165", "FLIR Lepton/Hadron"],
        "category": "procurement",
        "impact": "high",
    },
    {
        "name": "Army MRR (Medium Range Reconnaissance)",
        "agency": "U.S. Army",
        "status": "active — FY2026 budget requested 107 systems",
        "budget": "FY2026 budget line",
        "scope": "Company-level sUAS. 10km+ range, 30 min endurance.",
        "platforms": ["TBD — competitive"],
        "component_demand": ["Long-range datalinks", "Companion computers", "RTK GNSS"],
        "category": "procurement",
        "impact": "medium",
    },
    {
        "name": "Army FoSUAS (Family of Small UAS)",
        "agency": "U.S. Army",
        "status": "active — replacing RQ-11 Raven. Multiple tiers.",
        "budget": "Multi-year. Part of $1.4B reconciliation allocation.",
        "scope": "Fielding UAS 'in every Division by end of 2026' per SecDef memo.",
        "platforms": ["SRR winners", "MRR winners", "FTUAS candidates"],
        "component_demand": ["All Blue UAS components at scale"],
        "category": "procurement",
        "impact": "critical",
    },
    {
        "name": "Army FTUAS (Future Tactical UAS)",
        "agency": "U.S. Army PEO Aviation",
        "status": "active — Group 3 UAS replacement for Shadow.",
        "budget": "Major program of record",
        "scope": "Replacing RQ-7 Shadow. Longer range, VTOL, autonomous. Textron/L3Harris competing.",
        "platforms": ["Textron Aerosonde HQ", "L3Harris FVR-90"],
        "component_demand": ["Heavy-lift motors", "Tactical datalinks", "EO/IR payloads"],
        "category": "procurement",
        "impact": "high",
    },
    {
        "name": "USMC FPV Drone Program",
        "agency": "U.S. Marine Corps",
        "status": "active — $47M to Red Cat/Teal. RFI for <$4K FPV airframes.",
        "budget": "$47M+ initial",
        "scope": "FPV at scale for every Marine unit. Cost target: <$4,000/airframe.",
        "platforms": ["Teal 2", "Neros Archer", "Various FPV vendors"],
        "component_demand": ["STM32H7", "ELRS modules", "FPV cameras", "Walksnail/Caddx"],
        "category": "procurement",
        "impact": "high",
    },
    {
        "name": "USAF CCA (Collaborative Combat Aircraft)",
        "agency": "U.S. Air Force",
        "status": "active — Increment 1 flight demos 2026. Anduril YFQ-44A vs GA-ASI YFQ-42A.",
        "budget": "$5.8B (FY2025-2029 FYDP)",
        "scope": "Autonomous drone wingmen for F-35/NGAD. AI-enabled swarm combat.",
        "platforms": ["Anduril YFQ-44A (Fury)", "GA-ASI YFQ-42A"],
        "component_demand": ["Shield AI Hivemind", "NVIDIA Jetson (AI)", "Tactical mesh", "EW systems"],
        "category": "procurement",
        "impact": "critical",
    },
    # ── Counter-UAS Programs ──
    {
        "name": "JIATF-401 (Joint Interagency Task Force for C-UAS)",
        "agency": "DoD",
        "status": "active — established Aug 2025. Replicator 2 resources consolidated here.",
        "budget": "Replicator 2 budget + congressional funding",
        "scope": "Lead organization for C-sUAS. Homeland defense + force protection.",
        "platforms": ["Anduril Anvil", "Fortem DroneHunter", "Epirus Leonidas", "L3Harris C-UAS"],
        "component_demand": ["RF sensors", "SDR modules", "AI compute (detection)", "Directed energy"],
        "category": "counter_uas",
        "impact": "high",
    },
    {
        "name": "FEMA C-UAS Grant Program",
        "agency": "FEMA / DHS",
        "status": "active — $250M distributed to 11 World Cup sites",
        "budget": "$250M",
        "scope": "Counter-drone protection for FIFA 2026 World Cup venues + critical infrastructure.",
        "platforms": ["DroneShield", "Dedrone", "D-Fend", "Various C-UAS"],
        "component_demand": ["RF detection hardware", "Radar modules", "C2 compute"],
        "category": "counter_uas",
        "impact": "medium",
    },
    # ── Policy & Legislative ──
    {
        "name": "NDAA FY25 Section 1709 (Foreign Drone Ban)",
        "agency": "Congress / FCC",
        "status": "enacted — FCC implementing equipment authorization freeze",
        "budget": "Regulatory (no direct budget)",
        "scope": "Blocks new foreign-manufactured drone models from US market. Exemptions for Blue UAS.",
        "platforms": ["DJI (blocked)", "All domestic manufacturers (benefited)"],
        "component_demand": ["Demand shift to all domestic/NDAA components"],
        "category": "legislative",
        "impact": "critical",
    },
    {
        "name": "Drone Dominance Executive Order (Jul 2025)",
        "agency": "White House / SecDef",
        "status": "enacted — 'Unleashing U.S. Military Drone Dominance'",
        "budget": "Directs Pentagon spending priorities",
        "scope": "Rescinds restrictive drone policies. FAA BVLOS rulemaking. Domestic manufacturing priority.",
        "platforms": ["All domestic UAS manufacturers"],
        "component_demand": ["Broad demand acceleration across all Blue UAS components"],
        "category": "executive",
        "impact": "critical",
    },
    {
        "name": "ASDA (American Security Drone Act)",
        "agency": "Congress",
        "status": "enacted — bans DJI + covered entities for federal use",
        "budget": "Regulatory",
        "scope": "Federal agencies must transition to trusted/Blue UAS platforms.",
        "platforms": ["DJI (banned)", "All Blue UAS (demand surge)"],
        "component_demand": ["All Blue UAS companion computers", "NDAA radios", "Trusted sensors"],
        "category": "legislative",
        "impact": "high",
    },
    # ── Ukraine Security Assistance ──
    {
        "name": "Ukraine Security Assistance Initiative (USAI)",
        "agency": "DoD / State Dept",
        "status": "ongoing — multiple aid packages",
        "budget": "$50B+ total US military aid since 2022",
        "scope": "Includes Switchblade 600, various UAS, counter-drone systems, ammunition.",
        "platforms": ["Switchblade 600", "Various ISR drones"],
        "component_demand": ["FLIR Boson 640", "Custom AV SoC", "Xilinx FPGA", "Tactical batteries"],
        "category": "security_assistance",
        "impact": "high",
    },
    # ── Blue UAS Program ──
    {
        "name": "Blue UAS Cleared List (DCMA)",
        "agency": "DCMA (transferred from DIU Jul 2025)",
        "status": "active — 50+ platforms cleared. Continuous on-ramp.",
        "budget": "Evaluation/certification program",
        "scope": "Cybersecurity + supply chain vetting for federal drone procurement. Framework includes components.",
        "platforms": ["50+ cleared platforms", "14+ framework components"],
        "component_demand": ["All components must pass NDAA + cyber review"],
        "category": "certification",
        "impact": "high",
    },
]


def analyze_gov_programs(db):
    """Track government and DoD programs that drive UAS component demand."""
    flags = []
    models = db.get("drone_models", [])
    print(f"  Government programs tracked: {len(GOV_PROGRAMS)}")

    # Aggregate component demand across all programs
    component_demand_drivers = {}
    for prog in GOV_PROGRAMS:
        for comp in prog["component_demand"]:
            component_demand_drivers.setdefault(comp, []).append(prog["name"])

    # Flag programs by impact level
    for prog in GOV_PROGRAMS:
        severity = "warning" if prog["impact"] in ("critical", "high") else "info"

        # Count how many Forge DB platforms are involved
        involved = []
        for pname in prog["platforms"]:
            for m in models:
                if pname.lower() in (m.get("name") or "").lower():
                    involved.append(m.get("name", ""))
                    break

        flags.append({
            "id": flag_id(f"gov-{prog['name'][:30]}"),
            "timestamp": now,
            "flag_type": "contract_signal",
            "severity": severity,
            "title": f"{prog['agency']}: {prog['name']}",
            "detail": (
                f"Status: {prog['status']}. "
                f"Budget: {prog['budget']}. "
                f"Scope: {prog['scope']} "
                f"Platforms: {', '.join(prog['platforms'][:4])}. "
                f"Component demand: {', '.join(prog['component_demand'][:4])}."
                + (f" Forge DB matches: {', '.join(involved[:3])}." if involved else "")
            ),
            "confidence": 0.95,
            "prediction": f"Active program driving demand for {', '.join(prog['component_demand'][:2])}.",
            "platform_id": None,
            "component_id": prog["component_demand"][0].lower().replace(" ", "-") if prog["component_demand"] else None,
            "data_sources": ["gov_programs", "congress_gov", "defensescoop", "sam_gov"],
        })

    # Flag components with demand from 3+ government programs
    for comp, programs in component_demand_drivers.items():
        if len(programs) >= 3:
            flags.append({
                "id": flag_id(f"gov-compound-{comp}"),
                "timestamp": now,
                "flag_type": "procurement_spike",
                "severity": "warning",
                "title": f"{comp}: demand driven by {len(programs)} government programs simultaneously",
                "detail": (
                    f"{comp} is pulled by: {', '.join(programs[:5])}. "
                    f"Each program independently drives procurement volume. "
                    f"Combined demand creates compound pressure on a single component supply chain."
                ),
                "confidence": 0.88,
                "prediction": f"Multi-program demand makes {comp} a bottleneck candidate. Monitor distributor lead times.",
                "platform_id": None,
                "component_id": comp.lower().replace(" ", "-"),
                "data_sources": ["gov_programs", "supply_chain_analysis"],
            })

    return flags, component_demand_drivers




# ──────────────────────────────────────────
# 13c. FOREIGN UAS ECOSYSTEM INTELLIGENCE
# ──────────────────────────────────────────

FOREIGN_PROGRAMS = [
    {"country": "China", "program": "DJI global dominance + PLA drone swarm production",
     "significance": "80% global consumer share. NDAA ban shifts demand to domestic. PLA producing FPV at industrial scale.",
     "component_signals": ["DJI custom SoCs", "Chinese BLDC motors", "LiPo cells (CATL/BYD)", "Ambarella CV72"]},
    {"country": "Turkey", "program": "Baykar (TB2/TB3/Akinci/Kizilelma) — #2 drone exporter, 35+ customers",
     "significance": "Proved drone warfare doctrine in Libya, Nagorno-Karabakh, Ukraine. Building indigenous supply chain after Canada sensor embargo.",
     "component_signals": ["Rotax/TEI engines", "Aselsan EO/IR", "Ukrainian AI-322 engine (Kizilelma)"]},
    {"country": "Iran", "program": "Shahed mass production — supplying Russia at scale",
     "significance": "Drives gray market component demand. GUR teardowns show 15+ Western countries\'components despite sanctions.",
     "component_signals": ["Limbach L550E replicas", "Commercial GNSS", "Western chips via gray market", "RPi (diverted)"]},
    {"country": "Ukraine", "program": "Fastest-iterating FPV ecosystem — thousands/month, Brave1 accelerator",
     "significance": "Combat-testing drives global doctrine. Integrating Hivemind. Competes with US Drone Dominance for same FPV parts.",
     "component_signals": ["STM32 FCs", "ELRS/Crossfire", "Caddx/Walksnail cameras", "Chinese motors/ESCs"]},
    {"country": "EU/NATO", "program": "FCAS (€100B+), EuroDrone, Airbus Wingman, sovereignty push",
     "significance": "EU building indigenous drone capability to reduce US/Chinese dependency.",
     "component_signals": ["NanoXplore FPGAs", "Safran engines/sensors", "Thales electronics"]},
    {"country": "India", "program": "ideaForge + Solar Industries + Adani defense — indigenous drone push",
     "significance": "Rapidly building domestic capability. Nagastra-1 loitering munition deployed.",
     "component_signals": ["Indian electronics assembly", "Israeli technology transfer"]},
    {"country": "South Korea", "program": "KAI stealth UCAV + Samsung/SK Hynix DRAM supply",
     "significance": "Critical DRAM supplier for all SBCs globally. Stealth UCAV development.",
     "component_signals": ["Samsung DRAM", "SK Hynix memory", "Korean aerospace composites"]},
    {"country": "Australia", "program": "SYPAQ Corvo (cardboard drone, used in Ukraine) + MQ-28 Ghost Bat CCA",
     "significance": "Five Eyes ally. MQ-28 is CCA testbed feeding US/UK programs.",
     "component_signals": ["Boeing autonomy stack", "Australian composites"]},
    {"country": "Russia", "program": "Alabuga factory + Lancet + Orlan — mass drone production using diverted Western parts",
     "significance": "GUR tracks 5,534 foreign components across 190 Russian weapon systems. Drives diversion pipeline.",
     "component_signals": ["RPi (40K+ diverted)", "Chinese motors/ESCs", "Western MCUs via China/UAE"]},
    {"country": "Poland", "program": "WB Group Warmate/FlyEye — NATO eastern flank drone capability",
     "significance": "Polish drones combat-deployed. Poland investing €2B in anti-drone barrier.",
     "component_signals": ["European electronics", "NATO-interop datalinks"]},
    {"country": "Croatia", "program": "Orqa — EU-manufactured NDAA FPV ecosystem (FC, ESC, goggles)",
     "significance": "Only EU-manufactured complete FPV stack. NDAA-compliant. NATO ally.",
     "component_signals": ["STM32H7 (Orqa FC)", "IRONghost RC link", "Custom ESCs"]},
]


def analyze_foreign(db):
    """Track foreign UAS ecosystems and supply chain implications."""
    flags = []
    models = db.get("drone_models", [])
    country_platforms = {}
    for m in models:
        c = (m.get("country") or "Unknown").strip()
        country_platforms.setdefault(c, []).append(m)
    countries_in_db = len(country_platforms)
    non_us_count = sum(len(v) for k, v in country_platforms.items() if k.lower() not in ("usa", "united states"))
    print(f"  Foreign programs tracked: {len(FOREIGN_PROGRAMS)}")
    print(f"  Countries in Forge DB: {countries_in_db} ({non_us_count} non-US platforms)")

    for prog in FOREIGN_PROGRAMS:
        country = prog["country"]
        db_plats = []
        for c_key, plats in country_platforms.items():
            if country.lower() in c_key.lower():
                db_plats.extend(plats)
        sev = "warning" if country in ("China", "Russia", "Iran") else "info"
        flags.append({
            "id": flag_id(f"foreign-{country}-{prog['program'][:20]}"),
            "timestamp": now, "flag_type": "correlation", "severity": sev,
            "title": f"{country}: {prog['program'][:65]}",
            "detail": f"{prog['significance']} Components: {', '.join(prog['component_signals'][:4])}." + (f" Forge DB: {len(db_plats)} platforms." if db_plats else ""),
            "confidence": 0.85,
            "prediction": f"Monitor {country} UAS activity for supply chain implications.",
            "platform_id": None, "component_id": None,
            "data_sources": ["foreign_intel", "forge_parts_db"],
        })

    # Ukraine + US competing for same FPV parts
    ukr = country_platforms.get("Ukraine", [])
    if len(ukr) >= 10:
        flags.append({
            "id": flag_id("ukraine-us-fpv-competition"), "timestamp": now,
            "flag_type": "procurement_spike", "severity": "warning",
            "title": f"Ukraine ({len(ukr)} platforms) and US Drone Dominance compete for same FPV components",
            "detail": f"Both programs use STM32, ELRS, Caddx/Walksnail, Chinese motors/ESCs. Compound demand on shared FPV supply chain.",
            "confidence": 0.88, "prediction": "FPV component prices rise 10-20% from dual-program demand.",
            "platform_id": None, "component_id": "stm32h7",
            "data_sources": ["forge_parts_db", "foreign_intel"],
        })

    flags.append({
        "id": flag_id("global-landscape"), "timestamp": now,
        "flag_type": "correlation", "severity": "info",
        "title": f"Global UAS landscape: {countries_in_db} countries, {len(models)} platforms in Forge DB",
        "detail": f"42 countries tracked. Global proliferation means component demand is worldwide, not just US defense.",
        "confidence": 0.95, "prediction": "Global drone proliferation drives component demand beyond any single nation.",
        "platform_id": None, "component_id": None,
        "data_sources": ["forge_parts_db"],
    })
    return flags


# ──────────────────────────────────────────
# 14. MAIN
# ──────────────────────────────────────────

def main():
    print("=" * 60)
    print("PIE Live Pipeline — Reading real Forge DB")
    print("=" * 60)

    db = load_forge()
    all_flags = []

    print("\nAnalyzing platforms...")
    plat_flags, blue, ndaa, adversary = analyze_platforms(db)
    all_flags.extend(plat_flags)

    print("\nAnalyzing companion computers (SBCs)...")
    sbc_flags = analyze_sbcs(db)
    all_flags.extend(sbc_flags)

    print("\nAnalyzing mesh radios...")
    mesh_flags = analyze_mesh(db)
    all_flags.extend(mesh_flags)

    print("\nAnalyzing flight controllers...")
    fc_flags = analyze_fcs(db)
    all_flags.extend(fc_flags)

    print("\nCross-referencing GUR diversion data...")
    div_flags = analyze_diversion(db)
    all_flags.extend(div_flags)

    print("\nAnalyzing software ecosystem...")
    sw_flags, sw_hw_demand = analyze_software(db)
    all_flags.extend(sw_flags)

    print("\nAnalyzing manufacturers...")
    mfr_flags = analyze_manufacturers(db, sw_hw_demand)
    # Manufacturer profiles feed dependency graph + what-if but don't need individual flags
    print(f"  ({len(mfr_flags)} manufacturer profiles — data used internally, not added to flags)")

    print("\nAnalyzing Counter-UAS ecosystem...")
    cuas_flags = analyze_cuas(db)
    all_flags.extend(cuas_flags)

    print("\nAnalyzing tariff & trade policy...")
    policy_flags = analyze_policy()
    all_flags.extend(policy_flags)

    print("\nAnalyzing BOM cost index...")
    bom_flags = analyze_bom_cost(db)
    all_flags.extend(bom_flags)

    print("\nAnalyzing workforce & production capacity...")
    cap_flags = analyze_capacity()
    all_flags.extend(cap_flags)

    print("\nAnalyzing DRAM pricing...")
    dram_flags, dram_data = analyze_dram()
    all_flags.extend(dram_flags)

    print("\nAnalyzing allied nation supply chain...")
    geo_flags = analyze_allied_supply(db)
    all_flags.extend(geo_flags)

    print("\nAnalyzing government & DoD programs...")
    gov_flags, gov_demand = analyze_gov_programs(db)
    all_flags.extend(gov_flags)

    print("\nAnalyzing foreign UAS ecosystems...")
    foreign_flags = analyze_foreign(db)
    all_flags.extend(foreign_flags)

    print("\nAnalyzing RF/comms ecosystem...")
    rf_flags = analyze_rf_comms(db)
    all_flags.extend(rf_flags)

    print("\nAnalyzing EW threat landscape...")
    ew_flags = analyze_ew(db)
    all_flags.extend(ew_flags)

    print("\nAnalyzing SOF-specific programs...")
    sof_flags = analyze_sof(db)
    all_flags.extend(sof_flags)

    print("\nAnalyzing navigation/PNT (GPS-denied)...")
    nav_flags = analyze_nav_pnt(db)
    all_flags.extend(nav_flags)

    print("\nAnalyzing propulsion supply chain...")
    prop_flags = analyze_propulsion(db)
    all_flags.extend(prop_flags)

    print("\nAnalyzing battery supply chain...")
    batt_flags = analyze_battery_supply_chain(db)
    all_flags.extend(batt_flags)

    print("\nAnalyzing thermal camera supply chain...")
    therm_flags = analyze_thermal_supply_chain(db)
    all_flags.extend(therm_flags)

    print("\nAnalyzing control link (C2) supply chain...")
    c2_flags = analyze_control_link_supply_chain(db)
    all_flags.extend(c2_flags)

    print("\nAnalyzing FC+ESC stack supply chain...")
    stack_flags = analyze_stack_supply_chain(db)
    all_flags.extend(stack_flags)

    print("\nAnalyzing video transmitter (VTX) supply chain...")
    vtx_flags = analyze_vtx_supply_chain(db)
    all_flags.extend(vtx_flags)

    print("\nAnalyzing ESC supply chain...")
    esc_flags = analyze_esc_supply_chain(db)
    all_flags.extend(esc_flags)

    print("\nAnalyzing allied manufacturer profiles...")
    allied_flags = analyze_allied_manufacturers(db)
    all_flags.extend(allied_flags)

    print("\nAnalyzing FPV camera supply chain...")
    cam_flags = analyze_fpv_camera_supply_chain(db)
    all_flags.extend(cam_flags)

    print("\nAnalyzing frame supply chain...")
    frame_flags = analyze_frame_supply_chain(db)
    all_flags.extend(frame_flags)

    print("\nAnalyzing receiver supply chain...")
    rx_flags = analyze_receiver_supply_chain(db)
    all_flags.extend(rx_flags)

    print("\nAnalyzing antenna supply chain...")
    ant_flags = analyze_antenna_supply_chain(db)
    all_flags.extend(ant_flags)

    print("\nAnalyzing propeller supply chain...")
    prop_sc_flags = analyze_propeller_supply_chain(db)
    all_flags.extend(prop_sc_flags)

    print("\nAnalyzing battery parts-db cell sourcing (NDAA ban timelines)...")
    batt_partsdb_flags = analyze_battery_partsdb(db)
    all_flags.extend(batt_partsdb_flags)

    # ── Wire Mouser/DigiKey: enrich parts-db with live prices ──────────────
    print("\nFetching live component pricing from Mouser/DigiKey...")
    import os as _os, sys as _sys, json as _json
    from pathlib import Path as _Path
    _mouser_key = _os.environ.get("MOUSER_API_KEY", "")
    _dk_id      = _os.environ.get("DIGIKEY_CLIENT_ID", "")
    _dk_secret  = _os.environ.get("DIGIKEY_CLIENT_SECRET", "")
    if _mouser_key or (_dk_id and _dk_secret):
        try:
            _sys.path.insert(0, str(_Path(__file__).resolve().parent))
            from pricing import PricingClient
            _parts_db_dir = _Path(__file__).resolve().parent.parent / "data" / "parts-db"
            _pricing_client = PricingClient()
            if _pricing_client.available:
                for _cat in ["flight_controllers","escs","motors","batteries",
                             "fpv_cameras","video_transmitters","receivers",
                             "companion_computers","navigation_pnt"]:
                    _fp = _parts_db_dir / f"{_cat}.json"
                    if not _fp.exists():
                        continue
                    try:
                        _parts = _json.loads(_fp.read_text())
                        if isinstance(_parts, list):
                            _enriched = _pricing_client.enrich_parts_db(_parts, max_queries=30)
                            _fp.write_text(_json.dumps(_enriched, indent=2, ensure_ascii=False))
                            print(f"  [Pricing] {_cat}: enriched")
                    except Exception as _e:
                        print(f"  [Pricing] {_cat} error: {_e}")
        except Exception as _e:
            print(f"  [Pricing] enrich error: {_e}")
    else:
        print("  [Pricing] MOUSER_API_KEY not set — skipping live price fetch")

    print("\nChecking live component pricing signals (Mouser/DigiKey)...")
    pricing_flags = analyze_live_pricing(db)
    all_flags.extend(pricing_flags)

    print("\nAnalyzing test & training infrastructure...")
    test_flags = analyze_test_infra()
    all_flags.extend(test_flags)

    print("\nAnalyzing financial signals...")
    fin_flags = analyze_financial()
    all_flags.extend(fin_flags)

    print("\nDetecting gray zone / adversary-adjacent entities...")
    # Run the full gray zone detector if entities.json exists
    gz_entities_path = REPO_ROOT / "data" / "grayzone" / "entities.json"
    if gz_entities_path.exists():
        try:
            sys.path.insert(0, str(REPO_ROOT / "pipeline"))
            from grayzone.grayzone_detector import main as gz_main, FLAGS_OUT as GZ_FLAGS_OUT
            gz_main()
            # Merge gray zone flags into main flags
            if GZ_FLAGS_OUT.exists():
                gz_flags_data = load_json(GZ_FLAGS_OUT)
                # Add sources to gray zone flags
                for gf in gz_flags_data:
                    gf["sources"] = resolve_sources(gf.get("data_sources", []))
                all_flags.extend(gz_flags_data)
                print(f"  Merged {len(gz_flags_data)} gray zone flags into main pipeline")
            # Also load follow-up research flags if they exist
            gz_followup = REPO_ROOT / "data" / "grayzone" / "followup_flags.json"
            if gz_followup.exists():
                fu_flags = load_json(gz_followup)
                for gf in fu_flags:
                    gf["sources"] = resolve_sources(gf.get("data_sources", []))
                all_flags.extend(fu_flags)
                print(f"  Merged {len(fu_flags)} gray zone follow-up flags")
        except Exception as e:
            print(f"  Gray zone detector error: {e}")
            # Fallback to basic analysis
            gz_flags = analyze_gray_zone(db)
            all_flags.extend(gz_flags)
    else:
        gz_flags = analyze_gray_zone(db)
        all_flags.extend(gz_flags)

    print("\n── Advanced Algorithms ──")

    print("\nMapping dependency graph (cascade analysis)...")
    dep_flags = analyze_dependency_graph(db)
    all_flags.extend(dep_flags)

    print("\nPredicting lead time trajectories...")
    lt_flags = analyze_lead_times()
    all_flags.extend(lt_flags)

    print("\nCalculating contract → component demand...")
    contract_flags = analyze_contract_demand()
    all_flags.extend(contract_flags)

    print("\nTracking conflict consumption rates...")
    conflict_flags = analyze_conflict_consumption()
    all_flags.extend(conflict_flags)

    print("\nMapping alternative components...")
    alt_flags = analyze_alternatives(db)
    # Alternatives now rendered in the What-If simulator cascade — don't duplicate in flags
    print(f"  ({len(alt_flags)} alternative mappings in What-If simulator — not added to flags)")

    print("\nScoring price elasticity...")
    elast_flags = analyze_price_elasticity()
    all_flags.extend(elast_flags)

    print("\nDetecting sanctions evasion patterns...")
    sanct_flags = analyze_sanctions_evasion()
    all_flags.extend(sanct_flags)

    print("\nRunning what-if simulations...")
    whatif_flags = analyze_what_if()
    # What-if scenarios are in the interactive simulator tab — don't duplicate in flags list
    print(f"  (4 scenarios in What-If simulator tab — not added to flags)")

    print("\nMatching temporal patterns...")
    temp_flags = analyze_temporal_patterns()
    all_flags.extend(temp_flags)

    print("\nAnalyzing sentiment signals...")
    sent_flags = analyze_sentiment_signals()
    all_flags.extend(sent_flags)

    print("\nGenerating predictions (multi-model ensemble)...")
    try:
        from prediction_engine import run as _run_predictions
        preds = _run_predictions(db, all_flags)
        print(f"  ✓ Ensemble engine: {len(preds)} predictions")
        for p in preds[:3]:
            print(f"    [{p['probability']:.2f}] {p['event'][:65]}")
    except Exception as _e:
        print(f"  ⚠ Ensemble engine failed ({_e}) — falling back to legacy")
        preds = generate_predictions(len(blue), len(ndaa), db)

    # Sort flags: critical first, then by type
    severity_order = {"critical": 0, "warning": 1, "info": 2, "prediction": 3}
    all_flags.sort(key=lambda f: severity_order.get(f["severity"], 9))

    # Resolve source IDs → rich source objects with URLs, descriptions, validation
    for flag in all_flags:
        raw_sources = flag.get("data_sources", [])
        flag["sources"] = resolve_sources(raw_sources)

    # Write output
    FLAGS_OUT.parent.mkdir(exist_ok=True)
    with open(FLAGS_OUT, "w") as f:
        json.dump(all_flags, f, indent=2)
    with open(PREDS_OUT, "w") as f:
        json.dump(preds, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"PIE Live Pipeline — Complete")
    print(f"{'=' * 60}")
    print(f"  Components analyzed: {sum(len(v) for v in db.values() if isinstance(v, list))}")
    print(f"  Platforms: {len(db.get('drone_models', []))} ({len(blue)} Blue UAS)")
    print(f"  Software stacks: {len(SOFTWARE_ECOSYSTEM)}")
    print(f"  C-UAS companies: {len(CUAS_COMPANIES)}")
    print(f"  Allied nations: {len(ALLIED_SUPPLY)}")
    print(f"  Policy signals: {len(POLICY_SIGNALS)}")
    print(f"  Gov/DoD programs: {len(GOV_PROGRAMS)}")
    print(f"  Foreign programs: {len(FOREIGN_PROGRAMS)}")
    print(f"  Flags generated: {len(all_flags)}")
    sev_counts = {}
    for f in all_flags:
        sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1
    for sev, count in sorted(sev_counts.items(), key=lambda x: severity_order.get(x[0], 9)):
        print(f"    {sev.upper():12s} {count}")
    print(f"  Predictions: {len(preds)}")
    print(f"  Output: {FLAGS_OUT}, {PREDS_OUT}")


if __name__ == "__main__":
    main()
# triggered: 2026-04-05T06:47:39Z
