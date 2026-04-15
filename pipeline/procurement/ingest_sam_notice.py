#!/usr/bin/env python3
"""
ingest_sam_notice.py — Manually ingest a SAM.gov opportunity into PIE procurement data.

Fetches a specific SAM notice by ID or URL via the SAM.gov v2 API and appends it
to sam_opportunities.json, then rebuilds solicitations.json.

Usage:
    python pipeline/procurement/ingest_sam_notice.py <notice_id_or_url> [--dry-run]

Examples:
    python pipeline/procurement/ingest_sam_notice.py f7e84283efb64dbfbf8436ea598fe3f0
    python pipeline/procurement/ingest_sam_notice.py https://sam.gov/opp/f7e84283efb64dbfbf8436ea598fe3f0/view
    python pipeline/procurement/ingest_sam_notice.py https://sam.gov/workspace/contract/opp/f7e84283efb64dbfbf8436ea598fe3f0/view

Environment:
    SAM_API_KEY   — SAM.gov public API key (required)
                    Get free key: sam.gov → profile → Public API Key

If SAM_API_KEY is missing, the script will attempt a manual-entry fallback
prompting you to paste the notice title, agency, and deadline from the SAM page.
"""

import json, os, re, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests required. Run: pip install requests --break-system-packages")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT       = Path(__file__).resolve().parent.parent.parent
PROCUREMENT_DIR = REPO_ROOT / "data" / "procurement"

SAM_API_URL     = "https://api.sam.gov/prod/opportunities/v2/search"
SAM_DETAIL_URL  = "https://api.sam.gov/prod/opportunities/v2/{notice_id}"

now_iso = datetime.now(timezone.utc).isoformat()

# Gray zone / Blue UAS keyword lists (mirrors scraper.py)
GRAY_ZONE_KEYWORDS = [
    "anzu", "skyrov", "knowact", "cogito", "specta", "autel",
    "dji", "dahua", "hikvision", "huawei", "zte",
]
BLUE_UAS_MANUFACTURERS = [
    "skydio", "teal", "red cat", "freefly", "anduril", "shield ai",
    "neros", "modalai", "aerovironment", "joby", "wisk", "archer",
    "percepto", "teledyne flir", "flir",
]

def proc_id(raw: str) -> str:
    return "PIE-" + hashlib.md5(raw.encode()).hexdigest()[:8].upper()

def extract_notice_id(arg: str) -> str:
    """Pull bare notice ID from a URL or return as-is if already an ID."""
    # Matches both /opp/{id}/view and /workspace/contract/opp/{id}/view
    m = re.search(r'/opp/([a-f0-9]{32})(?:/|$)', arg)
    if m:
        return m.group(1)
    # Bare 32-char hex ID
    if re.match(r'^[a-f0-9]{32}$', arg.strip()):
        return arg.strip()
    print(f"ERROR: Could not extract notice ID from: {arg}")
    print("  Expected format: 32-char hex ID or sam.gov URL containing /opp/<id>/")
    sys.exit(1)

def flag_check(text: str):
    t = text.lower()
    gz = any(k in t for k in GRAY_ZONE_KEYWORDS)
    bu = any(k in t for k in BLUE_UAS_MANUFACTURERS)
    return gz, bu

