#!/usr/bin/env python3
"""Audit or reconcile existing production evidence jobs without dispatching work."""
import argparse
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError("Private API redirect rejected")


def request(origin, token, path, payload=None):
    parsed = urlsplit(origin)
    if parsed.scheme != "https" or parsed.hostname != "uas-handbook.com" or parsed.path not in ("", "/"):
        raise ValueError("Production audit origin must be https://uas-handbook.com")
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        origin.rstrip("/") + "/api/autonomy/" + path,
        data=data,
        method="GET" if payload is None else "POST",
        headers={
            "authorization": "Bearer " + token,
            "content-type": "application/json",
            "user-agent": "HandbookAutonomyAudit/1.0",
        },
    )
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=90) as response:
        body = response.read(2 * 1024 * 1024 + 1)
    if len(body) > 2 * 1024 * 1024:
        raise ValueError("Private audit response too large")
    value = json.loads(body)
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Invalid private audit response")
    return value


def iso_time(milliseconds):
    if not isinstance(milliseconds, int):
        return None
    return datetime.fromtimestamp(milliseconds / 1000, timezone.utc).isoformat()


def sanitized(value, reconciliation=None):
    jobs = []
    for job in value.get("jobs", []):
        jobs.append({
            "job_ref": hashlib.sha256(str(job.get("id", "")).encode()).hexdigest()[:12],
            "role": job.get("role"),
            "ledger_state": job.get("state"),
            "reserved": bool(job.get("reserved")),
            "has_response_id": bool(job.get("response_id")),
            "packet_stored": bool(job.get("packet_stored")),
            "provider_status": job.get("provider_status"),
            "provider_probe_error": job.get("provider_probe_error"),
        })
    trial = value.get("trial", {})
    result = {
        "provider_configured": bool(value.get("provider_configured")),
        "webhook_configured": bool(value.get("webhook_configured")),
        "trial": {
            "present": bool(trial.get("present")),
            "enabled": bool(trial.get("enabled")),
            "active": bool(trial.get("active")),
            "starts_at": iso_time(trial.get("starts_ms")),
            "ends_at": iso_time(trial.get("ends_ms")),
            "duration_ms": trial.get("duration_ms"),
        },
        "reservations": value.get("reservations", {}),
        "specs": value.get("specs", []),
        "jobs_by_state": value.get("jobs_by_state", []),
        "decisions": value.get("decisions", []),
        "unresolved_jobs": jobs,
        "paid_requests_started": 0,
    }
    if reconciliation is not None:
        result["reconciliation"] = reconciliation.get("summary", {})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", default=os.environ.get("AUTONOMY_DISPATCH_URL", ""))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--reconcile-existing", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("AUTONOMY_REVIEW_TOKEN", "")
    if not args.origin or not token:
        raise SystemExit("AUTONOMY_DISPATCH_URL and AUTONOMY_REVIEW_TOKEN are required")
    before = request(args.origin, token, "audit?probe=1")
    reconciliation = None
    if args.reconcile_existing:
        reconciliation = request(args.origin, token, "reconcile", {"confirm": "existing-jobs-only"})
    audit = request(args.origin, token, "audit?probe=1") if reconciliation else before
    if audit.get("reservations", {}).get("total") != before.get("reservations", {}).get("total"):
        raise ValueError("Reconciliation changed paid reservation count")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(audit, indent=2) + "\n")
        args.output.chmod(0o600)
    print(json.dumps(sanitized(audit, reconciliation), indent=2))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        raise SystemExit(f"Autonomy audit failed with HTTP {error.code}") from None
