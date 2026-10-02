"""Validate the generated public evidence snapshot and privacy/hold boundary."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from handbook_builder.evidence import load_evidence
def check(site):
    sources,claims=load_evidence(ROOT)
    data=json.loads((site/"assets/reference-data.json").read_text())
    assert data["schema_version"]==1
    assert len({r["id"] for r in data["references"]})==len(data["references"])
    assert len({r["id"] for r in data["records"]})==len(data["records"])
    holds={r["id"] for r in data["references"] if r.get("publication_state",r["status"])=="hold"}
    assert not any(r["article_id"] in holds for r in data["records"])
    assert not any(t["article_id"] in holds for t in data["tables"])
    disposition_file=ROOT/"data/table-dispositions.json"
    if disposition_file.exists():
        registered=json.loads(disposition_file.read_text())["tables"]
        fields=("id","article_id","path","disposition","classification_basis","review","rows","tool")
        normalized=lambda rows: {r["id"]:{k:r.get(k) for k in fields} for r in rows}
        assert normalized(registered)==normalized(data["tables"]), "Reconcile changed table dispositions before publication"
    table_ids={t["id"] for t in data["tables"]}
    assert all(t["disposition"] in {"comparison","queryable-lookup","calculator","guided-explanation","removed/held"} for t in data["tables"])
    assert all(t.get("classification_basis") for t in data["tables"])
    assert set(claims)=={r["id"] for r in data["records"] if r["record_type"]=="managed-claim"}
    for r in data["records"]:
        assert len(r["source_revision"])==64
        if r["record_type"]=="managed-claim":assert r["revision"]==claims[r["id"]]["revision"]
        if r["status"]!="unreviewed": assert r["sources"] and r["verified"] and r["scope"]
        else: assert not r["sources"] and r["verified"] is None
        if r["record_type"]=="table-row":assert r.get("table_id") in table_ids
    marker=json.loads((site/"release.json").read_text())
    release=marker["release"]
    assert data.get("commit")==marker.get("commit")
    assert data["release"]==release
    manifest=json.loads((site/"offline-manifest.json").read_text())
    assert manifest["release"]==release
    assert not any(p.startswith("/api/") or "review" in p for p in manifest["files"])
    assert "/evidence-lab.html" in manifest["files"]
    assert "/assets/autonomy-status.json" in manifest["files"]
    status=json.loads((site/"assets/autonomy-status.json").read_text())
    assert status["release"]==release
    assert status["scope"].startswith("Public aggregate only.")
    assert (site/"evidence-lab.html").is_file()
    queue=json.loads((site/"assets/citation-review-queue.json").read_text())
    assert queue["release"]==release
    assert queue["summary"]["records"]==data["coverage"]["unreviewed_records"]
    assert queue["summary"]["automated_low_risk_decisions"]+queue["summary"]["human_intervention_records"]==queue["summary"]["records"]
    assert not any("token_hash" in r or "receipt_token" in r for r in data["records"])
    print(json.dumps(data["coverage"],indent=2))
    return data
if __name__=="__main__":check(Path(sys.argv[1] if len(sys.argv)>1 else ROOT/"site"))
