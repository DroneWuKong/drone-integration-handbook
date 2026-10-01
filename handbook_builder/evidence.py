"""Public evidence export. Extracted legacy data is never verified by extraction."""
import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

MARKER=re.compile(r"\[claim:([a-z0-9-]+)\]")
TABLE=re.compile(r"<table>.*?</table>",re.S)
ROW=re.compile(r"<tr>(.*?)</tr>",re.S)
CELL=re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>",re.S)
TAG=re.compile(r"<[^>]*>")
def text(s):
    return re.sub(r"\s+"," ",html.unescape(TAG.sub(" ",s))).strip()
def load_evidence(base):
    p=base/"data/evidence.json"
    d=json.loads(p.read_text()) if p.exists() else {"sources":[],"claims":[]}
    sources={s["id"]:s for s in d["sources"]}
    claims={c["id"]:c for c in d["claims"]}
    if len(sources)!=len(d["sources"]) or len(claims)!=len(d["claims"]):
        raise ValueError("Duplicate evidence identity")
    for s in sources.values():
        u=urlsplit(s["url"])
        if u.scheme!="https" or not u.hostname: raise ValueError("HTTPS source required")
        date.fromisoformat(s["accessed"])
    for c in claims.values():
        if c["status"] not in {"derived","official-source","manufacturer-reported","field-observed","unreviewed"}: raise ValueError("Invalid evidence category")
        if c["status"]!="unreviewed" and not c.get("sources"): raise ValueError("Supported claims require sources")
        if set(c.get("sources",[]))-sources.keys(): raise ValueError("Missing claim source")
        date.fromisoformat(c["verified"])
        if not c.get("scope") or not c.get("statement"): raise ValueError("Claim scope and statement required")
    return sources,claims
def control(c,sources):
    esc=html.escape
    links="".join('<li><a href="'+esc(sources[s]["url"])+'">'+esc(sources[s]["title"])+"</a>: "+esc(sources[s]["passage"])+"; accessed "+esc(sources[s]["accessed"])+"</li>" for s in c.get("sources",[]))
    return '<details class="claim-evidence" id="'+esc(c["id"])+'"><summary>'+esc(c["status"])+' · evidence</summary><p>'+esc(c["statement"])+"</p><p>"+esc(c["scope"])+"</p><p>Verified "+esc(c["verified"])+'</p><ul>'+links+'</ul><button type="button" class="report-claim" data-report-claim="'+esc(c["id"])+'">Report a discrepancy</button></details>'
def expand_markers(source,sources,claims):
    def replace(m):
        if m[1] not in claims: raise ValueError("Unknown claim "+m[1])
        return control(claims[m[1]],sources)
    return MARKER.sub(replace,source)
def decorate_and_inventory(entry,sources,claims):
    rendered=entry.html
    if 'class="publication-hold"' in rendered:
        return rendered,[],[],"hold"
    revision=hashlib.sha256(entry.source_path.read_bytes()).hexdigest()
    records,tables=[],[]
    def record(body,kind,fields=None):
        plain=text(body)
        rid="legacy-"+hashlib.sha256((entry.identity+kind+plain).encode()).hexdigest()[:20]
        records.append({"id":rid,"article_id":entry.identity,"title":entry.title,"anchor":entry.anchor,"canonical":entry.canonical,"path":entry.relative_path,"revision":revision,"kind":entry.kind,"group":entry.group,"record_type":kind,"statement":plain,"fields":fields or {},"status":"unreviewed","verified":None,"sources":[],"source_candidates":re.findall(r'href="(https://[^"]+)"',body)})
        return rid
    def unknown(rid):
        return '<span class="unreviewed-claim" id="'+rid+'">Evidence not yet reviewed <button type="button" class="report-claim" data-report-claim="'+rid+'">Flag this</button></span>'
    protected=[]
    def protect(m):
        protected.append(m[0]);return "@@PROTECTED"+str(len(protected)-1)+"@@"
    rendered=re.sub(r'<details class="claim-evidence".*?</details>',protect,rendered,flags=re.S)
    def table(m):
        rows=ROW.findall(m[0])
        if not rows:return m[0]
        headers=[text(v) for v in CELL.findall(rows[0])]
        tid="table-"+hashlib.sha256((entry.identity+text(m[0])).encode()).hexdigest()[:20]
        tables.append({"id":tid,"article_id":entry.identity,"path":entry.relative_path,"headers":headers,"disposition":"queryable-lookup" if len(headers)==2 else "comparison","review":"unreviewed","rows":max(0,len(rows)-1)})
        pos=0
        def row(r):
            nonlocal pos
            pos+=1
            if pos==1:return r[0].replace("</tr>","<th>Evidence</th></tr>")
            vals=CELL.findall(r[1])
            if any("@@PROTECTED" in v for v in vals):return r[0].replace("</tr>","<td>See cited evidence</td></tr>")
            rid=record(r[1],"table-row",dict(zip(headers,[text(v) for v in vals])))
            return r[0].replace("</tr>","<td>"+unknown(rid)+"</td></tr>")
        return ROW.sub(row,m[0])
    rendered=TABLE.sub(table,rendered)
    rendered=TABLE.sub(protect,rendered)
    def block(m):
        if not re.search(r"\d",text(m[0])) or "@@PROTECTED" in m[0]:return m[0]
        rid=record(m[0],"numerical-passage")
        end="</"+m[1]+">"
        return m[0][:-len(end)]+" "+unknown(rid)+end
    rendered=re.sub(r"<(p|li)(?:\s[^>]*)?>.*?</\1>",block,rendered,flags=re.S)
    for i,v in enumerate(protected):rendered=rendered.replace("@@PROTECTED"+str(i)+"@@",v)
    for cid in sorted(set(MARKER.findall(entry.source_path.read_text()))):
        records.append({**claims[cid],"article_id":entry.identity,"title":entry.title,"anchor":entry.anchor,"canonical":entry.canonical,"path":entry.relative_path,"revision":revision,"kind":entry.kind,"group":entry.group,"record_type":"managed-claim","fields":{}})
    seen=set()
    def unique(m):
        if m[1] in seen:return ""
        seen.add(m[1]);return m[0]
    rendered=re.sub(r' id="(legacy-[a-f0-9]+)"',unique,rendered)
    return rendered,list({r["id"]:r for r in records}.values()),tables,"published"
def snapshot(entries,sources,records,tables,release):
    refs=[{"id":e.identity,"title":e.title,"kind":e.kind,"group":e.group,"anchor":e.anchor,"canonical":e.canonical,"path":e.relative_path,"status":"hold" if e.publication_state=="hold" else "unreviewed","publication_state":e.publication_state,"verified":None,"sources":[],"revision":hashlib.sha256(e.source_path.read_bytes()).hexdigest(),"statement":e.plain_text if e.publication_state!="hold" else "Publication hold; substantive guidance excluded","fields":{}} for e in entries]
    return {"schema_version":1,"release":release,"license":"CC BY-SA 4.0; third-party sources retain their rights","references":refs,"records":records,"sources":list(sources.values()),"tables":tables,"coverage":{"references":len(refs),"holds":sum(r["status"]=="hold" for r in refs),"tracked_records":len(records),"supported_records":sum(r["status"]!="unreviewed" for r in records),"unreviewed_records":sum(r["status"]=="unreviewed" for r in records),"tables":len(tables),"scope":"Tracked table rows and digit-bearing paragraphs/list items; not a completed semantic claim audit"}}
