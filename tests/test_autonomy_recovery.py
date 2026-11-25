import contextlib
import io
import json
import unittest
from unittest.mock import patch

from scripts import audit_autonomy


class ExistingEvidenceRecoveryTests(unittest.TestCase):
    def test_preflight_requires_active_original_trial_and_remaining_limits(self):
        summary={"provider_configured":True,"webhook_configured":True,
                 "trial":{"active":True},
                 "reservations":{"total":40,"distinct_claims_last_24h":0}}
        self.assertTrue(audit_autonomy.dispatch_ready(summary))
        for field,value in [("total",56),("total",-1),("total","40"),("distinct_claims_last_24h",2)]:
            changed={**summary,"reservations":{**summary["reservations"],field:value}}
            self.assertFalse(audit_autonomy.dispatch_ready(changed))
        self.assertFalse(audit_autonomy.dispatch_ready({**summary,"trial":{"active":False}}))
        self.assertFalse(audit_autonomy.dispatch_ready({**summary,"provider_configured":False}))
        self.assertFalse(audit_autonomy.dispatch_ready({}))

    def test_existing_recovery_never_submits_new_research_and_hides_response_ids(self):
        audit={"schema_version":1,"trial":{"present":True,"active":False},
               "reservations":{"total":44},"jobs":[{"id":"private-job","response_id":"private-response","role":"researcher"}]}
        output=io.StringIO()
        with patch.dict("os.environ",{"AUTONOMY_REVIEW_TOKEN":"private-token"},clear=True), \
             patch("sys.argv",["audit","--origin","https://uas-handbook.com","--reconcile-existing"]), \
             patch.object(audit_autonomy,"request",side_effect=[audit,{"summary":{"stale_without_response":2}},audit]) as request, \
             contextlib.redirect_stdout(output):
            audit_autonomy.main()
        paths=[call.args[2] for call in request.call_args_list]
        self.assertEqual(paths,["audit?probe=1","reconcile","audit?probe=1"])
        self.assertEqual(request.call_args_list[1].args[3],{"confirm":"existing-jobs-only"})
        result=json.loads(output.getvalue())
        self.assertEqual(result["paid_requests_started"],0)
        self.assertEqual(result["reservations"]["total"],44)
        for secret in ("private-job","private-response","private-token"):
            self.assertNotIn(secret,output.getvalue())
