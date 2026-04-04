"""
PIE Supplemental Analysis Modules
RF/Comms, EW, SOF, Nav/PNT, Propulsion, Test Infra, Financial Signals

Imported by pie_pipeline_live.py
"""

import hashlib
from datetime import datetime, timezone

now = datetime.now(timezone.utc).isoformat()

def flag_id(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:12]


# ══════════════════════════════════════════════════════════════
# 1. RF / COMMS / DATALINKS
# ══════════════════════════════════════════════════════════════

RF_ECOSYSTEM = [
    {"name": "TrellisWare Technologies", "hq": "San Diego, CA", "type": "waveform_provider",
     "products": ["TSM Shadow (TW-950)", "TW-400 TrellisWare Radio", "TSM Waveform SDK"],
     "significance": "Provides TSM (Tactical Scalable MANET) waveform — the standard MANET waveform for SOF and Army tactical networks. Licensed to L3Harris, Thales, Collins. TSM runs on AN/PRC-163, AN/PRC-167, and multiple handhelds.",
     "hw_dependency": ["FPGA (waveform execution)", "L3Harris AN/PRC-163 (host radio)", "SDR platforms"],
     "contracts": ["USSOCOM Tactical Handheld", "Army IVAS integration", "SOF MANET backbone"],
     "sof_relevance": "critical",
     "drone_link": "TrellisWare waveforms on drone mesh radios enable SOF UAS to operate on the same MANET as dismounted operators — same network, same COP.",
     "sources": ["trellis_primary", "sof_programs"]},

    {"name": "L3Harris — Tactical Radios", "hq": "Melbourne, FL", "type": "radio_platform",
     "products": ["AN/PRC-163 (Manpack)", "AN/PRC-167 (Handheld)", "RF-335M", "MUOS terminals"],
     "significance": "Primary tactical radio provider for US military. AN/PRC-163 is the backbone radio for SOF and conventional forces. Supports TrellisWare TSM + SRW + MUOS waveforms.",
     "hw_dependency": ["FPGA (Xilinx/AMD)", "GaN amplifiers", "SDR processing"],
     "contracts": ["HMS Manpack (Army)", "SOCOM tactical comms", "Multi-domain operations"],
     "sof_relevance": "critical",
     "drone_link": "Drone datalinks must be interoperable with PRC-163 networks for SOF integration. Gateway/bridge solutions needed.",
     "sources": ["defense_contracts", "sof_programs"]},

    {"name": "Collins Aerospace (RTX)", "hq": "Cedar Rapids, IA", "type": "radio_platform",
     "products": ["Team Connect MANET", "TruNet networking", "AN/ARC-210 (airborne)"],
     "significance": "Airborne radio/datalink provider. TruNet enables air-to-ground mesh. Critical for CCA and MUM-T operations.",
     "hw_dependency": ["FPGA", "GaN PAs", "Custom ASICs"],
     "contracts": ["USAF CCA datalinks", "MUM-T integration", "JADC2"],
     "sof_relevance": "high",
     "drone_link": "CCA programs need Collins/L3Harris datalinks to integrate autonomous drones with crewed fighter networks.",
     "sources": ["defense_contracts"]},

    {"name": "Persistent Systems", "hq": "New York, NY", "type": "mesh_radio",
     "products": ["MPU5 Wave Relay", "Embedded Module", "GVR5"],
     "significance": "Most deployed tactical mesh radio. Wave Relay OS (custom Android). Self-forming/healing. No master node. Used by SOF, Army, Marines. $10K-50K/node.",
     "hw_dependency": ["Qualcomm WiFi silicon", "Custom MIMO antennas", "ARM processors"],
     "contracts": ["USSOCOM tactical mesh", "Army Tactical Network", "Multi-national SOF"],
     "sof_relevance": "critical",
     "drone_link": "MPU5 on ground + Doodle Labs/Silvus on drones creates the mesh backbone for multi-domain UAS operations.",
     "sources": ["forge_parts_db", "defense_contracts"]},

    {"name": "Silvus Technologies", "hq": "Los Angeles, CA", "type": "mesh_radio",
     "products": ["StreamCaster SC4200", "MN Micro", "SC4400"],
     "significance": "High-throughput MIMO mesh. 100+ Mbps. Used on Teal 2 (Blue UAS). MN Micro is smallest tactical mesh at drone SWaP.",
     "hw_dependency": ["Custom MIMO silicon", "GaN amplifiers"],
     "contracts": ["Teal/Red Cat integration", "SOF ISR", "Multi-domain mesh"],
     "sof_relevance": "high",
     "drone_link": "MN Micro integrated on Teal 2 Blue UAS for SOF ISR. StreamCaster for ground relay.",
     "sources": ["forge_parts_db", "defense_contracts"]},

    {"name": "Doodle Labs", "hq": "Burnaby, BC / US operations", "type": "mesh_radio",
     "products": ["Helix Smart Radio", "Mini OEM", "RM-915/RM-2450"],
     "significance": "Most popular mesh radio for drone integration. OpenWRT + batman-adv under the hood. L/S/C-Band options. Used on Ghost-X.",
     "hw_dependency": ["Qualcomm/Atheros WiFi silicon", "Custom firmware"],
     "contracts": ["Anduril Ghost-X", "Lattice Mesh", "Multiple Blue UAS integrators"],
     "sof_relevance": "high",
     "drone_link": "Primary mesh radio for Anduril Ghost-X and multiple Blue UAS platforms. Handbook Ch.14 reference.",
     "sources": ["forge_parts_db", "defense_contracts"]},

    {"name": "Rajant Corporation", "hq": "Morrisville, PA", "type": "mesh_radio",
     "products": ["BreadCrumb LX5", "Sparrow", "Peregrine"],
     "significance": "Kinetic Mesh — each node is a router. Mobile ad-hoc networking for industrial + defense. InstaMesh protocol.",
     "hw_dependency": ["Dual-radio architecture", "Custom mesh firmware"],
     "contracts": ["Mining/industrial mesh", "Military mobile mesh", "UAS relay"],
     "sof_relevance": "medium",
     "drone_link": "Alternative to Doodle/Silvus for drone mesh. More capacity but higher SWaP.",
     "sources": ["forge_parts_db"]},

    {"name": "Mobilicom", "hq": "Israel/US", "type": "datalink",
     "products": ["SkyHopper PRO", "SkyHopper PRO Lite", "SkyHopper PRO Micro"],
     "significance": "Blue UAS Framework certified datalinks. IP mesh networking for UAS C2 + video.",
     "hw_dependency": ["SDR platform", "MIMO antennas"],
     "contracts": ["Blue UAS Framework component", "Multiple UAS integrators"],
     "sof_relevance": "medium",
     "drone_link": "Blue UAS Framework certified — pre-approved for integration on Blue UAS platforms.",
     "sources": ["diu_blue_uas", "defense_contracts"]},
]


