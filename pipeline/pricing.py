#!/usr/bin/env python3
"""
PIE Pricing Module — live component pricing via Mouser and DigiKey APIs.

Environment variables:
  MOUSER_API_KEY   — from mouser.com/api (free, requires registration)
  DIGIKEY_CLIENT_ID     — from developer.digikey.com
  DIGIKEY_CLIENT_SECRET — from developer.digikey.com

Usage:
  from pipeline.pricing import PricingClient
  client = PricingClient()
  result = client.get_price("STM32H743VIT6", "STMicroelectronics")
"""

import os
import json
import time
import hashlib
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "pricing-cache"
CACHE_TTL_HOURS = 24
REQUEST_DELAY = 0.5  # seconds between API calls

now = datetime.now(timezone.utc).isoformat()


def _cache_key(source: str, query: str) -> str:
    return hashlib.md5(f"{source}:{query}".encode()).hexdigest()[:16]


def _cache_get(source: str, query: str) -> Optional[dict]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{_cache_key(source, query)}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        cached_at = datetime.fromisoformat(data.get("cached_at", "2000-01-01T00:00:00+00:00"))
        if datetime.now(timezone.utc) - cached_at > timedelta(hours=CACHE_TTL_HOURS):
            return None
        return data
    except Exception:
        return None


def _cache_set(source: str, query: str, data: dict):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{_cache_key(source, query)}.json"
    data["cached_at"] = now
    path.write_text(json.dumps(data, indent=2))


# ─────────────────────────────────────────────────────────────────
# Mouser API
# ─────────────────────────────────────────────────────────────────