def fetch_via_api(notice_id: str, api_key: str) -> dict | None:
    """Try SAM v2 search by noticeId param."""
    print(f"  Fetching via SAM API: noticeId={notice_id}")
    params = {"api_key": api_key, "noticeid": notice_id, "limit": 1}
    try:
        r = requests.get(SAM_API_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        opps = data.get("opportunitiesData", [])
        if opps:
            print(f"  ✓ API returned 1 opportunity")
            return opps[0]
        print(f"  ✗ API returned 0 results for noticeId={notice_id}")
        # Try detail endpoint
        detail_url = SAM_DETAIL_URL.format(notice_id=notice_id)
        r2 = requests.get(detail_url, params={"api_key": api_key}, timeout=30)
        if r2.status_code == 200:
            d = r2.json()
            if d.get("noticeId") or d.get("title"):
                print(f"  ✓ Detail endpoint returned opportunity")
                return d
        print(f"  ✗ Detail endpoint also returned nothing (status {r2.status_code})")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ✗ API error: {e}")
        return None

def manual_entry_fallback(notice_id: str) -> dict:
    """Interactive fallback when API fails — paste key fields from the SAM page."""
    print()
    print("─" * 60)
    print("SAM API returned no data. Manual entry fallback.")
    print(f"Open: https://sam.gov/opp/{notice_id}/view")
    print("─" * 60)
    title        = input("Title (copy from SAM page): ").strip()
    agency       = input("Agency (e.g. Dept of the Air Force): ").strip()
    sol_number   = input("Solicitation Number (or leave blank): ").strip()
    notice_type  = input("Notice Type (e.g. Sources Sought / Presolicitation / Combined): ").strip() or "Solicitation"
    naics        = input("NAICS Code (e.g. 336411): ").strip()
    deadline     = input("Response Deadline YYYY-MM-DD (or blank): ").strip() or None
    posted_date  = input("Posted Date YYYY-MM-DD (or blank): ").strip() or now_iso[:10]
    set_aside    = input("Set-aside type (e.g. Small Business, or blank): ").strip() or None
    contact_name = input("POC Name (or blank): ").strip()
    contact_email= input("POC Email (or blank): ").strip()
    description  = input("Brief description (optional, paste first sentence): ").strip()

    return {
        "noticeId":              notice_id,
        "title":                 title,
        "fullParentPathName":    agency,
        "type":                  notice_type,
        "solicitationNumber":    sol_number,
        "naicsCode":             naics,
        "postedDate":            posted_date,
        "responseDeadLine":      deadline,
        "typeOfSetAsideDescription": set_aside,
        "pointOfContact":        [{"fullName": contact_name, "email": contact_email}] if contact_name else [],
        "award":                 {},
        "description":           description,
        "_manual_entry":         True,
        "_ingested_at":          now_iso,
    }

def opp_to_solicitation(opp: dict, notice_id: str) -> dict:
    """Convert raw SAM opportunity dict to unified solicitation schema."""
    contacts     = opp.get("pointOfContact") or []
    contact_email = contacts[0].get("email", "") if contacts else ""
    contact_name  = contacts[0].get("fullName", "") if contacts else ""
    award_data    = opp.get("award") or {}
    amount        = award_data.get("amount") if award_data else None
    title         = opp.get("title", "")
    full_text     = f"{title} {opp.get('description','')}"
    gz, bu        = flag_check(full_text)

    return {
        "id":             proc_id(f"sam-{notice_id}"),
        "source":         "sam",
        "source_label":   "SAM.gov",
        "type":           opp.get("type", "Solicitation"),
        "title":          title,
        "agency":         (opp.get("fullParentPathName", "") or "").split(".")[0],
        "sub_agency":     ".".join((opp.get("fullParentPathName") or "").split(".")[1:3]),
        "recipient":      (award_data.get("awardee") or {}).get("name", "") if award_data else "",
        "amount":         float(amount) if amount else None,
        "award_id":       opp.get("solicitationNumber"),
        "posted_date":    opp.get("postedDate") or now_iso[:10],
        "deadline":       opp.get("responseDeadLine"),
        "naics":          opp.get("naicsCode"),
        "set_aside":      opp.get("typeOfSetAsideDescription"),
        "contact_email":  contact_email,
        "contact_name":   contact_name,
        "description":    opp.get("description", ""),
        "url":            f"https://sam.gov/opp/{notice_id}/view",
        "sam_url":        f"https://sam.gov/workspace/contract/opp/{notice_id}/view",
        "notice_id":      notice_id,
        "gray_zone_flag": gz,
        "blue_uas_flag":  bu,
        "manual_entry":   opp.get("_manual_entry", False),
        "scraped_at":     now_iso,
    }

def load_existing_opportunities() -> list:
    path = PROCUREMENT_DIR / "sam_opportunities.json"
    if path.exists():
        try:
            d = json.load(open(path))
            return d.get("opportunities", [])
        except Exception:
            return []
    return []

def save_opportunities(opps: list):
    path = PROCUREMENT_DIR / "sam_opportunities.json"
    PROCUREMENT_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "opportunities": opps,
            "scraped_at":    now_iso,
            "count":         len(opps),
        }, f, indent=2)
    print(f"  ✓ Saved {len(opps)} opportunities → {path.relative_to(REPO_ROOT)}")

