"""Deterministic triage for unresolved public-handbook evidence records."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

NUMBER=re.compile(r"(?<![a-z])[-+]?\d+(?:[.,]\d+)*(?:e[-+]?\d+)?",re.I)
URL=re.compile(r"https?://\S+",re.I)
SPACE=re.compile(r"\s+")
SOURCE_FIELDS={"source","url","authority","verified","what it supports"}

RISK_RULES=(
    (5,"regulatory",re.compile(r"\b(faa|fcc|itar|ndaa|remote id|bvlos|regulat|legal|compliance)\b",re.I)),
    (5,"safety",re.compile(r"\b(safety|danger|hazard|arming|weapon|injury|fire|thermal runaway)\b",re.I)),
    (4,"performance",re.compile(r"\b(range|endurance|accuracy|latency|speed|power|voltage|current|watt|amp|mah|wh)\b",re.I)),
    (4,"commercial",re.compile(r"(?:\$|\b(price|cost|award|valuation)\b)",re.I)),
    (3,"configuration",re.compile(r"\b(firmware|version|protocol|baud|uart|pinout|parameter|command)\b",re.I)),
    (2,"failure",re.compile(r"\b(failure|fault|fix|symptom|interference|jamming)\b",re.I)),
)

def normalize_statement(statement):
    value=URL.sub("<url>",statement.lower())
    value=NUMBER.sub("<number>",value)
    return SPACE.sub(" ",value).strip()

def triage(record):
    score=1 if record.get("record_type")=="table-row" else 2
    reasons=[]
    statement=record.get("statement","")
    for weight,name,pattern in RISK_RULES:
        if pattern.search(statement):
            score+=weight;reasons.append(name)
    if record.get("source_candidates"):
        score+=1;reasons.append("candidate-source-present")
    field_names={str(k).strip().lower() for k in record.get("fields",{})}
    if record.get("source_candidates") and field_names & SOURCE_FIELDS:
        score=max(1,score-5);reasons.append("source-directory-entry")
    if re.fullmatch(r"last updated:\s*[a-z]+\s+\d{4}",statement.strip(),re.I):
        score=1;reasons.append("administrative-date")
    priority="P0" if score>=10 else "P1" if score>=7 else "P2" if score>=4 else "P3"
    normalized=normalize_statement(statement)
    cluster=hashlib.sha256(normalized.encode()).hexdigest()[:16]
    if record.get("source_candidates"):
        action="Check the candidate primary source and record the exact supporting passage or reject the association."
    elif record.get("table_id"):
        action="Review with the full table; verify the governing source and conditions before promoting any row."
    else:
        action="Locate a primary source, scope the statement, then support, correct, or remove it."
    return {"score":score,"priority":priority,"risk_reasons":reasons or ["general"],"cluster":cluster,"recommended_action":action}

def extract_article_sources(base,records):
    """Collect existing public links as research leads, never as verification."""
    base=Path(base)
    found={}
    for path in {r["path"] for r in records if r.get("status")=="unreviewed"}:
        source=base/path
        if source.exists():
            found[path]=sorted(set(re.findall(r'https://[^\s)<>\]"\']+',source.read_text())))
    return found

def propose(record,cluster_size):
    """Make a reversible workflow proposal; proposals never publish evidence."""
    reasons=set(record["risk_reasons"])
    exact=record.get("source_candidates",[])
    article=record.get("article_source_candidates",[])
    if "source-directory-entry" in reasons or "administrative-date" in reasons:
        return {
            "kind":"not-a-claim","decision":"not-a-claim","confidence":"high",
            "automation":"preselected","human_intervention":False,
            "why":"Administrative/source metadata is tracked for provenance but is not itself a factual handbook claim.",
            "bulk_scope":"record",
        }
    if exact:
        return {
            "kind":"check-exact-source","decision":"needs-source-check","confidence":"high",
            "automation":"prefilled","human_intervention":True,
            "why":"The statement already contains a source link; verify the exact passage and scope.",
            "bulk_scope":"table" if record.get("table_id") else "record",
        }
    if cluster_size>1:
        return {
            "kind":"review-cluster-once","decision":"needs-source-check","confidence":"medium",
            "automation":"grouped","human_intervention":True,
            "why":f"{cluster_size} normalized duplicates can share one reviewed disposition when their context agrees.",
            "bulk_scope":"cluster",
        }
    if len(article)==1:
        return {
            "kind":"check-article-source","decision":"needs-source-check","confidence":"medium",
            "automation":"prefilled","human_intervention":True,
            "why":"This article has one existing source lead; check whether it supports this exact statement.",
            "bulk_scope":"table" if record.get("table_id") else "record",
        }
    if article:
        return {
            "kind":"choose-article-source","decision":"needs-source-check","confidence":"low",
            "automation":"prefilled","human_intervention":True,
            "why":f"The article has {len(article)} source leads. Choose and verify an exact passage.",
            "bulk_scope":"table" if record.get("table_id") else "record",
        }
    return {
        "kind":"research","decision":"needs-research","confidence":"low",
        "automation":"queued","human_intervention":True,
        "why":"No existing source lead was found for this extracted statement.",
        "bulk_scope":"table" if record.get("table_id") else "record",
    }

def build_review_queue(snapshot,article_sources=None):
    article_sources=article_sources or {}
    references={r["id"]:r for r in snapshot["references"]}
    records=[]
    for record in snapshot["records"]:
        if record.get("status")!="unreviewed":continue
        if references[record["article_id"]].get("publication_state")=="hold":
            raise ValueError("Held content entered the review queue")
        records.append({
            "id":record["id"],"article_id":record["article_id"],"title":record["title"],
            "path":record["path"],"record_type":record["record_type"],
            "table_id":record.get("table_id"),"statement":record["statement"],
            "source_candidates":record.get("source_candidates",[]),
            "article_source_candidates":article_sources.get(record["path"],[]),**triage(record),
        })
    records.sort(key=lambda x:({"P0":0,"P1":1,"P2":2,"P3":3}[x["priority"]],-x["score"],x["path"],x["id"]))
    clusters=Counter(r["cluster"] for r in records)
    priorities=Counter(r["priority"] for r in records)
    articles=Counter(r["article_id"] for r in records)
    tables=Counter(r["table_id"] for r in records if r["table_id"])
    proposals=Counter()
    automated=0
    for record in records:
        record["cluster_size"]=clusters[record["cluster"]]
        record["proposal"]=propose(record,record["cluster_size"])
        proposals[record["proposal"]["kind"]]+=1
        automated+=not record["proposal"]["human_intervention"]
    batches=[]
    for path in sorted({r["path"] for r in records}):
        members=[r for r in records if r["path"]==path]
        counts=Counter(r["priority"] for r in members)
        batches.append({
            "path":path,"article_id":members[0]["article_id"],"title":members[0]["title"],
            "records":len(members),"priorities":dict(sorted(counts.items())),
            "tables":sorted({r["table_id"] for r in members if r["table_id"]}),
            "article_source_candidates":article_sources.get(path,[]),
        })
    batches.sort(key=lambda x:(-x["priorities"].get("P0",0),-x["priorities"].get("P1",0),x["path"]))
    return {
        "schema_version":1,
        "release":snapshot.get("release"),
        "scope":"Triage only. Priority, grouping and candidate links are not factual verification.",
        "summary":{
            "records":len(records),"priorities":dict(sorted(priorities.items())),
            "article_batches":len(articles),"table_batches":len(tables),
            "normalized_clusters":len(clusters),
            "records_in_repeated_clusters":sum(n for n in clusters.values() if n>1),
            "records_with_candidate_sources":sum(bool(r["source_candidates"]) for r in records),
            "article_batches_with_source_candidates":sum(bool(b["article_source_candidates"]) for b in batches),
            "automation_proposals":dict(sorted(proposals.items())),
            "automated_low_risk_decisions":automated,
            "human_intervention_records":len(records)-automated,
        },
        "batches":batches,
        "records":records,
    }