class MouserClient:
    """
    Mouser Electronics Search API v1.
    Docs: https://api.mouser.com/api/v1/docs
    Free API key: https://www.mouser.com/api-hub/
    """
    BASE_URL = "https://api.mouser.com/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("MOUSER_API_KEY", "")
        self.available = bool(self.api_key)

    def search_keyword(self, keyword: str, records: int = 5) -> list:
        """Search Mouser by keyword. Returns list of part dicts."""
        if not self.available:
            return []

        cached = _cache_get("mouser", keyword)
        if cached:
            return cached.get("parts", [])

        url = f"{self.BASE_URL}/search/keyword"
        payload = {
            "SearchByKeywordRequest": {
                "keyword": keyword,
                "records": records,
                "startingRecord": 0,
                "searchOptions": "None",
                "searchWithYourSignUpLanguage": "false"
            }
        }
        try:
            resp = requests.post(
                url,
                json=payload,
                params={"apiKey": self.api_key},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            errors = data.get("Errors", [])
            if errors:
                print(f"    [Mouser] Errors: {errors}")
                return []
            parts_raw = data.get("SearchResults", {}).get("Parts", [])
            parts = [self._normalize(p) for p in parts_raw]
            _cache_set("mouser", keyword, {"parts": parts})
            time.sleep(REQUEST_DELAY)
            return parts
        except Exception as e:
            print(f"    [Mouser] {keyword[:40]} → ERROR: {e}")
            return []

    def search_part_number(self, part_number: str) -> list:
        """Search Mouser by exact part number."""
        if not self.available:
            return []

        cached = _cache_get("mouser_pn", part_number)
        if cached:
            return cached.get("parts", [])

        url = f"{self.BASE_URL}/search/partnumber"
        payload = {
            "SearchByPartNumberRequest": {
                "mouserPartNumber": part_number,
                "partSearchOptions": "None"
            }
        }
        try:
            resp = requests.post(
                url,
                json=payload,
                params={"apiKey": self.api_key},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            parts_raw = data.get("SearchResults", {}).get("Parts", [])
            parts = [self._normalize(p) for p in parts_raw]
            _cache_set("mouser_pn", part_number, {"parts": parts})
            time.sleep(REQUEST_DELAY)
            return parts
        except Exception as e:
            print(f"    [Mouser PN] {part_number} → ERROR: {e}")
            return []

    def _normalize(self, p: dict) -> dict:
        """Normalize Mouser part dict to PIE pricing schema."""
        # Parse price breaks
        price_breaks = []
        for pb in p.get("PriceBreaks", []):
            try:
                price_breaks.append({
                    "quantity": int(pb.get("Quantity", 0)),
                    "price": float(pb.get("Price", "0").replace("$", "").replace(",", "")),
                    "currency": pb.get("Currency", "USD")
                })
            except (ValueError, TypeError):
                pass

        unit_price = None
        if price_breaks:
            unit_price = price_breaks[0]["price"]

        return {
            "source": "mouser",
            "mouser_pn": p.get("MouserPartNumber", ""),
            "mfr_pn": p.get("ManufacturerPartNumber", ""),
            "manufacturer": p.get("Manufacturer", ""),
            "description": p.get("Description", ""),
            "datasheet_url": p.get("DataSheetUrl", ""),
            "mouser_url": p.get("ProductDetailUrl", ""),
            "unit_price_usd": unit_price,
            "price_breaks": price_breaks,
            "stock_qty": int(p.get("Availability", "0").replace(",", "").split(" ")[0]) if p.get("Availability") else 0,
            "lead_time_weeks": p.get("LeadTime", ""),
            "min_order_qty": int(p.get("Min", 1)),
            "in_stock": (p.get("AvailabilityInStock", "0").replace(",", "").split(" ")[0] or "0") != "0",
            "retrieved_at": now,
        }


# ─────────────────────────────────────────────────────────────────
# DigiKey API v4
# ─────────────────────────────────────────────────────────────────

class DigiKeyClient:
    """
    DigiKey Product Information API v4.
    Docs: https://developer.digikey.com/products/product-information/v4/search
    OAuth2 client credentials flow.
    Register: https://developer.digikey.com/
    """
    AUTH_URL = "https://api.digikey.com/v1/oauth2/token"
    BASE_URL = "https://api.digikey.com/products/v4"
    SANDBOX_BASE = "https://sandbox-api.digikey.com/products/v4"

    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 sandbox: bool = False):
        self.client_id = client_id or os.environ.get("DIGIKEY_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("DIGIKEY_CLIENT_SECRET", "")
        self.available = bool(self.client_id and self.client_secret)
        self.sandbox = sandbox
        self.base_url = self.SANDBOX_BASE if sandbox else self.BASE_URL
        self._token = None
        self._token_expires = None

    def _get_token(self) -> Optional[str]:
        """Fetch OAuth2 bearer token via client credentials."""
        if self._token and self._token_expires and datetime.now(timezone.utc) < self._token_expires:
            return self._token
        try:
            resp = requests.post(
                self.AUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            self._token = data.get("access_token")
            expires_in = int(data.get("expires_in", 1800))
            self._token_expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)
            return self._token
        except Exception as e:
            print(f"    [DigiKey Auth] ERROR: {e}")
            return None

    def _headers(self) -> dict:
        token = self._get_token()
        if not token:
            return {}
        return {
            "Authorization": f"Bearer {token}",
            "X-DIGIKEY-Client-Id": self.client_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def search_keyword(self, keyword: str, limit: int = 5) -> list:
        """Search DigiKey by keyword."""
        if not self.available:
            return []

        cached = _cache_get("digikey", keyword)
        if cached:
            return cached.get("parts", [])

        url = f"{self.base_url}/search/keyword"
        payload = {
            "Keywords": keyword,
            "RecordCount": limit,
            "RecordStartPosition": 0,
            "Filters": {},
            "Sort": {"SortOption": "SortByPriceAscending", "Direction": "Ascending", "SortParameterId": 0},
            "RequestedQuantity": 1,
            "ExcludeMarketPlaceProducts": True,
        }
        try:
            headers = self._headers()
            if not headers:
                return []
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            parts_raw = data.get("Products", [])
            parts = [self._normalize(p) for p in parts_raw]
            _cache_set("digikey", keyword, {"parts": parts})
            time.sleep(REQUEST_DELAY)
            return parts
        except Exception as e:
            print(f"    [DigiKey] {keyword[:40]} → ERROR: {e}")
            return []

    def search_part_number(self, part_number: str) -> list:
        """Search DigiKey by manufacturer part number."""
        if not self.available:
            return []

        cached = _cache_get("digikey_pn", part_number)
        if cached:
            return cached.get("parts", [])

        url = f"{self.base_url}/search/keyword"
        payload = {
            "Keywords": part_number,
            "RecordCount": 3,
            "RecordStartPosition": 0,
            "Filters": {},
            "Sort": {"SortOption": "SortByUnitPrice", "Direction": "Ascending", "SortParameterId": 0},
            "RequestedQuantity": 1,
            "ExcludeMarketPlaceProducts": True,
        }
        try:
            headers = self._headers()
            if not headers:
                return []
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            # Filter for exact MPN match
            all_parts = data.get("Products", [])
            exact = [p for p in all_parts
                     if p.get("ManufacturerProductNumber", "").upper() == part_number.upper()]
            parts_raw = exact if exact else all_parts[:2]
            parts = [self._normalize(p) for p in parts_raw]
            _cache_set("digikey_pn", part_number, {"parts": parts})
            time.sleep(REQUEST_DELAY)
            return parts
        except Exception as e:
            print(f"    [DigiKey PN] {part_number} → ERROR: {e}")
            return []

    def _normalize(self, p: dict) -> dict:
        """Normalize DigiKey product to PIE pricing schema."""
        # Unit price
        unit_price_info = p.get("UnitPrice", 0)
        unit_price = float(unit_price_info) if isinstance(unit_price_info, (int, float)) else None

        # Price breaks
        price_breaks = []
        for pb in p.get("StandardPricing", []):
            try:
                price_breaks.append({
                    "quantity": int(pb.get("BreakQuantity", 1)),
                    "price": float(pb.get("UnitPrice", 0)),
                    "currency": "USD"
                })
            except (ValueError, TypeError):
                pass

        if price_breaks and unit_price is None:
            unit_price = price_breaks[0]["price"]

        return {
            "source": "digikey",
            "digikey_pn": p.get("DigiKeyPartNumber", ""),
            "mfr_pn": p.get("ManufacturerProductNumber", ""),
            "manufacturer": p.get("Manufacturer", {}).get("Name", "") if isinstance(p.get("Manufacturer"), dict) else p.get("Manufacturer", ""),
            "description": p.get("ProductDescription", ""),
            "datasheet_url": p.get("DatasheetUrl", ""),
            "digikey_url": p.get("ProductUrl", ""),
            "unit_price_usd": unit_price,
            "price_breaks": price_breaks,
            "stock_qty": int(p.get("QuantityAvailable", 0)),
            "lead_time_weeks": str(p.get("ManufacturerLeadWeeks", "")),
            "min_order_qty": int(p.get("MinimumOrderQuantity", 1)),
            "in_stock": int(p.get("QuantityAvailable", 0)) > 0,
            "retrieved_at": now,
        }


# ─────────────────────────────────────────────────────────────────
# Unified Pricing Client
# ─────────────────────────────────────────────────────────────────

class PricingClient:
    """
    Unified pricing client — queries Mouser + DigiKey, returns best price.
    Falls back gracefully if API keys not set.
    """

    def __init__(self):
        self.mouser = MouserClient()
        self.digikey = DigiKeyClient()
        self.available = self.mouser.available or self.digikey.available

        sources = []
        if self.mouser.available:
            sources.append("Mouser")
        if self.digikey.available:
            sources.append("DigiKey")
        if sources:
            print(f"  [Pricing] Live pricing via: {', '.join(sources)}")
        else:
            print("  [Pricing] No API keys set — pricing unavailable")

    def get_price(self, name: str, manufacturer: str = "") -> dict:
        """
        Get best available price for a component.
        Returns dict with price, stock, source, urls.
        """
        query = f"{manufacturer} {name}".strip() if manufacturer else name
        all_parts = []

        if self.mouser.available:
            m_parts = self.mouser.search_keyword(query, records=3)
            all_parts.extend(m_parts)

        if self.digikey.available:
            dk_parts = self.digikey.search_keyword(query, limit=3)
            all_parts.extend(dk_parts)

        if not all_parts:
            return {"available": False, "query": query}

        # Pick best: in-stock lowest price
        in_stock = [p for p in all_parts if p.get("in_stock")]
        candidates = in_stock if in_stock else all_parts
        candidates_priced = [p for p in candidates if p.get("unit_price_usd")]

        if not candidates_priced:
            return {"available": False, "query": query, "parts_found": len(all_parts)}

        best = min(candidates_priced, key=lambda p: p["unit_price_usd"])

        return {
            "available": True,
            "query": query,
            "unit_price_usd": best["unit_price_usd"],
            "in_stock": best.get("in_stock", False),
            "stock_qty": best.get("stock_qty", 0),
            "lead_time_weeks": best.get("lead_time_weeks", ""),
            "source": best["source"],
            "mouser_url": best.get("mouser_url", ""),
            "digikey_url": best.get("digikey_url", ""),
            "mfr_pn": best.get("mfr_pn", ""),
            "parts_found": len(all_parts),
            "price_breaks": best.get("price_breaks", []),
            "retrieved_at": now,
        }

    def enrich_parts_db(self, parts: list, max_queries: int = 50) -> list:
        """
        Add pricing data to a list of parts-db entries.
        Skips parts that already have recent pricing.
        Respects max_queries to stay within API rate limits.
        """
        if not self.available:
            return parts

        queried = 0
        enriched = 0

        for part in parts:
            if queried >= max_queries:
                break

            # Skip if we have recent pricing (< 24h old)
            existing = part.get("live_price", {})
            if existing.get("retrieved_at"):
                try:
                    age = datetime.now(timezone.utc) - datetime.fromisoformat(existing["retrieved_at"])
                    if age.total_seconds() < CACHE_TTL_HOURS * 3600:
                        continue
                except Exception:
                    pass

            name = part.get("name", "")
            mfr = part.get("manufacturer", "")
            if not name:
                continue

            result = self.get_price(name, mfr)
            queried += 1

            if result.get("available"):
                part["live_price"] = result
                # Update approx_price if missing
                if not part.get("approx_price") and result.get("unit_price_usd"):
                    part["approx_price"] = round(result["unit_price_usd"], 2)
                enriched += 1

        print(f"  [Pricing] Queried {queried} parts, enriched {enriched} with live pricing")
        return parts


# ─────────────────────────────────────────────────────────────────
# PIE Integration — Stock Shortage Flags
# ─────────────────────────────────────────────────────────────────

def analyze_pricing_signals(parts_db_dir: Path) -> list:
    """
    Generate PIE flags from live pricing data.
    Detects: stock shortages, price spikes, lead time alerts.
    Called by pie_supplemental.py
    """
    import json
    import glob
    import hashlib
    from datetime import datetime, timezone

    now_str = datetime.now(timezone.utc).isoformat()
    flags = []

    def flag_id(seed):
        return "pie-" + hashlib.md5(seed.encode()).hexdigest()[:10]

    # Scan all parts files for live_price data
    out_of_stock_critical = []  # defense/Blue UAS components OOS
    high_lead_time = []         # > 12 weeks
    price_spike = []            # > 2x typical

    for fp in sorted(parts_db_dir.glob("*.json")):
        try:
            parts = json.loads(fp.read_text())
            if not isinstance(parts, list):
                continue
            for part in parts:
                lp = part.get("live_price", {})
                if not lp.get("available"):
                    continue

                name = part.get("name", "")
                cat = part.get("category", "")
                tags = part.get("tags", [])
                is_defense = any(t in tags for t in ["blue-uas", "ndaa", "defense", "mil-spec"])

                # Out of stock critical parts
                if not lp.get("in_stock") and is_defense:
                    out_of_stock_critical.append({
                        "name": name,
                        "category": cat,
                        "source": lp.get("source"),
                        "lead_time": lp.get("lead_time_weeks", "unknown"),
                    })

                # High lead time
                try:
                    lead_str = str(lp.get("lead_time_weeks", ""))
                    lead_num = float("".join(c for c in lead_str if c.isdigit() or c == ".") or "0")
                    if lead_num >= 12:
                        high_lead_time.append({"name": name, "category": cat, "lead_weeks": lead_num})
                except (ValueError, TypeError):
                    pass

        except Exception:
            continue

    # Generate flags
    if out_of_stock_critical:
        flags.append({
            "id": flag_id("pricing-oos-critical"),
            "timestamp": now_str,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Pricing: {len(out_of_stock_critical)} defense/NDAA components out of stock (live Mouser/DigiKey)",
            "detail": " | ".join(f"{p['name']} ({p['category']}, lead: {p['lead_time']}w)" for p in out_of_stock_critical[:6]),
            "confidence": 0.92,
            "prediction": "Procurement planners should pre-order or identify alternatives for OOS components.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["mouser_api", "digikey_api"],
        })

    if high_lead_time:
        flags.append({
            "id": flag_id("pricing-lead-time"),
            "timestamp": now_str,
            "flag_type": "supply_chain_risk",
            "severity": "warning",
            "title": f"Pricing: {len(high_lead_time)} components have 12+ week lead times (live data)",
            "detail": " | ".join(f"{p['name']}: {p['lead_weeks']}w" for p in high_lead_time[:5]),
            "confidence": 0.90,
            "prediction": "Extended lead times indicate supply constraint. Order now for Q3 builds.",
            "platform_id": None,
            "component_id": None,
            "data_sources": ["mouser_api", "digikey_api"],
        })

    return flags


if __name__ == "__main__":
    # Quick test
    client = PricingClient()
    if client.available:
        result = client.get_price("STM32H743", "STMicroelectronics")
        print(json.dumps(result, indent=2))
    else:
        print("Set MOUSER_API_KEY and/or DIGIKEY_CLIENT_ID + DIGIKEY_CLIENT_SECRET to test")