def rebuild_solicitations():
    """Re-run the solicitations merge after adding new opportunity."""
    print("\n  Rebuilding solicitations.json…")
    scraper_path = Path(__file__).parent / "scraper.py"
    if not scraper_path.exists():
        print("  ⚠ scraper.py not found — skipping rebuild. Run scraper manually.")
        return
    import subprocess
    result = subprocess.run(
        [sys.executable, str(scraper_path), "--dry-run"],
        capture_output=True, text=True,
        cwd=str(REPO_ROOT)
    )
    # Dry-run just validates — do a real targeted rebuild
    # Import build function directly
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("scraper", scraper_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Load all current sources
        def _load(filename, key):
            p = PROCUREMENT_DIR / filename
            if p.exists():
                try:
                    return json.load(open(p)).get(key, [])
                except Exception:
                    pass
            return []

        usa_awards   = _load("federal_awards.json",    "awards")
        sam_opps     = _load("sam_opportunities.json", "opportunities")
        sbir_awards  = _load("sbir_awards.json",       "awards")
        news_articles= _load("news_signals.json",      "articles")

        sol_data = mod.build_solicitations_json(usa_awards, sam_opps, sbir_awards, news_articles)
        gz_data  = mod.build_gray_zone_matches(sol_data["solicitations"])

        with open(PROCUREMENT_DIR / "solicitations.json", "w", encoding="utf-8") as f:
            json.dump(sol_data, f, indent=2)
        with open(PROCUREMENT_DIR / "gray_zone_matches.json", "w", encoding="utf-8") as f:
            json.dump(gz_data, f, indent=2)

        m = sol_data["meta"]
        print(f"  ✓ solicitations.json: {m['total_solicitations']} records "
              f"(SAM: {m['by_source']['sam']}, GZ: {m['gray_zone_count']}, BU: {m['blue_uas_count']})")
    except Exception as e:
        print(f"  ⚠ Rebuild failed: {e} — run scraper manually to update solicitations.json")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manually ingest a SAM.gov notice into PIE")
    parser.add_argument("notice", help="SAM notice ID (32-char hex) or full SAM.gov URL")
    parser.add_argument("--dry-run", action="store_true", help="Print result without saving")
    parser.add_argument("--no-rebuild", action="store_true", help="Skip solicitations.json rebuild")
    args = parser.parse_args()

    notice_id = extract_notice_id(args.notice)
    api_key   = os.environ.get("SAM_API_KEY", "").strip()

    print(f"\n{'='*60}")
    print(f"SAM Notice Ingest")
    print(f"Notice ID: {notice_id}")
    print(f"API key:   {'set (' + api_key[:8] + '…)' if api_key else 'NOT SET'}")
    print(f"{'='*60}\n")

    # Try API fetch first
    raw_opp = None
    if api_key:
        raw_opp = fetch_via_api(notice_id, api_key)

    # Fall back to manual entry
    if not raw_opp:
        if not sys.stdin.isatty():
            print("ERROR: API returned no data and stdin is not a terminal (can't do manual entry).")
            print(f"  Open https://sam.gov/opp/{notice_id}/view and re-run interactively.")
            sys.exit(1)
        raw_opp = manual_entry_fallback(notice_id)

    # Convert to unified schema
    sol = opp_to_solicitation(raw_opp, notice_id)

    print(f"\n{'─'*60}")
    print(f"Title:      {sol['title']}")
    print(f"Agency:     {sol['agency']}")
    print(f"Type:       {sol['type']}")
    print(f"NAICS:      {sol['naics'] or '—'}")
    print(f"Deadline:   {sol['deadline'] or '—'}")
    print(f"Posted:     {sol['posted_date']}")
    print(f"Amount:     {'$'+str(sol['amount']) if sol['amount'] else '—'}")
    print(f"Gray Zone:  {'⚠ YES' if sol['gray_zone_flag'] else 'No'}")
    print(f"Blue UAS:   {'✓ YES' if sol['blue_uas_flag'] else 'No'}")
    print(f"URL:        {sol['url']}")
    print(f"{'─'*60}")

    if args.dry_run:
        print("\n[DRY RUN] Not saving. Full record:")
        print(json.dumps(sol, indent=2))
        return

    # Load existing, deduplicate by notice_id
    existing = load_existing_opportunities()
    existing_ids = {o.get("noticeId", "") for o in existing}

    if notice_id in existing_ids:
        print(f"\n  Notice {notice_id} already exists in sam_opportunities.json — updating.")
        existing = [o for o in existing if o.get("noticeId") != notice_id]

    # Append raw opp (with noticeId) so rebuild works correctly
    raw_opp["noticeId"] = raw_opp.get("noticeId") or notice_id
    existing.append(raw_opp)
    save_opportunities(existing)

    if not args.no_rebuild:
        rebuild_solicitations()

    print(f"\n✓ Done. Next step: commit data/procurement/ and push to trigger Forge sync.")
    print(f"  git add data/procurement/ && git commit -m 'ingest: SAM notice {notice_id[:8]}' && git push")

if __name__ == "__main__":
    main()