# ══════════════════════════════════════════════════════════════
# 2. EW & SPECTRUM WARFARE
# ══════════════════════════════════════════════════════════════

EW_ECOSYSTEM = [
    {"name": "Sierra Nevada Corporation (SNC)", "hq": "Sparks, NV",
     "products": ["MOD-X EW suite", "Counter-comms systems", "ISR platforms"],
     "significance": "Major EW provider. Counter-comms capability directly impacts drone C2 links. SNC EW drives need for resilient waveforms.",
     "drone_impact": "Drones operating in EW-contested environments need frequency-hopping (ELRS FHSS), GPS-denied nav, and mesh resilience."},
    {"name": "CACI International", "hq": "Reston, VA",
     "products": ["Electronic warfare systems", "SIGINT platforms", "Spectrum management"],
     "significance": "EW and SIGINT provider. Their systems are what drones face in contested environments.",
     "drone_impact": "Drives requirement for EW-resilient drone comms. ELRS frequency-hopping, Hivemind GPS-denied operation."},
    {"name": "Northrop Grumman — EW Division", "hq": "Linthicum, MD",
     "products": ["AN/ALQ-131", "JCREW counter-IED/EW", "Cyber/EW integrated systems"],
     "significance": "JCREW counter-IED jammers also affect drone control links. Same spectrum, same problem.",
     "drone_impact": "Friendly EW (JCREW) can inadvertently jam friendly drone links — frequency deconfliction is critical."},
    {"name": "Russian EW (Reported)", "hq": "Russia",
     "products": ["Krasukha-4", "Zhitel", "R-330Zh (drone-specific jammer)", "Pole-21"],
     "significance": "Russia deploys drone-specific jammers. R-330Zh targets 900MHz/2.4GHz/5.8GHz — exactly the bands drones use. Pole-21 GPS jammer.",
     "drone_impact": "Russian EW is why GPS-denied autonomy (Hivemind, Skydio VIO) and frequency-hopping links (ELRS, IRONghost) exist. The threat drives the technology."},
]


# ══════════════════════════════════════════════════════════════
# 3. SOF-SPECIFIC PROGRAMS
# ══════════════════════════════════════════════════════════════

