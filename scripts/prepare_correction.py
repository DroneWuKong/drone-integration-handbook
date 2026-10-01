"""Prepare an evidence-backed public correction proposal. Never edits published claims."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def prepare(data,claim_id,statement,source_ids,scope,reason,report_id=None):
    claims={c["id"]:c for c in data["claims"]};sources={s["id"]:s for s in data["sources"]}
    if claim_id not in claims:raise ValueError("Unknown managed claim")
    if not source_ids or set(source_ids)-sources.keys():raise ValueError("Known primary source identities required")
    if not statement.strip() or not scope.strip() or not reason.strip():raise ValueError("Statement, scope and review reason required")
    before=copy.deepcopy(claims[claim_id]);after=copy.deepcopy(before)
    after.pop("statement_template",None)
    after.update(statement=statement,sources=source_ids,scope=scope,revision=before.get("revision",1)+1)
    proposal_id=hashlib.sha256(json.dumps({"before":before,"statement":statement,"sources":source_ids,"scope":scope},sort_keys=True).encode()).hexdigest()[:24]
    event={"proposal_id":proposal_id,"from_revision":before.get("revision",1),"reason":reason,"report_id":report_id,"publication_state":"draft"}
    after["history"]=[*before.get("history",[]),event];after["verified"]=None
    return {"schema_version":1,"id":proposal_id,"publication_state":"draft","claim_id":claim_id,"before":before,"proposed":after,"requirements":["verify source passage and derivation","applicable qualified review","publisher approval of exact commit","rebuild all public surfaces","custom-domain release verification"],"warning":"No private report text or attachment is imported. This proposal is excluded from site builds."}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("claim_id");p.add_argument("--statement",required=True);p.add_argument("--source",action="append",required=True);p.add_argument("--scope",required=True);p.add_argument("--reason",required=True);p.add_argument("--report-id");p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();proposal=prepare(json.loads((ROOT/"data/evidence.json").read_text()),a.claim_id,a.statement,a.source,a.scope,a.reason,a.report_id)
    if a.output.exists():raise SystemExit("Refusing to overwrite an existing proposal; reconcile its disposition first")
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(proposal,indent=2))
    print(json.dumps({"proposal_id":proposal["id"],"publication_state":"draft","publication_changed":False,"output":str(a.output)}))
if __name__=="__main__":main()
