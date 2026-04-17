#!/usr/bin/env python3
"""
PIE Prediction Engine — Multi-Model Ensemble Scorer
====================================================
Five independent models, confidence-weighted ensemble.

Models:
  1. ConcentrationRisk   — BOM concentration → supply disruption probability
  2. ContractSignal      — DoD contract flag velocity → demand pressure
  3. RegulatoryProgression — legislative stage → enforcement timing
  4. GrayZoneEscalation  — entity risk score + legal momentum → action probability
  5. CrossCorrelation    — trigger/outcome flag co-occurrence → cascade probability
"""

import json, math, hashlib, os
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent
now = datetime.now(timezone.utc).isoformat()

# Production parameters loaded from PREDICTION_PARAMS env var
_DEFAULT_PARAMS = {
    "concentration_risk_baseline": 0.40,
    "contract_signal_baseline": 0.40,
    "contract_signal_critical_weight": 0.08,
    "contract_signal_warning_weight": 0.04,
    "regulatory_baseline": 0.30,
    "grayzone_baseline": 0.30,
    "cross_correlation_baseline": 0.35,
    "cross_correlation_trigger_cap": 20,
    "black_swan_cap": 0.25,
}
PARAMS = {**_DEFAULT_PARAMS, **json.loads(os.environ.get("PREDICTION_PARAMS", "{}"))}


def pred_id(seed): return "pred-" + hashlib.md5(seed.encode()).hexdigest()[:10]
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))


def weighted_ensemble(model_outputs):
    if not model_outputs: return 0.5, 0.0
    total_weight = sum(m["confidence"] for m in model_outputs)
    if total_weight == 0: return 0.5, 0.0
    prob = sum(m["probability"] * m["confidence"] for m in model_outputs) / total_weight
    conf = total_weight / len(model_outputs)
    return clamp(prob), clamp(conf)


# ── Model 1: Concentration Risk ───────────────────────────────────

def model_concentration_risk(db, target_component, target_vendors, baseline_prob=None):
    if baseline_prob is None:
        baseline_prob = PARAMS["concentration_risk_baseline"]
    # Support both flat db (pipeline) and nested (forge_database.json)
    cat_items = db.get(target_component) or db.get("components", {}).get(target_component, [])
    models = db.get("drone_models", [])

    if not cat_items:
        return {"model": "concentration_risk", "probability": baseline_prob,
                "confidence": 0.1, "signal_count": 0, "drivers": ["No component data"]}

    target_count = 0
    total_count = len(cat_items)
    for item in cat_items:
        text = " ".join(str(v) for v in item.values() if isinstance(v, (str, int, float))).lower()
        if any(v.lower() in text for v in target_vendors):
            target_count += 1

    concentration_ratio = target_count / total_count if total_count else 0
    blue_count = len([m for m in models if m.get("blue_uas") or m.get("ndaa_compliant")])

    prob = baseline_prob + (0.90 - baseline_prob) * (1 - math.exp(-3 * concentration_ratio))
    if blue_count >= 10:
        prob = clamp(prob * 1.10)

    confidence = clamp(0.3 + 0.5 * (total_count / 50) + 0.2 * (blue_count / 20))

    return {
        "model": "concentration_risk",
        "probability": round(prob, 3),
        "confidence": round(confidence, 3),
        "signal_count": total_count,
        "drivers": [
            f"{target_count}/{total_count} {target_component} use target vendor(s) ({concentration_ratio:.0%} concentration)",
            f"{blue_count} Blue UAS platforms in Forge DB exposed",
        ],
    }


# ── Model 2: Contract Signal ──────────────────────────────────────

def model_contract_signal(flags, component_keywords, baseline_prob=None):
    if baseline_prob is None:
        baseline_prob = PARAMS["contract_signal_baseline"]
    contract_flags = [f for f in flags
                      if f.get("flag_type") in ("contract_signal", "procurement_spike")
                      and any(kw.lower() in (f.get("title","") + f.get("detail","")).lower()
                              for kw in component_keywords)]

    critical = [f for f in contract_flags if f.get("severity") == "critical"]
    warning  = [f for f in contract_flags if f.get("severity") == "warning"]

    signal_strength = len(critical) * PARAMS["contract_signal_critical_weight"] + len(warning) * PARAMS["contract_signal_warning_weight"]
    prob = clamp(baseline_prob + signal_strength)

    # Dilute when keywords match too broadly (>8 flags = broad)
    if len(contract_flags) > 12:
        prob = clamp(baseline_prob + signal_strength * (8 / len(contract_flags)))

    confidences = [f.get("confidence", 0.8) for f in contract_flags]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0.3
    dilution = clamp(1.0 - max(0, len(contract_flags) - 8) * 0.04)
    confidence = clamp(avg_conf * (0.5 + 0.5 * min(len(contract_flags) / 5, 1.0)) * dilution)

    return {
        "model": "contract_signal",
        "probability": round(prob, 3),
        "confidence": round(confidence, 3),
        "signal_count": len(contract_flags),
        "drivers": [
            f"{len(contract_flags)} contract/procurement flags matched",
            f"{len(critical)} critical, {len(warning)} warning signals",
        ],
    }


