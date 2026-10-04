"""Autonomous, reproducible evidence research and deterministic adjudication.

The model may collect evidence, but it never decides publication policy.  This
module deliberately supports a complete software-only path so CI can exercise
the same planning, packet validation, adjudication, forecasting and recovery
logic used by a live Responses API provider.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import ipaddress
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit

SCHEMA_VERSION = 1
ROLES = ("researcher", "verifier")
CONCLUSIONS = {"supports", "partially-supports", "contradicts", "insufficient"}
SOURCE_CLASSES = {
    "controlling-authority", "government-guidance", "standard", "manufacturer",
    "peer-reviewed", "independent-technical", "field-observation", "other",
}
PUBLICATION_STATES = {
    "primary-source-supported", "independently-reproduced", "software-tested",
    "field-observed", "corroborated", "not-a-claim", "abstained",
    "contradicted", "exception",
}
NUMBER = re.compile(r"(?<![a-z])[-+]?\d+(?:[.,]\d+)*(?:e[-+]?\d+)?", re.I)

CLAIM_POLICIES = {
    "administrative": {"risk": "low", "min_sources": 0, "auto_publish": True},
    "factual": {"risk": "medium", "min_sources": 1, "auto_publish": True},
    "configuration": {"risk": "medium", "min_sources": 1, "auto_publish": True},
    "commercial": {"risk": "medium", "min_sources": 1, "auto_publish": True},
    "calculation": {"risk": "medium", "min_sources": 1, "auto_publish": True, "reproduce": True},
    "performance": {"risk": "high", "min_sources": 2, "auto_publish": True},
    "compatibility": {"risk": "high", "min_sources": 2, "auto_publish": True},
    "regulatory": {"risk": "high", "min_sources": 1, "auto_publish": True, "authority": True},
    "safety": {"risk": "critical", "min_sources": 2, "auto_publish": False},
    "recommendation": {"risk": "critical", "min_sources": 2, "auto_publish": False, "alternatives": True},
}

DEFAULT_AUTHORITY_DOMAINS = (
    "faa.gov", "ecfr.gov", "govinfo.gov", "federalregister.gov", "fcc.gov",
    "nist.gov", "cisa.gov", "ntia.gov", "itu.int",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_id(*parts: object, size: int = 24) -> str:
    raw = "\x1f".join(str(part) for part in parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:size]


def claim_type(record: dict[str, Any]) -> str:
    reasons = set(record.get("risk_reasons", []))
    statement = record.get("statement", "")
    if "source-directory-entry" in reasons or "administrative-date" in reasons:
        return "administrative"
    if "regulatory" in reasons:
        return "regulatory"
    if "safety" in reasons:
        return "safety"
    if re.search(r"\b(recommend|should|best|prefer|avoid|use instead)\b", statement, re.I):
        return "recommendation"
    if "performance" in reasons:
        return "performance"
    if "commercial" in reasons:
        return "commercial"
    if "configuration" in reasons:
        return "configuration"
    if record.get("record_type") == "managed-claim" and record.get("calculation"):
        return "calculation"
    if re.search(r"\b(compatible|works with|interoperab|supported by)\b", statement, re.I):
        return "compatibility"
    return "factual"


def evidence_packet_schema() -> dict[str, Any]:
    source = {
        "type": "object", "additionalProperties": False,
        "properties": {
            "url": {"type": "string", "maxLength": 2048},
            "title": {"type": "string", "maxLength": 200},
            "publisher": {"type": "string", "maxLength": 160},
            "source_class": {"type": "string", "enum": sorted(SOURCE_CLASSES)},
            "passage": {"type": "string", "maxLength": 600},
            "locator": {"type": "string", "maxLength": 200},
            "retrieved_at": {"type": "string", "format": "date"},
            "content_sha256": {"type": "string", "maxLength": 64},
            "supports": {"type": "string", "maxLength": 400},
            "version": {"type": "string", "maxLength": 100},
        },
        "required": ["url", "title", "publisher", "source_class", "passage", "locator",
                     "retrieved_at", "content_sha256", "supports", "version"],
    }
    calculation = {
        "type": "object", "additionalProperties": False,
        "properties": {
            "method": {"type": "string", "maxLength": 300},
            "inputs": {"type": "string", "maxLength": 400},
            "units": {"type": "string", "maxLength": 100},
            "result": {"type": "string", "maxLength": 300},
            "reproduced": {"type": "boolean"},
            "code": {"type": "string", "maxLength": 1000},
        },
        "required": ["method", "inputs", "units", "result", "reproduced", "code"],
    }
    return {
        "type": "object", "additionalProperties": False,
        "properties": {
            "claim_id": {"type": "string"},
            "role": {"type": "string", "enum": list(ROLES)},
            "conclusion": {"type": "string", "enum": sorted(CONCLUSIONS)},
            "proposed_statement": {"type": "string", "maxLength": 800},
            "scope": {"type": "string", "maxLength": 500},
            "jurisdiction": {"type": "string", "maxLength": 200},
            "effective_date": {"type": "string", "maxLength": 40},
            "sources": {"type": "array", "maxItems": 3, "items": source},
            "contradictions": {"type": "array", "maxItems": 3,
                               "items": {"type": "string", "maxLength": 400}},
            "calculations": {"type": "array", "maxItems": 3, "items": calculation},
            "alternatives": {"type": "array", "maxItems": 3,
                             "items": {"type": "string", "maxLength": 400}},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "limitations": {"type": "array", "maxItems": 3,
                            "items": {"type": "string", "maxLength": 400}},
            "notes": {"type": "string", "maxLength": 800},
        },
        "required": ["claim_id", "role", "conclusion", "proposed_statement", "scope",
                     "jurisdiction", "effective_date", "sources", "contradictions",
                     "calculations", "alternatives", "confidence", "limitations", "notes"],
    }


def research_spec(record: dict[str, Any], release: str) -> dict[str, Any]:
    ctype = claim_type(record)
    policy = CLAIM_POLICIES[ctype]
    spec_id = stable_id(release, record["id"], record.get("source_revision", ""), ctype)
    return {
        "schema_version": SCHEMA_VERSION, "id": spec_id, "release": release,
        "claim_id": record["id"], "article_id": record.get("article_id"),
        "path": record.get("path"), "anchor": record.get("anchor"),
        "statement": record.get("statement", ""),
        "claim_type": ctype, "risk": policy["risk"],
        "source_revision": record.get("source_revision"),
        "candidate_sources": sorted(set(record.get("source_candidates", []) + record.get("article_source_candidates", []))),
        "requirements": dict(policy), "created_at": utcnow(),
    }


def _role_prompt(spec: dict[str, Any], role: str) -> str:
    stance = (
        "Find the strongest current evidence for the exact claim, narrowing its wording when needed."
        if role == "researcher" else
        "Independently try to falsify the claim. Search for superseding versions, exceptions, scope errors, and contrary evidence."
    )
    candidates = "\n".join(f"- {url}" for url in spec["candidate_sources"]) or "- none"
    return f"""You are the {role} in an evidence-validation system. {stance}