SOF_PROGRAMS = [
    {"name": "USSOCOM PEO-SOF Warrior", "scope": "All SOF-unique equipment including UAS",
     "significance": "SOF has its own procurement path — faster, less bureaucratic than Big Army. PEO-SOF Warrior buys directly.",
     "platforms": ["V-BAT", "Ghost-X", "Switchblade", "SOF-unique FPV"],
     "component_demand": ["Silvus MN Micro", "TrellisWare TSM", "FLIR thermals", "Jetson Orin"]},
    {"name": "SOFWERX / SOCOM Forge", "scope": "Rapid prototyping and evaluation for SOF",
     "significance": "SOFWERX runs rapid experimentation events. SOCOM Forge tests new tech in weeks, not years. Pipeline for emerging drone companies.",
     "platforms": ["Multiple emerging platforms tested"],
     "component_demand": ["Diverse — whatever prototypes use"]},
    {"name": "SOF Tactical UAS (SOF TUAS)", "scope": "Group 3 UAS for SOF missions — ISR, strike, resupply",
     "significance": "SOF needs longer range, longer endurance, more payload than SRR quads. V-BAT, Altius fill this gap.",
     "platforms": ["Shield AI V-BAT", "Anduril Altius", "AeroVironment platforms"],
     "component_demand": ["Tactical mesh radios", "Heavy-lift motors", "EO/IR gimbals", "Fuel cells"]},
    {"name": "USSOCOM Counter-UAS", "scope": "Protecting SOF from enemy drones",
     "significance": "SOF teams are high-value targets for enemy FPV drones. Portable C-UAS is critical. DroneShield RfPatrol, D-Fend EnforceAir.",
     "platforms": ["DroneShield RfPatrol", "D-Fend EnforceAir", "Anduril Anvil"],
     "component_demand": ["SDR modules", "RF detection antennas", "AI compute for classification"]},
    {"name": "AFSOC (Air Force Special Ops Command)", "scope": "AFSOC drone programs — STRATFI with Shield AI",
     "significance": "AFSOC funded Shield AI STRATFI contract to integrate Hivemind onto V-BAT. AFSOC drives autonomous ISR requirements.",
     "platforms": ["Shield AI V-BAT Teams", "Various ISR platforms"],
     "component_demand": ["Hivemind compute (Jetson)", "V-BAT airframes", "SATCOM terminals"]},
]


# ══════════════════════════════════════════════════════════════
# 4. NAVIGATION / PNT (GPS-DENIED)
# ══════════════════════════════════════════════════════════════

NAV_PNT = [
    {"name": "VectorNav Technologies", "hq": "Dallas, TX", "type": "IMU/INS",
     "products": ["VN-100 (IMU)", "VN-200 (GPS/INS)", "VN-310 (Dual GNSS/INS)"],
     "significance": "Tactical-grade inertial navigation. When GPS is jammed, INS provides dead-reckoning. Used in defense and commercial UAS.",
     "gps_denied_role": "Primary sensor for inertial dead-reckoning during GPS denial. Drift rate determines useful duration without GPS."},
    {"name": "Emcore / KVH Industries", "hq": "Various US", "type": "FOG/IMU",
     "products": ["Emcore EN-300 (FOG)", "KVH 1750 IMU (FOG)"],
     "significance": "Fiber-optic gyro — highest accuracy inertial. Used in precision navigation for cruise missiles and high-end UAS.",
     "gps_denied_role": "FOG provides much lower drift than MEMS. Enables hours of GPS-denied operation vs minutes for MEMS."},
    {"name": "Skydio Visual-Inertial Odometry", "hq": "San Mateo, CA", "type": "visual_nav",
     "products": ["Skydio Autonomy (VIO)", "NightSense"],
     "significance": "Camera-based navigation — no GPS needed. Uses 6 fisheye cameras + AI to build real-time 3D map and localize. Best-in-class commercial visual nav.",
     "gps_denied_role": "Purely visual navigation. Works indoors, in GPS-denied environments, under jamming. Requires good visibility."},
    {"name": "Shield AI Hivemind (GPS-denied)", "hq": "San Diego, CA", "type": "ai_nav",
     "products": ["Hivemind Pilot (GPS-denied state estimator)"],
     "significance": "Fuses IMU + camera + any available sensors for navigation without GPS. Combat-tested in Ukraine under Russian EW.",
     "gps_denied_role": "Multi-sensor fusion for GPS-denied flight. 200+ flights in Ukraine under active Russian jamming."},
    {"name": "Chip-Scale Atomic Clocks (CSAC)", "hq": "Various", "type": "timing",
     "products": ["Microsemi SA.45s CSAC", "Teledyne CSAC"],
     "significance": "GPS provides timing as much as position. When GPS is jammed, CSAC provides precise timing for FHSS radios and sensor fusion.",
     "gps_denied_role": "Maintains timing accuracy for mesh radios and sensor synchronization when GPS timing is unavailable."},
    {"name": "u-blox GNSS Modules", "hq": "Switzerland", "type": "gnss",
     "products": ["ZED-F9P (RTK)", "NEO-M9N", "MAX-M10S"],
     "significance": "Dominant GNSS module supplier for commercial and Blue UAS drones. ZED-F9P is the standard RTK module.",
     "gps_denied_role": "Primary GNSS receiver. First component to fail under jamming — drives need for INS backup."},
]


# ══════════════════════════════════════════════════════════════
# 5. PROPULSION — NDAA RISK
# ══════════════════════════════════════════════════════════════

