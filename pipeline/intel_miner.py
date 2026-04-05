#!/usr/bin/env python3
"""
Intel News Miner — mines RSS feeds from 7 defense/drone news sources
and appends new articles to intel_articles.json in the Forge repo.

Sources: militarnyi, breakingdefense, dronelife, defensenews,
         thewarzone, unmannedairspace, defensescoop

No external dependencies — stdlib only.
"""

import json
import xml.etree.ElementTree as ET
import urllib.request
import hashlib
import re
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

OUT_FILE = Path("data/intel_articles_new.json")

SOURCES = [
    {"id": "defensescoop",    "rss": "https://defensescoop.com/feed/",                                           "type": "defense"},
    {"id": "breakingdefense", "rss": "https://breakingdefense.com/feed/",                                        "type": "defense"},
    {"id": "defensenews",     "rss": "https://www.defensenews.com/arc/outboundfeeds/rss/?rss=defense-news",      "type": "defense"},
    {"id": "twz",             "rss": "https://www.thedrive.com/feed/the-war-zone",                               "type": "defense"},
    {"id": "dronelife",       "rss": "https://dronelife.com/feed/",                                              "type": "commercial"},
    {"id": "unmannedairspace","rss": "https://www.unmannedairspace.info/feed/",                                   "type": "commercial"},
    {"id": "militarnyi",      "rss": "https://mil.in.ua/en/feed/",                                               "type": "defense"},
]

DRONE_KW = [
    "drone","uas","uav","unmanned","quadcopter","fpv","blue uas","ndaa",
    "dji","skydio","autel","anzu","replicator","switchblade","loitering",
    "counter-uas","c-uas","anti-drone","betaflight","ardupilot","mavlink",
    "flir","thermal","payload","ukraine","russia","iran","hamas","hezbollah",
]

COMPANIES = [
    "skydio","autel","anzu","dji","flir","teledyne","l3harris","aerovironment",
    "textron","shield ai","joby","archer","wisk","firestorm","modalai","auterion",
    "skycutter","napatree","teal drones","quantum systems","wingtra","halo aeronautics",
    "ascent aerosystems","griffon aerospace","nokturnal","neros","titan dynamics",
    "orqa","fatshark","caddx","runcam","trellisware","silvus","persistent systems",
    "domo tactical","cogito","specta","skyrover","knowact","unusual machines",
]

PROGRAMS = [
    "replicator","blue uas","suas","switchblade","puma","rq-20","mq-9","mq-1",
    "drone dominance","ndaa","itar","fcc","diu","afwerx","soar","brinc",
    "ussocom","socom","army futures","air force research",
]

TAGS = [
    "loitering munition","one-way attack","fpv","counter-uas","supply chain",
    "gray zone","blue uas","ndaa","firmware","thermal","eo/ir","mesh","swarm",
    "autonomy","ai","ukraine","russia","iran","israel","china",
]

REGIONS = {
    "Ukraine":  ["ukraine","ukrainian","kyiv"],
    "Russia":   ["russia","russian","moscow","kremlin"],
    "Iran":     ["iran","iranian","tehran"],
    "Israel":   ["israel","israeli","idf","gaza"],
    "China":    ["china","chinese","pla","beijing"],
    "NATO":     ["nato"],
    "UK":       ["british","britain"," mod "],
    "Germany":  ["germany","german","bundeswehr"],
    "Australia":["australia","adf"],
    "Japan":    ["japan","japanese","jsdf"],
    "US":       ["pentagon","dod"," army ","air force","usmc","u.s. "],
}


def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PIE-IntelMiner/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    fetch error: {e}")
        return None


def parse_date(raw):
    if not raw:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for fmt in ["%a, %d %b %Y %H:%M:%S %z","%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z","%Y-%m-%d"]:
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    m = re.search(r"\d{4}-\d{2}-\d{2}", raw)
    return m.group() if m else datetime.now(timezone.utc).strftime("%Y-%m-%d")


def aid(url):
    return hashlib.md5(url.encode()).hexdigest()[:12]


def is_relevant(title, desc):
    text = (title + " " + desc).lower()
    return any(k in text for k in DRONE_KW)


def extract_entities(title, body):
    text = (title + " " + body).lower()
    return {
        "companies":     sorted({c.title() for c in COMPANIES if c in text})[:10],
        "programs":      sorted({p.upper() if p == p.upper() else p.title() for p in PROGRAMS if p in text})[:8],
        "platforms":     [],
        "dollar_amounts": re.findall(r"\$[\d,.]+\s*(?:million|billion|M|B|K)\b", title+" "+body, re.I)[:5],
        "tags":          sorted({t for t in TAGS if t in text})[:10],
    }


def guess_region(title, body):
    text = (title + " " + body).lower()
    for region, kws in REGIONS.items():
        if any(k in text for k in kws):
            return region
    return "US"


def guess_type(title, site_type):
    t = title.lower()
    if any(w in t for w in ["contract","award","billion","million","purchase"]):
        return "financial"
    if any(w in t for w in ["ukraine","russia","iran","israel","attack","strike","war"]):
        return "defense"
    return site_type


def scrape(source, existing_urls):
    print(f"  [{source['id']:20s}]", end=" ")
    raw = fetch_rss(source["rss"])
    if not raw:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"parse error: {e}")
        return []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = []
    for item in root.findall(".//item"):
        url = (item.findtext("link") or "").strip()
        if not url or url in existing_urls:
            continue
        title = (item.findtext("title") or "").strip()
        desc = re.sub(r"<[^>]+>", "", item.findtext("description") or "")
        if not is_relevant(title, desc):
            continue
        ent = extract_entities(title, desc)
        out.append({
            "title":        title,
            "pub_date":     parse_date(item.findtext("pubDate") or ""),
            "author":       (item.findtext("author") or "").strip(),
            "body_text":    desc[:2000],
            "summary":      desc[:300],
            "url":          url,
            "site":         source["id"],
            "scraped_date": today,
            "entities":     ent,
            "aid":          aid(url),
            "article_type": guess_type(title, source["type"]),
            "region":       guess_region(title, desc),
        })
        existing_urls.add(url)
    print(f"{len(out)} new")
    return out


def main():
    print("=" * 50)
    print(f"  Intel News Miner  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 50)

    forge_path = os.environ.get("FORGE_INTEL_PATH", "")
    existing = []
    existing_urls = set()
    if forge_path and Path(forge_path).exists():
        try:
            existing = json.load(open(forge_path))
            existing_urls = {a.get("url","") for a in existing}
            print(f"  Loaded {len(existing)} existing articles from Forge")
        except Exception as e:
            print(f"  Warning: {e}")

    new_arts = []
    for src in SOURCES:
        new_arts.extend(scrape(src, existing_urls))

    print(f"\n  Total new: {len(new_arts)}")
    if not new_arts:
        print("  Nothing new — skipping write")
        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUT_FILE.write_text(json.dumps({"new_count": 0}))
        return

    merged = new_arts + existing
    seen, deduped = set(), []
    for a in merged:
        k = a.get("url") or a.get("aid")
        if k and k not in seen:
            seen.add(k)
            deduped.append(a)
    deduped.sort(key=lambda x: x.get("pub_date",""), reverse=True)
    deduped = deduped[:1500]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(deduped, indent=2, ensure_ascii=False))
    print(f"  ✓ {len(deduped)} articles written to {OUT_FILE}")

    sites = Counter(a.get("site","") for a in new_arts)
    for s, n in sorted(sites.items(), key=lambda x: -x[1]):
        print(f"    {s:25s} {n}")


if __name__ == "__main__":
    main()