Claim ID: {spec['claim_id']}
Claim type: {spec['claim_type']}
Risk: {spec['risk']}
Exact statement: {spec['statement']}
Existing leads (leads are not proof):
{candidates}

Rules:
- Use current primary authorities, standards, manufacturer documentation, peer-reviewed work, or reproducible technical evidence.
- Quote only the exact short passage needed and record a precise locator.
- Do not infer a broader model, version, jurisdiction, date, configuration, or performance envelope than the source establishes.
- Search for contradictions and superseding documents.
- A page title, search snippet, retailer listing, or marketing summary is not adequate support by itself.
- If evidence is insufficient, return insufficient. Never fill missing facts with assumptions.
- For calculations, record inputs, units, method, result, and whether independently reproduced.
- Keep the packet concise: at most three sources and three items in each supporting list.
- Return only the required structured object. The role field must be {role!r} and claim_id must be {spec['claim_id']!r}.
"""


def openai_request(spec: dict[str, Any], role: str, *, model: str = "gpt-5.5",
                   allowed_domains: Iterable[str] | None = None) -> dict[str, Any]:
    if role not in ROLES:
        raise ValueError("invalid research role")
    domains = sorted(set(allowed_domains or DEFAULT_AUTHORITY_DOMAINS) | {
        urlsplit(url).hostname for url in spec.get("candidate_sources", []) if urlsplit(url).hostname
    })
    return {
        "model": model, "background": True, "store": True,
        "reasoning": {"effort": "high"},
        "tools": [{"type": "web_search", "external_web_access": True,
                   "filters": {"allowed_domains": domains}}],
        "tool_choice": "required",
        "include": ["web_search_call.action.sources"],
        "input": _role_prompt(spec, role),
        "text": {"format": {"type": "json_schema", "name": "evidence_packet",
                            "strict": True, "schema": evidence_packet_schema()}},
        "metadata": {"research_spec_id": spec["id"], "claim_id": spec["claim_id"], "role": role},
    }


def validate_packet(packet: dict[str, Any], *, claim_id: str | None = None,
                    role: str | None = None) -> list[str]:
    errors: list[str] = []
    required = evidence_packet_schema()["required"]
    errors.extend(f"missing:{name}" for name in required if name not in packet)
    if claim_id and packet.get("claim_id") != claim_id:
        errors.append("claim-id-mismatch")
    if role and packet.get("role") != role:
        errors.append("role-mismatch")
    if packet.get("role") not in ROLES:
        errors.append("invalid-role")
    if packet.get("conclusion") not in CONCLUSIONS:
        errors.append("invalid-conclusion")
    confidence = packet.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        errors.append("invalid-confidence")
    for index, source in enumerate(packet.get("sources", [])):
        prefix = f"source-{index}"
        try:
            parsed = urlsplit(source.get("url", ""))
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                errors.append(prefix + ":invalid-url")
        except (TypeError, ValueError):
            errors.append(prefix + ":invalid-url")
        if source.get("source_class") not in SOURCE_CLASSES:
            errors.append(prefix + ":invalid-class")
        for field in ("title", "publisher", "passage", "locator", "supports"):
            if not str(source.get(field, "")).strip():
                errors.append(prefix + ":missing-" + field)
        try:
            date.fromisoformat(source.get("retrieved_at", ""))
        except (TypeError, ValueError):
            errors.append(prefix + ":invalid-date")
        digest = str(source.get("content_sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(prefix + ":invalid-digest")
    return sorted(set(errors))


def source_domains(spec: dict[str, Any]) -> set[str]:
    return set(DEFAULT_AUTHORITY_DOMAINS) | {
        urlsplit(url).hostname.lower() for url in spec.get("candidate_sources", []) if urlsplit(url).hostname
    }


def _public_allowed_host(hostname: str, allowed: set[str]) -> bool:
    host = hostname.lower().rstrip(".")
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        return False
    return any(host == domain or host.endswith("." + domain) for domain in allowed)


def fetch_source(url: str, allowed: set[str]) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or not _public_allowed_host(parsed.hostname, allowed):
        raise ValueError("source URL is outside the research domain allowlist")

    class SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, file_pointer, code, message, headers, new_url):
            target = urlsplit(urljoin(request.full_url, new_url))
            if target.scheme != "https" or not target.hostname or not _public_allowed_host(target.hostname, allowed):
                raise ValueError("source redirect left the research domain allowlist")
            return super().redirect_request(request, file_pointer, code, message, headers, new_url)

    request = urllib.request.Request(url, headers={"User-Agent": "UAS-Handbook-Evidence/1.0"})
    with urllib.request.build_opener(SafeRedirect()).open(request, timeout=20) as response:
        final = urlsplit(response.geturl())
        if not final.hostname or not _public_allowed_host(final.hostname, allowed):
            raise ValueError("source redirect left the research domain allowlist")
        body = response.read(4 * 1024 * 1024 + 1)
        if len(body) > 4 * 1024 * 1024:
            raise ValueError("source snapshot exceeds four MiB")
        if not body:
            raise ValueError("source snapshot is empty")
        return body


def verify_source_snapshots(packet: dict[str, Any], spec: dict[str, Any], *, fetch=fetch_source) -> dict[str, Any]:
    """Replace model-provided digests with hashes of bytes fetched by trusted code."""
    verified = json.loads(json.dumps(packet))
    if len(verified.get("sources", [])) > 10:
        raise ValueError("evidence packet contains too many sources")
    allowed = source_domains(spec)
    for source in verified.get("sources", []):
        source["content_sha256"] = hashlib.sha256(fetch(source["url"], allowed)).hexdigest()
    return verified


def _unique_sources(packets: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}
    for packet in packets:
        for source in packet.get("sources", []):
            found[(source.get("url", ""), source.get("content_sha256", ""))] = source
    return list(found.values())


def adjudicate(spec: dict[str, Any], packets: Iterable[dict[str, Any]]) -> dict[str, Any]:
    packets = list(packets)
    decision_id = stable_id(spec["id"], *(json.dumps(p, sort_keys=True) for p in packets))
    base = {
        "schema_version": SCHEMA_VERSION, "id": decision_id, "research_spec_id": spec["id"],
        "claim_id": spec["claim_id"], "claim_type": spec["claim_type"],
        "created_at": utcnow(), "publication_state": "abstained", "publish": False,
        "human_intervention": False, "reasons": [], "source_count": 0,
    }
    if spec["claim_type"] == "administrative":
        return {**base, "publication_state": "not-a-claim", "reasons": ["deterministic-administrative-classification"]}
    by_role = {packet.get("role"): packet for packet in packets}
    if set(by_role) != set(ROLES):
        return {**base, "reasons": ["independent-research-and-verification-required"]}
    errors = []
    for role in ROLES:
        errors.extend(validate_packet(by_role[role], claim_id=spec["claim_id"], role=role))
    if errors:
        return {**base, "reasons": ["invalid-evidence-packet", *sorted(set(errors))], "human_intervention": False}
    conclusions = {packet["conclusion"] for packet in packets}
    contradictions = [item for packet in packets for item in packet["contradictions"] if item.strip()]
    if "contradicts" in conclusions or ("supports" in conclusions and "insufficient" in conclusions):
        return {**base, "publication_state": "contradicted", "human_intervention": True,
                "reasons": ["independent-runs-disagree"] + (["reported-contradictions"] if contradictions else [])}
    if conclusions != {"supports"}:
        return {**base, "reasons": ["evidence-does-not-fully-support-exact-claim"]}
    sources = _unique_sources(packets)
    base["source_count"] = len(sources)
    policy = CLAIM_POLICIES[spec["claim_type"]]
    if len(sources) < policy["min_sources"]:
        return {**base, "reasons": ["minimum-independent-source-count-not-met"]}
    if min(packet["confidence"] for packet in packets) < 0.75:
        return {**base, "reasons": ["confidence-below-publication-threshold"]}
    if policy.get("authority"):
        authority = [s for s in sources if s["source_class"] in {"controlling-authority", "government-guidance"}]
        if not authority or any(not packet["jurisdiction"].strip() or not packet["effective_date"].strip() for packet in packets):
            return {**base, "human_intervention": True,
                    "reasons": ["regulatory-authority-jurisdiction-or-effective-date-missing"]}
    if policy.get("reproduce"):
        calculations = [c for packet in packets for c in packet["calculations"]]
        if not calculations or not all(c.get("reproduced") for c in calculations):
            return {**base, "reasons": ["deterministic-reproduction-required"]}
    if policy.get("alternatives") and any(not packet["alternatives"] for packet in packets):
        return {**base, "reasons": ["recommendation-alternatives-required"]}
    if contradictions:
        return {**base, "publication_state": "exception", "human_intervention": True,
                "reasons": ["unresolved-counterevidence"]}
    if not policy["auto_publish"]:
        return {**base, "publication_state": "exception", "human_intervention": True,
                "reasons": ["critical-risk-policy-requires-exception-review"]}
    state = "primary-source-supported" if spec["claim_type"] == "regulatory" else "corroborated"
    if policy.get("reproduce"):
        state = "independently-reproduced"
    return {**base, "publication_state": state, "publish": True,
            "reasons": ["deterministic-publication-policy-passed"],
            "statement": by_role["verifier"]["proposed_statement"],
            "scope": by_role["verifier"]["scope"],
            "source_urls": sorted({s["url"] for s in sources})}


def plan_jobs(queue: dict[str, Any], *, maximum: int | None = None) -> dict[str, Any]:
    records = queue.get("records", [])
    if maximum is not None:
        records = records[:maximum]
    specs = [research_spec(record, queue["release"]) for record in records]
    jobs = []
    decisions = []
    for record, spec in zip(records, specs):
        if spec["claim_type"] == "administrative":
            decisions.append(adjudicate(spec, []))
            continue
        for role in ROLES:
            jobs.append({"id": stable_id(spec["id"], role), "spec_id": spec["id"],
                         "claim_id": spec["claim_id"], "role": role, "state": "planned",
                         "attempts": 0, "created_at": utcnow()})
    return {
        "schema_version": SCHEMA_VERSION, "kind": "uas-handbook-autonomous-evidence-plan",
        "release": queue["release"], "created_at": utcnow(), "specs": specs,
        "jobs": jobs, "decisions": decisions,
        "summary": {"records": len(records), "research_specs": len(specs),
                    "background_jobs": len(jobs), "automatic_decisions": len(decisions),
                    "human_interventions": sum(d["human_intervention"] for d in decisions)},
    }


def public_status(queue: dict[str, Any], prediction_ledger: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a non-sensitive, release-bound autonomy and experiment summary."""
    prediction_ledger = prediction_ledger or {"predictions": []}
    predictions = prediction_ledger.get("predictions", [])
    resolved = [row for row in predictions if row.get("state") == "resolved" and row.get("resolution")]
    types: dict[str, int] = {}
    automatic = 0
    for record in queue.get("records", []):
        kind = claim_type(record); types[kind] = types.get(kind, 0) + 1
        automatic += kind == "administrative"
    return {
        "schema_version": SCHEMA_VERSION, "release": queue.get("release"),
        "mode": "software-ready-live-optional",
        "scope": "Public aggregate only. Research packets, field submissions, exceptions and credentials remain private.",
        "pipeline": [
            {"id": "inventory", "label": "Review-unit inventory", "state": "implemented"},
            {"id": "research", "label": "Independent research", "state": "implemented"},
            {"id": "verification", "label": "Adversarial verification", "state": "implemented"},
            {"id": "policy", "label": "Deterministic policy", "state": "implemented"},
            {"id": "publication", "label": "Release proposal", "state": "fail-closed"},
            {"id": "monitoring", "label": "Source monitoring", "state": "implemented"},
        ],
        "evidence": {
            "records": len(queue.get("records", [])),
            "priorities": queue.get("summary", {}).get("priorities", {}),
            "claim_types": dict(sorted(types.items())),
            "automatic_nonclaims": automatic,
            "research_jobs_required": 2 * (len(queue.get("records", [])) - automatic),
            "human_intervention_policy": "Only contradictions, critical-risk recommendations, regulatory ambiguity, field-only facts, and system/security failures.",
        },
        "predictions": {
            "total": len(predictions), "open": sum(row.get("state") == "open" for row in predictions),
            "resolved": len(resolved),
            "mean_brier": sum(row["resolution"]["brier"] for row in resolved) / len(resolved) if resolved else None,
            "mean_baseline_brier": sum(row["resolution"]["baseline_brier"] for row in resolved) / len(resolved) if resolved else None,
        },
        "publication_policy": {name: dict(value) for name, value in CLAIM_POLICIES.items()},
    }