PROPULSION_INTEL = {
    "motor_china_dependency": {
        "title": "Drone motor supply chain: majority Chinese-manufactured",
        "detail": "T-Motor, BrotherHobby, EMAX, iFlight, XING (iFlight), Sunnysky — dominant FPV motor brands are all Chinese. Even 'premium' motors from Western brands often use Chinese stator laminations, magnets, and bearings. NDAA-compliant motor alternatives exist (KDE Direct, Allied Motion, Plettenberg, MAD Components) but at 3-5x cost.",
        "sources": ["forge_parts_db", "fpv_market"],
    },
    "battery_china_dependency": {
        "title": "LiPo/Li-Ion cells: CATL, BYD, EVE dominate global production",
        "detail": "Nearly all drone LiPo packs use Chinese-manufactured cells. Molicel (Taiwan/Canada) and Samsung (S.Korea) are alternatives but at higher cost and limited availability for drone-format cells. This is the deepest NDAA compliance challenge — there is no US LiPo cell manufacturer at scale.",
        "sources": ["forge_parts_db", "supply_chain_mapping"],
    },
    "fuel_cell_emerging": {
        "title": "Hydrogen fuel cells emerging for long-endurance UAS",
        "detail": "Intelligent Energy (UK), Doosan Mobility (S.Korea), HES Energy (Singapore) — fuel cells enable 2-4 hour flight vs 30-45 min on LiPo. Still early-stage for tactical UAS but defense interest growing.",
        "sources": ["forge_parts_db", "defense_contracts"],
    },
    "hybrid_electric": {
        "title": "Hybrid-electric propulsion for Group 3+ UAS",
        "detail": "Parallel Flight Technologies, Currawong Engineering (Australia) — hybrid systems combining small engines with electric motors for heavy-lift, long-endurance. Addresses the range limitation of pure-electric UAS.",
        "sources": ["forge_parts_db"],
    },
}


# ══════════════════════════════════════════════════════════════
# 6. TEST & TRAINING INFRASTRUCTURE
# ══════════════════════════════════════════════════════════════

TEST_INFRA = [
    {"name": "Drone Dominance Gauntlet", "location": "Fort Benning, GA (and rotating)",
     "significance": "DoD competitive evaluation for DDP vendors. Phase 1 winners announced Mar 2026. Defines which platforms get volume orders.",
     "demand_signal": "Gauntlet results directly determine which manufacturers scale production → which components see demand spikes."},
    {"name": "Army Yuma Proving Ground", "location": "Yuma, AZ",
     "significance": "Primary Army UAS test range. FTUAS, SRR, and FoSUAS evaluation conducted here.",
     "demand_signal": "Test failures can delay programs. Test successes accelerate procurement timelines."},
    {"name": "AUVSI XPONENTIAL", "location": "Annual conference",
     "significance": "Largest UAS industry event. New product launches, partnership announcements, procurement signals.",
     "demand_signal": "Leading indicator — announcements at XPONENTIAL often precede contract awards by 3-6 months."},
    {"name": "Army Best Drone Warfighter Competition", "location": "Huntsville, AL (Feb 2026)",
     "significance": "Competitive evaluation of soldier drone skills. Drives training requirements and platform standardization.",
     "demand_signal": "Competition results influence which platforms get adopted at unit level."},
]


# ══════════════════════════════════════════════════════════════
# 7. FINANCIAL SIGNALS
# ══════════════════════════════════════════════════════════════