# ── Model 3: Regulatory Progression ──────────────────────────────

REGULATORY_STAGES = {
    "proposed": 0.10, "committee": 0.20, "passed_one_chamber": 0.35,
    "signed": 0.55, "effective": 0.75, "enforced": 0.90, "litigated": 0.65,
}

def model_regulatory_progression(flags, topic_keywords, baseline_prob=None):
    if baseline_prob is None:
        baseline_prob = PARAMS["regulatory_baseline"]
    reg_flags = [f for f in flags
                 if f.get("flag_type") in ("regulatory", "regulatory_deadline",
                                            "compliance", "legislation",
                                            "legal_action", "legal_precedent")
                 and any(kw.lower() in (f.get("title","") + f.get("detail","")).lower()
                         for kw in topic_keywords)]

    if not reg_flags:
        return {"model": "regulatory_progression", "probability": baseline_prob,
                "confidence": 0.2, "signal_count": 0, "drivers": ["No regulatory flags matched"]}

    stage_scores = []
    for f in reg_flags:
        if f.get("flag_type") == "regulatory_deadline":
            stage_scores.append(REGULATORY_STAGES["effective"])
        elif f.get("flag_type") == "legal_action":
            stage_scores.append(REGULATORY_STAGES["litigated"])
        else:
            stage_scores.append(REGULATORY_STAGES["proposed"])  # conservative default

    avg_stage = sum(stage_scores) / len(stage_scores)
    breadth_boost = clamp(0.05 * len(reg_flags))
    prob = clamp(avg_stage + breadth_boost)

    flag_confs = [f.get("confidence", 0.80) for f in reg_flags]
    confidence = clamp(sum(flag_confs) / len(flag_confs) * min(len(reg_flags) / 3, 1.0))

    return {
        "model": "regulatory_progression",
        "probability": round(prob, 3),
        "confidence": round(confidence, 3),
        "signal_count": len(reg_flags),
        "drivers": [
            f"{len(reg_flags)} regulatory/compliance flags matched",
            f"Mean stage score: {avg_stage:.2f}",
        ],
    }


# ── Model 4: Gray Zone Escalation ────────────────────────────────

def model_grayzone_escalation(entities, entity_names, flags, baseline_prob=None):
    if baseline_prob is None:
        baseline_prob = PARAMS["grayzone_baseline"]
    matched = [e for e in entities
               if any(n.lower() in e.get("name","").lower() for n in entity_names)]

    if not matched:
        return {"model": "grayzone_escalation", "probability": baseline_prob,
                "confidence": 0.1, "signal_count": 0, "drivers": ["No matching entities"]}

    scores = [e.get("composite_score", 0.5) for e in matched]
    avg_score = sum(scores) / len(scores)

    gz_flags = [f for f in flags
                if f.get("flag_type") in ("grayzone", "grayzone_xref", "legal_action",
                                           "corporate_evasion", "buyer_exposure")
                and any(n.lower() in (f.get("title","") + f.get("detail","")).lower()
                        for n in entity_names)]

    legal_flags = [f for f in gz_flags if f.get("flag_type") in ("legal_action", "compliance")]
    legal_boost = 0.08 * len(legal_flags)
    prob = clamp(0.4 * avg_score + 0.35 * clamp(len(gz_flags) / 10) + legal_boost + 0.1)
    confidence = clamp(0.5 + 0.3 * min(len(gz_flags) / 8, 1.0) + 0.2 * min(len(matched) / 4, 1.0))

    return {
        "model": "grayzone_escalation",
        "probability": round(prob, 3),
        "confidence": round(confidence, 3),
        "signal_count": len(gz_flags),
        "drivers": [
            f"{len(matched)} entity(ies): avg composite score {avg_score:.3f}",
            f"{len(gz_flags)} gray zone flags, {len(legal_flags)} legal action flags",
            f"Risk levels: {[e.get('risk_level','?') for e in matched]}",
        ],
    }


