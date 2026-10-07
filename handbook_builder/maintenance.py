"""Bounded source/repository discovery and deterministic factual publication.

Remote content is data. Only managed claims and exact standalone legacy
paragraphs can be promoted; code, policy, held articles and private files cannot.
"""
from __future__ import annotations
import copy
import hashlib
import html
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit
import urllib.request
import markdown
from .autonomous import adjudicate, research_spec, stable_id, verify_source_snapshots, claim_type
from .evidence import text
from .review import triage

WATCH_PATH = "field/update-status.md"
EMERGING_PATH = "integration/emerging-technology-watch.md"
ADDITIONS_PATH = "integration/repository-updates.md"
BLOCKED = re.compile(r"\b(weapon|ordnance|intercept|targeting|explosive|elint|jammer|electronic.attack|identification.defeat)\b", re.I)
CONTENT_ROOTS = {"fundamentals", "firmware", "field", "integration", "components", "platforms", "autonomy", "appendices"}

def json_write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

def plain(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", str(value)))).strip()

def cell(value):
    return html.escape(plain(value)).replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;")

class GitHubReader:
    def __init__(self, token=""):
        self.token = token
    def __call__(self, resource):
        if not resource.startswith(("repos/", "search/repositories?")):
            raise ValueError("Unsupported GitHub resource")
        request = urllib.request.Request("https://api.github.com/" + resource, headers={
            "user-agent": "HandbookMaintenance/1.0", "accept": "application/vnd.github+json",
            **({"authorization": "Bearer " + self.token} if self.token else {})})
        # Never forward a token to redirects or arbitrary source hosts.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs): raise ValueError("Unexpected API redirect")
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            body = response.read(4 * 1024 * 1024 + 1)
            if len(body) > 4 * 1024 * 1024: raise ValueError("API response too large")
            return json.loads(body)

def releases(rows, today, prefix=""):
    """Future/undated/draft entries cannot be described as released."""
    valid = []
    for row in rows:
        stamp = row.get("published_at")
        if row.get("draft") or not stamp or not row.get("tag_name", "").startswith(prefix): continue
        try: released = datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()
        except (TypeError, ValueError): continue
        if released > today: continue
        valid.append(row)
    valid.sort(key=lambda x: x["published_at"], reverse=True)
    return next((x for x in valid if not x.get("prerelease")), None), next((x for x in valid if x.get("prerelease")), None)

def update_watchlist(config, reader, today, previous=None):
    previous = {x["id"]: x for x in (previous or {}).get("items", [])}
    items = []
    for item in config["releases"]:
        row = {**item, "checked": today.isoformat(), "next_check": (today + timedelta(days=item.get("check_days", 7))).isoformat()}
        try:
            stable, preview = releases(reader("repos/" + item["repository"] + "/releases?per_page=100"), today, item.get("tag_prefix", ""))
            row.update(latest=stable["tag_name"] if stable else None,
                released=stable["published_at"][:10] if stable else None,
                url=stable["html_url"] if stable else "https://github.com/" + item["repository"] + "/releases",
                preview=preview["tag_name"] if preview else None,
                preview_released=preview["published_at"][:10] if preview else None,
                status="check-section" if stable and item.get("covered") != stable["tag_name"] else "version-matches" if stable else "no-published-release")
        except Exception as error:
            old = previous.get(item["id"], {})
            row.update({k: old.get(k) for k in ("latest", "released", "url", "preview", "preview_released")})
            row.update(status="unavailable", error=type(error).__name__)
        items.append(row)
    return {"schema_version": 1, "checked": today.isoformat(), "items": items}

def discover(config, reader, today):
    """Public source declarations become research candidates, never proof."""
    records, observations = [], []
    import base64
    for source in config["repositories"]:
        repo = source["repository"]
        try:
            meta = reader("repos/" + repo)
            if meta.get("private") or meta.get("visibility") == "private":
                raise ValueError("Private repository requires a sanitized public export")
            branch = reader("repos/" + repo + "/commits/" + quote(meta["default_branch"], safe=""))
            sha = branch["sha"]
            if not re.fullmatch(r"[0-9a-f]{40}", sha): raise ValueError("Invalid source revision")
            observations.append({"repository": repo, "revision": sha, "pushed": meta.get("pushed_at"), "checked": today.isoformat(), "status": "observed"})
            for path in source.get("paths", ["README.md"]):
                if not re.fullmatch(r"[a-zA-Z0-9_./-]+", path) or ".." in Path(path).parts: raise ValueError("Invalid discovery path")
                obj = reader("repos/" + repo + "/contents/" + path + "?ref=" + sha)
                body = base64.b64decode(obj["content"], validate=False).decode("utf-8")
                if len(body) > 120000: continue
                for block in re.split(r"\n\s*\n", body):
                    if block.startswith(("#", "|", "```", ">")) or re.match(r'^[-*+]\s',block) or "```" in block: continue
                    statement = text(markdown.markdown(block))
                    if re.search(r'browser hardware|dry-run|playwright|website audit',statement,re.I):continue
                    if not 60 <= len(statement) <= 800 or BLOCKED.search(statement): continue
                    if not re.search(r"\b(telemetry|mavlink|simulation|replay|video|firmware|sensor|coordinate|protocol|decoder|logging|camera)\b", statement, re.I): continue
                    # Attribute assertions to their source; the independent checks
                    # can establish implementation facts without certifying hardware.
                    statement = f"{repo}: {statement}"
                    rid = "repo-" + stable_id(repo, path, statement)
                    url = f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
                    record = {"id": rid, "article_id": "article-62", "title": "Repository Integration Notes", "anchor": "ch62", "path": ADDITIONS_PATH,
                        "record_type": "repository-candidate", "statement": statement, "source_candidates": [url], "article_source_candidates": [],
                        "evidence_revision": obj["sha"], "discovery_repository": repo, "source_release_date": None}
                    record.update(triage(record)); records.append(record)
                    if sum(x.get("discovery_repository") == repo for x in records) >= 3: break
        except Exception as error:
            observations.append({"repository": repo, "checked": today.isoformat(), "status": "unavailable", "error": type(error).__name__})
    return records, observations

def emerging_watch(config, reader, today, previous=None):
    found, errors = {}, []
    cutoff = (today - timedelta(days=180)).isoformat()
    for query in config["emerging_queries"]:
        q = query.format(created_after=(today-timedelta(days=365)).isoformat()) + " archived:false fork:false pushed:>=" + cutoff
        try:
            result = reader("search/repositories?" + urlencode({"q": q, "sort": "updated", "per_page": 5}))
            for item in result.get("items", []):
                name = item["full_name"]
                if item.get("private") or item.get("archived") or not item.get('description') or not item.get('language') or not item.get('size') or BLOCKED.search(name + " " + str(item.get("description", ""))): continue
                if not re.search(r'mavlink|dronecan|telemetry|simulation|slam|odometry|vio|gstreamer|firmware|px4|ardupilot|betaflight|drone',item['description'],re.I):continue
                if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name): continue
                entry = {"repository": name, "url": "https://github.com/" + name,
                    "description": plain(item.get("description") or "No project description"),
                    "created": item.get("created_at"), "pushed": item.get("pushed_at"),
                    "license": (item.get("license") or {}).get("spdx_id") or "unknown",
                    "stars": item.get("stargazers_count", 0), "matched_queries": [query],
                    "status": "watch-only; capability unverified", "checked": today.isoformat()}
                if name in found: found[name]["matched_queries"].append(query)
                else: found[name] = entry
        except Exception as error: errors.append({"query": query, "error": type(error).__name__})
    # Preserve prior results on failure, marking them stale instead of erasing them.
    if errors:
        for old in (previous or {}).get("projects", []):
            if old["repository"] not in found: found[old["repository"]] = {**old, "status": "stale; search incomplete"}
    projects = sorted(found.values(), key=lambda x: (-len(x["matched_queries"]), -datetime.fromisoformat(x["pushed"].replace("Z", "+00:00")).timestamp() if x.get("pushed") else 0, x["repository"]), reverse=False)[:12]
    for project in projects:
        try:
            stable, preview = releases(reader("repos/" + project["repository"] + "/releases?per_page=30"), today)
            project.update(release=stable["tag_name"] if stable else None, released=stable["published_at"][:10] if stable else None,
                preview=preview["tag_name"] if preview else None)
        except Exception: project.update(release=None, released=None, release_status="unavailable")
    return {"schema_version": 1, "checked": today.isoformat(), "next_check": (today + timedelta(days=7)).isoformat(), "projects": projects, "errors": errors}

