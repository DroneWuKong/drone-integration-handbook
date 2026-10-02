#!/usr/bin/env python3
"""Register or resolve immutable prediction-ledger entries."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from handbook_builder.autonomous import register_prediction, resolve_prediction, write_plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("register"); add.add_argument("prediction", type=Path)
    resolve = sub.add_parser("resolve"); resolve.add_argument("prediction_id"); resolve.add_argument("outcome", choices=("true", "false")); resolve.add_argument("source_url")
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text()) if args.ledger.exists() else {"schema_version": 1, "predictions": []}
    if args.command == "register":
        item = register_prediction(json.loads(args.prediction.read_text()))
        if any(row["id"] == item["id"] for row in ledger["predictions"]):
            raise SystemExit("prediction identity already registered")
        ledger["predictions"].append(item)
    else:
        index = next((i for i, row in enumerate(ledger["predictions"]) if row["id"] == args.prediction_id), None)
        if index is None: raise SystemExit("prediction not found")
        ledger["predictions"][index] = resolve_prediction(ledger["predictions"][index], args.outcome == "true", source_url=args.source_url)
    resolved = [row for row in ledger["predictions"] if row["state"] == "resolved"]
    ledger["summary"] = {"total": len(ledger["predictions"]), "open": len(ledger["predictions"]) - len(resolved), "resolved": len(resolved),
                         "mean_brier": sum(row["resolution"]["brier"] for row in resolved) / len(resolved) if resolved else None,
                         "mean_baseline_brier": sum(row["resolution"]["baseline_brier"] for row in resolved) / len(resolved) if resolved else None}
    write_plan(args.ledger, ledger)
    print(json.dumps(ledger["summary"], indent=2))


if __name__ == "__main__":
    main()