# ── Model 5: Cross-Correlation ────────────────────────────────────

def model_cross_correlation(flags, trigger_keywords, outcome_keywords,
                             lag_weeks=6, baseline_prob=None):
    if baseline_prob is None:
        baseline_prob = PARAMS["cross_correlation_baseline"]
    trigger_flags = [f for f in flags
                     if any(kw.lower() in (f.get("title","") + f.get("detail","")).lower()
                            for kw in trigger_keywords)]
    outcome_flags  = [f for f in flags
                      if any(kw.lower() in (f.get("title","") + f.get("detail","")).lower()
                             for kw in outcome_keywords)]

    if not trigger_flags or not outcome_flags:
        conf = 0.15 if (trigger_flags or outcome_flags) else 0.1
        return {"model": "cross_correlation", "probability": baseline_prob,
                "confidence": conf, "signal_count": 0,
                "drivers": [f"Trigger: {len(trigger_flags)}, outcome: {len(outcome_flags)}"]}

    # Cap triggers to avoid broad-keyword inflation
    effective_triggers = min(len(trigger_flags), PARAMS["cross_correlation_trigger_cap"])
    trigger_strength = clamp(effective_triggers / 10)
    outcome_strength = clamp(len(outcome_flags) / 5)
    correlation_score = (trigger_strength * outcome_strength) ** 0.5

    # Dilute if outcome/trigger ratio is very low (noisy signal)
    if len(trigger_flags) > 0 and len(outcome_flags) / len(trigger_flags) < 0.1:
        correlation_score *= 0.6

    all_flagged = trigger_flags + outcome_flags
    avg_conf = sum(f.get("confidence", 0.8) for f in all_flagged) / len(all_flagged)

    prob = clamp(baseline_prob + 0.4 * correlation_score)
    confidence = clamp(avg_conf * (0.4 + 0.6 * correlation_score))

    return {
        "model": "cross_correlation",
        "probability": round(prob, 3),
        "confidence": round(confidence, 3),
        "signal_count": len(trigger_flags) + len(outcome_flags),
        "drivers": [
            f"{len(trigger_flags)} trigger × {len(outcome_flags)} outcome flags (lag ~{lag_weeks}w)",
            f"Correlation score: {correlation_score:.3f}",
        ],
    }


# ── Driver merge ──────────────────────────────────────────────────

def _merge_drivers(model_outputs, extra):
    seen, result = set(), []
    for m in model_outputs:
        for d in m.get("drivers", [])[:1]:
            if d not in seen:
                seen.add(d); result.append(d)
    for d in extra:
        if d not in seen:
            seen.add(d); result.append(d)
    return result


# ── Prediction Definitions ────────────────────────────────────────