FINANCIAL_SIGNALS = [
    {"company": "Shield AI", "event": "Valued at $2.7B+ (Series F)", "date": "2024-2025",
     "significance": "Largest defense AI startup valuation. Signals investor confidence in autonomous drone software. Hivemind licensing model.",
     "demand_prediction": "High growth trajectory → Jetson Orin demand increases as Hivemind deploys on more platforms."},
    {"company": "Anduril Industries", "event": "Valued at $14B+ / Arsenal-1 factory planned", "date": "2024-2026",
     "significance": "Building 'Arsenal-1' mass production facility. $14B valuation. Largest defense tech startup.",
     "demand_prediction": "Arsenal-1 drives massive component demand when online — Jetson AGX Orin, Lattice FPGA, Doodle Labs mesh at scale."},
    {"company": "Red Cat Holdings (RCAT)", "event": "SRR win + Drone Dominance + stock 400%+ YoY", "date": "2025-2026",
     "significance": "Teal Black Widow won SRR. Stock surged. Raised capital. Scaling production. $47M USMC contract.",
     "demand_prediction": "RCAT scaling → QRB5165 (VOXL 2), FLIR Lepton/Hadron, Silvus MN Micro demand."},
    {"company": "AeroVironment (AVAV)", "event": "Revenue $745M+ FY25, Switchblade production ramp", "date": "2025-2026",
     "significance": "Dominant loitering munition maker. Ukraine USAI packages drive Switchblade demand. Sustained revenue growth.",
     "demand_prediction": "AVAV production ramp → FLIR Boson 640, Xilinx FPGA, custom AV SoC demand sustained through Ukraine aid."},
    {"company": "Raspberry Pi Holdings (LON:RPI)", "event": "Revenue $323M FY25 +25%, shares +24%", "date": "2025-2026",
     "significance": "RPi now public company. Revenue growth driven by US+China demand. Acknowledged drone diversion issue. DRAM costs driving price hikes.",
     "demand_prediction": "RPi pricing continues up. CM4/CM5 constrained. Gray market premium persists."},
    {"company": "Axon (AXON)", "event": "Acquired Dedrone (C-UAS)", "date": "2024",
     "significance": "Axon acquiring Dedrone signals C-UAS market maturation. Big-company entry validates space.",
     "demand_prediction": "Axon resources accelerate Dedrone scaling → C-UAS RF sensor demand increases."},
    {"company": "DroneShield (DRO.AX)", "event": "A$1.2B European pipeline, multiple contracts", "date": "2025-2026",
     "significance": "Australian C-UAS company with massive European pipeline. $6.2M Asia-Pacific contract Mar 2026.",
     "demand_prediction": "DroneShield scaling → SDR module demand, RF detection hardware, AI classification compute."},
    {"company": "Kratos Defense (KTOS)", "event": "Valkyrie CCA + drone target production", "date": "2025-2026",
     "significance": "Attritable drone maker. XQ-58 Valkyrie is CCA candidate. Also makes BQM target drones. Airbus partnership for German Valkyrie.",
     "demand_prediction": "CCA production → tactical datalink demand, AI compute, propulsion components."},
]


# ══════════════════════════════════════════════════════════════
# ANALYSIS FUNCTIONS
# ══════════════════════════════════════════════════════════════

def analyze_rf_comms(db):
    """Analyze RF/comms ecosystem and tie to UAS supply chain."""
    flags = []
    mesh = db.get("mesh_radios", [])
    print(f"  RF/comms companies tracked: {len(RF_ECOSYSTEM)}")

    for rf in RF_ECOSYSTEM:
        sev = "warning" if rf["sof_relevance"] == "critical" else "info"
        flags.append({
            "id": flag_id(f"rf-{rf['name'][:20]}"),
            "timestamp": now, "flag_type": "correlation", "severity": sev,
            "title": f"RF/Comms: {rf['name']} — {rf['significance'][:70]}",
            "detail": (
                f"{rf['name']} ({rf['hq']}): {rf['significance']} "
                f"Products: {', '.join(rf['products'][:3])}. "
                f"SOF relevance: {rf['sof_relevance']}. "
                f"Drone link: {rf['drone_link']} "
                f"HW deps: {', '.join(rf['hw_dependency'][:3])}."
            ),
            "confidence": 0.88,
            "prediction": f"SOF drone operations depend on {rf['name']} interoperability. Contract wins drive HW demand for {', '.join(rf['hw_dependency'][:2])}.",
            "platform_id": None, "component_id": rf["products"][0].lower().replace(" ", "-")[:30] if rf["products"] else None,
            "data_sources": rf.get("sources", ["defense_contracts", "forge_parts_db"]),
        })

    # Flag TrellisWare specifically — it's the missing link in the current analysis
    flags.append({
        "id": flag_id("trellisware-sof-bridge"),
        "timestamp": now, "flag_type": "correlation", "severity": "warning",
        "title": "TrellisWare TSM waveform is the bridge between SOF ground radios and drone mesh networks",
        "detail": (
            "TrellisWare's TSM (Tactical Scalable MANET) waveform runs on L3Harris AN/PRC-163, the standard SOF radio. "
            "For drones to operate on SOF networks, they need either: (a) a TSM-compatible radio onboard, or "
            "(b) a gateway bridging drone mesh (Doodle Labs/Silvus/Persistent) to TSM network. "
            "This integration requirement drives demand for both drone mesh radios AND gateway hardware. "
            "Handbook Ch.14 and Ch.15 (TAK Integration) cover the technical bridge."
        ),
        "confidence": 0.90,
        "prediction": "SOF UAS interop with TrellisWare/PRC-163 networks is a procurement requirement. Companies solving this bridge get contracts.",
        "platform_id": None, "component_id": "trellisware-tsm",
        "data_sources": ["sof_programs", "defense_contracts", "forge_parts_db"],
    })

    return flags


