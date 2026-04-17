#!/usr/bin/env python3
"""
PIE Daily Brief Generator
==========================
Runs after pie_pipeline_live.py. Reads flags, predictions, gray zone entities,
and procurement signals, then calls the Claude API to write a structured
intelligence brief. Saves to data/briefs/YYYY-MM-DD.json and .md.

The brief has five sections:
  1. Lead Story    — single most actionable development today
  2. Gray Zone     — entity-specific updates (legal, market, buyer exposure)
  3. Supply Chain  — component/pricing/lead-time signals worth acting on
  4. Watch List    — things moving slowly but worth tracking
  5. Predictions   — top 3 with recommended hedges

Usage:
  python pipeline/brief_generator.py           # today's brief
  python pipeline/brief_generator.py --dry-run # print prompt only, no API call
  python pipeline/brief_generator.py --date 2026-04-01  # regenerate past brief
"""

import json
import os
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

REPO_ROOT = Path(__file__).resolve().parent.parent
BRIEFS_DIR = REPO_ROOT / "data" / "briefs"
BRIEFS_DIR.mkdir(parents=True, exist_ok=True)

now_utc = datetime.now(timezone.utc)
today_str = now_utc.strftime("%Y-%m-%d")


# ── Data loaders ─────────────────────────────────────────────────

def load_flags():
    p = REPO_ROOT / "data" / "flags.json"
    return json.loads(p.read_text()) if p.exists() else []

def load_predictions():
    p = REPO_ROOT / "data" / "predictions.json"
    return json.loads(p.read_text()) if p.exists() else []

def load_entities():
    p = REPO_ROOT / "data" / "grayzone" / "entities.json"
    if not p.exists(): return []
    raw = json.loads(p.read_text())
    return raw if isinstance(raw, list) else raw.get("entities", [])

def load_procurement():
    p = REPO_ROOT / "data" / "procurement" / "gray_zone_matches.json"
    return json.loads(p.read_text()) if p.exists() else {}

def load_prev_brief(date_str=None):
    """Load yesterday's brief for delta comparison."""
    if date_str:
        p = BRIEFS_DIR / f"{date_str}.json"
    else:
        # Find most recent brief before today
        briefs = sorted(BRIEFS_DIR.glob("*.json"), reverse=True)
        briefs = [b for b in briefs if b.stem != today_str]
        p = briefs[0] if briefs else None
    if p and p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return None


# ── Delta tracking ────────────────────────────────────────────────

def compute_delta(flags, prev_brief):
    """Compare today's flags against yesterday's brief to find new/escalated."""
    if not prev_brief:
        return {"new_flags": len(flags), "escalated": [], "resolved": [], "is_first": True}

    prev_flag_ids = set(prev_brief.get("flag_ids", []))
    curr_flag_ids = set(f["id"] for f in flags)

    new_ids = curr_flag_ids - prev_flag_ids
    resolved_ids = prev_flag_ids - curr_flag_ids

    # Escalated = same ID but severity went up
    prev_sevs = prev_brief.get("flag_severities", {})
    sev_rank = {"critical": 3, "warning": 2, "high": 2, "info": 1}
    escalated = []
    for f in flags:
        if f["id"] in prev_sevs:
            prev_rank = sev_rank.get(prev_sevs[f["id"]], 0)
            curr_rank = sev_rank.get(f.get("severity", ""), 0)
            if curr_rank > prev_rank:
                escalated.append(f["title"][:80])

    new_flags = [f for f in flags if f["id"] in new_ids]

    return {
        "new_count": len(new_ids),
        "resolved_count": len(resolved_ids),
        "escalated": escalated[:5],
        "new_critical": [f for f in new_flags if f.get("severity") == "critical"],
        "new_warning":  [f for f in new_flags if f.get("severity") == "warning"],
        "is_first": False,
    }


# ── Prompt builder ────────────────────────────────────────────────