def build_predictions(db, flags, entities):
    predictions = []

    # Flat-or-nested db accessor
    _nested = db.get("components", {})
    def _cat(key): return db.get(key) or _nested.get(key, [])

    blue_count = len([m for m in db.get("drone_models", [])
                      if m.get("blue_uas") or m.get("ndaa_compliant")])

    # P1: Jetson Orin NX allocation-only
    jetson_boards = [c for c in _cat("companion_computers")
                     if "jetson" in (c.get("processor") or "").lower()]
    p1 = [
        model_concentration_risk(db, "companion_computers", ["Jetson","NVIDIA"], 0.45),
        model_contract_signal(flags, ["Jetson","NVIDIA","companion computer","edge AI","autonomy"], 0.40),
        model_cross_correlation(flags, ["AI","datacenter","NVIDIA","GPU"],
                                ["Jetson","companion","embedded","edge"], 8, 0.40),
    ]
    p1_prob, p1_conf = weighted_ensemble(p1)
    predictions.append({
        "id": pred_id("jetson-allocation-defense"),
        "timeframe": "Q3 2026",
        "event": f"Jetson Orin NX goes allocation-only for defense ({len(jetson_boards)} boards in Forge DB at risk)",
        "probability": p1_prob, "confidence": p1_conf, "impact": "critical",
        "model": "ensemble:concentration_risk(0.45) + contract_signal(0.35) + cross_correlation(0.20)",
        "model_outputs": p1,
        "drivers": _merge_drivers(p1, [
            f"{blue_count} Blue UAS platforms scaling simultaneously",
            f"{len(jetson_boards)} companion boards depend on Jetson silicon",
        ]),
        "last_updated": now,
    })

    # P2: STM32H7 allocated for defense FPV
    fcs = _cat("flight_controllers")
    stm_fcs = [fc for fc in fcs if any("stm32" in str(fc.get(f,"")).lower()
               for f in ["mcu","mcu_family","name","description"])]
    p2 = [
        model_concentration_risk(db, "flight_controllers", ["STM32","STMicro"], 0.50),
        model_contract_signal(flags, ["STM32","flight controller","FPV","Neros","Archer"], 0.45),
        model_cross_correlation(flags, ["FPV production","Drone Dominance","Neros"],
                                ["STM32","flight controller","MCU"], 4, 0.45),
    ]
    p2_prob, p2_conf = weighted_ensemble(p2)
    predictions.append({
        "id": pred_id("stm32-defense-allocation"),
        "timeframe": "Q2–Q3 2026",
        "event": f"STM32H7 becomes allocated for defense FPV ({len(stm_fcs)}/{len(fcs)} FCs in DB use STM32)",
        "probability": p2_prob, "confidence": p2_conf, "impact": "high",
        "model": "ensemble:concentration_risk(0.40) + contract_signal(0.40) + cross_correlation(0.20)",
        "model_outputs": p2,
        "drivers": _merge_drivers(p2, [
            f"{len(stm_fcs)}/{len(fcs)} flight controllers in Forge DB use STM32",
            "Defense FPV programs scaling (Neros Archer 2,200+/mo)",
        ]),
        "last_updated": now,
    })

    # P3: Mesh radio bottleneck
    mesh = _cat("mesh_radios")
    ndaa_mesh = [m for m in mesh if any(t in (m.get("tags") or [])
                 for t in ["ndaa","blue-uas","defense"])]
    p3 = [
        model_concentration_risk(db, "mesh_radios",
                                 ["Persistent Systems","Doodle Labs","Silvus"], 0.50),
        model_contract_signal(flags, ["mesh","radio","MANET","Lattice","Replicator","swarm"], 0.45),
        model_cross_correlation(flags, ["Lattice","Replicator","swarm","multi-vehicle"],
                                ["mesh","radio","MANET","communication"], 6, 0.40),
    ]
    p3_prob, p3_conf = weighted_ensemble(p3)
    predictions.append({
        "id": pred_id("mesh-radio-bottleneck"),
        "timeframe": "Q3–Q4 2026",
        "event": f"Mesh radio supply bottleneck — {len(mesh)} options tracked, only {len(ndaa_mesh)} NDAA-compliant",
        "probability": p3_prob, "confidence": p3_conf, "impact": "high",
        "model": "ensemble:concentration_risk(0.35) + contract_signal(0.40) + cross_correlation(0.25)",
        "model_outputs": p3,
        "drivers": _merge_drivers(p3, [
            f"Only {len(ndaa_mesh)}/{len(mesh)} mesh radios are NDAA-tagged in Forge DB",
            "Doodle Labs + Silvus dominate Blue UAS mesh — duopoly concentration risk",
        ]),
        "last_updated": now,
    })

    # P4: FLIR Boson 640 tightens
    thermal = _cat("thermal_cameras")
    boson = [t for t in thermal if "boson" in (t.get("name") or "").lower()]
    p4 = [
        model_concentration_risk(db, "thermal_cameras",
                                 ["FLIR","Teledyne FLIR","Boson"], 0.55),
        model_contract_signal(flags, ["FLIR","Boson","thermal","Switchblade","Ukraine","USAI"], 0.55),
        model_cross_correlation(flags, ["Ukraine","USAI","Switchblade","strike drone"],
                                ["FLIR","Boson","thermal","EO/IR"], 6, 0.55),
    ]
    p4_prob, p4_conf = weighted_ensemble(p4)
    predictions.append({
        "id": pred_id("flir-boson-allocation"),
        "timeframe": "H2 2026",
        "event": f"FLIR Boson 640 tightens — {len(boson)} Boson units tracked, AeroV Switchblade ramp drives demand",
        "probability": p4_prob, "confidence": p4_conf, "impact": "high",
        "model": "ensemble:concentration_risk(0.30) + contract_signal(0.40) + cross_correlation(0.30)",
        "model_outputs": p4,
        "drivers": _merge_drivers(p4, [
            "AeroVironment Switchblade 600 production ramp",
            "Ukraine USAI packages — 6-week lag correlation with Boson lead times",
        ]),
        "last_updated": now,
    })

    # P5: Gray zone enforcement — Anzu/SkyRover
    p5 = [
        model_grayzone_escalation(entities, ["Anzu","SkyRover","Knowact"], flags, 0.35),
        model_regulatory_progression(flags, ["NDAA","FCC","covered list","Anzu",
                                             "gray zone","adversary","ban"], 0.30),
        model_contract_signal(flags, ["Anzu","SkyRover","gray zone",
                                      "government buyer","law enforcement"], 0.25),
    ]
    p5_prob, p5_conf = weighted_ensemble(p5)
    predictions.append({
        "id": pred_id("grayzone-enforcement-event"),
        "timeframe": "H2 2026–2027",
        "event": "Gray zone enforcement event — federal action against Anzu/SkyRover operators or buyers",
        "probability": p5_prob, "confidence": p5_conf, "impact": "critical",
        "model": "ensemble:grayzone_escalation(0.45) + regulatory_progression(0.35) + contract_signal(0.20)",
        "model_outputs": p5,
        "drivers": _merge_drivers(p5, [
            "TX AG lawsuit active (45+ days, no Anzu response)",
            "FCC Covered List expansion Dec 2025",
            "NDAA FY2025 §1709 enforcement pipeline",
        ]),
        "last_updated": now,
    })

    # P6: FCC firmware cliff Jan 2027
    p6 = [
        model_regulatory_progression(flags, ["FCC","firmware","2027","cliff",
                                             "covered list","conditional"], 0.60),
        model_grayzone_escalation(entities, ["Anzu","Autel","SkyRover","Cogito"], flags, 0.45),
        model_cross_correlation(flags, ["FCC","covered list","conditional approval"],
                                ["firmware","deadline","2027","cliff","grounded"], 0, 0.55),
    ]
    p6_prob, p6_conf = weighted_ensemble(p6)
    predictions.append({
        "id": pred_id("fcc-firmware-cliff-2027"),
        "timeframe": "Jan 2027",
        "event": "FCC firmware cliff — 3 simultaneous deadlines ground uncertified gray zone drones",
        "probability": p6_prob, "confidence": p6_conf, "impact": "critical",
        "model": "ensemble:regulatory_progression(0.45) + grayzone_escalation(0.30) + cross_correlation(0.25)",
        "model_outputs": p6,
        "drivers": _merge_drivers(p6, [
            "FCC Conditional Approval: 3 deadlines converge Jan 1 2027",
            "OR/NASAO: 467 drones grounded across 25 states — $50M–$2B exposure",
            "FAA ASSURE: DJI = 96% of detected US drone platforms",
        ]),
        "last_updated": now,
    })

    # P7: QRB5165 successor enters Blue UAS Framework
    qrb_boards = [c for c in _cat("companion_computers")
                  if "qrb5165" in (c.get("processor") or "").lower()]
    p7 = [
        model_concentration_risk(db, "companion_computers",
                                 ["QRB5165","ModalAI","VOXL"], 0.60),
        model_contract_signal(flags, ["ModalAI","QRB5165","VOXL",
                                      "companion computer","Blue UAS"], 0.55),
    ]
    p7_prob, p7_conf = weighted_ensemble(p7)
    predictions.append({
        "id": pred_id("qrb5165-successor-blueas"),
        "timeframe": "2027",
        "event": f"QRB5165 successor enters Blue UAS Framework ({len(qrb_boards)} boards currently depend on QRB5165)",
        "probability": p7_prob, "confidence": p7_conf, "impact": "medium",
        "model": "ensemble:concentration_risk(0.50) + contract_signal(0.50)",
        "model_outputs": p7,
        "drivers": _merge_drivers(p7, [
            f"{len(qrb_boards)} companion computers use QRB5165 in Forge DB",
            "ModalAI next-gen roadmap (VOXL 3 expected 2026–2027)",
        ]),
        "last_updated": now,
    })

    # P8: Blue UAS BOM cost index >$5,000
    p8 = [
        model_cross_correlation(flags, ["DRAM","tariff","pricing","cost","price spike"],
                                ["BOM","cost","index","Blue UAS","compliance"], 12, 0.50),
        model_contract_signal(flags, ["DRAM","tariff","component cost","price increase"], 0.45),
        model_regulatory_progression(flags, ["tariff","Section 301","NDAA",
                                             "compliance premium"], 0.40),
    ]
    p8_prob, p8_conf = weighted_ensemble(p8)
    predictions.append({
        "id": pred_id("bom-cost-index-5k"),
        "timeframe": "2026–2027",
        "event": "Blue UAS BOM cost index exceeds $5,000 (currently ~$4,348)",
        "probability": p8_prob, "confidence": p8_conf, "impact": "high",
        "model": "ensemble:cross_correlation(0.40) + contract_signal(0.30) + regulatory_progression(0.30)",
        "model_outputs": p8,
        "drivers": _merge_drivers(p8, [
            "DRAM pricing +22% YoY",
            "Section 301 tariff escalation on Chinese components",
            "NDAA compliance premium — 15–30% over commercial pricing",
        ]),
        "last_updated": now,
    })

    # P9: Taiwan / TSMC disruption — black swan
    p9 = [
        model_concentration_risk(db, "companion_computers",
                                 ["Jetson","QRB5165","NVIDIA","Qualcomm"], 0.10),
        model_cross_correlation(flags, ["Taiwan","TSMC","geopolitical","China tension"],
                                ["Jetson","QRB5165","SoC","foundry","semiconductor"], 0, 0.08),
    ]
    p9_prob, p9_conf = weighted_ensemble(p9)
    p9_prob = clamp(p9_prob, hi=PARAMS["black_swan_cap"])  # hard cap — black swan
    predictions.append({
        "id": pred_id("tsmc-disruption-cascade"),
        "timeframe": "2026–2028",
        "event": "Taiwan tension: TSMC disruption cascades to all Jetson + QRB5165 Blue UAS platforms",
        "probability": p9_prob, "confidence": p9_conf, "impact": "critical",
        "model": "ensemble:concentration_risk(0.50) + cross_correlation(0.50) [black swan cap: 0.25]",
        "model_outputs": p9,
        "drivers": _merge_drivers(p9, [
            "TSMC concentration for advanced nodes (3nm, 5nm)",
            "All Blue UAS companion SoCs fabricated in Taiwan",
            "No alternative foundry at scale — hard cap applied at 0.25",
        ]),
        "last_updated": now,
    })

    # P10: C-UAS demand compounds UAS supply pressure
    p10 = [
        model_contract_signal(flags, ["C-UAS","counter-UAS","DroneShield",
                                      "Epirus","FEMA","FIFA"], 0.45),
        model_cross_correlation(flags, ["C-UAS","counter-drone","DroneShield","Epirus"],
                                ["STM32","FPGA","radar","RF component",
                                 "component shortage"], 8, 0.40),
    ]
    p10_prob, p10_conf = weighted_ensemble(p10)
    predictions.append({
        "id": pred_id("cuas-demand-compounds"),
        "timeframe": "Q2–Q3 2026",
        "event": "C-UAS component demand compounds UAS supply pressure on shared silicon",
        "probability": p10_prob, "confidence": p10_conf, "impact": "medium",
        "model": "ensemble:contract_signal(0.55) + cross_correlation(0.45)",
        "model_outputs": p10,
        "drivers": _merge_drivers(p10, [
            "FEMA $250M C-UAS grant program",
            "FIFA World Cup 2026 security procurement",
            "DroneShield + Epirus share RF/FPGA supply chain with UAS makers",
        ]),
        "last_updated": now,
    })

    predictions.sort(key=lambda p: p["probability"], reverse=True)
    return predictions


def run(db, flags):
    gz_path = REPO_ROOT / "data" / "grayzone" / "entities.json"
    try:
        raw = json.loads(gz_path.read_text())
        entities = raw if isinstance(raw, list) else raw.get("entities", [])
    except Exception:
        entities = []
    return build_predictions(db, flags, entities)


if __name__ == "__main__":
    db = json.loads((REPO_ROOT / "data" / "forge_database.json").read_text())
    flags = json.loads((REPO_ROOT / "data" / "flags.json").read_text())
    preds = run(db, flags)
    print(f"\nPrediction Engine — {len(preds)} predictions\n{'='*60}")
    for p in preds:
        bar = "█" * int(p["probability"] * 20) + "░" * (20 - int(p["probability"] * 20))
        print(f"[{p['probability']:.2f}] {bar} {p['event'][:65]}")
        print(f"       conf={p['confidence']:.2f} | {p['model'][:70]}")
        for m in p["model_outputs"]:
            print(f"         ↳ {m['model']:25s} p={m['probability']:.3f} conf={m['confidence']:.3f} n={m['signal_count']}")
        print()
