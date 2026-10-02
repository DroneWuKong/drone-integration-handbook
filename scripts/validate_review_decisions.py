#!/usr/bin/env python3
"""Validate a workbench export without publishing or editing handbook evidence."""
import argparse
import json
from datetime import date
from pathlib import Path

DECISIONS={"source-supported","not-a-claim","illustrative","needs-research","correct-remove","defer"}

def validate(payload,queue):
    if payload.get("schema_version")!=1 or payload.get("kind")!="uas-handbook-citation-review":
        raise ValueError("unsupported citation review file")
    if payload.get("release")!=queue.get("release"):
        raise ValueError("review file and queue releases do not match")
    records={record["id"]:record for record in queue.get("records",[])}
    normalized=[]
    for record_id,decision in payload.get("decisions",{}).items():
        if record_id not in records:raise ValueError(f"unknown queue record: {record_id}")
        kind=decision.get("decision")
        if kind not in DECISIONS:raise ValueError(f"unknown decision for {record_id}: {kind}")
        if kind=="source-supported":
            missing=[name for name in ("source_url","source_passage","scope","checked_at") if not str(decision.get(name,"")).strip()]
            if missing:raise ValueError(f"supported decision {record_id} is missing: {', '.join(missing)}")
            if not str(decision["source_url"]).startswith(("https://","http://")):raise ValueError(f"supported decision {record_id} has an invalid source URL")
            try:date.fromisoformat(decision["checked_at"])
            except (TypeError,ValueError):raise ValueError(f"supported decision {record_id} has an invalid check date")
        normalized.append({"record_id":record_id,"statement":records[record_id]["statement"],"path":records[record_id]["path"],**decision})
    return {"schema_version":1,"kind":"uas-handbook-citation-review-actions","release":queue["release"],"summary":{"decisions":len(normalized),"source_supported":sum(row["decision"]=="source-supported" for row in normalized),"automated":sum(bool(row.get("automated")) for row in normalized)},"actions":sorted(normalized,key=lambda row:(row["path"],row["record_id"]))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review",type=Path,help="JSON file exported by citation-review.html")
    parser.add_argument("--queue",type=Path,default=Path("site/assets/citation-review-queue.json"))
    parser.add_argument("--output",type=Path,default=Path(".local/citation-review-actions.json"))
    parser.add_argument("--check",action="store_true",help="Validate without writing normalized actions")
    args=parser.parse_args()
    result=validate(json.loads(args.review.read_text()),json.loads(args.queue.read_text()))
    if not args.check:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["summary"],indent=2))

if __name__=="__main__":main()
