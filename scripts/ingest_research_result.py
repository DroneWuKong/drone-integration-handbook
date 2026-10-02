#!/usr/bin/env python3
"""Validate completed research responses and deterministically adjudicate claims."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from handbook_builder.autonomous import adjudicate, extract_packet_from_response, validate_packet, verify_source_snapshots, write_plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("responses", type=Path, nargs="+", help="Saved Responses API objects or evidence packets")
    parser.add_argument("--output", type=Path, default=ROOT / ".local/autonomy/adjudicated.json")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    specs = {item["id"]: item for item in plan["specs"]}
    jobs_by_response = {item.get("response_id"): item for item in plan["jobs"] if item.get("response_id")}
    packets = {}
    rejected = []
    for path in args.responses:
        raw = json.loads(path.read_text())
        packet = raw if raw.get("claim_id") and raw.get("role") else extract_packet_from_response(raw)
        response_id = raw.get("id")
        job = jobs_by_response.get(response_id)
        spec = next((s for s in specs.values() if s["claim_id"] == packet.get("claim_id")), None)
        role = packet.get("role")
        try:
            if spec is not None: packet=verify_source_snapshots(packet,spec)
            errors = validate_packet(packet, claim_id=spec["claim_id"] if spec else None, role=job["role"] if job else role)
        except Exception as error:
            errors=["source-snapshot-failed:"+type(error).__name__]
        if spec is None or errors:
            rejected.append({"path": str(path), "errors": errors or ["unknown-claim"]})
            continue
        packets[(spec["id"], role)] = packet
    decisions = list(plan.get("decisions", []))
    for spec in specs.values():
        group = [packets[key] for key in ((spec["id"], "researcher"), (spec["id"], "verifier")) if key in packets]
        if group:
            decisions.append(adjudicate(spec, group))
    result = {"schema_version": 1, "kind": "uas-handbook-autonomous-evidence-results",
              "release": plan["release"], "packets": list(packets.values()),
              "decisions": decisions, "rejected": rejected,
              "summary": {"packets": len(packets), "decisions": len(decisions),
                          "publishable": sum(d["publish"] for d in decisions),
                          "exceptions": sum(d["human_intervention"] for d in decisions),
                          "abstained": sum(d["publication_state"] == "abstained" for d in decisions),
                          "rejected": len(rejected), "publication_changed": False}}
    write_plan(args.output, result)
    print(json.dumps(result["summary"], indent=2))
    if rejected:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
