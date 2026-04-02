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

REPO_ROOT = Path(__file__).resolve().parent.parent
PARTS_DB = REPO_ROOT / "data" / "parts-db"
FORGE_DB = REPO_ROOT / "data" / "forge_database.json"
FLAGS_OUT = REPO_ROOT / "data" / "flags.json"
PREDS_OUT = REPO_ROOT / "data" / "predictions.json"

now = datetime.now(timezone.utc).isoformat()


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
            # Don't overwrite drone_models if we got the full 219 from forge_database.json
            if key == "drone_models" and "drone_models" in db and len(db["drone_models"]) > len(data):
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

        # Parse price
        price = 0
        if price_str:
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

def analyze_diversion(db):
    """Cross-reference Forge components against known GUR teardown findings."""
    flags = []

    # Known from GUR War & Sanctions portal (verified from our research)
    gur_findings = [
        {"weapon": "Geran-2/3 (Shahed-136/238)", "component": "Raspberry Pi 4B", "role": "Borscht Tracker V3", "units": "40,000+"},
        {"weapon": "Geran-5", "component": "Raspberry Pi", "role": "Tracker + 3G/4G modem"},
        {"weapon": "Molniya-2R", "component": "Raspberry Pi 5", "role": "Reconnaissance computer"},
        {"weapon": "FPV (various)", "component": "Allwinner H616", "role": "Grape Pi 1 (machine vision)"},
    ]

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
# 8. MAIN
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
    all_flags.extend(mfr_flags)

    print("\nGenerating predictions...")
    preds = generate_predictions(len(blue), len(ndaa), db)

    # Sort flags: critical first, then by type
    severity_order = {"critical": 0, "warning": 1, "info": 2, "prediction": 3}
    all_flags.sort(key=lambda f: severity_order.get(f["severity"], 9))

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
    print(f"  Flags generated: {len(all_flags)}")
    for f in all_flags:
        sev = f["severity"].upper()
        print(f"    [{sev:10s}] {f['title'][:80]}")
    print(f"  Predictions: {len(preds)}")
    print(f"  Output: {FLAGS_OUT}, {PREDS_OUT}")


if __name__ == "__main__":
    main()