def analyze_ew(db):
    """Analyze EW threat landscape and how it drives drone tech requirements."""
    flags = []
    print(f"  EW systems tracked: {len(EW_ECOSYSTEM)}")

    # The EW→drone technology driver chain
    flags.append({
        "id": flag_id("ew-drives-drone-tech"),
        "timestamp": now, "flag_type": "correlation", "severity": "warning",
        "title": "EW threat landscape drives GPS-denied autonomy, FHSS links, and mesh resilience requirements",
        "detail": (
            "Russian EW (R-330Zh, Pole-21, Krasukha-4) jams 900MHz/2.4GHz/5.8GHz — exactly the drone bands. "
            "This drives demand for: (1) GPS-denied navigation (Hivemind, Skydio VIO, VectorNav INS), "
            "(2) frequency-hopping RC links (ELRS FHSS, IRONghost dual-band), "
            "(3) resilient mesh networking (Doodle Labs, Silvus with anti-jam), "
            "(4) chip-scale atomic clocks for timing without GPS. "
            "Every EW advance by adversaries creates component demand for the countermeasure. "
            "Handbook Ch.2 (Frequency Bands) and component ref (EW-Resilient Communications) cover this."
        ),
        "confidence": 0.92,
        "prediction": "EW arms race accelerates. Expect continued demand growth for FHSS radios, INS modules, and autonomous navigation compute.",
        "platform_id": None, "component_id": "ew-resilient-comms",
        "data_sources": ["foreign_intel", "defense_contracts", "forge_parts_db"],
    })

    for ew in EW_ECOSYSTEM:
        flags.append({
            "id": flag_id(f"ew-{ew['name'][:20]}"),
            "timestamp": now, "flag_type": "correlation", "severity": "info",
            "title": f"EW: {ew['name']} — {ew['drone_impact'][:65]}",
            "detail": f"{ew['name']} ({ew.get('hq','')}) Products: {', '.join(ew['products'][:3])}. {ew['significance']} Drone impact: {ew['drone_impact']}",
            "confidence": 0.82,
            "prediction": f"EW capability from {ew['name']} drives countermeasure demand in drone ecosystem.",
            "platform_id": None, "component_id": None,
            "data_sources": ["foreign_intel", "defense_contracts"],
        })

    return flags


def analyze_sof(db):
    """Track SOF-specific programs and their component demand."""
    flags = []
    print(f"  SOF programs tracked: {len(SOF_PROGRAMS)}")

    for prog in SOF_PROGRAMS:
        flags.append({
            "id": flag_id(f"sof-{prog['name'][:25]}"),
            "timestamp": now, "flag_type": "contract_signal", "severity": "warning",
            "title": f"SOF: {prog['name']} — {prog['scope'][:60]}",
            "detail": (
                f"{prog['name']}: {prog['significance']} "
                f"Platforms: {', '.join(prog['platforms'][:3])}. "
                f"Component demand: {', '.join(prog['component_demand'][:4])}."
            ),
            "confidence": 0.88,
            "prediction": f"SOF procurement drives demand for {', '.join(prog['component_demand'][:2])}.",
            "platform_id": None, "component_id": prog["component_demand"][0].lower().replace(" ", "-") if prog["component_demand"] else None,
            "data_sources": ["sof_programs", "defense_contracts"],
        })

    return flags


def analyze_nav_pnt(db):
    """Track navigation/PNT ecosystem — GPS-denied is the whole fight."""
    flags = []
    gps = db.get("gps_modules", [])
    print(f"  Nav/PNT systems tracked: {len(NAV_PNT)}")
    print(f"  GPS modules in Forge DB: {len(gps)}")

    flags.append({
        "id": flag_id("gps-denied-demand"),
        "timestamp": now, "flag_type": "procurement_spike", "severity": "warning",
        "title": f"GPS-denied navigation demand surging — {len(NAV_PNT)} PNT solutions tracked",
        "detail": (
            "Every contested drone operation assumes GPS jamming. This drives parallel demand for: "
            "INS/IMU (VectorNav, Emcore, KVH), visual navigation (Skydio VIO, Hivemind), "
            "chip-scale atomic clocks (Microsemi CSAC), and multi-constellation GNSS with anti-jam (u-blox F9P + Tallysman antennas). "
            f"Forge DB tracks {len(gps)} GPS modules. The shift from GPS-reliant to GPS-resilient drives component demand across all Blue UAS platforms."
        ),
        "confidence": 0.90,
        "prediction": "GPS-denied nav components become standard on all tactical UAS. Expect INS + VIO as baseline requirements by 2027.",
        "platform_id": None, "component_id": "gps-denied-nav",
        "data_sources": ["forge_parts_db", "defense_contracts", "sof_programs"],
    })

    for nav in NAV_PNT:
        flags.append({
            "id": flag_id(f"nav-{nav['name'][:20]}"),
            "timestamp": now, "flag_type": "correlation", "severity": "info",
            "title": f"Nav/PNT: {nav['name']} — {nav['gps_denied_role'][:60]}",
            "detail": f"{nav['name']} ({nav.get('hq','')}, {nav['type']}): {nav['significance']} GPS-denied role: {nav['gps_denied_role']}",
            "confidence": 0.85,
            "prediction": f"{nav['name']} demand grows as GPS-denied requirements become standard.",
            "platform_id": None, "component_id": nav["products"][0].lower().replace(" ", "-")[:30] if nav["products"] else None,
            "data_sources": ["forge_parts_db", "defense_contracts"],
        })

    return flags


