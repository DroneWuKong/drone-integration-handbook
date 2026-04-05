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
    "battery_supply_chain": {
        "name": "Battery Supply Chain Intelligence",
        "url": "https://amprius.com",
        "description": "Cell manufacturer landscape, white-label mapping, raw material chokepoints, emerging tech for UAS batteries.",
        "validation": "SEC filings, company press releases, DIU contract awards, About:Energy teardowns, Molicel fire reports.",
        "type": "aggregated",
    },
    "thermal_supply_chain": {
        "name": "Thermal Camera Supply Chain Intelligence",
        "url": "https://www.teledyneflir.com",
        "description": "FPA manufacturers, camera integrators, ITAR status, DJI thermal sourcing for UAS thermal payloads.",
        "validation": "Manufacturer datasheets, export control regulations, ITAR classifications.",
        "type": "aggregated",
    },
    "control_link_supply_chain": {
        "name": "Control Link (C2) Supply Chain Intelligence",
        "url": "https://github.com/ExpressLRS/ExpressLRS",
        "description": "Radio manufacturers, RF chip sourcing (Semtech SX1280/SX1276), firmware ecosystem (ELRS/EdgeTX/Crossfire), enterprise/defense datalinks.",
        "validation": "Manufacturer websites, Semtech datasheets, PCN filings, corporate registrations.",
        "type": "aggregated",
    },
    "stack_supply_chain": {
        "name": "FC+ESC Stack Supply Chain Intelligence",
        "url": "https://oscarliang.com/at32-flight-controllers/",
        "description": "Stack manufacturers, FC/ESC MCU landscape (STM32 vs AT32), ESC firmware (AM32/BLHeli_32), MOSFET sourcing, IMU vendors.",
        "validation": "Betaflight documentation, Oscar Liang teardowns, manufacturer specs, ArteryTek corporate filings.",
        "type": "aggregated",
    },
    "vtx_supply_chain": {
        "name": "Video Transmitter (VTX) Supply Chain Intelligence",
        "url": "https://www.divimath.com/pages/ndaa-compliance",
        "description": "Digital FPV systems (DJI, Walksnail, HDZero/Divimath, OpenIPC), analog VTX landscape, camera sensors, NDAA compliance paths.",
        "validation": "Divimath NDAA declarations, CaddxFPV corporate info, Oscar Liang reviews, Betaflight ecosystem documentation.",
        "type": "aggregated",
    },
    "esc_supply_chain": {
        "name": "ESC Supply Chain Intelligence",
        "url": "https://www.fettec.net",
        "description": "ESC manufacturers, firmware ecosystem (BLHeli_32/AM32/proprietary), NDAA-compliant options (Lumenier, FETtec, KDE, Vertiq).",
        "validation": "Manufacturer websites, Betaflight ESC firmware documentation, product datasheets.",
        "type": "aggregated",
    },
    "allied_manufacturers": {
        "name": "Allied Manufacturer Profiles",
        "url": "https://orqafpv.com",
        "description": "Consolidated profiles of NDAA-compliant allied drone manufacturers with defense customers, supply chain verification, and risk factors.",
        "validation": "Corporate filings, defense contract announcements, investor disclosures, Wikipedia, defense press.",
        "type": "aggregated",
    },
    "fpv_camera_supply_chain": {
        "name": "FPV Camera Supply Chain Intelligence",
        "url": "https://www.foxeer.com",
        "description": "Camera manufacturers (Foxeer, Caddx, RunCam), image sensor supply (Sony CMOS), ISP chips, NDAA gap analysis.",
        "validation": "Manufacturer product specs, sensor datasheets, teardown analysis.",
        "type": "aggregated",
    },
    "frame_supply_chain": {
        "name": "Frame Supply Chain Intelligence",
        "url": "https://www.getfpv.com/brands/lumenier",
        "description": "Frame manufacturers, carbon fiber precursor sourcing (Toray, Hexcel), CNC cutting landscape, NDAA assessment.",
        "validation": "Manufacturer websites, carbon fiber industry reports, Chinese supplier directories.",
        "type": "aggregated",
    },
    "receiver_supply_chain": {
        "name": "Receiver Supply Chain Intelligence",
        "url": "https://github.com/ExpressLRS/ExpressLRS",
        "description": "ELRS/Crossfire/Ghost receiver manufacturers, MCU dependencies (ESP vs STM32), Ukrainian combat receivers, frequency landscape.",
        "validation": "ExpressLRS targets database, manufacturer specs, Forge parts-db analysis.",
        "type": "aggregated",
    },
    "antenna_supply_chain": {
        "name": "Antenna Supply Chain Intelligence",
        "url": "https://truerc.com",
        "description": "FPV antenna manufacturers (TrueRC, Lumenier, VAS), antenna technology, NDAA assessment — most compliant category.",
        "validation": "TrueRC patent filings, manufacturer websites, GetFPV distribution data.",
        "type": "aggregated",
    },
    "propeller_supply_chain": {
        "name": "Propeller Supply Chain Intelligence",
        "url": "https://www.gemfanhobby.com",
        "description": "Propeller manufacturers (HQProp, Gemfan, APC), materials supply (polycarbonate, nylon), injection molding landscape, NDAA assessment.",
        "validation": "Manufacturer websites, material supplier specs, ISO certifications.",
        "type": "aggregated",
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


# ══════════════════════════════════════════════════════════════
# 9. BATTERY SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_battery_supply_chain(db):
    """Analyze battery supply chain data from data/battery-supply-chain/."""
    flags = []
    from pathlib import Path
    batt_dir = Path(__file__).resolve().parent.parent / "data" / "battery-supply-chain"
    if not batt_dir.exists():
        return flags

    import json

    # Load all battery supply chain files
    us_mfrs = []
    allied_mfrs = []
    chinese_data = {}
    materials_data = {}

    us_path = batt_dir / "us_manufacturers.json"
    if us_path.exists():
        with open(us_path) as f:
            d = json.load(f)
        us_mfrs = d.get("us_cell_manufacturers", [])
        us_packs = d.get("us_pack_assemblers", [])

    allied_path = batt_dir / "allied_manufacturers.json"
    if allied_path.exists():
        with open(allied_path) as f:
            d = json.load(f)
        allied_mfrs = d.get("allied_cell_manufacturers", [])

    chinese_path = batt_dir / "chinese_supply_chain.json"
    if chinese_path.exists():
        with open(chinese_path) as f:
            chinese_data = json.load(f)

    materials_path = batt_dir / "materials_and_emerging_tech.json"
    if materials_path.exists():
        with open(materials_path) as f:
            materials_data = json.load(f)

    # === Flag: Molicel single point of failure ===
    molicel = next((m for m in allied_mfrs if m["id"] == "molicel"), None)
    if molicel and molicel.get("supply_crisis"):
        crisis = molicel["supply_crisis"]
        flags.append({
            "id": flag_id("battery-molicel-spof"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "critical",
            "title": f"Battery SPOF: Molicel capacity halved by {crisis.get('kaohsiung_fire_date','')} fire — {crisis.get('capacity_after_gwh','')} GWh remaining",
            "detail": (
                f"Molicel is the single non-Chinese source for high-drain cylindrical drone cells (P42A, P45B, P50B, P60C). "
                f"The {crisis.get('factory','')} fire destroyed ~${crisis.get('losses_usd',0)/1e6:.0f}M in capacity. "
                f"Remaining: {crisis.get('capacity_after_gwh','')} GWh from Tainan only. "
                f"Canada factory suspended Nov 2024. Recovery plan: SE Asia OEM (timeline unknown). "
                f"Every Blue UAS platform using 21700 cells is affected."
            ),
            "confidence": 0.95,
            "prediction": "Molicel lead times extend to 16-24 weeks through 2026. Pack builders switch to Samsung 40T as stopgap (lower performance).",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: Pouch cell gap ===
    pouch_gap = materials_data.get("pouch_cell_gap", {})
    if pouch_gap:
        flags.append({
            "id": flag_id("battery-pouch-gap"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "critical",
            "title": "Battery gap: Zero commercial-scale US/allied LiPo pouch cell production",
            "detail": (
                f"Most multirotor drones use LiPo pouch cells. China controls ~{pouch_gap.get('chinese_share_pct', 90)}% of production. "
                f"Molicel and Samsung make cylindrical cells only, not pouch. Amprius pouch production is pilot-scale (<10 MWh/year). "
                f"Best domestic hope: {pouch_gap.get('best_hope', 'unknown')}. "
                f"NDAA compliance deadlines (2027-2028) will arrive before US/allied pouch production catches up."
            ),
            "confidence": 0.92,
            "prediction": f"Realistic timeline for US/allied pouch cell parity: {pouch_gap.get('realistic_timeline', '2029-2030 minimum')}.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: Raw material chokepoints ===
    chokepoints = materials_data.get("raw_material_chokepoints", [])
    critical_mats = [c for c in chokepoints if c.get("risk") == "CRITICAL"]
    if critical_mats:
        flags.append({
            "id": flag_id("battery-raw-materials"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Battery upstream: {len(critical_mats)} critical raw materials with >75% Chinese control",
            "detail": (
                f"Even 'NDAA-compliant' cells carry upstream Chinese exposure. "
                + " | ".join(f"{c['material']}: {c['chinese_control_pct']}%" for c in critical_mats[:5])
                + f". No cell is truly China-free at the raw material level."
            ),
            "confidence": 0.90,
            "prediction": "China has weaponized export controls (graphite 2023, LFP cathode 2025, cobalt quotas 2026). Expect further restrictions targeting battery minerals.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: Skydio crisis as pattern ===
    skydio = chinese_data.get("skydio_crisis", {})
    if skydio:
        flags.append({
            "id": flag_id("battery-skydio-pattern"),
            "timestamp": now,
            "flag_type": "diversion_risk",
            "severity": "warning",
            "title": "Battery precedent: China weaponized TDK/Dongguan Poweramp to cut off Skydio",
            "detail": (
                f"On {skydio.get('date','')}, China ordered Dongguan Poweramp (TDK subsidiary) to halt Skydio battery supply. "
                f"Impact: rationing from 3 batteries per drone to 1. "
                f"Strategic lesson: {skydio.get('strategic_lesson', '')}. "
                f"DJI batteries also supplied by ATL (same TDK subsidiary family)."
            ),
            "confidence": 0.95,
            "prediction": "Any Blue UAS maker with Chinese-manufactured cells (even from allied-owned companies) faces identical coercion risk.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: White label exposure ===
    white_labels = chinese_data.get("white_label_map", [])
    if white_labels:
        flags.append({
            "id": flag_id("battery-white-label"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Battery white-label map: {len(white_labels)} brands traced to Chinese cell sources",
            "detail": (
                "PIE tracks brand → factory mapping for LiPo batteries. "
                + " | ".join(f"{w['brand']} ← {w['cell_source']}" for w in white_labels[:5])
                + f" + {max(0, len(white_labels)-5)} more."
            ),
            "confidence": 0.85,
            "prediction": "White-label LiPo packs remain dominant for hobbyist/commercial drones. Defense procurement must verify cell origin, not just pack brand.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: US manufacturer landscape ===
    shipping = [m for m in us_mfrs if any(
        p.get("status", "").startswith("shipping") for p in m.get("products", [])
    )]
    if us_mfrs:
        flags.append({
            "id": flag_id("battery-us-landscape"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"US battery landscape: {len(us_mfrs)} cell manufacturers, {len(shipping)} actively shipping drone cells",
            "detail": (
                " | ".join(
                    f"{m['name']} ({m.get('cell_chemistry','?')})"
                    for m in us_mfrs
                )
                + f". Pack assemblers: {len(us_packs) if 'us_packs' in dir() else '?'}."
            ),
            "confidence": 0.90,
            "prediction": "Amprius (silicon-anode) and Lyten (Li-S) are the two most credible paths to NDAA-compliant US-made drone cells by 2027.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: NDAA cost premium ===
    cost = materials_data.get("cost_analysis", {})
    if cost:
        flags.append({
            "id": flag_id("battery-ndaa-premium"),
            "timestamp": now,
            "flag_type": "cost_analysis",
            "severity": "warning",
            "title": f"Battery NDAA premium: {cost.get('ndaa_premium_cylindrical', '3-6x')} for cylindrical, {cost.get('ndaa_premium_us_pouch', '10-20x')} for US pouch",
            "detail": (
                f"NDAA-compliant battery sourcing carries significant cost premium. "
                f"Molicel/Samsung cylindrical: {cost.get('ndaa_premium_cylindrical', '3-6x')} vs Chinese LiPo. "
                f"US pouch (Amprius pilot scale): {cost.get('ndaa_premium_us_pouch', '10-20x')}. "
                f"Example 6S2P Molicel pack: ${cost.get('example_6s2p_molicel', {}).get('cell_cost_usd', '?')} cells vs "
                f"${cost.get('example_6s2p_molicel', {}).get('comparable_chinese_lipo_usd', '?')} Chinese LiPo equivalent."
            ),
            "confidence": 0.85,
            "prediction": "Cost premium narrows as Amprius/Lyten scale, but remains 2-4x through 2028.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    # === Flag: Emerging tech summary ===
    emerging = materials_data.get("emerging_technologies", [])
    if emerging:
        near_term = [e for e in emerging if e.get("trl", "0").split("-")[0].isdigit() and int(e.get("trl", "0").split("-")[0]) >= 7]
        flags.append({
            "id": flag_id("battery-emerging-tech"),
            "timestamp": now,
            "flag_type": "prediction",
            "severity": "info",
            "title": f"Battery tech pipeline: {len(emerging)} emerging technologies, {len(near_term)} at TRL 7+",
            "detail": (
                " | ".join(f"{e['name']} (TRL {e.get('trl','?')})" for e in emerging)
                + ". Silicon-anode and hydrogen fuel cells are near-term viable. Li-S niche fixed-wing. Solid-state 2028-2030."
            ),
            "confidence": 0.80,
            "prediction": "Silicon-anode lithium-ion is the strongest near-term path to NDAA-compliant high-performance drone batteries.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 10. THERMAL CAMERA SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_thermal_supply_chain(db):
    """Analyze thermal camera supply chain data from data/thermal-supply-chain/."""
    flags = []
    from pathlib import Path
    thermal_dir = Path(__file__).resolve().parent.parent / "data" / "thermal-supply-chain"
    if not thermal_dir.exists():
        return flags

    import json
    thermal_path = thermal_dir / "thermal_manufacturers.json"
    if not thermal_path.exists():
        return flags

    with open(thermal_path) as f:
        data = json.load(f)

    fpa_mfrs = data.get("fpa_manufacturers", [])
    integrators = data.get("camera_integrators", [])
    dji_thermal = data.get("dji_thermal_sourcing", {})
    itar_status = data.get("itar_status", {})
    reg_flags = data.get("regulatory_flags", [])

    # === Flag: FPA manufacturer landscape ===
    us_fpa = [m for m in fpa_mfrs if m.get("country") == "US"]
    allied_fpa = [m for m in fpa_mfrs if m.get("ndaa_compliant") and m.get("country") != "US"]
    chinese_fpa = [m for m in fpa_mfrs if not m.get("ndaa_compliant")]
    if fpa_mfrs:
        flags.append({
            "id": flag_id("thermal-fpa-landscape"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Thermal FPA landscape: {len(fpa_mfrs)} manufacturers — {len(us_fpa)} US, {len(allied_fpa)} allied, {len(chinese_fpa)} Chinese",
            "detail": (
                "US: " + ", ".join(m["name"] for m in us_fpa)
                + ". Allied: " + ", ".join(m["name"] for m in allied_fpa)
                + ". Chinese: " + ", ".join(m["name"] for m in chinese_fpa)
                + ". Teledyne FLIR dominates NDAA-compliant drone thermal (Boson series)."
            ),
            "confidence": 0.92,
            "prediction": "FLIR Boson+ 640 remains the go-to NDAA thermal core. Chinese competition (DJI Zenmuse H30T, Autel EVO Max 4T) pressures on price.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["thermal_supply_chain"],
        })

    # === Flag: DJI thermal sourcing ===
    if dji_thermal:
        fpa_source = dji_thermal.get("fpa_source", "unknown")
        flags.append({
            "id": flag_id("thermal-dji-sourcing"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"DJI thermal sourcing: FPA likely from {fpa_source}",
            "detail": (
                f"DJI thermal cameras (Zenmuse H20T/H30T) use FPAs sourced from {fpa_source}. "
                + (dji_thermal.get("note", ""))
            ),
            "confidence": 0.75,
            "prediction": "As China develops indigenous FPA capability (Guide, IRay), DJI may shift away from allied FPA sources — reducing Western leverage.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["thermal_supply_chain"],
        })

    # === Flag: ITAR considerations ===
    if itar_status:
        itar_items = [k for k, v in itar_status.items() if isinstance(v, dict) and v.get("itar")]
        non_itar = [k for k, v in itar_status.items() if isinstance(v, dict) and not v.get("itar")]
        if itar_items or non_itar:
            flags.append({
                "id": flag_id("thermal-itar"),
                "timestamp": now,
                "flag_type": "compliance",
                "severity": "info",
                "title": f"Thermal ITAR status: {len(non_itar)} ITAR-free cores available for export/commercial use",
                "detail": (
                    f"ITAR-free (EAR-controlled): {', '.join(non_itar[:5])}. "
                    f"ITAR-restricted: {', '.join(itar_items[:5])}. "
                    f"Most drone-grade uncooled VOx microbolometers (≤640x512, ≥12μm pitch) are ITAR-free under EAR 6A003.b.4."
                ),
                "confidence": 0.88,
                "prediction": "ITAR-free thermal cores dominate drone market. Cooled MWIR/LWIR sensors remain ITAR-restricted for military-grade imaging.",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["thermal_supply_chain"],
            })

    # === Flag: Regulatory flags from thermal data ===
    for rf in reg_flags:
        flags.append({
            "id": flag_id(f"thermal-reg-{rf.get('id', rf.get('title','')[:20])}"),
            "timestamp": now,
            "flag_type": "compliance",
            "severity": rf.get("severity", "info"),
            "title": rf.get("title", "Thermal regulatory flag"),
            "detail": rf.get("detail", ""),
            "confidence": rf.get("confidence", 0.75),
            "prediction": rf.get("prediction", ""),
            "platform_id": None,
            "component_id": None,
            "data_sources": ["thermal_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 11. CONTROL LINK (C2) SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_control_link_supply_chain(db):
    """Analyze control link C2 supply chain from data/control-link-supply-chain/."""
    flags = []
    from pathlib import Path
    c2_dir = Path(__file__).resolve().parent.parent / "data" / "control-link-supply-chain"
    if not c2_dir.exists():
        return flags

    import json

    # Load all files
    radio_mfrs = []
    rf_data = {}
    enterprise_data = {}

    rp = c2_dir / "radio_manufacturers.json"
    if rp.exists():
        with open(rp) as f:
            d = json.load(f)
        radio_mfrs = d.get("radio_manufacturers", [])
        ukr_links = d.get("ukrainian_combat_links", [])

    rfp = c2_dir / "rf_chip_supply_chain.json"
    if rfp.exists():
        with open(rfp) as f:
            rf_data = json.load(f)

    ep = c2_dir / "enterprise_and_defense_links.json"
    if ep.exists():
        with open(ep) as f:
            enterprise_data = json.load(f)

    # === Flag: Chinese dominance in FPV radio hardware ===
    chinese_mfrs = [m for m in radio_mfrs if m.get("country", "").startswith("China")]
    allied_mfrs = [m for m in radio_mfrs if m.get("ndaa_compliant")]
    if radio_mfrs:
        flags.append({
            "id": flag_id("c2-chinese-dominance"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"C2 link hardware: {len(chinese_mfrs)}/{len(radio_mfrs)} radio manufacturers are Chinese",
            "detail": (
                f"Chinese: {', '.join(m['name'].split('(')[0].strip() for m in chinese_mfrs)}. "
                f"NDAA-compliant alternatives: {', '.join(m['name'].split('(')[0].strip() for m in allied_mfrs) or 'None'}. "
                f"RadioMaster (Shenzhen) and Jumper (Changzhou) dominate the open-source radio market. "
                f"ImmersionRC/Orqa (Croatia) is the only Western manufacturer with in-house production."
            ),
            "confidence": 0.95,
            "prediction": "ELRS ecosystem remains 95%+ Chinese-manufactured hardware through 2027. Orqa is the only viable NDAA path for FPV-class C2 links.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    # === Flag: Semtech single-source for ELRS ===
    semtech = rf_data.get("semtech_corporate", {})
    if semtech:
        flags.append({
            "id": flag_id("c2-semtech-single-source"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "critical",
            "title": "C2 silicon: Semtech SX1280 is sole-source RF chip for all ELRS hardware — TSMC fab'd",
            "detail": (
                f"Every 2.4 GHz ELRS device uses Semtech SX1280 (US-designed, TSMC-fabricated in Taiwan). "
                f"No second-source LoRa transceiver exists from any vendor. "
                f"Semtech is fabless since 2002 — all wafers from TSMC Fab 6/11. "
                f"900 MHz ELRS uses SX1276/78 (same Semtech/TSMC dependency). "
                f"A Semtech allocation or TSMC disruption halts all ELRS hardware production globally."
            ),
            "confidence": 0.95,
            "prediction": "No alternative LoRa RF silicon is on any vendor's roadmap. ELRS remains single-source Semtech indefinitely.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    # === Flag: Espressif Chinese MCU in ELRS ===
    esp_data = next((m for m in rf_data.get("critical_mcus", []) if m["id"] == "esp32"), None)
    if esp_data:
        flags.append({
            "id": flag_id("c2-espressif-mcu"),
            "timestamp": now,
            "flag_type": "compliance",
            "severity": "warning",
            "title": "C2 compliance: Most ELRS receivers use Espressif (Shanghai) MCU — Chinese IP in 'open-source' link",
            "detail": (
                f"ESP8285 and ESP32 from Espressif Systems (Shanghai) are used in most ELRS receivers for WiFi configuration and OTA updates. "
                f"Even when the RF chip (SX1280) is from US-based Semtech, the MCU running the firmware is Chinese-designed silicon. "
                f"Alternative: STM32 (STMicroelectronics, Switzerland) — used in some receivers and all radios, but less common in nano receivers."
            ),
            "confidence": 0.90,
            "prediction": "ELRS community may shift to STM32-only receivers for NDAA compliance, but ESP-based receivers dominate for cost and WiFi convenience.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    # === Flag: Enterprise C2 gap (SIYI vs Microhard) ===
    gap = enterprise_data.get("ndaa_gap_analysis", {}).get("enterprise_commercial", {})
    if gap:
        flags.append({
            "id": flag_id("c2-enterprise-gap"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": "C2 enterprise gap: SIYI (China) dominates commercial drone links — Microhard (Canada) is 3-5x costlier",
            "detail": (
                f"SIYI MK32/MK15/HM30 are the standard enterprise links for ArduPilot/PX4 commercial drones. "
                f"No NDAA-compliant equivalent exists at SIYI's price point ($300-$1200). "
                f"Microhard pDDL2450 ($3000-$5000) is the NDAA alternative but 3-5x more expensive. "
                f"HereLink Blue marketed for Blue UAS but manufactured in HK/China."
            ),
            "confidence": 0.88,
            "prediction": "SIYI remains embedded in commercial drone ecosystem. Defense programs absorb Microhard/Silvus cost premium. Gap persists for non-defense government buyers.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    # === Flag: Ukrainian combat links ===
    if 'ukr_links' in dir() and ukr_links:
        total_ukr = sum(u.get("products_in_forge", 0) for u in ukr_links)
        flags.append({
            "id": flag_id("c2-ukraine-combat"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"C2 combat links: {len(ukr_links)} Ukrainian manufacturers, {total_ukr} products in Forge — EW-hardened protocols",
            "detail": (
                f"Ukrainian manufacturers ({', '.join(u['name'] for u in ukr_links)}) produce combat-proven control links "
                f"operating on non-standard frequencies (370-560 MHz) with custom EW-resistant protocols. "
                f"These represent real-world validated alternatives to consumer ELRS for contested environments."
            ),
            "confidence": 0.85,
            "prediction": "Ukrainian combat link technology transfers to Western defense programs as NATO FPV drone doctrine matures.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    # === Flag: ELRS protocol landscape ===
    elrs = next((f for f in rf_data.get("firmware_ecosystem", []) if f["id"] == "elrs"), None)
    if elrs:
        flags.append({
            "id": flag_id("c2-elrs-ecosystem"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"C2 protocol: ExpressLRS dominates with ~{elrs.get('market_share_estimate', '70-80%')} of FPV builds — open-source, single-source silicon",
            "detail": (
                f"ELRS is open-source (GPL-3.0) with 1000 Hz packet rate on 2.4 GHz. "
                f"Protocol is hardware-agnostic but all silicon is Semtech SX1280 (sole-source). "
                f"Supported by {len(elrs.get('supported_manufacturers', []))} manufacturers, all Chinese except ImmersionRC/Orqa. "
                f"Crossfire (TBS, HK/Austria) declining to ~15-20%. DJI RC protocol is closed/proprietary."
            ),
            "confidence": 0.90,
            "prediction": "ELRS continues to gain share. Protocol openness enables future NDAA hardware if a Western manufacturer scales production.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["control_link_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 12. FC+ESC STACK SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_stack_supply_chain(db):
    """Analyze FC+ESC stack supply chain from data/stack-supply-chain/."""
    flags = []
    from pathlib import Path
    stack_dir = Path(__file__).resolve().parent.parent / "data" / "stack-supply-chain"
    if not stack_dir.exists():
        return flags

    import json

    mfr_data = {}
    silicon_data = {}

    mp = stack_dir / "stack_manufacturers.json"
    if mp.exists():
        with open(mp) as f:
            mfr_data = json.load(f)

    sp = stack_dir / "silicon_and_firmware.json"
    if sp.exists():
        with open(sp) as f:
            silicon_data = json.load(f)

    # === Flag: Chinese PCB assembly dominance ===
    country = mfr_data.get("country_breakdown", {})
    china_pct = country.get("China", {}).get("pct", 0)
    if china_pct > 0:
        flags.append({
            "id": flag_id("stack-china-pcb"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Stack supply: {china_pct}% of FC+ESC stacks are Chinese-manufactured — PCBA is the bottleneck",
            "detail": (
                f"Of 115 stacks in Forge DB, {china_pct}% are from Chinese manufacturers (SkyStars, Diatone, Flywoo, SpeedyBee, etc.). "
                f"Even US brands (NewBeeDrone, Lumenier) likely use Chinese contract manufacturers for PCB assembly. "
                f"Virtually all FPV-grade PCBs are assembled in Shenzhen. NDAA compliance requires US/allied PCBA — very limited capacity exists."
            ),
            "confidence": 0.92,
            "prediction": "PCB assembly remains the hardest NDAA bottleneck for stacks. No significant allied PCBA capacity for FPV-grade boards before 2028.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["stack_supply_chain"],
        })

    # === Flag: AT32 Chinese MCU infiltration ===
    at32 = next((m for m in silicon_data.get("fc_mcu_landscape", {}).get("mcus", []) if m["id"] == "at32f435"), None)
    if at32:
        flags.append({
            "id": flag_id("stack-at32-infiltration"),
            "timestamp": now,
            "flag_type": "compliance",
            "severity": "warning",
            "title": "Stack MCU: AT32 (Chinese ArteryTek) gaining rapid FC+ESC adoption — threatens NDAA compliance",
            "detail": (
                f"AT32F435 (Chongqing, China) is 30-50% cheaper than STM32F405 and now has full Betaflight support. "
                f"AT32F421 is the most popular new ESC MCU. "
                f"Even nominally US/allied stack brands may adopt AT32 to cut costs. "
                f"STM32 (STMicroelectronics, Switzerland) remains the NDAA-compliant alternative for both FC and ESC MCUs."
            ),
            "confidence": 0.88,
            "prediction": "AT32 adoption accelerates in budget and mid-range stacks. NDAA-compliant builds must explicitly verify STM32 MCU, not assume it.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["stack_supply_chain"],
        })

    # === Flag: ESC firmware — AM32 as NDAA path ===
    firmware = silicon_data.get("esc_firmware_ecosystem", [])
    am32 = next((f for f in firmware if f["id"] == "am32"), None)
    blheli = next((f for f in firmware if f["id"] == "blheli_32"), None)
    if am32 and blheli:
        flags.append({
            "id": flag_id("stack-am32-ndaa-path"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": "ESC firmware: AM32 (open-source) is the best NDAA path — runs on STM32, auditable, Betaflight-recommended",
            "detail": (
                f"AM32 is open-source (GPL), supports allied MCUs (STM32G071, STM32F051), and is Betaflight-recommended. "
                f"BLHeli_32 is closed-source with per-unit licensing — cannot be audited for supply chain compliance. "
                f"However, AM32 also supports Chinese MCUs (AT32F421, GD32E230) — MCU choice, not firmware, determines NDAA status."
            ),
            "confidence": 0.85,
            "prediction": "AM32 + STM32 ESC MCU is the viable NDAA-compliant ESC stack. BLHeli_32's closed-source model becomes a liability for defense procurement.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["stack_supply_chain"],
        })

    # === Flag: IMU supply is allied ===
    imu = silicon_data.get("imu_sensors", {})
    if imu.get("ndaa_status"):
        flags.append({
            "id": flag_id("stack-imu-allied"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": "Stack IMU: Allied supply — Bosch BMI270 (Germany) and InvenSense ICM-42688 (US/Japan) dominate",
            "detail": (
                f"Both major FC IMU vendors are NDAA-compliant. Bosch Sensortec (Germany) BMI270 is the Betaflight standard. "
                f"InvenSense/TDK (US/Japan) ICM-42688-P is the premium alternative. "
                f"IMU is NOT a supply chain chokepoint for NDAA compliance."
            ),
            "confidence": 0.92,
            "prediction": "IMU supply remains stable and allied. No Chinese dependency for FC inertial sensors.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["stack_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 13. VIDEO TRANSMITTER (VTX) SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_vtx_supply_chain(db):
    """Analyze VTX supply chain from data/vtx-supply-chain/."""
    flags = []
    from pathlib import Path
    vtx_dir = Path(__file__).resolve().parent.parent / "data" / "vtx-supply-chain"
    if not vtx_dir.exists():
        return flags

    import json
    vp = vtx_dir / "vtx_manufacturers.json"
    if not vp.exists():
        return flags

    with open(vp) as f:
        data = json.load(f)

    systems = data.get("video_systems", [])
    country = data.get("country_breakdown_vtx", {})

    # === Flag: Divimath/HDZero as NDAA digital FPV path ===
    hdzero = next((s for s in systems if s["id"] == "hdzero"), None)
    if hdzero:
        flags.append({
            "id": flag_id("vtx-divimath-ndaa"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": "VTX NDAA path: Divimath (US) is the only NDAA-compliant digital FPV system — proprietary ASICs, Thailand manufacturing",
            "detail": (
                f"Divimath, Inc. (US company) makes HDZero — the only digital FPV system with an NDAA-compliant product line. "
                f"NDAA line: proprietary ASICs (no off-the-shelf Chinese silicon), manufactured in Thailand by allied-owned factories, encrypted video. "
                f"HDZero hobby line is still assembled in China. "
                f"Divimath is also building NDAA-compliant FCs (STM32H743, Thailand-manufactured). "
                f"This is the most credible path to a full NDAA-compliant FPV electronics stack."
            ),
            "confidence": 0.92,
            "prediction": "Divimath becomes the reference NDAA digital FPV platform for defense and federal drone programs.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["vtx_supply_chain"],
        })

    # === Flag: Chinese dominance in video systems ===
    china_pct = country.get("China", {}).get("pct", 0)
    if china_pct > 0:
        flags.append({
            "id": flag_id("vtx-chinese-dominance"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"VTX supply: {china_pct}% of video transmitters are Chinese — DJI and Walksnail dominate digital",
            "detail": (
                f"Of {sum(c.get('count',0) for c in country.values())} VTXs in Forge DB, {china_pct}% are from Chinese manufacturers. "
                f"DJI O3/O4 (proprietary, banned under ASDA/NDAA) and Walksnail Avatar (Caddx, Shenzhen) control the digital FPV market. "
                f"HDZero/Divimath (US) is the sole NDAA digital option. Analog remains available from ImmersionRC/Orqa (Croatia)."
            ),
            "confidence": 0.93,
            "prediction": "DJI and Walksnail maintain digital FPV dominance. Divimath grows in defense segment. Analog persists for budget and combat use.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["vtx_supply_chain"],
        })

    # === Flag: OpenIPC — open-source but Chinese silicon ===
    openipc = next((s for s in systems if s["id"] == "openipc"), None)
    if openipc:
        flags.append({
            "id": flag_id("vtx-openipc-chinese"),
            "timestamp": now,
            "flag_type": "compliance",
            "severity": "info",
            "title": "VTX: OpenIPC is open-source digital FPV but uses HiSilicon/Huawei SoCs — not NDAA viable",
            "detail": (
                f"OpenIPC repurposes Chinese IP camera SoCs (HiSilicon Hi3516, Sigmastar) for ultra-low-cost digital FPV. "
                f"Open-source firmware but Chinese hardware — HiSilicon is a Huawei subsidiary on the Entity List. "
                f"Demonstrates open-source digital FPV is technically feasible, but not viable for NDAA compliance."
            ),
            "confidence": 0.88,
            "prediction": "OpenIPC grows in hobbyist/combat use (Ukraine adoption) but remains non-compliant for US government procurement.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["vtx_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 14. ESC SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_esc_supply_chain(db):
    """Analyze ESC supply chain from data/esc-supply-chain/."""
    flags = []
    from pathlib import Path
    esc_dir = Path(__file__).resolve().parent.parent / "data" / "esc-supply-chain"
    if not esc_dir.exists():
        return flags

    import json
    ep = esc_dir / "esc_manufacturers.json"
    if not ep.exists():
        return flags

    with open(ep) as f:
        data = json.load(f)

    mfrs = data.get("esc_manufacturers", [])
    country = data.get("country_breakdown", {})
    firmware = data.get("firmware_breakdown", {})
    ndaa = data.get("ndaa_esc_landscape", {})

    # === Flag: NDAA ESC options ===
    fpv_options = ndaa.get("fpv_class", {}).get("compliant_options", [])
    if fpv_options:
        flags.append({
            "id": flag_id("esc-ndaa-options"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"ESC NDAA: {len(fpv_options)} compliant FPV-class options — Lumenier (US), FETtec (Germany), Divimath (US/Thailand)",
            "detail": (
                f"FPV-class NDAA ESCs: {', '.join(fpv_options)}. "
                f"FETtec (Germany) is the only manufacturer with confirmed European PCB assembly and proprietary FOC firmware. "
                f"Lumenier NDAA line uses AM32 on STM32 — US design but PCB assembly origin requires verification. "
                f"Cost premium: {ndaa.get('fpv_class', {}).get('cost_premium', '1.5-3x')} vs Chinese equivalents."
            ),
            "confidence": 0.88,
            "prediction": "FETtec and Divimath emerge as reference NDAA ESC suppliers. Lumenier scales NDAA line as defense demand grows.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["esc_supply_chain"],
        })

    # === Flag: BLHeli_32 closed-source risk ===
    blheli = firmware.get("BLHeli_32", {})
    am32 = firmware.get("AM32", {})
    if blheli and am32:
        flags.append({
            "id": flag_id("esc-blheli32-risk"),
            "timestamp": now,
            "flag_type": "compliance",
            "severity": "warning",
            "title": f"ESC firmware: BLHeli_32 (closed-source) still on {blheli.get('pct',0)}% of ESCs — unauditable for defense",
            "detail": (
                f"BLHeli_32 is closed-source firmware with per-unit licensing. Cannot be audited for supply chain compliance. "
                f"Betaflight officially recommends AM32 (open-source) and warns of bugs in BLHeli_32 versions after 32.7. "
                f"AM32 currently on {am32.get('pct',0)}% of ESCs but growing. "
                f"Defense procurement should require AM32 or proprietary allied firmware (FETtec, KDE, Vertiq)."
            ),
            "confidence": 0.85,
            "prediction": "AM32 overtakes BLHeli_32 in new ESC designs by 2027. BLHeli_32 becomes legacy.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["esc_supply_chain"],
        })

    # === Flag: FETtec as European champion ===
    fettec = next((m for m in mfrs if m["id"] == "fettec"), None)
    if fettec:
        flags.append({
            "id": flag_id("esc-fettec-eu"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": "ESC: FETtec (Germany) — European-manufactured FOC ESC with proprietary firmware, genuine NDAA alternative",
            "detail": (
                f"FETtec is German-engineered with proprietary sinusoidal FOC firmware (smoother and more efficient than trapezoidal). "
                f"First to use STM32G473 MCU. European PCB assembly confirmed. "
                f"{fettec.get('products_in_forge', 0)} products in Forge DB. Premium pricing but genuinely allied supply chain."
            ),
            "confidence": 0.90,
            "prediction": "FETtec gains defense/enterprise adoption as NDAA deadlines approach. May license firmware to other allied manufacturers.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["esc_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 15. ALLIED MANUFACTURER PROFILES
# ══════════════════════════════════════════════════════════════

def analyze_allied_manufacturers(db):
    """Analyze allied manufacturer profiles from data/allied/."""
    flags = []
    from pathlib import Path
    allied_dir = Path(__file__).resolve().parent.parent / "data" / "allied"
    if not allied_dir.exists():
        return flags

    import json

    for fp in sorted(allied_dir.glob("*_profile.json")):
        with open(fp) as f:
            profile = json.load(f)

        name = profile.get("name", "Unknown")
        country = profile.get("country", "Unknown")
        sig = profile.get("strategic_significance", {})
        mfg = profile.get("manufacturing", {})
        risks = profile.get("risk_factors", [])
        customers = profile.get("defense_customers", [])
        cap = mfg.get("capacity_drones_per_year", 0)
        china_free = profile.get("china_free", False)

        # Main profile flag
        flags.append({
            "id": flag_id(f"allied-{profile.get('id', name.lower())}"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Allied manufacturer: {name} ({country}) — {cap:,} drones/year capacity, {'China-free' if china_free else 'origin TBD'}",
            "detail": sig.get("summary", ""),
            "confidence": 0.90,
            "prediction": sig.get("us_market", ""),
            "platform_id": None,
            "component_id": None,
            "data_sources": ["allied_manufacturers"],
        })

        # Defense customers flag if significant
        active_customers = [c for c in customers if c.get("status", "").startswith(("ordered", "purchased", "active"))]
        if len(active_customers) >= 2:
            flags.append({
                "id": flag_id(f"allied-{profile.get('id','')}-defense"),
                "timestamp": now,
                "flag_type": "component_analysis",
                "severity": "info",
                "title": f"Allied defense: {name} has {len(active_customers)} confirmed defense customers",
                "detail": " | ".join(
                    f"{c['customer']}: {c.get('product', 'drones')}" for c in active_customers
                ),
                "confidence": 0.88,
                "prediction": "",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["allied_manufacturers"],
            })

        # Risk flag if Chinese component incident
        china_incidents = [r for r in risks if "chinese" in r.lower() or "china" in r.lower()]
        if china_incidents:
            flags.append({
                "id": flag_id(f"allied-{profile.get('id','')}-risk"),
                "timestamp": now,
                "flag_type": "compliance",
                "severity": "warning",
                "title": f"Allied risk: {name} — {len(china_incidents)} China-related supply chain incident(s)",
                "detail": " | ".join(china_incidents),
                "confidence": 0.85,
                "prediction": "Any future component origin issues in NDAA-marketed products would severely damage credibility with DoD procurement.",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["allied_manufacturers"],
            })

    return flags


# ══════════════════════════════════════════════════════════════
# 16. FPV CAMERA SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_fpv_camera_supply_chain(db):
    """Analyze FPV camera supply chain from data/fpv-camera-supply-chain/."""
    flags = []
    from pathlib import Path
    cam_dir = Path(__file__).resolve().parent.parent / "data" / "fpv-camera-supply-chain"
    if not cam_dir.exists():
        return flags

    import json
    cp = cam_dir / "fpv_camera_landscape.json"
    if not cp.exists():
        return flags

    with open(cp) as f:
        data = json.load(f)

    country = data.get("country_breakdown", {})
    sensors = data.get("image_sensor_supply_chain", {})
    gap = data.get("ndaa_gap", {})

    china_pct = country.get("China", {}).get("pct", 0)
    if china_pct > 0:
        flags.append({
            "id": flag_id("cam-chinese-dominance"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"FPV camera: {china_pct}% Chinese-manufactured — Foxeer, Caddx, RunCam dominate",
            "detail": (
                f"Of 193 FPV cameras in Forge DB, {china_pct}% are from Chinese manufacturers. "
                f"Foxeer (79), Caddx (43), RunCam (30) account for 79% of all FPV cameras. All Shenzhen-based. "
                f"Sony (Japan) CMOS sensors used in ~90% of cameras — sensor silicon is NDAA-compliant, but camera PCB assembly is entirely Chinese. "
                f"{gap.get('problem', '')}"
            ),
            "confidence": 0.95,
            "prediction": "FPV cameras remain the most China-dependent component category. Divimath NDAA cameras and Orqa in-house production are the only allied alternatives.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["fpv_camera_supply_chain"],
        })

    # Sony sensor as bright spot
    sony = next((v for v in sensors.get("sensor_vendors", []) if "Sony" in v.get("name", "")), None)
    if sony:
        flags.append({
            "id": flag_id("cam-sony-sensor-allied"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"FPV sensor: Sony (Japan) supplies ~{sony.get('market_share_pct', 90)}% of FPV camera sensors — allied silicon, Chinese assembly",
            "detail": (
                f"Sony Starvis/Starvis II CMOS sensors are the industry standard for FPV cameras. "
                f"Fabricated in Japan (Kumamoto, Nagasaki). NDAA-compliant at the sensor level. "
                f"The gap is camera PCB assembly (Shenzhen) and ISP chips (varies). "
                f"A hypothetical NDAA FPV camera needs: Sony sensor + allied ISP + allied PCB assembly."
            ),
            "confidence": 0.92,
            "prediction": "Sony sensor supply remains stable and allied. Camera assembly is the NDAA bottleneck, not sensor silicon.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["fpv_camera_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 17. FRAME SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_frame_supply_chain(db):
    """Analyze frame supply chain from data/frame-supply-chain/."""
    flags = []
    from pathlib import Path
    frame_dir = Path(__file__).resolve().parent.parent / "data" / "frame-supply-chain"
    if not frame_dir.exists():
        return flags

    import json
    fp = frame_dir / "frame_landscape.json"
    if not fp.exists():
        return flags

    with open(fp) as f:
        data = json.load(f)

    country = data.get("country_breakdown", {})
    cf = data.get("carbon_fiber_supply_chain", {})
    ndaa = data.get("ndaa_frame_assessment", {})

    # === Flag: Frames are easiest NDAA path ===
    if ndaa:
        flags.append({
            "id": flag_id("frame-ndaa-easy"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": "Frames: Easiest component to make NDAA-compliant — Toray (Japan) carbon fiber + allied CNC cutting",
            "detail": (
                f"{ndaa.get('good_news', '')} "
                f"US brands (Lumenier, Armattan, ImpulseRC) design domestically but likely CNC-cut in China for cost. "
                f"Moving to US/EU CNC adds {cf.get('cnc_cutting', {}).get('cost_premium', '2-4x')} cost premium."
            ),
            "confidence": 0.92,
            "prediction": ndaa.get("realistic_path", ""),
            "platform_id": None,
            "component_id": None,
            "data_sources": ["frame_supply_chain"],
        })

    # === Flag: Carbon fiber precursor is allied ===
    precursors = cf.get("precursor_manufacturers", [])
    allied_precursors = [p for p in precursors if p.get("ndaa_compliant")]
    toray = next((p for p in precursors if "Toray" in p.get("name", "")), None)
    if toray:
        flags.append({
            "id": flag_id("frame-toray-allied"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Carbon fiber: {len(allied_precursors)} allied precursor manufacturers — Toray (Japan/USA) dominates at {toray.get('market_share_pct', 30)}%",
            "detail": (
                f"Toray Industries (Japan) is the world's largest carbon fiber producer. "
                f"US production: Toray CMA in Decatur, AL. NDAA-compliant carbon fiber is available on US soil. "
                f"Chinese producers (~20% share) are gaining but quality still below Toray T300 for structural applications. "
                f"Even Chinese frame factories typically use Toray precursor."
            ),
            "confidence": 0.90,
            "prediction": "Carbon fiber precursor remains a Japanese/allied strength. Chinese producers narrow quality gap but Toray retains premium drone market.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["frame_supply_chain"],
        })

    # === Flag: US has strong frame brand presence ===
    us_pct = country.get("USA", {}).get("pct", 0)
    us_count = country.get("USA", {}).get("count", 0)
    if us_pct > 0:
        flags.append({
            "id": flag_id("frame-us-brands"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Frames: {us_pct}% US-branded ({us_count} frames) — strongest US presence of any component category",
            "detail": (
                f"Lumenier (88), XILO (15), Armattan (12), ImpulseRC (11) give the US 30% of frame products. "
                f"This is the highest US share of any major component category. "
                f"Ukraine adds 6% (22 frames — PIRAT, FiberForm, combat-proven designs). "
                f"Combined allied share: 36% — only category where China doesn't exceed 70%."
            ),
            "confidence": 0.90,
            "prediction": "Frames become the reference 'NDAA success story' as US brands move CNC cutting to domestic shops.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["frame_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 18. RECEIVER SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_receiver_supply_chain(db):
    """Analyze receiver supply chain from data/receiver-supply-chain/."""
    flags = []
    from pathlib import Path
    rx_dir = Path(__file__).resolve().parent.parent / "data" / "receiver-supply-chain"
    if not rx_dir.exists():
        return flags

    import json
    rp = rx_dir / "receiver_landscape.json"
    if not rp.exists():
        return flags

    with open(rp) as f:
        data = json.load(f)

    mcu = data.get("mcu_breakdown", {})
    combat = data.get("combat_frequency_landscape", {})
    ukr = data.get("ukrainian_receiver_ecosystem", {})
    ndaa = data.get("ndaa_receiver_assessment", {})

    # === Flag: Espressif MCU dominance in receivers ===
    esp_total = sum(mcu.get(k, {}).get("count", 0) for k in ["esp8285", "esp32_c3", "esp32", "esp32_s3"])
    stm_total = mcu.get("stm32", {}).get("count", 0)
    if esp_total > 0:
        flags.append({
            "id": flag_id("rx-espressif-dominance"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Receiver MCU: {esp_total} receivers use Espressif (Shanghai) silicon vs {stm_total} STM32 — hidden Chinese dependency",
            "detail": (
                f"60% of ELRS receivers with known MCU use Espressif ESP8285/ESP32 from Shanghai. "
                f"Only 4% use STM32 (STMicroelectronics, Switzerland). "
                f"{mcu.get('ndaa_concern', '')} "
                f"WiFi OTA update convenience drives ESP adoption, but it embeds Chinese silicon into every receiver."
            ),
            "confidence": 0.92,
            "prediction": "ELRS community unlikely to shift away from ESP due to WiFi convenience. NDAA builds must explicitly source STM32-based receivers.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["receiver_supply_chain"],
        })

    # === Flag: Ukrainian combat receiver ecosystem ===
    if ukr.get("total", 0) > 0:
        flags.append({
            "id": flag_id("rx-ukraine-ecosystem"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Receivers: Ukraine has {ukr['total']} receivers from {ukr.get('manufacturers', 0)} manufacturers — largest allied receiver ecosystem",
            "detail": (
                f"Ukraine's {ukr.get('manufacturers', 0)} receiver manufacturers outnumber any other allied nation. "
                f"Key brands: {', '.join(ukr.get('key_manufacturers', [])[:4])}. "
                f"Many run MafiaLRS (combat-optimized ELRS fork with EW hardening). "
                f"37 receivers operate on non-standard frequencies (400-500 MHz) to avoid jammed ISM bands."
            ),
            "confidence": 0.88,
            "prediction": "Ukrainian combat receiver tech transfers to NATO programs. Non-standard frequency operation becomes doctrine for contested environments.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["receiver_supply_chain"],
        })

    # === Flag: Combat frequency diversity ===
    combat_ns = combat.get("combat_non_standard", {})
    if combat_ns.get("total", 0) > 0:
        flags.append({
            "id": flag_id("rx-combat-frequencies"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Receivers: {combat_ns['total']} combat receivers on non-standard frequencies (400-500 MHz) — EW-resilient",
            "detail": (
                f"Standard FPV uses 2.4 GHz (control) and 5.8 GHz (video) — both heavily jammed in EW environments. "
                f"Ukrainian manufacturers produce receivers at 400 MHz ({combat_ns.get('400mhz', {}).get('count', 0)}), "
                f"500 MHz ({combat_ns.get('500mhz', {}).get('count', 0)}), and 433 MHz ({combat_ns.get('433mhz', {}).get('count', 0)}). "
                f"These frequencies offer better penetration and avoid consumer-band jamming."
            ),
            "confidence": 0.85,
            "prediction": "Frequency-agile receivers become standard for defense FPV. NATO adopts multi-band approach from Ukrainian combat experience.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["receiver_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 19. ANTENNA SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_antenna_supply_chain(db):
    """Analyze antenna supply chain from data/antenna-supply-chain/."""
    flags = []
    from pathlib import Path
    ant_dir = Path(__file__).resolve().parent.parent / "data" / "antenna-supply-chain"
    if not ant_dir.exists():
        return flags

    import json
    ap = ant_dir / "antenna_landscape.json"
    if not ap.exists():
        return flags

    with open(ap) as f:
        data = json.load(f)

    ndaa = data.get("ndaa_antenna_assessment", {})
    country = data.get("country_breakdown", {})

    if ndaa:
        allied_pct = ndaa.get("allied_share_pct", 0)
        flags.append({
            "id": flag_id("ant-ndaa-strong"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Antennas: {allied_pct}% allied-branded — most NDAA-compliant component category. Solved problem.",
            "detail": (
                f"TrueRC (Canada, 95 products, patented, manufactured in Canada), Lumenier (US, 92), VAS (US, 78) dominate. "
                f"Antennas are passive RF components — no electronics, firmware, or Chinese silicon dependency. "
                f"Allied manufacturing is mature and cost-competitive. Not a supply chain concern for NDAA builds."
            ),
            "confidence": 0.95,
            "prediction": "Antennas remain the NDAA reference category. TrueRC expands defense/enterprise business.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["antenna_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 20. PROPELLER SUPPLY CHAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_propeller_supply_chain(db):
    """Analyze propeller supply chain from data/propeller-supply-chain/."""
    flags = []
    from pathlib import Path
    prop_dir = Path(__file__).resolve().parent.parent / "data" / "propeller-supply-chain"
    if not prop_dir.exists():
        return flags

    import json
    pp = prop_dir / "propeller_landscape.json"
    if not pp.exists():
        return flags

    with open(pp) as f:
        data = json.load(f)

    country = data.get("country_breakdown", {})
    ndaa = data.get("ndaa_propeller_assessment", {})

    china_pct = country.get("China", {}).get("pct", 0)
    if ndaa:
        flags.append({
            "id": flag_id("prop-chinese-but-fixable"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Propellers: {china_pct}% Chinese (HQProp + Gemfan = 81%) but easiest to reshore — no electronics, commodity injection molding",
            "detail": (
                f"Propellers are injection-molded thermoplastics with no electronics, firmware, or silicon. "
                f"Raw materials (polycarbonate, nylon) available from allied sources (Covestro Germany, BASF, DuPont). "
                f"APC (Woodland, CA) already manufactures propellers in the US. "
                f"Barrier is aerodynamic design IP (HQProp/Gemfan hold 50+ combined patents), not manufacturing capability."
            ),
            "confidence": 0.90,
            "prediction": "Propellers follow frames as next NDAA reshoring success. APC expands FPV line. US injection molding at 2-3x premium for consumable component.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["propeller_supply_chain"],
        })

    return flags


# ══════════════════════════════════════════════════════════════
# 17. LIVE PRICING — Mouser + DigiKey
# ══════════════════════════════════════════════════════════════

def analyze_live_pricing(db):
    """
    Generate PIE flags from live Mouser/DigiKey pricing data.
    Requires MOUSER_API_KEY and/or DIGIKEY_CLIENT_ID + DIGIKEY_CLIENT_SECRET env vars.
    Falls back gracefully if keys not set.
    """
    flags = []
    import os
    from pathlib import Path

    # Only run if at least one API key is available
    mouser_key = os.environ.get("MOUSER_API_KEY", "")
    dk_id = os.environ.get("DIGIKEY_CLIENT_ID", "")
    dk_secret = os.environ.get("DIGIKEY_CLIENT_SECRET", "")

    if not mouser_key and not (dk_id and dk_secret):
        return flags  # No keys — skip silently

    try:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from pricing import analyze_pricing_signals
        parts_db_dir = Path(__file__).resolve().parent.parent / "data" / "parts-db"
        flags = analyze_pricing_signals(parts_db_dir)
    except Exception as e:
        print(f"  [Pricing] analyze_live_pricing error: {e}")

    return flags


# ══════════════════════════════════════════════════════════════
# 18. BATTERY PARTS-DB ENRICHMENT FLAGS
# ══════════════════════════════════════════════════════════════

def analyze_battery_partsdb(db):
    """
    Generate PIE flags from cell_manufacturer enrichment in parts-db/batteries.json.
    Flags NDAA ban timelines, Chinese cell dependency, Molicel shortage exposure.
    """
    import json
    from pathlib import Path

    flags = []
    parts_db = Path(__file__).resolve().parent.parent / "data" / "parts-db" / "batteries.json"
    if not parts_db.exists():
        return flags

    batteries = json.loads(parts_db.read_text())
    if not isinstance(batteries, list):
        return flags

    total = len(batteries)
    chinese = [b for b in batteries if b.get("cell_country") == "China"]
    ndaa_ok = [b for b in batteries if b.get("cell_ndaa_compliant") is True]
    ndaa_bad = [b for b in batteries if b.get("cell_ndaa_compliant") is False]
    molicel = [b for b in batteries if "Molicel" in b.get("cell_manufacturer", "")]
    unknown = [b for b in batteries if b.get("cell_manufacturer") == "Unknown" or not b.get("cell_manufacturer")]

    # NDAA ban timeline flags
    NDAA_BANS = {
        "EVE Energy": "October 2027",
        "CATL": "October 2027",
        "BYD": "October 2027",
        "CALB": "October 2027",
        "Gotion": "October 2027",
        "SVOLT": "October 2027",
    }
    for banned_mfr, ban_date in NDAA_BANS.items():
        affected = [b for b in batteries if banned_mfr.lower() in b.get("cell_manufacturer", "").lower()]
        if affected:
            flags.append({
                "id": flag_id(f"battery-ndaa-ban-{banned_mfr.lower().replace(' ', '-')}"),
                "timestamp": now,
                "flag_type": "compliance",
                "severity": "critical",
                "title": f"Battery NDAA ban: {len(affected)} packs use {banned_mfr} cells — banned from DoD use {ban_date}",
                "detail": (
                    f"FY2024 NDAA Section 154 bans procurement of batteries containing cells from {banned_mfr} "
                    f"effective {ban_date}. {len(affected)} Forge DB batteries affected. "
                    f"Procurement planning must identify alternatives before ban date."
                ),
                "confidence": 0.97,
                "prediction": f"Any platform relying on {banned_mfr} cells must re-qualify with alternative cell by {ban_date}.",
                "platform_id": None,
                "component_id": None,
                "data_sources": ["battery_parts_db", "ndaa_fy2024"],
            })

    # Chinese cell dependency summary
    chinese_pct = round(len(chinese) / total * 100) if total else 0
    if chinese_pct > 50:
        flags.append({
            "id": flag_id("battery-chinese-cells-partsdb"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "critical",
            "title": f"Battery DB: {chinese_pct}% of {total} tracked batteries use Chinese cells (Forge parts-db verified)",
            "detail": (
                f"{len(chinese)}/{total} batteries in the Forge parts-db have confirmed Chinese cell sourcing. "
                f"Key brands: Tattu→Grepow (Shenzhen), Lumenier LiPo→Shenzhen OEM. "
                f"Only {len(ndaa_ok)} batteries ({round(len(ndaa_ok)/total*100)}%) are NDAA-compliant. "
                f"NDAA FEOC ban effective January 2028 will affect all remaining Chinese-cell packs."
            ),
            "confidence": 0.95,
            "prediction": "86% of available UAS battery inventory will require replacement or re-qualification before 2028 NDAA FEOC deadline.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_parts_db"],
        })

    # Molicel exposure
    if molicel:
        flags.append({
            "id": flag_id("battery-molicel-exposure-partsdb"),
            "timestamp": now,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Battery DB: {len(molicel)} NDAA-compliant packs depend on Molicel (Taiwan, capacity halved July 2025)",
            "detail": (
                f"{len(molicel)} batteries in Forge DB use Molicel cells (P42A/P45B/P50B/P60C). "
                f"Molicel is the primary non-Chinese source for high-drain cylindrical drone cells. "
                f"Kaohsiung factory fire July 2025 halved capacity from 3.3→1.5 GWh. "
                f"Canada plant suspended Nov 2024. Lead times now 16-24 weeks."
            ),
            "confidence": 0.93,
            "prediction": "Molicel-dependent platforms face extended lead times and price increases through 2026-2027.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_parts_db", "battery_supply_chain"],
        })

    # Unknown cell sourcing
    if len(unknown) > 5:
        flags.append({
            "id": flag_id("battery-unknown-cells"),
            "timestamp": now,
            "flag_type": "component_analysis",
            "severity": "info",
            "title": f"Battery DB: {len(unknown)} batteries have unidentified cell sourcing — manual research needed",
            "detail": (
                f"{len(unknown)} batteries in Forge DB have unknown cell_manufacturer. "
                f"These cannot be assessed for NDAA compliance or supply chain risk until cell sourcing is confirmed."
            ),
            "confidence": 0.85,
            "prediction": "Unknown-origin batteries should be assumed Chinese-sourced until verified otherwise.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["battery_parts_db"],
        })

    return flags
