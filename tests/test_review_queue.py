import json
import unittest
from pathlib import Path

from handbook_builder.evidence import classify_table
from handbook_builder.review import build_review_queue, propose, triage
from scripts.check_deployment import verify
from scripts.validate_review_decisions import validate


class ReviewQueueTests(unittest.TestCase):
    def test_semantic_table_treatments_are_explainable(self):
        self.assertEqual(classify_table(["Symptom","Likely cause","Fix"])[0],"guided-explanation")
        self.assertEqual(classify_table(["Spec","Value"])[0],"queryable-lookup")
        self.assertEqual(classify_table(["Product","Range","Price"])[0],"comparison")

    def test_queue_prioritizes_material_claims_and_excludes_holds(self):
        high={"record_type":"numerical-passage","statement":"FAA compliance requires a 10 V safety limit","source_candidates":[]}
        low={"record_type":"table-row","statement":"Blue","source_candidates":[]}
        self.assertLess(int(triage(high)["priority"][1]),int(triage(low)["priority"][1]))
        snapshot={"release":"test","references":[{"id":"a","publication_state":"published"}],"records":[
            {"id":"r","article_id":"a","title":"A","path":"a.md","anchor":"ch1","canonical":"ref-a","record_type":"numerical-passage","statement":"Range 10 km","source_candidates":[],"status":"unreviewed"}
        ]}
        queue=build_review_queue(snapshot)
        self.assertEqual(queue["summary"]["records"],1)
        self.assertEqual(queue["records"][0]["anchor"],"ch1")
        snapshot["references"][0]["publication_state"]="hold"
        with self.assertRaises(ValueError):build_review_queue(snapshot)

    def test_proposals_automate_only_obvious_nonclaims(self):
        metadata={"risk_reasons":["source-directory-entry"],"source_candidates":["https://example.test"],"article_source_candidates":[],"table_id":None}
        self.assertFalse(propose(metadata,1)["human_intervention"])
        claim={"risk_reasons":["performance"],"source_candidates":["https://example.test"],"article_source_candidates":[],"table_id":None}
        self.assertTrue(propose(claim,1)["human_intervention"])
        self.assertEqual(propose(claim,1)["decision"],"needs-source-check")

    def test_supported_decisions_require_exact_review_context(self):
        queue={"release":"r1","records":[{"id":"one","statement":"Range 10 km","path":"a.md"}]}
        payload={"schema_version":1,"kind":"uas-handbook-citation-review","release":"r1","decisions":{"one":{"decision":"source-supported","source_url":"https://example.test"}}}
        with self.assertRaisesRegex(ValueError,"source_passage"):validate(payload,queue)
        payload["decisions"]["one"].update({"source_passage":"Section 2, p. 4","scope":"Model A","checked_at":"2026-10-02"})
        result=validate(payload,queue)
        self.assertEqual(result["summary"]["source_supported"],1)

    def test_proposed_part108_is_not_presented_as_current_authority(self):
        root=Path(__file__).resolve().parents[1]
        text="\n".join((root/path).read_text() for path in ("components/bvlos-pathways.md","components/utm-airspace-awareness.md"))
        for stale in ("BVLOS requires a waiver or Part 108 Permit","Required under Part 108","Part 108 requires UAS","Part 108 Permits will require"):
            self.assertNotIn(stale,text)
        self.assertIn("does not itself authorize an operation",text)

    def test_exact_deployment_check_rejects_mixed_releases_and_missing_storage(self):
        commit="a"*40;release="b"*20
        responses={
            "/release.json":json.dumps({"release":release,"commit":commit}),
            "/assets/reference-data.json":json.dumps({"release":release,"commit":commit}),
            "/api/capabilities":json.dumps({"submission":False,"review":False,"attachments":False}),
            "/reference.html":f"release {release} commit {commit}",
        }
        fetch=lambda url:(responses[url.removeprefix("https://example.test")],"application/json")
        self.assertTrue(verify("https://example.test",commit,fetch=fetch)["exact_release_verified"])
        with self.assertRaisesRegex(ValueError,"not enabled"):verify("https://example.test",commit,require_storage=True,fetch=fetch)
        responses["/assets/reference-data.json"]=json.dumps({"release":"c"*20,"commit":commit})
        with self.assertRaisesRegex(ValueError,"does not match"):verify("https://example.test",commit,fetch=fetch)


if __name__=="__main__":unittest.main()