def build_prompt(flags, predictions, entities, procurement, delta):
    """Build the analyst prompt for Claude."""

    # Distill key data into compact intel packages
    critical_flags = [f for f in flags if f.get("severity") == "critical"]
    warning_flags  = [f for f in flags if f.get("severity") == "warning"]
    grayzone_flags = [f for f in flags if f.get("flag_type") in ("grayzone", "grayzone_xref",
                       "legal_action", "buyer_exposure", "corporate_evasion")]

    # Entity summaries
    entity_summaries = []
    for e in entities:
        latest = e.get("latest_developments", {})
        buyers = e.get("known_government_buyers", [])
        buyer_count = len(buyers) if isinstance(buyers, list) else 0
        legal = e.get("legal_actions", [])
        entity_summaries.append({
            "name": e["name"],
            "score": e.get("composite_score", 0),
            "risk_level": e.get("risk_level", "?"),
            "status": e.get("status", ""),
            "key_development": (
                latest.get("tx_lawsuit_status") or
                latest.get("product_status") or
                latest.get("fcc_status") or
                str(latest)[:200]
            ) if latest else "No recent updates",
            "buyer_count": buyer_count,
            "legal_action_count": len(legal) if isinstance(legal, list) else 0,
        })

    # Top predictions with model backing
    top_preds = []
    for p in predictions[:5]:
        model_outputs = p.get("model_outputs", [])
        strongest_model = max(model_outputs, key=lambda m: m.get("probability", 0)) if model_outputs else {}
        top_preds.append({
            "event": p["event"],
            "probability": p["probability"],
            "timeframe": p["timeframe"],
            "impact": p["impact"],
            "top_driver": p.get("drivers", [""])[0],
            "strongest_model": strongest_model.get("model", ""),
            "model_confidence": strongest_model.get("confidence", 0),
        })

    # News signals
    news = procurement.get("all_gray_zone_signals", [])
    recent_news = sorted(
        [s for s in news if s.get("source") == "news"],
        key=lambda x: x.get("published", ""), reverse=True
    )[:5]

    # Delta summary
    delta_line = ""
    if delta.get("is_first"):
        delta_line = "This is the first brief — no previous day to compare against."
    else:
        delta_line = (
            f"{delta.get('new_count', 0)} new flags since last brief, "
            f"{delta.get('resolved_count', 0)} resolved. "
            f"Escalated: {', '.join(delta.get('escalated', [])) or 'none'}."
        )

    # Build compact flag digest (top 15 by severity + confidence)
    top_flags = sorted(
        critical_flags + warning_flags[:10],
        key=lambda f: (
            {"critical": 0, "warning": 1, "high": 1, "info": 2}.get(f.get("severity", ""), 9),
            -(f.get("confidence", 0))
        )
    )[:15]

    flag_digest = "\n".join(
        f"- [{f['severity'].upper()}] [{f['flag_type']}] {f['title'][:90]}\n"
        f"  {f.get('detail','')[:150]}..."
        for f in top_flags
    )

    entity_block = "\n".join(
        f"- {e['name']} (score={e['score']:.3f}, {e['risk_level']}): "
        f"{e['key_development'][:200]}"
        for e in entity_summaries
    )

    pred_block = "\n".join(
        f"- [{p['probability']:.0%}] {p['event'][:80]} [{p['timeframe']}]\n"
        f"  Driver: {p['top_driver']}\n"
        f"  Strongest model: {p['strongest_model']} (conf={p['model_confidence']:.2f})"
        for p in top_preds
    )

    news_block = "\n".join(
        f"- {s.get('published','')[:16]} | {s.get('title','')[:80]}"
        for s in recent_news
    ) or "No recent news signals."

    # Default generic fallback prompt
    DEFAULT_BRIEF_PROMPT = (
        "You are an intelligence analysis assistant. "
        "Given the raw intelligence data below, produce a structured JSON intelligence brief "
        "covering: lead story, entity updates, supply chain signals, watch list, and predictions. "
        "Be specific, cite numbers from the data, and include actionable recommendations."
    )

    # Production prompt loaded from PIE_BRIEF_PROMPT env var
    prompt_template = os.environ.get("PIE_BRIEF_PROMPT", DEFAULT_BRIEF_PROMPT)

    prompt = f"""{prompt_template}

Today is {today_str}.

Delta from yesterday: {delta_line}

## RAW INTELLIGENCE DATA

### TOP FLAGS ({len(flags)} total, {len(critical_flags)} critical, {len(warning_flags)} warning)
{flag_digest}

### GRAY ZONE ENTITIES
{entity_block}

### PREDICTIONS (ensemble model outputs)
{pred_block}

### RECENT NEWS SIGNALS
{news_block}

## BRIEF FORMAT

Write the brief in this exact JSON structure:

{{
  "date": "{today_str}",
  "headline": "single sentence — the most important thing happening today",
  "lead_story": {{
    "title": "short title",
    "body": "3-4 sentences. What is happening, why it matters, what the signal strength is. Specific. Cite actual numbers from the data.",
    "action": "one concrete thing a procurement officer or program manager should do this week because of this",
    "sources": [{{"name": "source name", "url": "https://...", "type": "primary|reporting|derived"}}]
  }},
  "gray_zone": [
    {{
      "entity": "entity name",
      "status": "one sentence current status",
      "development": "2-3 sentences on the most significant recent development",
      "buyer_exposure": "who is exposed and what is their risk",
      "action": "what should an agency currently using this equipment do",
      "sources": [{{"name": "source name", "url": "https://...", "type": "primary|reporting|derived"}}]
    }}
  ],
  "supply_chain": [
    {{
      "component": "component name",
      "signal": "what the data shows — probability, concentration ratio, flag count",
      "window": "how much time before this becomes a problem",
      "action": "specific hedge or action",
      "sources": [{{"name": "source name", "url": "https://...", "type": "primary|reporting|derived"}}]
    }}
  ],
  "watch_list": [
    {{
      "item": "thing to watch",
      "why": "one sentence on significance",
      "trigger": "what event would escalate this from watch to action"
    }}
  ],
  "predictions": [
    {{
      "event": "prediction text",
      "probability": 0.00,
      "timeframe": "timeframe",
      "hedge": "specific recommended action to take now to prepare for this outcome"
    }}
  ],
  "signal_summary": {{
    "total_flags": {len(flags)},
    "critical": {len(critical_flags)},
    "warning": {len(warning_flags)},
    "new_today": {delta.get('new_count', 0)},
    "top_concern": "one phrase — the single biggest risk in today's data"
  }}
}}

Rules:
- Be specific. Use actual numbers from the data.
- No vague hedge language. If the data supports a conclusion, state it.
- Actions must be concrete and time-bound.
- Gray zone section: cover all entities, ordered by risk score.
- Supply chain: pick the 3 most actionable signals, not all of them.
- Watch list: 3 items that are trending but not yet critical.
- Predictions: top 3 only, with real hedges a procurement team could execute.
- sources: each section must include 1-3 relevant source objects from the data above.
- Respond ONLY with the JSON object. No preamble, no markdown fences.
"""
    return prompt


