import contextlib
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from scripts import maintain_handbook, package_maintenance, run_autonomous_evidence


class IndependentUpkeepTests(unittest.TestCase):
    def run_cycle(self, private_reads, *, configured=True):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for folder in ['data', 'field', 'integration', 'site/assets']:
            (root / folder).mkdir(parents=True, exist_ok=True)
        (root / 'data/maintenance-config.json').write_text(json.dumps({
            'repositories': [], 'releases': [], 'emerging_queries': []}))
        (root / 'data/evidence.json').write_text('{"sources":[],"claims":[]}')
        original = '# Reference\n\nThe protocol includes a sequence field.\n'
        (root / 'integration/reference.md').write_text(original)
        (root / 'site/assets/reference-data.json').write_text(json.dumps({
            'release': 'software-release', 'records': [{
                'id': 'legacy-test', 'status': 'unreviewed', 'record_type': 'prose',
                'path': 'integration/reference.md',
                'statement': 'The protocol includes a sequence field.'}]}))
        stdout, stderr = io.StringIO(), io.StringIO()
        env = {'AUTONOMY_DISPATCH_URL': 'https://uas-handbook.com',
               'AUTONOMY_REVIEW_TOKEN': 'private-test-token'} if configured else {}
        with patch.object(maintain_handbook, 'ROOT', root), \
                patch.object(maintain_handbook, 'private_rows', side_effect=private_reads) as reads, \
                patch.dict(os.environ, env, clear=True), \
                patch('sys.argv', ['maintain_handbook', '--refresh', '--apply']), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            maintain_handbook.main()
        return root, json.loads(stdout.getvalue()), stderr.getvalue(), reads

    def test_unavailable_ledger_preserves_public_upkeep_and_blocks_paid_dispatch(self):
        for failure in [urllib.error.URLError('private-test-token'),
                        urllib.error.HTTPError('https://uas-handbook.com', 401, 'Unauthorized', {}, None),
                        TimeoutError('private-test-token'), ValueError('invalid private snapshot')]:
            with self.subTest(failure=type(failure).__name__):
                root, summary, warning, reads = self.run_cycle([failure])
                reads.assert_called_once()
                self.assertFalse(summary['private_ledger_connected'])
                self.assertFalse(summary['paid_research_started'])
                self.assertEqual(summary['pending_records'], 0)
                self.assertIn('deferred', summary['research_deferred_reason'])
                self.assertNotIn('private-test-token', warning)
                queue = json.loads((root / '.local/autonomy/maintenance-queue.json').read_text())
                self.assertEqual(queue['records'], [])
                self.assertTrue((root / 'field/update-status.md').is_file())
                self.assertTrue((root / 'integration/emerging-technology-watch.md').is_file())
                self.assertEqual(json.loads((root / 'data/evidence.json').read_text())['claims'], [])
                with patch.object(package_maintenance, 'ROOT', root):
                    self.assertEqual(package_maintenance.package(Path('.local/maintenance-candidate')), 4)
                # Replay the actual next workflow command, with configured
                # credentials, and prove the blocked queue cannot send a job.
                with patch.dict(os.environ, {'AUTONOMY_DISPATCH_URL': 'https://uas-handbook.com',
                        'AUTONOMY_REVIEW_TOKEN': 'private-test-token'}, clear=True), \
                        patch('sys.argv', ['run_autonomous_evidence', '--provider', 'auto',
                            '--input', str(root / '.local/autonomy/maintenance-queue.json'),
                            '--output', str(root / '.local/autonomy/plan.json'),
                            '--request-dir', str(root / '.local/autonomy/requests')]), \
                        patch.object(run_autonomous_evidence.urllib.request, 'urlopen') as dispatch, \
                        contextlib.redirect_stdout(io.StringIO()):
                    run_autonomous_evidence.main()
                dispatch.assert_not_called()
                plan = json.loads((root / '.local/autonomy/plan.json').read_text())
                self.assertEqual(plan['summary']['started_background_jobs'], 0)

    def test_failed_decision_read_discards_partial_ledger(self):
        root, summary, _, reads = self.run_cycle([
            [{'id': 'known-spec', 'state': 'complete'}], urllib.error.URLError('offline')])
        self.assertEqual(reads.call_count, 2)
        self.assertEqual(summary['durable_specs'], 0)
        self.assertEqual(summary['pending_records'], 0)
        self.assertEqual(json.loads((root / '.local/autonomy/publication-summary.json').read_text())['changed'], [])

    def test_connected_ledger_keeps_normal_evidence_queue(self):
        _, summary, warning, reads = self.run_cycle([[], []])
        self.assertEqual(reads.call_count, 2)
        self.assertTrue(summary['private_ledger_connected'])
        self.assertEqual(summary['pending_records'], 1)
        self.assertIsNone(summary['research_deferred_reason'])
        self.assertEqual(warning, '')

    def test_missing_credentials_keep_software_planning_without_paid_calls(self):
        _, summary, warning, reads = self.run_cycle([], configured=False)
        reads.assert_not_called()
        self.assertFalse(summary['private_ledger_connected'])
        self.assertFalse(summary['paid_research_started'])
        self.assertEqual(summary['pending_records'], 1)
        self.assertIn('software planning only', summary['research_deferred_reason'])
        self.assertEqual(warning, '')

    def test_stopped_trial_defers_research_without_failing_the_metadata_cycle(self):
        root, _, _, _ = self.run_cycle([[], []])
        stopped = urllib.error.HTTPError('https://uas-handbook.com/api/autonomy/runs',
            503, 'Unavailable', {}, io.BytesIO(b'{"error":"Trial is not active"}'))
        output = io.StringIO()
        with patch.dict(os.environ, {'AUTONOMY_DISPATCH_URL': 'https://uas-handbook.com',
                'AUTONOMY_REVIEW_TOKEN': 'private-test-token'}, clear=True), \
                patch('sys.argv', ['run_autonomous_evidence', '--provider', 'dispatch',
                    '--input', str(root / '.local/autonomy/maintenance-queue.json'),
                    '--output', str(root / '.local/autonomy/plan.json'),
                    '--request-dir', str(root / '.local/autonomy/requests')]), \
                patch.object(run_autonomous_evidence.urllib.request, 'urlopen', side_effect=stopped), \
                contextlib.redirect_stdout(output):
            run_autonomous_evidence.main()
        summary = json.loads(output.getvalue())
        self.assertEqual(summary['started_background_jobs'], 0)
        self.assertIn('expired, disabled or at its workload limit', summary['deferred_reason'])
        with patch.object(package_maintenance, 'ROOT', root):
            self.assertEqual(package_maintenance.package(Path('.local/maintenance-candidate')), 4)
