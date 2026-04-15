#!/usr/bin/env python3
"""
PIE Procurement Scraper v2 — discovers UAS government solicitations across
federal, state, and local sources. Outputs solicitations.json for intel.html
Solicitations tab + gray_zone_matches.json for PIE cross-reference.

Data Sources:
  1. USAspending.gov API (free, no auth)  — federal contract awards
  2. SAM.gov Opportunities v2 API        — open solicitations (SAM_API_KEY)
  3. SBIR.gov API (free, no auth)        — R&D solicitations & awards
  4. Google News RSS                      — state/local procurement signals

Filter stack (applied in order):
  1. NAICS codes: 336411, 334515, 334511, 517410, 541370, 541519, 541715, 928110
  2. Keywords:    drone, UAS, sUAS, unmanned aerial, counter-UAS, UAV, Blue UAS, uncrewed
  3. Blue UAS manufacturer names
  4. Dollar threshold: >= $25,000 (configurable, 0 = no floor)

Outputs:
  data/procurement/solicitations.json      — unified feed for Forge intel.html
  data/procurement/federal_awards.json     — raw USAspending results
  data/procurement/sam_opportunities.json  — raw SAM.gov results
  data/procurement/sbir_awards.json        — raw SBIR results
  data/procurement/news_signals.json       — news-sourced signals
  data/procurement/gray_zone_matches.json  — cross-ref with gray zone entities

Usage:
  python pipeline/procurement/scraper.py [--full] [--start-date YYYY-MM-DD] [--limit N]

Environment variables:
  SAM_API_KEY   — SAM.gov API key (free at sam.gov; get key under profile → Public API Key)
"""

import json, time, hashlib, argparse, os, re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install: pip install requests --break-system-packages")
    exit(1)

REPO_ROOT       = Path(__file__).resolve().parent.parent.parent
PROCUREMENT_DIR = REPO_ROOT / "data" / "procurement"
GRAYZONE_DIR    = REPO_ROOT / "data" / "grayzone"

now     = datetime.now(timezone.utc)
now_iso = now.isoformat()

REQUEST_DELAY   = 1.2   # seconds between API calls — be polite
MIN_AMOUNT      = 25_000  # dollar floor; 0 = no floor

# ── NAICS codes ────────────────────────────────────────────────────────────
NAICS_CODES = [
    "336411",  # Aircraft Manufacturing (primary UAS)
    "334515",  # Instrument Mfg for Measuring/Testing Electricity — Blue UAS SIN 627-50
    "334511",  # Search, Detection, Navigation, Guidance Instruments
    "517410",  # Satellite Telecommunications — UAS data links, ISR
    "541370",  # Surveying & Mapping Services — commercial UAS inspection
    "541519",  # Other Computer Related Services — UAS software/GCS
    "541715",  # R&D in Physical/Engineering Sciences — DoD sUAS R&D
    "928110",  # National Security — C-UAS, counter-drone DoD
]

# ── Keyword sets ─────────────────────────────────────────────────────────────
UAS_KEYWORDS = [
    "unmanned aircraft system",
    "unmanned aerial system",
    "UAS",
    "sUAS",
    "small unmanned aircraft",
    "drone",
    "counter-UAS",
    "C-UAS",
    "UAV",
    "Blue UAS",
    "uncrewed aircraft",
    "RPAS",
]

# SAM.gov title searches (must be short — title-only search only)
SAM_TITLE_TERMS = [
    "unmanned aircraft",
    "UAS",
    "sUAS",
    "drone",
    "Blue UAS",
    "counter-UAS",
    "uncrewed",
]

# Blue UAS manufacturer names (for news / award cross-ref)
BLUE_UAS_MANUFACTURERS = [
    "Skydio", "Teal Drones", "BRINC", "Anduril", "Inspired Flight",
    "Freefly", "AeroVironment", "Parrot", "ModalAI", "Wingtra",
    "Vantage Robotics", "Quantum Systems", "Ascent AeroSystems",
    "FlightWave", "ACSL", "Auterion", "AgEagle", "Red Cat",
]