# ── Claude API call ───────────────────────────────────────────────

def call_claude(prompt):
    """Call Claude API to generate the brief."""
    try:
        import urllib.request, urllib.error, ssl, json as _json

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            print("  ⚠ ANTHROPIC_API_KEY not set — cannot generate brief")
            return None

        payload = _json.dumps({
            "model": "claude-sonnet-4-5",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()

        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )

        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            data = _json.loads(r.read())
            text = data["content"][0]["text"].strip()

            # Strip markdown fences if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]

            return _json.loads(text)

    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"  ✗ Claude API error {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  ✗ Brief generation failed: {type(e).__name__}: {e}")
        return None


# ── Brief formatter ───────────────────────────────────────────────

def format_markdown(brief):
    """Convert brief JSON to readable markdown."""
    lines = []
    lines.append(f"# PIE Intelligence Brief — {brief.get('date', today_str)}")
    lines.append(f"\n**{brief.get('headline', '')}**\n")

    # Signal summary bar
    sig = brief.get("signal_summary", {})
    lines.append(f"```")
    lines.append(f"Flags: {sig.get('total_flags',0)} total  |  "
                 f"Critical: {sig.get('critical',0)}  |  "
                 f"Warning: {sig.get('warning',0)}  |  "
                 f"New today: {sig.get('new_today',0)}")
    lines.append(f"Top concern: {sig.get('top_concern','')}")
    lines.append(f"```\n")

    # Lead story
    lead = brief.get("lead_story", {})
    lines.append(f"## 🔴 Lead Story: {lead.get('title','')}")
    lines.append(f"\n{lead.get('body','')}\n")
    lines.append(f"**→ Action:** {lead.get('action','')}\n")

    # Gray zone
    lines.append("## ⚠ Gray Zone Entities\n")
    for e in brief.get("gray_zone", []):
        lines.append(f"### {e.get('entity','')}")
        lines.append(f"**Status:** {e.get('status','')}")
        lines.append(f"\n{e.get('development','')}\n")
        lines.append(f"**Buyer exposure:** {e.get('buyer_exposure','')}")
        lines.append(f"\n**→ Action:** {e.get('action','')}\n")

    # Supply chain
    lines.append("## 🔩 Supply Chain Signals\n")
    for s in brief.get("supply_chain", []):
        lines.append(f"**{s.get('component','')}**")
        lines.append(f"{s.get('signal','')} | Window: {s.get('window','')}")
        lines.append(f"→ {s.get('action','')}\n")

    # Watch list
    lines.append("## 👁 Watch List\n")
    for w in brief.get("watch_list", []):
        lines.append(f"- **{w.get('item','')}** — {w.get('why','')}")
        lines.append(f"  *Trigger:* {w.get('trigger','')}")

    # Predictions
    lines.append("\n## 🔮 Predictions & Hedges\n")
    for p in brief.get("predictions", []):
        pct = int(p.get("probability", 0) * 100)
        lines.append(f"**[{pct}%] {p.get('event','')}** _{p.get('timeframe','')}_")
        lines.append(f"→ Hedge: {p.get('hedge','')}\n")

    return "\n".join(lines)


