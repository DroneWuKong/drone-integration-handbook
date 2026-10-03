import json
import tempfile
import unittest
from pathlib import Path

from handbook_builder.autonomous import (
    SoftwareProvider,
    adjudicate,
    brier_score,
    claim_type,
    evidence_packet_schema,
    openai_request,
    plan_jobs,
    register_prediction,
    research_spec,
    resolve_prediction,
    verify_source_snapshots,
    validate_packet,
    write_plan,
)


def source(url, kind="manufacturer"):
    return {"url": url, "title": "Manual", "publisher": "Example", "source_class": kind,
            "passage": "The documented value is 10 km under stated conditions.", "locator": "Section 2",
            "retrieved_at": "2026-10-02", "content_sha256": "a" * 64,
            "supports": "The exact scoped value", "version": "1.0"}


def packet(claim, role, urls=("https://example.test/manual",), **changes):
    value = {"claim_id": claim, "role": role, "conclusion": "supports",
             "proposed_statement": "Model A range is manufacturer-reported as 10 km.",
             "scope": "Model A, manual version 1.0, stated conditions", "jurisdiction": "",
             "effective_date": "2026-10-02", "sources": [source(url) for url in urls],
             "contradictions": [], "calculations": [], "alternatives": [], "confidence": .9,
             "limitations": ["Manufacturer-reported; not field-observed"], "notes": ""}
    value.update(changes); return value


class AutonomousEvidenceTests(unittest.TestCase):
    def test_plan_automates_only_deterministic_metadata(self):
        queue = {"release": "r1", "records": [
            {"id": "meta", "statement": "Last updated: October 2026", "record_type": "table-row",
             "risk_reasons": ["administrative-date"], "source_candidates": [], "article_source_candidates": []},
            {"id": "range", "statement": "Range 10 km", "record_type": "table-row",
             "risk_reasons": ["performance"], "source_candidates": [], "article_source_candidates": []},
        ]}
        plan = plan_jobs(queue)
        self.assertEqual(plan["summary"]["automatic_decisions"], 1)
        self.assertEqual(plan["summary"]["background_jobs"], 2)
        self.assertEqual(plan["decisions"][0]["publication_state"], "not-a-claim")

    def test_openai_request_is_background_bounded_and_structured(self):
        record = {"id": "range", "statement": "Range 10 km", "risk_reasons": ["performance"],
                  "source_candidates": [], "article_source_candidates": []}
        request = openai_request(research_spec(record, "r1"), "verifier")
        self.assertTrue(request["background"])
        self.assertEqual(request["tools"][0]["type"], "web_search")
        self.assertEqual(request["tool_choice"], "required")
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(request["metadata"]["role"], "verifier")
        schema = evidence_packet_schema()
        self.assertEqual(schema["properties"]["sources"]["maxItems"], 3)
        self.assertEqual(schema["properties"]["notes"]["maxLength"], 800)

    def test_independent_runs_and_source_threshold_are_enforced(self):
        record = {"id": "range", "statement": "Range 10 km", "risk_reasons": ["performance"],
                  "source_candidates": [], "article_source_candidates": []}
        spec = research_spec(record, "r1")
        one = packet("range", "researcher")
        self.assertEqual(adjudicate(spec, [one])["publication_state"], "abstained")
        same = [one, packet("range", "verifier")]
        self.assertIn("minimum-independent-source-count-not-met", adjudicate(spec, same)["reasons"])
        two = [one, packet("range", "verifier", urls=("https://independent.test/report",))]
        decision = adjudicate(spec, two)
        self.assertTrue(decision["publish"]); self.assertEqual(decision["publication_state"], "corroborated")

    def test_disagreement_escalates_but_insufficient_evidence_abstains(self):
        spec = research_spec({"id": "rule", "statement": "FAA requires 10", "risk_reasons": ["regulatory"],
                              "source_candidates": [], "article_source_candidates": []}, "r1")
        a = packet("rule", "researcher", jurisdiction="US", sources=[source("https://faa.gov/rule", "controlling-authority")])
        b = packet("rule", "verifier", conclusion="contradicts", jurisdiction="US", sources=[source("https://ecfr.gov/rule", "controlling-authority")])
        result = adjudicate(spec, [a, b])
        self.assertEqual(result["publication_state"], "contradicted"); self.assertTrue(result["human_intervention"])
        b["conclusion"] = "insufficient"
        result = adjudicate(spec, [a, b])
        self.assertEqual(result["publication_state"], "contradicted")

    def test_packet_validation_and_software_replay_fail_closed(self):
        value = packet("x", "researcher")
        self.assertEqual(validate_packet(value, claim_id="x", role="researcher"), [])
        value["sources"][0]["content_sha256"] = "invented"
        self.assertIn("source-0:invalid-digest", validate_packet(value))
        provider = SoftwareProvider({("x", "researcher"): value})
        copy = provider.run({"claim_id": "x"}, "researcher"); copy["claim_id"] = "changed"
        self.assertEqual(provider.run({"claim_id": "x"}, "researcher")["claim_id"], "x")

    def test_source_digest_is_calculated_by_software_not_trusted_from_model(self):
        spec={"candidate_sources":["https://example.test/manual"]}
        value=packet("x","researcher");value["sources"][0]["content_sha256"]="0"*64
        checked=verify_source_snapshots(value,spec,fetch=lambda url,allowed:b"exact source bytes")
        import hashlib
        self.assertEqual(checked["sources"][0]["content_sha256"],hashlib.sha256(b"exact source bytes").hexdigest())
        self.assertEqual(value["sources"][0]["content_sha256"],"0"*64)

    def test_prediction_is_immutable_and_scored_against_baseline(self):
        registered = register_prediction({"question": "Will event X occur?", "probability": .8,
            "baseline_probability": .5, "data_cutoff": "2026-10-02", "target_date": "2026-12-31",
            "resolution_source": "https://example.test/outcome", "evidence_ids": ["b", "a", "a"]}, now="2026-10-02T12:00:00Z")
        resolved = resolve_prediction(registered, True, source_url="https://example.test/outcome", resolved_at="2027-01-01T00:00:00Z")
        self.assertAlmostEqual(resolved["resolution"]["brier"], .04)
        self.assertAlmostEqual(resolved["resolution"]["baseline_brier"], .25)
        self.assertEqual(registered["state"], "open")
        with self.assertRaises(ValueError): resolve_prediction(resolved, False, source_url="https://example.test/outcome")
        with self.assertRaises(ValueError): resolve_prediction(registered, True, source_url="https://example.test/other")
        with self.assertRaises(ValueError): brier_score(2, True)

    def test_atomic_plan_write(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nested/plan.json"; write_plan(path, {"ok": True})
            self.assertEqual(json.loads(path.read_text()), {"ok": True})


if __name__ == "__main__": unittest.main()