def analyze_propulsion(db):
    """Track propulsion supply chain — motors, batteries, fuel cells."""
    flags = []
    motors = db.get("motors", [])
    batteries = db.get("batteries", [])
    print(f"  Motors in Forge DB: {len(motors)}")
    print(f"  Batteries in Forge DB: {len(batteries)}")

    for key, intel in PROPULSION_INTEL.items():
        sev = "warning" if "china" in key or "battery" in key else "info"
        flags.append({
            "id": flag_id(f"prop-{key}"),
            "timestamp": now, "flag_type": "supply_constraint" if "china" in key else "correlation",
            "severity": sev,
            "title": intel["title"],
            "detail": intel["detail"],
            "confidence": 0.87,
            "prediction": "NDAA motor/battery compliance remains the hardest supply chain challenge for domestic UAS manufacturing.",
            "platform_id": None, "component_id": key,
            "data_sources": intel["sources"],
        })

    return flags


def analyze_test_infra():
    """Track test/training events that generate procurement signals."""
    flags = []
    print(f"  Test infrastructure tracked: {len(TEST_INFRA)}")

    for t in TEST_INFRA:
        flags.append({
            "id": flag_id(f"test-{t['name'][:20]}"),
            "timestamp": now, "flag_type": "contract_signal", "severity": "info",
            "title": f"Test/Event: {t['name']} — {t['demand_signal'][:60]}",
            "detail": f"{t['name']} ({t['location']}): {t['significance']} Demand signal: {t['demand_signal']}",
            "confidence": 0.80,
            "prediction": f"Watch {t['name']} results for procurement direction signals.",
            "platform_id": None, "component_id": None,
            "data_sources": ["gov_programs", "defense_contracts"],
        })

    return flags


def analyze_financial():
    """Track financial signals that predict component demand 6-12 months ahead."""
    flags = []
    print(f"  Financial signals tracked: {len(FINANCIAL_SIGNALS)}")

    for fin in FINANCIAL_SIGNALS:
        sev = "warning" if any(k in fin["event"].lower() for k in ["$14b", "$2.7b", "400%", "ramp"]) else "info"
        flags.append({
            "id": flag_id(f"fin-{fin['company'][:15]}"),
            "timestamp": now, "flag_type": "contract_signal", "severity": sev,
            "title": f"Financial: {fin['company']} — {fin['event'][:55]}",
            "detail": f"{fin['company']}: {fin['significance']} Demand prediction: {fin['demand_prediction']}",
            "confidence": 0.82,
            "prediction": fin["demand_prediction"],
            "platform_id": None, "component_id": None,
            "data_sources": ["rpi_earnings", "defense_contracts", "forge_industry_intel"],
        })

    return flags


# ── Source registry additions for new modules ──
SUPPLEMENTAL_SOURCES = {
    "sof_programs": {
        "name": "USSOCOM Program Tracking",
        "url": "https://www.socom.mil",
        "description": "SOF-specific procurement programs: PEO-SOF Warrior, SOFWERX, AFSOC STRATFI, SOF TUAS.",
        "validation": "DoD press releases, SOCOM budget documents, SOFWERX event reports.",
        "type": "aggregated",
    },
    "trellis_primary": {
        "name": "TrellisWare Technologies",
        "url": "https://www.trellisware.com",
        "description": "TSM waveform provider for SOF tactical MANET. Licensed to L3Harris, Thales, Collins.",
        "validation": "Company primary source. Product datasheets and integration documentation.",
        "type": "primary",
    },
    "diu_blue_uas": {
        "name": "DIU/DCMA Blue UAS Cleared List",
        "url": "https://www.diu.mil/blue-uas-cleared-list",
        "description": "Official DoD Blue UAS list. 50+ platforms, 14+ framework components.",
        "validation": "Official DoD certification. Primary source.",
        "type": "primary",
    },
    "gray_zone_tracking": {
        "name": "Gray Zone Entity Tracking",
        "url": "https://dronedj.com/2026/02/19/anzu-raptor-drone-texas-lawsuit/",
        "description": "Companies adjacent to Blue UAS ecosystem marketing to government buyers with adversary supply chain dependencies.",
        "validation": "Texas AG lawsuit filings, House Select Committee letters, security researcher teardowns, FCC filings.",
        "type": "primary",
    },
}


# ══════════════════════════════════════════════════════════════
# 8. GRAY ZONE / ADVERSARY-ADJACENT ENTITY DETECTION
# ══════════════════════════════════════════════════════════════

