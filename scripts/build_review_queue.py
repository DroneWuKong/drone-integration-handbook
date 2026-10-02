"""Build a local citation-review queue from the public release snapshot."""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from handbook_builder.review import build_review_queue

def safe(value):
    value=str(value or "")
    return "'"+value if value.startswith(("=","+","-","@")) else value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=ROOT/"site/assets/reference-data.json")
    parser.add_argument("--json",type=Path,default=ROOT/".local/citation-review-queue.json")
    parser.add_argument("--csv",type=Path,default=ROOT/".local/citation-review-queue.csv")
    parser.add_argument("--check",action="store_true",help="Validate and summarize without writing queue files")
    args=parser.parse_args()
    snapshot=json.loads(args.input.read_text())
    article_sources={}
    for path in {r["path"] for r in snapshot["records"] if r.get("status")=="unreviewed"}:
        source=ROOT/path
        if source.exists():
            article_sources[path]=sorted(set(re.findall(r'https://[^\s)<>\]"\']+',source.read_text())))
    queue=build_review_queue(snapshot,article_sources)
    if not args.check:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(queue,indent=2)+"\n")
        with args.csv.open("w",newline="",encoding="utf-8") as handle:
            fields=["priority","score","id","article_id","path","table_id","record_type","cluster","cluster_size","risk_reasons","statement","source_candidates","article_source_candidates","recommended_action"]
            writer=csv.DictWriter(handle,fieldnames=fields);writer.writeheader()
            for record in queue["records"]:
                row={k:record.get(k) for k in fields};row["risk_reasons"]="; ".join(record["risk_reasons"]);row["source_candidates"]="; ".join(record["source_candidates"]);row["article_source_candidates"]="; ".join(record["article_source_candidates"])
                writer.writerow({k:safe(v) for k,v in row.items()})
    print(json.dumps(queue["summary"],indent=2))

if __name__=="__main__":main()