# Gray zone vendor strings to flag in awards/news
GRAY_ZONE_VENDORS = [
    "anzu robotics", "anzu",
    "cogito tech", "specta",
    "skyrover", "knowact",
    "autel robotics", "autel",
    "dji", "dajiang",
]


def ensure_dirs():
    PROCUREMENT_DIR.mkdir(parents=True, exist_ok=True)


def proc_id(seed: str) -> str:
    return "sol-" + hashlib.md5(seed.encode()).hexdigest()[:10]


def is_uas_relevant(text: str) -> bool:
    """Quick keyword check on title/description text."""
    t = (text or "").lower()
    return any(k.lower() in t for k in UAS_KEYWORDS)


def passes_dollar_floor(amount) -> bool:
    if MIN_AMOUNT == 0:
        return True
    try:
        return float(amount or 0) >= MIN_AMOUNT
    except (TypeError, ValueError):
        return True  # unknown amount — keep it


# ══════════════════════════════════════════════════════════════════════════════
# 1. USAspending.gov — Federal Contract Awards
# ══════════════════════════════════════════════════════════════════════════════

class USASpendingScraper:
    """No auth required. Free. Rate-limited."""

    BASE_URL = "https://api.usaspending.gov/api/v2"

    # NAICS filter is contract-only on USAspending. Applying it to grant
    # award_type_codes (02-05) returns 0 results (and recent API versions
    # return 200+empty rather than 400, so the old keyword-only fallback
    # never fired). Also: in-progress awards have Award Amount=null while
    # Total Outlays is populated — request both and fall back in
    # to_solicitation() so the dollar floor doesn't silently drop them.
    NAICS_REQUIRE = ["336411", "334515", "334511", "517410", "541370", "541519", "541715"]
    QUERY_GROUPS = [
        # (label, award_type_codes, apply_naics_filter)
        ("contracts", ["A", "B", "C", "D"],     True),
        ("grants",    ["02", "03", "04", "05"], False),
    ]

    def search_awards(self, keyword: str, start_date: str, limit: int = 50) -> list:
        end_date = now.strftime("%Y-%m-%d")
        url      = f"{self.BASE_URL}/search/spending_by_award/"
        results  = []

        for label, award_types, apply_naics in self.QUERY_GROUPS:
            filters = {
                "keywords": [keyword],
                "time_period": [{"start_date": start_date, "end_date": end_date}],
                "award_type_codes": award_types,
            }
            if apply_naics:
                filters["naics_codes"] = {"require": self.NAICS_REQUIRE}

            payload = {
                "filters": filters,
                "fields": [
                    "Award ID", "Recipient Name", "Award Amount", "Total Outlays",
                    "Description", "Start Date", "End Date",
                    "Awarding Agency", "Awarding Sub Agency", "Award Type",
                ],
                "page": 1, "limit": limit,
                "sort": "Award Amount", "order": "desc",
                "subawards": False,
            }
            try:
                resp = requests.post(url, json=payload, timeout=30)
                if resp.status_code == 400 and apply_naics:
                    # Belt-and-braces: contract NAICS rejected → retry keyword-only
                    del payload["filters"]["naics_codes"]
                    resp = requests.post(url, json=payload, timeout=30)
                resp.raise_for_status()
                data   = resp.json()
                batch  = data.get("results", [])
                total  = data.get("page_metadata", {}).get("total", "?")
                print(f"    [{keyword[:28]:28s}/{label}] → {len(batch)} (of {total})")
                results.extend(batch)
            except requests.exceptions.RequestException as e:
                print(f"    [{keyword[:28]:28s}/{label}] → ERROR: {e}")

        return results

    def run(self, start_date: str, limit: int = 50) -> list:
        all_results, seen = [], set()
        for kw in UAS_KEYWORDS:
            for r in self.search_awards(kw, start_date, limit):
                aid = r.get("Award ID") or r.get("internal_id", "")
                if aid and aid not in seen:
                    seen.add(aid)
                    all_results.append(r)
            time.sleep(REQUEST_DELAY)
        print(f"  USAspending: {len(all_results)} unique awards across {len(UAS_KEYWORDS)} keywords")
        return all_results

    @staticmethod
    def to_solicitation(award: dict) -> dict:
        """Normalize to unified solicitation schema."""
        # Award Amount is null on in-progress awards; Total Outlays is populated.
        # Without this fallback those rows are silently dropped by the dollar floor.
        amount = award.get("Award Amount") or award.get("Total Outlays") or 0
        return {
            "id":           proc_id(f"usa-{award.get('Award ID', '')}"),
            "source":       "usaspending",
            "source_label": "USAspending.gov",
            "type":         "award",
            "title":        award.get("Description") or "Federal Award",
            "agency":       award.get("Awarding Agency", ""),
            "sub_agency":   award.get("Awarding Sub Agency", ""),
            "recipient":    award.get("Recipient Name", ""),
            "amount":       float(amount) if amount else None,
            "award_id":     award.get("Award ID"),
            "posted_date":  award.get("Start Date"),
            "deadline":     None,
            "naics":        None,
            "set_aside":    None,
            "url":          f"https://www.usaspending.gov/award/{award.get('Award ID', '')}",
            "gray_zone_flag": any(v in (award.get("Recipient Name") or "").lower() for v in GRAY_ZONE_VENDORS),
            "blue_uas_flag": any(m.lower() in (award.get("Recipient Name") or "").lower() for m in BLUE_UAS_MANUFACTURERS),
            "scraped_at":   now_iso,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 2. SAM.gov Opportunities v2
# ══════════════════════════════════════════════════════════════════════════════

class SAMScraper:
    """
    Free SAM.gov API key: sam.gov → Sign In → Profile icon → Public API Key
    Key expires every 90 days. Rate limit: 1,000 req/day with key.
    IMPORTANT: SAM v2 search only supports `title` field — no full-text keyword param.
    """

    OPP_URL = "https://api.sam.gov/prod/opportunities/v2/search"

    # PSC codes for UAS hardware/services
    PSC_CODES = ["1550", "1510", "1520", "1540"]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SAM_API_KEY", "").strip()
        if not self.api_key:
            print("  ⚠ SAM_API_KEY not set — get free key at sam.gov (profile → Public API Key)")

    def search_by_title(self, title: str, posted_from: str, limit: int = 100) -> list:
        if not self.api_key:
            return []
        params = {
            "api_key":    self.api_key,
            "title":      title,
            "postedFrom": posted_from,
            "limit":      limit,
            "offset":     0,
            "active":     "true",
        }
        try:
            resp = requests.get(self.OPP_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            opps = data.get("opportunitiesData", [])
            total = data.get("totalRecords", "?")
            print(f"    [SAM title={title:<20s}] → {len(opps)} (of {total})")
            return opps
        except requests.exceptions.RequestException as e:
            print(f"    [SAM title={title}] → ERROR: {e}")
            return []

    def search_by_naics(self, naics: str, posted_from: str, limit: int = 100) -> list:
        if not self.api_key:
            return []
        params = {
            "api_key":    self.api_key,
            "naicsCode":  naics,
            "postedFrom": posted_from,
            "limit":      limit,
            "offset":     0,
            "active":     "true",
        }
        try:
            resp = requests.get(self.OPP_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            opps = data.get("opportunitiesData", [])
            print(f"    [SAM NAICS={naics}] → {len(opps)}")
            return opps
        except requests.exceptions.RequestException as e:
            print(f"    [SAM NAICS={naics}] → ERROR: {e}")
            return []

    def fetch_by_notice_id(self, notice_id: str):
        """Fetch a single SAM opportunity by its exact notice ID."""
        if not self.api_key:
            return None
        # Try search endpoint with noticeid param
        try:
            r = requests.get(self.OPP_URL,
                             params={"api_key": self.api_key, "noticeid": notice_id, "limit": 1},
                             timeout=30)
            r.raise_for_status()
            opps = r.json().get("opportunitiesData", [])
            if opps:
                return opps[0]
        except requests.exceptions.RequestException:
            pass
        # Try detail endpoint fallback
        try:
            detail_url = f"https://api.sam.gov/prod/opportunities/v2/{notice_id}"
            r2 = requests.get(detail_url, params={"api_key": self.api_key}, timeout=30)
            if r2.status_code == 200:
                d = r2.json()
                if d.get("noticeId") or d.get("title"):
                    return d
        except requests.exceptions.RequestException:
            pass
        return None

    def fetch_watchlist(self, watchlist_path) -> list:
        """
        Fetch all notice IDs in sam_watchlist.json.
        Returns list of raw opportunity dicts.
        Notices that 404 are retained as stubs so they still appear in the tab.
        """
        if not watchlist_path.exists():
            return []
        try:
            data = json.load(open(watchlist_path))
        except Exception:
            return []

        notices = data.get("notices", [])
        if not notices:
            return []

        print(f"  [SAM watchlist] {len(notices)} pinned notice(s)")
        results = []
        for entry in notices:
            nid = entry.get("notice_id", "")
            if not nid:
                continue
            opp = self.fetch_by_notice_id(nid) if self.api_key else None
            if opp:
                opp["_watchlisted"] = True
                opp["_watchlist_label"] = entry.get("label", "")
                print(f"    + {nid[:12]}... {(opp.get('title') or '')[:60]}")
                results.append(opp)
            else:
                # API miss — create a stub so it still appears in Procurement tab
                stub = {
                    "noticeId":           nid,
                    "title":              entry.get("label") or f"SAM Notice {nid[:12]}...",
                    "fullParentPathName": "",
                    "type":               "Solicitation",
                    "solicitationNumber": "",
                    "naicsCode":          "",
                    "postedDate":         entry.get("added", now_iso[:10]),
                    "responseDeadLine":   None,
                    "pointOfContact":     [],
                    "award":              {},
                    "_watchlisted":       True,
                    "_watchlist_label":   entry.get("label", ""),
                    "_stub":              True,
                    "_ingested_at":       now_iso,
                }
                print(f"    ~ {nid[:12]}... API miss, stub retained")
                results.append(stub)
            time.sleep(REQUEST_DELAY)

        return results

    def run(self, start_date: str, limit: int = 100) -> list:
        # Format date as MM/DD/YYYY for SAM API
        try:
            dt = datetime.strptime(start_date, "%Y-%m-%d")
            posted_from = dt.strftime("%m/%d/%Y")
        except ValueError:
            posted_from = "01/01/2025"

        all_opps, seen = [], set()

        # Watchlist: always fetch pinned notice IDs first
        watchlist_path = PROCUREMENT_DIR / "sam_watchlist.json"
        for opp in self.fetch_watchlist(watchlist_path):
            nid = opp.get("noticeId", "")
            if nid and nid not in seen:
                seen.add(nid)
                all_opps.append(opp)

        # Title searches
        for term in SAM_TITLE_TERMS:
            for opp in self.search_by_title(term, posted_from, limit):
                nid = opp.get("noticeId", "")
                if nid and nid not in seen:
                    seen.add(nid)
                    all_opps.append(opp)
            time.sleep(REQUEST_DELAY)

        # NAICS searches (336411 + 334515 most productive for UAS)
        for naics in ["336411", "334515", "334511"]:
            for opp in self.search_by_naics(naics, posted_from, limit):
                nid = opp.get("noticeId", "")
                if nid and nid not in seen:
                    # Post-filter: must be UAS-relevant by title
                    title = opp.get("title", "")
                    if is_uas_relevant(title) or any(
                        n in (opp.get("naicsCode") or "") for n in ["336411", "334515"]
                    ):
                        seen.add(nid)
                        all_opps.append(opp)
            time.sleep(REQUEST_DELAY)

        wl_count = len([o for o in all_opps if o.get("_watchlisted")])
        print(f"  SAM.gov: {len(all_opps)} unique opportunities ({wl_count} watchlisted)")
        return all_opps

    @staticmethod
    def to_solicitation(opp: dict) -> dict:
        contacts = opp.get("pointOfContact") or []
        contact_email = contacts[0].get("email", "") if contacts else ""
        contact_name  = contacts[0].get("fullName", "") if contacts else ""
        award_data    = opp.get("award") or {}
        amount        = award_data.get("amount") if award_data else None
        return {
            "id":           proc_id(f"sam-{opp.get('noticeId', '')}"),
            "source":       "sam",
            "source_label": "SAM.gov",
            "type":         opp.get("type", "Solicitation"),
            "title":        opp.get("title", ""),
            "agency":       opp.get("fullParentPathName", "").split(".")[0] if opp.get("fullParentPathName") else "",
            "sub_agency":   ".".join((opp.get("fullParentPathName") or "").split(".")[1:3]),
            "recipient":    (award_data.get("awardee") or {}).get("name", "") if award_data else "",
            "amount":       float(amount) if amount else None,
            "award_id":     opp.get("solicitationNumber"),
            "posted_date":  opp.get("postedDate"),
            "deadline":     opp.get("responseDeadLine"),
            "naics":        opp.get("naicsCode"),
            "set_aside":    opp.get("typeOfSetAsideDescription"),
            "contact_email": contact_email,
            "contact_name":  contact_name,
            "url":          f"https://sam.gov/opp/{opp.get('noticeId', '')}/view",
            "gray_zone_flag": False,
            "blue_uas_flag": any(m.lower() in (opp.get("title") or "").lower() for m in BLUE_UAS_MANUFACTURERS),
            "scraped_at":   now_iso,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 3. SBIR.gov — R&D Solicitations & Awards
# ══════════════════════════════════════════════════════════════════════════════

class SBIRScraper:
    """
    SBIR.gov public API — no auth required. High UAS R&D volume.
    Covers DoD SBIR/STTR Phase I & II drone-related topics.
    """

    BASE_URL = "https://api.sbir.gov/public/api"

    def search_awards(self, keyword: str, limit: int = 50) -> list:
        params = {
            "keyword": keyword,
            "rows":    limit,
            "start":   0,
        }
        try:
            resp = requests.get(f"{self.BASE_URL}/awards", params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            results = data if isinstance(data, list) else data.get("docs", data.get("results", []))
            print(f"    [SBIR kw={keyword:<20s}] → {len(results)}")
            return results
        except requests.exceptions.RequestException as e:
            print(f"    [SBIR kw={keyword}] → ERROR: {e}")
            return []

    def run(self, limit: int = 50) -> list:
        all_results, seen = [], set()
        sbir_kws = ["drone", "UAS", "unmanned aircraft", "counter-UAS", "sUAS"]
        for kw in sbir_kws:
            for r in self.search_awards(kw, limit):
                # SBIR uses 'award_uid' or 'contract'
                aid = r.get("award_uid") or r.get("contract") or r.get("award_number", "")
                if aid and str(aid) not in seen:
                    seen.add(str(aid))
                    all_results.append(r)
            time.sleep(REQUEST_DELAY)
        print(f"  SBIR.gov: {len(all_results)} unique R&D awards")
        return all_results

    @staticmethod
    def to_solicitation(award: dict) -> dict:
        amount_str = award.get("award_amount") or award.get("contract_award_amount") or "0"
        try:
            amount = float(str(amount_str).replace(",", "").replace("$", ""))
        except (ValueError, TypeError):
            amount = None
        company = award.get("firm") or award.get("company") or ""
        title   = award.get("title") or award.get("award_title") or "SBIR Award"
        agency  = award.get("agency") or ""
        return {
            "id":           proc_id(f"sbir-{award.get('award_uid', title[:20])}"),
            "source":       "sbir",
            "source_label": "SBIR.gov",
            "type":         "SBIR/STTR Award",
            "title":        title,
            "agency":       agency,
            "sub_agency":   award.get("branch") or "",
            "recipient":    company,
            "amount":       amount,
            "award_id":     str(award.get("award_uid") or award.get("contract", "")),
            "posted_date":  award.get("date_signed") or award.get("award_year", ""),
            "deadline":     None,
            "naics":        None,
            "set_aside":    "SBIR/STTR",
            "url":          award.get("agency_url") or f"https://www.sbir.gov/node/{award.get('award_uid', '')}",
            "gray_zone_flag": any(v in company.lower() for v in GRAY_ZONE_VENDORS),
            "blue_uas_flag": any(m.lower() in company.lower() or m.lower() in title.lower() for m in BLUE_UAS_MANUFACTURERS),
            "scraped_at":   now_iso,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 4. Google News RSS — State/Local Procurement Signals
# ══════════════════════════════════════════════════════════════════════════════

class NewsScraper:
    """Google News RSS — no auth. Captures state/local procurement signals."""

    RSS_URL = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    HEADERS = {"User-Agent": "PIE-Procurement-Scanner/2.0"}

    # Procurement-specific queries — more targeted than general news
    QUERIES = [
        # Federal program signals
        "UAS government solicitation contract award 2026",
        "drone procurement RFP government agency 2026",
        "counter-UAS government contract award",
        "Blue UAS cleared list contract",
        "Drone Dominance Program contract",
        # State/local purchasing
        "police department drone RFP 2026",
        "sheriff drone purchase contract",
        "fire department UAS procurement",
        "public safety drone grant award",
        "city county drone contract solicitation",
        # Gray zone monitoring
        "Anzu Robotics government contract",
        "Autel government purchase law enforcement",
        "DJI ban government procurement alternative",
        # Blue UAS winner signals
        "Skydio government contract award",
        "BRINC drone law enforcement contract",
    ]

    def search(self, query: str, max_results: int = 8) -> list:
        url = self.RSS_URL.format(q=query.replace(" ", "+"))
        try:
            resp = requests.get(url, timeout=15, headers=self.HEADERS)
            resp.raise_for_status()
            root  = ET.fromstring(resp.content)
            items = root.findall(".//item")
            results = []
            for item in items[:max_results]:
                pub = item.findtext("pubDate", "")
                results.append({
                    "title":     item.findtext("title", ""),
                    "url":       item.findtext("link", ""),
                    "published": pub,
                    "source":    item.findtext("source", ""),
                    "query":     query,
                })
            print(f"    [News: {query[:45]:<45s}] → {len(results)}")
            return results
        except Exception as e:
            print(f"    [News: {query[:45]}] → ERROR: {e}")
            return []

    def run(self, max_per: int = 6) -> list:
        all_results, seen = [], set()
        for q in self.QUERIES:
            for r in self.search(q, max_per):
                url = r.get("url", "")
                if url and url not in seen:
                    seen.add(url)
                    all_results.append(r)
            time.sleep(REQUEST_DELAY)
        print(f"  News RSS: {len(all_results)} unique articles across {len(self.QUERIES)} queries")
        return all_results

    @staticmethod
    def to_solicitation(article: dict) -> dict:
        gz = any(v in (article.get("title") or "").lower() for v in GRAY_ZONE_VENDORS)
        bu = any(m.lower() in (article.get("title") or "").lower() for m in BLUE_UAS_MANUFACTURERS)
        # Parse ISO date from RSS pubDate
        pub = article.get("published", "")
        return {
            "id":           proc_id(f"news-{article.get('url', '')}"),
            "source":       "news",
            "source_label": article.get("source") or "News",
            "type":         "news_signal",
            "title":        article.get("title", ""),
            "agency":       "",
            "sub_agency":   "",
            "recipient":    "",
            "amount":       None,
            "award_id":     None,
            "posted_date":  pub,
            "deadline":     None,
            "naics":        None,
            "set_aside":    None,
            "url":          article.get("url", ""),
            "gray_zone_flag": gz,
            "blue_uas_flag":  bu,
            "query":          article.get("query", ""),
            "scraped_at":   now_iso,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 5. Cross-reference & Unified Output
# ══════════════════════════════════════════════════════════════════════════════

def build_solicitations_json(usa_awards, sam_opps, sbir_awards, news_articles):
    """
    Merge all sources into unified solicitations.json for intel.html Solicitations tab.
    Apply dollar floor. Deduplicate. Tag gray zone / Blue UAS signals.
    """
    unified = []

    for a in usa_awards:
        s = USASpendingScraper.to_solicitation(a)
        if passes_dollar_floor(s.get("amount")):
            unified.append(s)

    for o in sam_opps:
        unified.append(SAMScraper.to_solicitation(o))  # SAM solicitations: no amount filter (unknown value)

    for a in sbir_awards:
        s = SBIRScraper.to_solicitation(a)
        if passes_dollar_floor(s.get("amount")):
            unified.append(s)

    for n in news_articles:
        unified.append(NewsScraper.to_solicitation(n))

    # Sort: gray zone signals first, then by date desc
    def sort_key(s):
        return (
            0 if s.get("gray_zone_flag") else 1,
            0 if s.get("blue_uas_flag")  else 1,
            s.get("posted_date") or "",
        )
    unified.sort(key=sort_key, reverse=True)

    gray_zone_signals = [s for s in unified if s.get("gray_zone_flag")]
    blue_uas_signals  = [s for s in unified if s.get("blue_uas_flag")]
    sam_live          = [s for s in unified if s["source"] == "sam" and s.get("deadline")]

    meta = {
        "generated_at":        now_iso,
        "total_solicitations": len(unified),
        "by_source": {
            "usaspending": len([s for s in unified if s["source"] == "usaspending"]),
            "sam":         len([s for s in unified if s["source"] == "sam"]),
            "sbir":        len([s for s in unified if s["source"] == "sbir"]),
            "news":        len([s for s in unified if s["source"] == "news"]),
        },
        "gray_zone_count": len(gray_zone_signals),
        "blue_uas_count":  len(blue_uas_signals),
        "open_solicitations": len(sam_live),
        "min_amount_filter":  MIN_AMOUNT,
    }

    return {
        "meta":           meta,
        "solicitations":  unified,
    }


def build_gray_zone_matches(unified_solicitations):
    """Generate gray_zone_matches.json for backward compat with PIE pipeline."""
    federal_awards = [s for s in unified_solicitations if s["source"] == "usaspending"]
    gz_matches     = [s for s in unified_solicitations if s.get("gray_zone_flag")]
    news_matches   = [s for s in unified_solicitations if s["source"] == "news" and s.get("gray_zone_flag")]

    vendors = list(set(
        v for s in gz_matches
        for v in GRAY_ZONE_VENDORS
        if v in (s.get("title") or "").lower() or v in (s.get("recipient") or "").lower()
    ))

    return {
        "generated_at":             now_iso,
        "federal_awards_total":     len(federal_awards),
        "gray_zone_federal_matches": len([s for s in gz_matches if s["source"] == "usaspending"]),
        "news_signals_total":        len([s for s in unified_solicitations if s["source"] == "news"]),
        "gray_zone_news_mentions":   len(news_matches),
        "all_gray_zone_signals":     gz_matches,
        "vendors_flagged":           vendors,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="PIE Procurement + Solicitations Scraper v2")
    parser.add_argument("--full",         action="store_true", help="Run all scrapers (default)")
    parser.add_argument("--federal-only", action="store_true")
    parser.add_argument("--sam-only",     action="store_true")
    parser.add_argument("--news-only",    action="store_true")
    parser.add_argument("--sbir-only",    action="store_true")
    parser.add_argument("--start-date",   default="2024-01-01", help="YYYY-MM-DD")
    parser.add_argument("--limit",        type=int, default=50)
    parser.add_argument("--dry-run",      action="store_true")
    args = parser.parse_args()

    specific = args.federal_only or args.sam_only or args.news_only or args.sbir_only
    run_federal = args.full or args.federal_only or not specific
    run_sam     = args.full or args.sam_only     or not specific
    run_news    = args.full or args.news_only    or not specific
    run_sbir    = args.full or args.sbir_only    or not specific

    print("=" * 65)
    print("PIE Procurement + Solicitations Scraper v2")
    print(f"Start date: {args.start_date}  |  Dollar floor: ${MIN_AMOUNT:,}")
    print("=" * 65)

    ensure_dirs()

    usa_awards, sam_opps, sbir_awards, news_articles = [], [], [], []

    if run_federal:
        print(f"\n[1] USAspending.gov — Federal Awards (start={args.start_date})")
        usa_awards = USASpendingScraper().run(args.start_date, args.limit)

    if run_sam:
        print(f"\n[2] SAM.gov — Solicitations & Opportunities")
        sam_opps = SAMScraper().run(args.start_date, args.limit)

    if run_sbir:
        print(f"\n[3] SBIR.gov — R&D Solicitations & Awards")
        sbir_awards = SBIRScraper().run(args.limit)

    if run_news:
        print(f"\n[4] Google News RSS — State/Local Procurement Signals")
        news_articles = NewsScraper().run()

    # ── Cache fallback: if a live scraper returned 0 results, load from last cache ──
    # This prevents solicitations.json from being built with missing sources
    # when a scraper fails silently (network blip, API rate limit, missing key).
    def _load_cache(filename, key):
        path = PROCUREMENT_DIR / filename
        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)
                cached = data.get(key, [])
                print(f"  ↩ {filename}: loaded {len(cached)} cached records (live returned 0)")
                return cached
            except Exception as e:
                print(f"  ↩ {filename}: cache load failed — {e}")
        return []

    if not usa_awards and run_federal:
        usa_awards = _load_cache("federal_awards.json", "awards")
    if not sam_opps and run_sam:
        sam_opps = _load_cache("sam_opportunities.json", "opportunities")
    if not sbir_awards and run_sbir:
        sbir_awards = _load_cache("sbir_awards.json", "awards")
    if not news_articles and run_news:
        news_articles = _load_cache("news_signals.json", "articles")

    print(f"\n[5] Building unified solicitations.json...")
    sol_data = build_solicitations_json(usa_awards, sam_opps, sbir_awards, news_articles)
    unified  = sol_data["solicitations"]
    gz_data  = build_gray_zone_matches(unified)

    if not args.dry_run:
        # Always write solicitations.json and gray_zone_matches.json
        with open(PROCUREMENT_DIR / "solicitations.json", "w") as f:
            json.dump(sol_data, f, indent=2)
        with open(PROCUREMENT_DIR / "gray_zone_matches.json", "w") as f:
            json.dump(gz_data, f, indent=2)
        # Write per-source caches — always, even if empty (so cache is current)
        with open(PROCUREMENT_DIR / "federal_awards.json", "w") as f:
            json.dump({"awards": usa_awards, "scraped_at": now_iso, "count": len(usa_awards)}, f, indent=2)
        with open(PROCUREMENT_DIR / "sam_opportunities.json", "w") as f:
            json.dump({"opportunities": sam_opps, "scraped_at": now_iso, "count": len(sam_opps)}, f, indent=2)
        with open(PROCUREMENT_DIR / "sbir_awards.json", "w") as f:
            json.dump({"awards": sbir_awards, "scraped_at": now_iso, "count": len(sbir_awards)}, f, indent=2)
        with open(PROCUREMENT_DIR / "news_signals.json", "w") as f:
            json.dump({"articles": news_articles, "scraped_at": now_iso, "count": len(news_articles)}, f, indent=2)

    m = sol_data["meta"]
    print(f"\n{'=' * 65}")
    print(f"Complete  |  {m['total_solicitations']} total solicitations")
    print(f"  USAspending:  {m['by_source']['usaspending']:>5}  awards")
    print(f"  SAM.gov:      {m['by_source']['sam']:>5}  open solicitations")
    print(f"  SBIR.gov:     {m['by_source']['sbir']:>5}  R&D awards")
    print(f"  News signals: {m['by_source']['news']:>5}  state/local signals")
    print(f"  ⚠ Gray zone:  {m['gray_zone_count']:>5}  flagged entries")
    print(f"  ✓ Blue UAS:   {m['blue_uas_count']:>5}  trusted manufacturer hits")
    if not args.dry_run:
        print(f"  → data/procurement/solicitations.json")
        print(f"  → data/procurement/gray_zone_matches.json")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
