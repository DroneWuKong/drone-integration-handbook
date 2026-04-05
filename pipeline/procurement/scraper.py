#!/usr/bin/env python3
"""
PIE Procurement Scraper — discovers drone/UAS procurement across
federal, state, and local government using public data sources.

Data Sources:
  1. USAspending.gov API (free, no auth) — federal contracts & grants
  2. SAM.gov Opportunities API (free, API key optional for search) — solicitations & awards
  3. News scraper — local news coverage of agency drone program launches

Outputs:
  data/procurement/federal_awards.json   — USAspending results
  data/procurement/sam_opportunities.json — SAM.gov solicitations/awards
  data/procurement/news_signals.json     — news-sourced procurement signals
  data/procurement/gray_zone_matches.json — cross-ref with gray zone entities

Usage:
  python pipeline/procurement/scraper.py [--full] [--news-only] [--federal-only]

Environment variables (optional):
  SAM_API_KEY    — SAM.gov API key (free at api.data.gov) for contract awards
  NEWS_API_KEY   — NewsAPI key for broader news coverage
"""

import json
import time
import hashlib
import argparse
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install: pip install requests --break-system-packages")
    exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROCUREMENT_DIR = REPO_ROOT / "data" / "procurement"
GRAYZONE_DIR = REPO_ROOT / "data" / "grayzone"

now = datetime.now(timezone.utc).isoformat()

# Rate limiting
REQUEST_DELAY = 1.0  # seconds between API calls


def ensure_dirs():
    PROCUREMENT_DIR.mkdir(parents=True, exist_ok=True)


def proc_id(seed: str) -> str:
    return "proc-" + hashlib.md5(seed.encode()).hexdigest()[:10]


# ──────────────────────────────────────────
# 1. USAspending.gov — Federal Awards
# ──────────────────────────────────────────

class USASpendingScraper:
    """
    Searches USAspending.gov for drone/UAS-related federal awards.
    API docs: https://api.usaspending.gov/
    No authentication required. Free. Rate limited.
    """

    BASE_URL = "https://api.usaspending.gov/api/v2"

    # Search terms that capture UAS procurement
    KEYWORDS = [
        "unmanned aircraft system",
        "unmanned aerial system",
        "UAS",
        "sUAS",
        "small unmanned aircraft",
        "drone",
        "quadcopter",
        "Blue UAS",
    ]

    # Gray zone vendor names to flag
    GRAY_ZONE_VENDORS = [
        "anzu robotics",
        "anzu",
        "cogito tech",
        "specta",
        "skyrover",
        "knowact",
        "autel robotics",
        "autel",
        "dji",
        "dajiang",
    ]

    # NAICS codes relevant to UAS
    NAICS_CODES = [
        "334511",  # Search, detection, navigation instruments
        "336411",  # Aircraft manufacturing
        "334220",  # Radio/TV broadcast equipment
        "334290",  # Other communications equipment
        "541715",  # R&D in physical/engineering/life sciences
    ]

    def __init__(self):
        self.results = []

    def search_awards_by_keyword(self, keyword: str, start_date: str = "2023-01-01",
                                  end_date: Optional[str] = None, limit: int = 50) -> list:
        """Search federal awards by keyword."""
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        url = f"{self.BASE_URL}/search/spending_by_award/"
        payload = {
            "filters": {
                "keywords": [keyword],
                "time_period": [
                    {"start_date": start_date, "end_date": end_date}
                ],
                "award_type_codes": [
                    "A", "B", "C", "D",   # Contracts
                    "02", "03", "04", "05", # Grants
                ]
            },
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "Description",
                "Start Date",
                "End Date",
                "Awarding Agency",
                "Awarding Sub Agency",
                "Award Type",
                "recipient_id",
                "internal_id",
                "generated_internal_id",
            ],
            "page": 1,
            "limit": limit,
            "sort": "Award Amount",
            "order": "desc",
            "subawards": False,
        }

        try:
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            print(f"    [{keyword[:30]:30s}] → {len(results)} awards (of {data.get('page_metadata', {}).get('total', '?')} total)")
            return results
        except requests.exceptions.RequestException as e:
            print(f"    [{keyword[:30]:30s}] → ERROR: {e}")
            return []

    def search_all_keywords(self, start_date: str = "2023-01-01", limit_per: int = 25) -> list:
        """Search all UAS-related keywords and deduplicate."""
        all_results = []
        seen_ids = set()

        for kw in self.KEYWORDS:
            results = self.search_awards_by_keyword(kw, start_date=start_date, limit=limit_per)
            for r in results:
                award_id = r.get("Award ID") or r.get("internal_id") or r.get("generated_internal_id")
                if award_id and award_id not in seen_ids:
                    seen_ids.add(award_id)
                    all_results.append(r)
            time.sleep(REQUEST_DELAY)

        print(f"  USAspending: {len(all_results)} unique awards across {len(self.KEYWORDS)} keyword searches")
        return all_results

    def flag_gray_zone_matches(self, awards: list) -> list:
        """Flag any awards to gray zone vendors."""
        matches = []
        for award in awards:
            recipient = (award.get("Recipient Name") or "").lower()
            description = (award.get("Description") or "").lower()

            for vendor in self.GRAY_ZONE_VENDORS:
                if vendor in recipient or vendor in description:
                    matches.append({
                        "id": proc_id(f"usa-{award.get('Award ID', '')}-{vendor}"),
                        "source": "usaspending",
                        "award_id": award.get("Award ID"),
                        "recipient": award.get("Recipient Name"),
                        "amount": award.get("Award Amount"),
                        "description": award.get("Description"),
                        "agency": award.get("Awarding Agency"),
                        "sub_agency": award.get("Awarding Sub Agency"),
                        "start_date": award.get("Start Date"),
                        "matched_vendor": vendor,
                        "flag_type": "gray_zone_vendor_match",
                        "severity": "critical" if vendor in ("dji", "anzu", "autel") else "warning",
                        "scraped_at": now,
                    })
                    break

        if matches:
            print(f"  ⚠ GRAY ZONE MATCHES: {len(matches)} federal awards to flagged vendors")
        return matches