GRAY_ZONE_ENTITIES = [
    {
        "name": "Anzu Robotics",
        "hq": "Austin, TX (Delaware LLC)",
        "status": "Raptor series discontinued Feb 2026. TX AG lawsuit pending.",
        "adversary_link": "DJI — licensed Mavic 3 Enterprise design. Hardware identical per teardowns. Firmware signed with DJI cryptographic keys. Remote controller is relabeled DJI RC Pro.",
        "marketing_claim": "Marketed as American-aligned secure alternative to Chinese drones. 'Your Data is Your Data.' US-based operations.",
        "reality": "TX AG alleges Raptor T is 'essentially a DJI Mavic 3 painted green.' House Select Committee flagged as potential passthrough. ~50% of components from China. DJI retains root crypto keys.",
        "government_buyers": ["Little Rock PD (6 Raptor T units, SOAR grant)", "Unknown other agencies"],
        "legal_status": "TX AG lawsuit filed Feb 2026 — seeking civil penalties up to $10K/violation, injunction, disclosure order.",
        "risk_indicators": [
            "Licensed adversary technology marketed as domestic alternative",
            "DJI cryptographic keys control firmware signing",
            "FCC filings initially omitted DJI relationship",
            "Component shortage caused by adversary supply chain dependency",
            "Discontinued after NDAA 2025 demand surge exposed fragility",
        ],
        "sources": ["gray_zone_tracking", "congress_gov"],
    },
    {
        "name": "Autel Robotics",
        "hq": "Bothell, WA (Chinese-owned — Autel Intelligent Technology, Shenzhen)",
        "status": "Active — selling EVO MAX series to US law enforcement/enterprise.",
        "adversary_link": "Wholly-owned subsidiary of Shenzhen-based Autel Intelligent Technology. Chinese engineering, Chinese manufacturing.",
        "marketing_claim": "Markets as alternative to DJI. US office, US support. Not on DJI sanctions list.",
        "reality": "Chinese-owned, Chinese-manufactured. Not Blue UAS. Not NDAA compliant. Selling to state/local agencies that aren't subject to federal restrictions.",
        "government_buyers": ["Multiple state/local law enforcement agencies"],
        "legal_status": "No active litigation. Not on Entity List. But NDAA §1709 may restrict future sales.",
        "risk_indicators": [
            "Chinese-owned company marketing to US government agencies",
            "Benefits from DJI restrictions without being compliant itself",
            "State/local agencies may not be aware of ownership structure",
        ],
        "sources": ["gray_zone_tracking", "foreign_intel"],
    },
]


def analyze_gray_zone(db):
    """Detect adversary-adjacent entities marketing to government buyers."""
    flags = []
    print(f"  Gray zone entities tracked: {len(GRAY_ZONE_ENTITIES)}")

    for entity in GRAY_ZONE_ENTITIES:
        risk_count = len(entity["risk_indicators"])
        sev = "critical" if risk_count >= 4 else "warning" if risk_count >= 2 else "info"

        flags.append({
            "id": flag_id(f"grayzone-{entity['name'][:20]}"),
            "timestamp": now,
            "flag_type": "diversion_risk",
            "severity": sev,
            "title": f"Gray zone: {entity['name']} — {entity['status'][:55]}",
            "detail": (
                f"{entity['name']} ({entity['hq']}). "
                f"Adversary link: {entity['adversary_link']} "
                f"Marketing: {entity['marketing_claim']} "
                f"Reality: {entity['reality']} "
                f"Government buyers: {', '.join(entity['government_buyers'][:3])}. "
                f"Legal: {entity['legal_status']} "
                f"Risk indicators: {'; '.join(entity['risk_indicators'][:3])}."
            ),
            "confidence": 0.90,
            "prediction": f"Gray zone pattern: adversary technology rebranded for domestic market. Watch for similar entities emerging as DJI restrictions tighten.",
            "platform_id": None,
            "component_id": None,
            "data_sources": entity.get("sources", ["gray_zone_tracking"]),
        })

    # Systemic flag about the gray zone pattern
    flags.append({
        "id": flag_id("grayzone-systemic"),
        "timestamp": now,
        "flag_type": "diversion_risk",
        "severity": "warning",
        "title": f"Systemic: {len(GRAY_ZONE_ENTITIES)} adversary-adjacent entities detected marketing to US government buyers",
        "detail": (
            f"As DJI restrictions tighten (ASDA, NDAA §1709, FCC equipment auth freeze), "
            f"adversary-linked companies are licensing, rebranding, or white-labeling Chinese drone technology "
            f"for the US market. Pattern: license DJI/Chinese design → manufacture in third country (Malaysia, etc.) "
            f"→ market as 'American alternative' → sell to agencies that don't verify supply chain. "
            f"PIE tracks {len(GRAY_ZONE_ENTITIES)} known entities. This is a growing attack vector against Blue UAS compliance."
        ),
        "confidence": 0.88,
        "prediction": "Expect more gray zone entities to emerge as the DJI ban creates market opportunity. Procurement safeguards needed at state/local level.",
        "platform_id": None,
        "component_id": None,
        "data_sources": ["gray_zone_tracking", "policy_tracker", "congress_gov"],
    })

    return flags