def render_watch(status):
    lines = ["# Release and Information Update Watchlist", "", f"Last checked: **{status['checked']}**. Version matches establish metadata only; they do not verify every claim in a chapter. A changed release opens a section check. Preview releases remain separate from published stable releases. This table observes GitHub releases; projects may also distribute builds through other channels. A tag or code push is not a published release.", "", "| Project | Version covered | Latest stable GitHub release / date | Preview | Status | Check these sections | Next check |", "|---|---|---|---|---|---|---|"]
    for row in status["items"]:
        links = ", ".join(f"[{Path(p).stem}]({Path('..') / p})" for p in row["sections"])
        url = row.get("url") or "https://github.com/" + row["repository"] + "/releases"
        lines.append(f"| [{cell(row['id'])}]({url}) | {cell(row.get('covered') or 'not version-pinned')} | {cell(row.get('latest') or 'unknown')} / {cell(row.get('released') or 'unknown')} | {cell(row.get('preview') or 'none observed')} | {cell(row['status'])} | {links} | {row['next_check']} |")
    lines += ["", "## Check list", "", "- Firmware: changed parameters, units, defaults, board targets and configurator compatibility.", "- Protocols: XML/DSDL definitions, versioned serialization, enums and service support.", "- Video/compute: image/kernel/driver/compiler compatibility, model operators and timing boundary.", "- Procurement/regulations: exact authority, effective date, configuration and superseding material.", "- Prices/availability: current first-party offer/date; a release is not stock availability.", "", "Source availability and due dates are checked nightly. Software release metadata is refreshed nightly; each entry has a seven-day maximum intended interval. A failed check retains the previous observation as unavailable rather than claiming freshness. New releases trigger independent claim checks; they never silently change an aircraft's configuration.", "", "See [emerging projects](../integration/emerging-technology-watch.md) and [repository notes](../integration/repository-updates.md)."]
    if status.get('repositories'):
        lines += ['', '## Related repository discovery', '', '| Repository | Observed revision | Last push | Check attempted | Status |', '|---|---|---|---|---|']
        for row in status['repositories']:
            lines.append(f"| [{cell(row['repository'])}](https://github.com/{row['repository']}) | {cell((row.get('revision') or 'unknown')[:12])} | {cell((row.get('pushed') or 'unknown')[:10])} | {row['checked']} | {cell(row['status'])} |")
    if status.get("sources"):
        lines += ["", "## Source checks and review dates", "", "Reachability is a check; the verification date below is the last factual review. Unavailable checks retain prior fingerprints.", "", "| Source | Last verified/accessed | Check attempted | Availability | Next factual review |", "|---|---|---|---|---|"]
        for source in status["sources"]:
            lines.append(f"| [{cell(source['title'])}]({source['url']}) | {source['accessed']} | {source['checked']} | {cell(source['status'])} | {source['due']} |")
    return "\n".join(lines) + "\n"