# ──────────────────────────────────────────
# 2. SAM.gov — Opportunities & Solicitations
# ──────────────────────────────────────────

class SAMScraper:
    """
    Searches SAM.gov for UAS-related contract opportunities.
    Opportunities search: no API key required.
    Contract awards: requires free API key from api.data.gov.
    """

    OPPORTUNITIES_URL = "https://api.sam.gov/prod/opportunities/v2/search"
    AWARDS_URL = "https://api.sam.gov/contract-awards/v1/search"

    UAS_KEYWORDS = [
        "unmanned aircraft",
        "UAS",
        "sUAS",
        "drone",
        "Blue UAS",
        "unmanned aerial",
    ]

    # NAICS codes for UAS
    NAICS_CODES = ["334511", "336411"]

    # PSC (Product Service Codes) for aircraft/UAS
    PSC_CODES = [
        "1550",  # Unmanned aircraft
        "1510",  # Aircraft, fixed wing
        "1520",  # Aircraft, rotary wing
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SAM_API_KEY", "")

    def search_opportunities(self, keyword: str, posted_from: str = "01/01/2024",
                              limit: int = 25) -> list:
        """Search SAM.gov contract opportunities (no API key required)."""
        params = {
            "api_key": self.api_key,
            "keyword": keyword,
            "postedFrom": posted_from,
            "limit": limit,
            "offset": 0,
        }

        if not self.api_key:
            print(f"    [{keyword:20s}] → SKIPPED (no SAM_API_KEY — get free key at api.data.gov)")
            return []

        try:
            resp = requests.get(self.OPPORTUNITIES_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            opps = data.get("opportunitiesData", [])
            print(f"    [{keyword:20s}] → {len(opps)} opportunities")
            return opps
        except requests.exceptions.RequestException as e:
            print(f"    [{keyword:20s}] → ERROR: {e}")
            return []

    def search_contract_awards(self, keyword: str = None, naics: str = None,
                                 start_date: str = "2023-01-01", limit: int = 25) -> list:
        """Search SAM.gov contract awards (requires API key)."""
        if not self.api_key:
            print(f"    Contract awards → SKIPPED (no SAM_API_KEY)")
            return []

        params = {
            "api_key": self.api_key,
            "lastModifiedDate": f"[{start_date.replace('-', '/')},]",
            "limit": limit,
        }
        if naics:
            params["naicsCode"] = naics
        if keyword:
            params["descriptionOfContractRequirement"] = keyword

        try:
            resp = requests.get(self.AWARDS_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            awards = data.get("awardSummary", [])
            search_desc = keyword or f"NAICS:{naics}"
            print(f"    [{search_desc:30s}] → {len(awards)} contract awards")
            return awards
        except requests.exceptions.RequestException as e:
            print(f"    [contract awards] → ERROR: {e}")
            return []

    def search_all(self, posted_from: str = "01/01/2024") -> dict:
        """Run all SAM.gov searches."""
        all_opportunities = []
        all_awards = []
        seen_ids = set()

        # Search opportunities by keyword
        for kw in self.UAS_KEYWORDS:
            opps = self.search_opportunities(kw, posted_from=posted_from)
            for opp in opps:
                opp_id = opp.get("noticeId", "")
                if opp_id not in seen_ids:
                    seen_ids.add(opp_id)
                    all_opportunities.append(opp)
            time.sleep(REQUEST_DELAY)

        # Search contract awards by NAICS
        for naics in self.NAICS_CODES:
            awards = self.search_contract_awards(naics=naics)
            all_awards.extend(awards)
            time.sleep(REQUEST_DELAY)

        print(f"  SAM.gov: {len(all_opportunities)} opportunities, {len(all_awards)} contract awards")
        return {
            "opportunities": all_opportunities,
            "contract_awards": all_awards,
        }


# ──────────────────────────────────────────
# 3. News Signal Scraper
# ──────────────────────────────────────────

class NewsScraper:
    """
    Scrapes Google News RSS for local agency drone procurement announcements.
    No API key required — uses RSS feeds.
    """

    # Search queries designed to surface procurement announcements
    QUERIES = [
        "police department drone program launch",
        "sheriff drone purchase",
        "fire department drone procurement",
        "city council drone purchase approved",
        "police drone Anzu Raptor",
        "police drone Autel",
        "police drone Skydio",
        "public safety drone grant",
        "SOAR grant drone",
        "drone program first responder",
    ]

    GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    def search_query(self, query: str, max_results: int = 10) -> list:
        """Search Google News RSS for a query."""
        import xml.etree.ElementTree as ET

        url = self.GOOGLE_NEWS_RSS.format(query=query.replace(" ", "+"))
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "PIE-Procurement-Scanner/1.0"})
            resp.raise_for_status()

            root = ET.fromstring(resp.content)
            items = root.findall(".//item")

            results = []
            for item in items[:max_results]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")
                source = item.findtext("source", "")

                results.append({
                    "title": title,
                    "url": link,
                    "published": pub_date,
                    "source": source,
                    "query": query,
                })

            print(f"    [{query[:40]:40s}] → {len(results)} articles")
            return results
        except Exception as e:
            print(f"    [{query[:40]:40s}] → ERROR: {e}")
            return []

    def search_all(self, max_per_query: int = 5) -> list:
        """Run all news searches and deduplicate."""
        all_results = []
        seen_urls = set()

        for query in self.QUERIES:
            results = self.search_query(query, max_results=max_per_query)
            for r in results:
                url = r.get("url", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(r)
            time.sleep(REQUEST_DELAY)

        print(f"  News: {len(all_results)} unique articles across {len(self.QUERIES)} queries")
        return all_results

    def flag_gray_zone_mentions(self, articles: list) -> list:
        """Flag articles mentioning gray zone vendors."""
        gray_terms = ["anzu", "raptor t", "autel", "evo max", "cogito", "specta", "skyrover"]
        matches = []

        for article in articles:
            title_lower = article.get("title", "").lower()
            for term in gray_terms:
                if term in title_lower:
                    matches.append({
                        "id": proc_id(f"news-{article.get('url', '')}"),
                        "source": "news",
                        "title": article.get("title"),
                        "url": article.get("url"),
                        "published": article.get("published"),
                        "news_source": article.get("source"),
                        "matched_term": term,
                        "flag_type": "gray_zone_news_mention",
                        "severity": "info",
                        "scraped_at": now,
                    })
                    break

        if matches:
            print(f"  ⚠ GRAY ZONE NEWS: {len(matches)} articles mentioning flagged vendors")
        return matches


# ──────────────────────────────────────────
# 4. Cross-reference with Gray Zone Entities
# ──────────────────────────────────────────

def cross_reference_procurement(federal_awards: list, gray_zone_matches: list,
                                  news_matches: list) -> dict:
    """
    Merge all procurement signals and generate summary for PIE.
    """
    summary = {
        "generated_at": now,
        "federal_awards_total": len(federal_awards),
        "gray_zone_federal_matches": len(gray_zone_matches),
        "news_signals_total": len(news_matches),
        "gray_zone_news_mentions": len(news_matches),
        "all_gray_zone_signals": gray_zone_matches + news_matches,
        "vendors_flagged": list(set(
            m.get("matched_vendor", m.get("matched_term", ""))
            for m in gray_zone_matches + news_matches
        )),
    }

    return summary


# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PIE Procurement Scraper")
    parser.add_argument("--full", action="store_true", help="Run all scrapers")
    parser.add_argument("--federal-only", action="store_true", help="USAspending only")
    parser.add_argument("--news-only", action="store_true", help="News scraper only")
    parser.add_argument("--sam-only", action="store_true", help="SAM.gov only")
    parser.add_argument("--start-date", default="2023-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=25, help="Results per search")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    args = parser.parse_args()

    # Default to full if no specific flag
    run_federal = args.full or args.federal_only or not (args.news_only or args.sam_only)
    run_sam = args.full or args.sam_only
    run_news = args.full or args.news_only

    print("=" * 60)
    print("PIE Procurement Scraper")
    print("=" * 60)

    ensure_dirs()

    federal_awards = []
    gray_zone_matches = []
    sam_data = {"opportunities": [], "contract_awards": []}
    news_articles = []
    news_matches = []

    # 1. USAspending
    if run_federal:
        print("\n[1] USAspending.gov — Federal Awards")
        usa = USASpendingScraper()
        federal_awards = usa.search_all_keywords(start_date=args.start_date, limit_per=args.limit)
        gray_zone_matches = usa.flag_gray_zone_matches(federal_awards)

    # 2. SAM.gov
    if run_sam:
        print("\n[2] SAM.gov — Opportunities & Awards")
        sam = SAMScraper()
        sam_data = sam.search_all(posted_from=args.start_date.replace("-", "/"))

    # 3. News
    if run_news:
        print("\n[3] News — Agency Drone Procurement Signals")
        news = NewsScraper()
        news_articles = news.search_all(max_per_query=args.limit)
        news_matches = news.flag_gray_zone_mentions(news_articles)

    # 4. Cross-reference
    print("\n[4] Cross-referencing with Gray Zone entities...")
    summary = cross_reference_procurement(federal_awards, gray_zone_matches, news_matches)

    # Write outputs
    if not args.dry_run:
        if federal_awards:
            with open(PROCUREMENT_DIR / "federal_awards.json", "w") as f:
                json.dump({"awards": federal_awards, "scraped_at": now, "count": len(federal_awards)}, f, indent=2)

        if sam_data["opportunities"] or sam_data["contract_awards"]:
            with open(PROCUREMENT_DIR / "sam_opportunities.json", "w") as f:
                json.dump({"data": sam_data, "scraped_at": now}, f, indent=2)

        if news_articles:
            with open(PROCUREMENT_DIR / "news_signals.json", "w") as f:
                json.dump({"articles": news_articles, "scraped_at": now, "count": len(news_articles)}, f, indent=2)

        with open(PROCUREMENT_DIR / "gray_zone_matches.json", "w") as f:
            json.dump(summary, f, indent=2)

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Procurement Scraper — Complete")
    print(f"{'=' * 60}")
    print(f"  Federal awards found:      {len(federal_awards)}")
    print(f"  SAM.gov opportunities:     {len(sam_data['opportunities'])}")
    print(f"  SAM.gov contract awards:   {len(sam_data['contract_awards'])}")
    print(f"  News articles:             {len(news_articles)}")
    print(f"  Gray zone vendor matches:  {len(gray_zone_matches)}")
    print(f"  Gray zone news mentions:   {len(news_matches)}")
    if summary.get("vendors_flagged"):
        print(f"  Vendors flagged:           {', '.join(summary['vendors_flagged'])}")
    if not args.dry_run:
        print(f"  Output: {PROCUREMENT_DIR}/")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