def extract_packet_from_response(response: dict[str, Any]) -> dict[str, Any]:
    texts = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                texts.append(content.get("text", ""))
    if not texts:
        raise ValueError("response contains no output_text")
    packet = json.loads("".join(texts))
    if not isinstance(packet, dict):
        raise ValueError("evidence packet must be an object")
    return packet


@dataclass
class OpenAIProvider:
    api_key: str
    model: str = "gpt-5.5"
    endpoint: str = "https://api.openai.com/v1/responses"
    timeout: int = 60

    @classmethod
    def from_environment(cls) -> "OpenAIProvider":
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not configured; use the software provider or configure the secret")
        return cls(key, os.environ.get("OPENAI_RESEARCH_MODEL", "gpt-5.5"))

    def _request(self, url: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(url, data=body, method=method, headers={
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "UAS-Handbook-Evidence/1.0",
        })
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            detail = error.read(4096).decode(errors="replace")
            raise RuntimeError(f"OpenAI request failed ({error.code}): {detail}") from error

    def start(self, spec: dict[str, Any], role: str) -> dict[str, Any]:
        response = self._request(self.endpoint, method="POST", payload=openai_request(spec, role, model=self.model))
        if not response.get("id") or response.get("status") not in {"queued", "in_progress", "completed"}:
            raise RuntimeError("OpenAI did not acknowledge the background response")
        return response

    def retrieve(self, response_id: str) -> dict[str, Any]:
        if not re.fullmatch(r"resp_[A-Za-z0-9_-]+", response_id):
            raise ValueError("invalid response identity")
        return self._request(self.endpoint + "/" + response_id)


class SoftwareProvider:
    """Deterministic replay provider used by tests and disconnected operation."""

    def __init__(self, packets: dict[tuple[str, str], dict[str, Any]] | None = None):
        self.packets = packets or {}

    def run(self, spec: dict[str, Any], role: str) -> dict[str, Any] | None:
        packet = self.packets.get((spec["claim_id"], role))
        return json.loads(json.dumps(packet)) if packet is not None else None


def brier_score(probability: float, outcome: bool) -> float:
    if isinstance(probability, bool) or not isinstance(probability, (int, float)) or not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError("probability must be finite and between zero and one")
    return (float(probability) - float(outcome)) ** 2


def register_prediction(item: dict[str, Any], *, now: str | None = None) -> dict[str, Any]:
    required = ("question", "probability", "data_cutoff", "target_date", "resolution_source", "baseline_probability")
    missing = [key for key in required if item.get(key) in (None, "")]
    if missing:
        raise ValueError("prediction missing: " + ", ".join(missing))
    for key in ("probability", "baseline_probability"):
        value = item[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise ValueError(key + " must be between zero and one")
    date.fromisoformat(item["data_cutoff"]); date.fromisoformat(item["target_date"])
    if item["data_cutoff"] > item["target_date"]:
        raise ValueError("prediction data cutoff follows target date")
    resolution_url = urlsplit(item["resolution_source"])
    if resolution_url.scheme != "https" or not resolution_url.hostname:
        raise ValueError("prediction resolution source must be HTTPS")
    registered = now or utcnow()
    frozen = {key: item[key] for key in required}
    frozen.update({"evidence_ids": sorted(set(item.get("evidence_ids", []))),
                   "model": item.get("model", "unspecified"), "prompt_version": item.get("prompt_version", "unspecified")})
    return {"schema_version": 1, "id": stable_id(json.dumps(frozen, sort_keys=True), registered),
            **frozen, "registered_at": registered, "state": "open", "resolution": None}


def resolve_prediction(prediction: dict[str, Any], outcome: bool, *, source_url: str,
                       resolved_at: str | None = None) -> dict[str, Any]:
    if prediction.get("state") != "open":
        raise ValueError("prediction is already resolved")
    parsed = urlsplit(source_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("HTTPS resolution source required")
    if source_url != prediction.get("resolution_source"):
        raise ValueError("resolution source does not match the pre-registered source")
    result = json.loads(json.dumps(prediction))
    result["state"] = "resolved"
    result["resolution"] = {"outcome": bool(outcome), "source_url": source_url,
                            "resolved_at": resolved_at or utcnow(),
                            "brier": brier_score(result["probability"], outcome),
                            "baseline_brier": brier_score(result["baseline_probability"], outcome)}
    return result


def write_plan(path: Path, plan: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
