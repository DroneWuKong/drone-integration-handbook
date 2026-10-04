import hashlib
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from handbook_builder.evidence import load_evidence,decorate_and_inventory
from handbook_builder.site import discover_entries
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_sources import inspect
ROOT=Path(__file__).resolve().parents[1]
class EvidenceTests(unittest.TestCase):
    def test_frozen_profile_urls_do_not_follow_directory_order(self):
        current={e.relative_path:(e.identity,e.anchor) for e in discover_entries(ROOT)}
        original=Path.iterdir
        def reverse(path):return iter(reversed(list(original(path))))
        with patch.object(Path,"iterdir",reverse):
            reordered={e.relative_path:(e.identity,e.anchor) for e in discover_entries(ROOT)}
        self.assertEqual(current,reordered)
        self.assertEqual(len(current),152)
    def test_missing_and_duplicate_sources_fail_closed(self):
        data=json.loads((ROOT/"data/evidence.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/"data").mkdir()
            data["claims"][0]["sources"]=["does-not-exist"]
            (root/"data/evidence.json").write_text(json.dumps(data))
            with self.assertRaises(ValueError):load_evidence(root)
    def test_held_text_has_no_data_records(self):
        entry=discover_entries(ROOT)[0];entry.html='<aside class="notice publication-hold urgent">Hidden specs 999 W</aside><table><tr><th>Power</th></tr><tr><td>999 W</td></tr></table>'
        _,records,tables,state=decorate_and_inventory(entry,{}, {})
        self.assertEqual((records,tables,state),([],[],"hold"))
    def test_monitor_change_failure_and_due_tasks_are_deduplicable(self):
        source={"id":"test","url":"https://example.test","accessed":"2020-01-01","review_days":365}
        a=inspect(source,{"digest":"old"},date(2026,10,1),lambda u:"new")
        b=inspect(source,{"digest":"old"},date(2026,10,1),lambda u:"new")
        self.assertEqual([t["id"] for t in a[2]],[t["id"] for t in b[2]])
        self.assertEqual({t["reason"] for t in a[2]},{"source-content-changed","verification-due"})
        def unavailable(url):raise OSError("network")
        result=inspect(source,{"digest":"old"},date(2026,10,1),unavailable)
        self.assertEqual(result[1]["digest"],"old")
        self.assertIn("source-unavailable",{t["reason"] for t in result[2]})

    def test_correction_is_draft_deduplicable_and_preserves_old_version(self):
        from prepare_correction import prepare
        data=json.loads((ROOT/"data/evidence.json").read_text());old=json.dumps(data,sort_keys=True);claim=data["claims"][0]
        proposal=prepare(data,claim["id"],"Updated public wording",claim["sources"],"Explicit scope","Evidence correction","nonsecret-report-id")
        again=prepare(data,claim["id"],"Updated public wording",claim["sources"],"Explicit scope","Evidence correction","nonsecret-report-id")
        self.assertEqual(proposal["id"],again["id"]);self.assertEqual(proposal["before"],claim)
        self.assertIsNone(proposal["proposed"]["verified"]);self.assertEqual(proposal["publication_state"],"draft")
        self.assertNotIn("statement_template",proposal["proposed"]);self.assertEqual(proposal["proposed"]["statement"],"Updated public wording")
        self.assertEqual(json.dumps(data,sort_keys=True),old)

    def test_two_column_specs_are_queryable_without_losing_original_fields(self):
        from handbook_builder.evidence import snapshot
        entry=discover_entries(ROOT)[0]
        entry.html='<table><tr><th>Property</th><th>Value</th></tr><tr><td>Voltage</td><td>5 V</td></tr><tr><td>Voltage</td><td>3.3 V</td></tr></table>'
        rendered,records,tables,state=decorate_and_inventory(entry,{}, {})
        self.assertEqual(records[0]["fields"]["Voltage"],"5 V")
        self.assertEqual(records[0]["fields"]["Property"],"Voltage")
        self.assertEqual(records[0]["status"],"unreviewed")
        self.assertFalse(records[0]["reader_alert"])
        self.assertNotIn("Evidence</th>",rendered)
        self.assertNotIn("material-review-flag",rendered)
        entry.publication_state=state
        exported=snapshot([entry],{},records,tables,"test")
        self.assertEqual(exported["references"][0]["fields"]["Voltage"],["5 V","3.3 V"])

    def test_only_material_unresolved_claims_get_reader_alerts(self):
        entry=discover_entries(ROOT)[0]
        entry.html='<p>Flight time is 25 minutes.</p><p>FAA compliance requires a 10 V safety limit.</p>'
        rendered,records,_,_=decorate_and_inventory(entry,{}, {})
        self.assertEqual(len(records),2)
        self.assertFalse(records[0]["reader_alert"])
        self.assertTrue(records[1]["reader_alert"])
        self.assertEqual(records[1]["reader_alert_priority"],"P0")
        self.assertEqual(rendered.count("material-review-flag"),1)
        self.assertIn("Review needed: regulatory / safety",rendered)
        self.assertNotIn("Evidence not yet reviewed",rendered)

    def test_deployment_commit_is_validated_and_not_invented_locally(self):
        from handbook_builder.site import _source_commit
        with patch.dict("os.environ",{},clear=True):self.assertIsNone(_source_commit())
        with patch.dict("os.environ",{"CF_PAGES_COMMIT_SHA":"a"*40},clear=True):self.assertEqual(_source_commit(),"a"*40)
        with patch.dict("os.environ",{"GITHUB_SHA":"invalid"},clear=True):self.assertIsNone(_source_commit())

    def test_asset_bytes_and_commit_change_release_but_unused_raw_data_does_not(self):
        from test_builder import BuilderTestCase
        from handbook_builder.site import build_site
        fixture=BuilderTestCase();fixture.setUp()
        try:
            root=fixture.root;image=root/"assets/example.svg";image.write_text("<svg>first</svg>")
            build_site(root,root/"site")
            first=json.loads((root/"site/release.json").read_text())["release"]
            (root/"data").mkdir();(root/"data/unused-collection.json").write_text('{"counter":1}')
            build_site(root,root/"site")
            self.assertEqual(first,json.loads((root/"site/release.json").read_text())["release"])
            image.write_text("<svg>second</svg>");build_site(root,root/"site")
            second=json.loads((root/"site/release.json").read_text())["release"];self.assertNotEqual(first,second)
            with patch.dict("os.environ",{"CF_PAGES_COMMIT_SHA":"b"*40},clear=True):build_site(root,root/"site")
            self.assertNotEqual(second,json.loads((root/"site/release.json").read_text())["release"])
            (root/"data/evidence.json").write_text('{"sources":[],"claims":[]}')
            with self.assertRaisesRegex(ValueError,"permanent identity"):discover_entries(root)
        finally:fixture.tearDown()