# ── Save brief ────────────────────────────────────────────────────

def save_brief(brief, flags, date_str=None):
    """Save brief JSON + markdown + metadata."""
    ds = date_str or today_str

    # Attach metadata for delta tracking
    brief["flag_ids"] = [f["id"] for f in flags]
    brief["flag_severities"] = {f["id"]: f.get("severity", "") for f in flags}
    brief["generated_at"] = now_utc.isoformat()
    brief["pipeline_version"] = "PIE v0.9"

    json_path = BRIEFS_DIR / f"{ds}.json"
    md_path   = BRIEFS_DIR / f"{ds}.md"

    json_path.write_text(json.dumps(brief, indent=2))
    md_path.write_text(format_markdown(brief))

    print(f"  ✓ Brief saved: {json_path}")
    print(f"  ✓ Markdown:    {md_path}")
    return json_path, md_path


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print prompt, skip API call")
    parser.add_argument("--date", default=today_str, help="Date string YYYY-MM-DD")
    parser.add_argument("--force", action="store_true", help="Regenerate even if brief exists")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"PIE Brief Generator — {args.date}")
    print(f"{'='*60}")

    # Skip if already generated today
    brief_path = BRIEFS_DIR / f"{args.date}.json"
    if brief_path.exists() and not args.force:
        print(f"  Brief already exists for {args.date}. Use --force to regenerate.")
        return

    # Load data
    print("\nLoading pipeline data...")
    flags       = load_flags()
    predictions = load_predictions()
    entities    = load_entities()
    procurement = load_procurement()
    prev_brief  = load_prev_brief()

    print(f"  Flags: {len(flags)} | Predictions: {len(predictions)} | Entities: {len(entities)}")
    print(f"  Previous brief: {prev_brief['date'] if prev_brief else 'none'}")

    # Delta
    delta = compute_delta(flags, prev_brief)
    print(f"  Delta: {delta.get('new_count',0)} new, {delta.get('resolved_count',0)} resolved")

    # Build prompt
    print("\nBuilding prompt...")
    prompt = build_prompt(flags, predictions, entities, procurement, delta)
    print(f"  Prompt length: {len(prompt):,} chars")

    if args.dry_run:
        print("\n" + "─"*60)
        print(prompt)
        print("─"*60)
        print("\n[DRY RUN] Skipping API call.")
        return

    # Call Claude
    print("\nGenerating brief via Claude API...")
    brief = call_claude(prompt)

    if not brief:
        print("  ✗ Brief generation failed — check API credits at console.anthropic.com/billing")
        print("  ⚠ Skipping brief — pipeline will continue to sync flags and predictions")
        sys.exit(0)  # Soft exit — don't block Forge sync

    # Save
    print("\nSaving brief...")
    save_brief(brief, flags, args.date)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Brief complete — {args.date}")
    print(f"{'='*60}")
    print(f"Headline: {brief.get('headline','')}")
    print(f"Lead:     {brief.get('lead_story',{}).get('title','')}")
    sig = brief.get("signal_summary", {})
    print(f"Signals:  {sig.get('total_flags',0)} flags | {sig.get('critical',0)} critical | {sig.get('new_today',0)} new")


if __name__ == "__main__":
    main()