def render_emerging(status):
    lines = ["# Emerging Technology Watch", "", f"Observed **{status['checked']}**; next scheduled check by **{status['next_check']}**. This automatically maintained list uses GitHub search metadata. Selection is an editorial inference from topic relevance and recent activity, not a performance endorsement or hardware acceptance.", "", "| Project | Project description (unverified) | Latest stable GitHub release / date | Last code push | License | Evidence status |", "|---|---|---|---|---|---|"]
    for p in status["projects"]:
        lines.append(f"| [{cell(p['repository'])}]({p['url']}) | {cell(p['description'][:220])} | {cell(p.get('release') or 'none observed')} / {cell(p.get('released') or 'unknown')} | {cell((p.get('pushed') or 'unknown')[:10])} | {cell(p['license'])} | {cell(p['status'])} |")
    if not status["projects"]: lines.append("| No results available | Search will retry; no capability inferred | unknown | unknown | unknown | unverified |")
    lines += ["", "## What the next check must establish", "", "- Exact released version and publication date; a recent code push is not a release.", "- License/rights, supported interfaces, reproducible examples and active issue/release history.", "- Whether the claimed capability exists in source/tests, and what remains simulation, bench or field evidence.", "- Primary documentation, conflicting evidence and relevance to an existing integration gap.", "", "No discovered code is executed, installed or granted credentials. Repository descriptions are attributed claims. Relevant factual additions enter separate researcher/verifier checks before becoming handbook guidance. Stars and commit activity indicate attention/activity, not technical quality."]
    if status["errors"]: lines += ["", "Some searches were unavailable; retained entries may be stale. The next cycle retries them."]
    return "\n".join(lines) + "\n"

