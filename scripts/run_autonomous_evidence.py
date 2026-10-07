#!/usr/bin/env python3
"""Plan and execute an autonomous evidence cycle.

Without an API key this command still performs the complete deterministic
planning and policy path and records every unresolved item as queued research.
Live mode starts bounded background Responses API jobs; it never fabricates a
successful run when credentials or storage are unavailable.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from handbook_builder.autonomous import OpenAIProvider, openai_request, plan_jobs, write_plan
from handbook_builder.review import build_review_queue, extract_article_sources


def load_queue(path: Path) -> dict:
    snapshot = json.loads(path.read_text())
    return snapshot if "references" not in snapshot else build_review_queue(snapshot, extract_article_sources(ROOT, snapshot["records"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "site/assets/reference-data.json")
    parser.add_argument("--output", type=Path, default=ROOT / ".local/autonomy/plan.json")
    parser.add_argument("--request-dir", type=Path, default=ROOT / ".local/autonomy/requests")
    parser.add_argument("--provider", choices=("auto", "software", "openai", "dispatch"), default="auto")
    parser.add_argument("--maximum", type=int, default=None, help="Bound records considered in this cycle")
    parser.add_argument("--start-limit", type=int, default=10, help="Maximum live background requests")
    parser.add_argument("--request-limit", type=int, default=20, help="Maximum request fixtures written locally")
    parser.add_argument("--offset", type=int, default=0, help="Deterministic record offset for bounded cycles")
    parser.add_argument("--model", default=os.environ.get("OPENAI_RESEARCH_MODEL", "gpt-5.5"))
    args = parser.parse_args()
    if args.maximum is not None and args.maximum < 1:
        parser.error("--maximum must be positive")
    if not 0 <= args.start_limit <= 100:
        parser.error("--start-limit must be between 0 and 100")

    queue = load_queue(args.input)
    if args.offset < 0: parser.error("--offset cannot be negative")
    if args.offset:
        queue = {**queue, "records": queue["records"][args.offset:]}
    plan = plan_jobs(queue, maximum=args.maximum)
    args.request_dir.mkdir(parents=True, exist_ok=True)
    specs = {item["id"]: item for item in plan["specs"]}
    for job in plan["jobs"][:args.request_limit]:
        request = openai_request(specs[job["spec_id"]], job["role"], model=args.model)
        (args.request_dir / f"{job['id']}.json").write_text(json.dumps(request, indent=2) + "\n")

    dispatch_url=os.environ.get("AUTONOMY_DISPATCH_URL","").strip().rstrip("/")
    review_token=os.environ.get("AUTONOMY_REVIEW_TOKEN","").strip()
    use_dispatch=args.provider=="dispatch" or (args.provider=="auto" and bool(dispatch_url and review_token))
    use_openai = args.provider == "openai"
    if args.provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for --provider openai; software planning completed but no request was sent")
    if args.provider == "dispatch" and not (dispatch_url and review_token):
        raise SystemExit("AUTONOMY_DISPATCH_URL and AUTONOMY_REVIEW_TOKEN are required for --provider dispatch")
    started = 0
    deferred = None
    if use_dispatch:
        spec_jobs={}
        for job in plan["jobs"][:args.start_limit]:spec_jobs.setdefault(job["spec_id"],[]).append(job)
        for spec_id,jobs in spec_jobs.items():
            if {job["role"] for job in jobs} != {"researcher","verifier"}:continue
            spec=specs[spec_id];payload={"spec":spec,"requests":{role:openai_request(spec,role,model=args.model) for role in ("researcher","verifier")}}
            request=urllib.request.Request(dispatch_url+"/api/autonomy/runs",data=json.dumps(payload).encode(),method="POST",headers={"authorization":"Bearer "+review_token,"content-type":"application/json","user-agent":"UAS-Handbook-Evidence/1.0"})
            try:
                with urllib.request.urlopen(request,timeout=90) as response:ack=json.loads(response.read())
            except urllib.error.HTTPError as error:
                message=error.read(1000).decode(errors='replace')
                if 'Trial stopped:' in message or 'trial is not active' in message.lower():
                    deferred='Existing research trial expired, disabled or at its workload limit'
                    break
                raise SystemExit(f"Autonomy dispatcher failed ({error.code}): {message}") from error
            acknowledgements={row["role"]:row for row in ack.get("jobs",[])}
            for job in jobs:
                remote=acknowledgements[job["role"]];job.update(state=remote["state"],response_id=remote["response_id"],attempts=1);started+=1
    elif use_openai:
        client = OpenAIProvider.from_environment()
        client.model = args.model
        for job in plan["jobs"][:args.start_limit]:
            response = client.start(specs[job["spec_id"]], job["role"])
            job.update(state=response["status"], response_id=response["id"], attempts=1)
            started += 1
    plan["provider"] = "dispatch" if use_dispatch else "openai" if use_openai else "software"
    plan["offset"] = args.offset
    plan["summary"]["started_background_jobs"] = started
    plan["summary"]["queued_for_future_cycles"] = len(plan["jobs"]) - started
    plan["summary"]["publication_changed"] = False
    plan['summary']['deferred_reason'] = deferred
    write_plan(args.output, plan)
    print(json.dumps(plan["summary"], indent=2))


if __name__ == "__main__":
    main()