def scheduled_records(snapshot, sources, source_state, today, watched=None):
    records = []
    by_source = {s["id"]: s for s in sources}
    for record in snapshot["records"]:
        if record.get('path') in {WATCH_PATH,EMERGING_PATH} or record.get('path','').startswith('legal/'):continue
        if record.get("status") != "unreviewed":
            used = [by_source[s] for s in record.get("sources", []) if s in by_source]
            days = min([s.get("review_days", 365) for s in used] or [365])
            verified = date.fromisoformat(record.get("verified") or "1970-01-01")
            changes = any(source_state.get("sources", {}).get(s["id"], {}).get("digest") != s.get("content_sha256") for s in used if s.get("content_sha256"))
            release_changed = any(record.get('path') in row['sections'] and row.get('status') == 'check-section' for row in (watched or []))
            if (today - verified).days < days and not changes and not release_changed: continue
            cycle = max(1, (today - verified).days // days)
        else: cycle = 0
        fingerprints = {s: source_state.get("sources", {}).get(s, {}).get("digest", "") for s in record.get("sources", [])}
        item = {**record, "review_cycle": cycle, "evidence_revision": stable_id(json.dumps(fingerprints, sort_keys=True)) if fingerprints else ""}
        item.update(triage(item)); records.append(item)
    return records

def pending(records, ledger, release):
    known = {row["id"] for row in ledger if row.get('state') != 'planned'}
    result = []
    for record in records:
        spec = research_spec(record, release)
        if spec["id"] in known: continue
        # Migrate old deploy-bound jobs without restarting active/completed work.
        if any(row.get("spec", {}).get("verification_protocol") is None and row.get("spec", {}).get("claim_id") == spec["claim_id"] and row.get("spec", {}).get("statement") == spec["statement"] and row.get("state") in {"researching", "adjudicating", "complete", "exception", "abstained"} for row in ledger): continue
        result.append(record)
        known.add(spec['id'])
    ordered=sorted(result, key=lambda x: ({"P0":0,"P1":1,"P2":2,"P3":3}.get(x.get("priority"),3), -x.get("score",0), x["id"]))
    # Reserve one of the bounded two daily records for additions, so a large
    # legacy audit cannot starve related/emerging repository discovery.
    candidate=next((r for r in ordered if r.get('record_type')=='repository-candidate'),None)
    if candidate and ordered and candidate is not ordered[0]:
        ordered.remove(candidate);ordered.insert(1,candidate)
    return ordered

def apply_verified(root, bundles, *, today, fetch=None):
    """Re-adjudicate exact statements; never execute model-provided patches."""
    data = json.loads((root / "data/evidence.json").read_text())
    claims = {c["id"]: c for c in data["claims"]}
    changed, outcomes = set(), []
    for bundle in bundles:
        spec, packets = bundle["spec"], bundle.get("packets", [])
        try:
            if spec.get("verification_protocol") != "exact-statement-v2": raise ValueError("legacy-proposal-needs-exact-check")
            if (today - date.fromisoformat(bundle["decision"]["created_at"][:10])).days not in range(31): raise ValueError("stale-decision")
            statement = spec["statement"]
            if not 1 <= len(statement) <= 1600 or '\n' in statement or '\r' in statement or BLOCKED.search(statement): raise ValueError("excluded-content")
            classified = claim_type({"statement": statement, **triage({"statement":statement})})
            if classified in {"safety", "recommendation"} or spec["claim_type"] in {"safety", "recommendation", "calculation"}: raise ValueError("exception-policy")
            if {p.get("role") for p in packets} != {"researcher", "verifier"} or len(packets) != 2: raise ValueError("two-isolated-roles-required")
            if any(p["proposed_statement"] != statement for p in packets) or packets[0]["scope"] != packets[1]["scope"] or not packets[0]["scope"].strip(): raise ValueError("exact-statement-and-scope-required")
            if any(s["source_class"] in {"other", "field-observation"} for p in packets for s in p["sources"]): raise ValueError("primary-source-required")
            if classified in {'performance','compatibility'} or spec['claim_type'] in {'performance','compatibility'}:
                hosts={urlsplit(s['url']).hostname for p in packets for s in p['sources']}
                publishers={plain(s['publisher']).casefold() for p in packets for s in p['sources']}
                if len(hosts)<2 or len(publishers)<2: raise ValueError('independent-publishers-required')
            checked = [verify_source_snapshots(p, spec, **({"fetch":fetch} if fetch else {})) for p in packets]
            for before, after in zip(packets, checked):
                if any(x["content_sha256"] != y["content_sha256"] for x,y in zip(before["sources"],after["sources"])): raise ValueError("source-changed-since-research")
            effective = {**spec, "claim_type": classified} if classified in {"performance", "compatibility", "regulatory"} else spec
            decision = adjudicate(effective, checked)
            if not decision["publish"]: raise ValueError("independent-policy-failed")
            path = Path(spec.get("path") or "")
            if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] not in CONTENT_ROOTS or path.suffix != ".md": raise ValueError("excluded-target")
            target = root / path
            if not target.resolve().is_relative_to(root.resolve()): raise ValueError('excluded-target')
            original = target.read_text()
            if "publication-hold" in original or path.as_posix() in {WATCH_PATH,EMERGING_PATH}: raise ValueError("protected-target")
            cid = spec["claim_id"] if spec["claim_id"] in claims else "auto-" + stable_id(spec["claim_id"])
            old = claims.get(cid)
            if old and old.get("maintenance_decision") == bundle["decision"]["id"]: continue
            expected = spec.get("target_statement", statement)
            if old and old["statement"] != expected: raise ValueError("claim-changed-since-plan")
            marker = f"<!-- auto-fact:{cid} -->"
            escaped = re.sub(r"([\\`*_{}\[\]<>#!])", r"\\\1", statement)
            block = f"{marker}\n{escaped}\n\n[claim:{cid}]\n<!-- /auto-fact:{cid} -->"
            if marker in original:
                pattern = re.compile(re.escape(marker) + r".*?" + re.escape(f"<!-- /auto-fact:{cid} -->"), re.S)
                if len(pattern.findall(original)) != 1: raise ValueError("ambiguous-managed-block")
                updated = pattern.sub(lambda _: block, original)
            elif old:
                # Existing canonical claim markers render registry values. Never
                # rewrite arbitrary adjacent prose or generated numerical tables.
                if f"[claim:{cid}]" not in original or old.get("calculation"): raise ValueError("explicit-managed-marker-required")
                if statement != expected: raise ValueError('managed-prose-change-needs-exact-block')
                updated = original
            elif spec.get("record_type") == "repository-candidate" and path.as_posix() == ADDITIONS_PATH:
                updated = original.rstrip() + "\n\n" + block + "\n"
            else:
                blocks = re.split(r"(\n\s*\n)", original)
                matches = [i for i,b in enumerate(blocks) if b.strip() and not b.lstrip().startswith(("#","|","-","*",">","```")) and "```" not in b and text(markdown.markdown(b)) == expected]
                if len(matches) != 1: raise ValueError("exact-standalone-paragraph-required")
                blocks[matches[0]] = block; updated = "".join(blocks)
            source_ids = []
            for packet in checked:
                for source in packet["sources"]:
                    sid = "auto-source-" + stable_id(source["url"], source["content_sha256"])
                    if sid not in {s["id"] for s in data["sources"]}:
                        data["sources"].append({"id":sid,"title":source["title"],"url":source["url"],"passage":source["locator"],"accessed":today.isoformat(),"review_days":30,"content_sha256":source["content_sha256"],"release_version":source["version"]})
                    source_ids.append(sid)
            category = "manufacturer-reported" if any(s["source_class"] == "manufacturer" for p in checked for s in p["sources"]) else "official-source"
            history = copy.deepcopy((old or {}).get("history", []))
            before={k:v for k,v in (old or {"statement":expected,"status":"unreviewed"}).items() if k!='history'}
            history.append({"at":today.isoformat(),"reason":"Independent exact-statement maintenance", "decision":bundle["decision"]["id"],"before":before})
            claim = {"id":cid,"statement":statement,"scope":packets[0]["scope"],"status":category,"sources":sorted(set(source_ids)),"verified":today.isoformat(),"revision":(old or {}).get("revision",0)+1,"history":history,"maintenance_decision":bundle["decision"]["id"]}
            claims[cid] = claim
            target.write_text(updated); changed.add(path.as_posix())
            outcomes.append({"claim":spec["claim_id"],"state":"applied"})
        except (ValueError, KeyError, TypeError, OSError) as error:
            outcomes.append({"claim":spec.get("claim_id"),"state":"abstained","reason":str(error)[:150]})
    if changed:
        data["claims"] = list(claims.values()); json_write(root / "data/evidence.json",data); changed.add("data/evidence.json")
    return sorted(changed), outcomes
