import hashlib
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from handbook_builder.autonomous import research_spec, verify_source_snapshots
from handbook_builder.maintenance import apply_verified, pending, releases, update_watchlist, cell, scheduled_records

TODAY=date(2026,10,7)
STATEMENT='The documented protocol includes a sequence field.'
BODY=b'The documented protocol includes a sequence field.'

def bundle(path='integration/repository-updates.md'):
    record={'id':'repository-test','statement':STATEMENT,'scope':'Documentation for release 1; no hardware acceptance.',
        'path':path,'record_type':'repository-candidate','source_candidates':['https://example.test/manual']}
    spec=research_spec(record,'release-1')
    packets=[]
    for role in ['researcher','verifier']:
        packets.append({'claim_id':record['id'],'role':role,'conclusion':'supports','proposed_statement':STATEMENT,
            'scope':record['scope'],'jurisdiction':'','effective_date':'2026-10-07','sources':[{
            'url':'https://example.test/manual','title':'Manual','publisher':'Example','source_class':'manufacturer',
            'passage':STATEMENT,'locator':'Protocol section','retrieved_at':'2026-10-07',
            'content_sha256':hashlib.sha256(BODY).hexdigest(),'supports':STATEMENT,'version':'1'}],
            'contradictions':[],'calculations':[],'alternatives':[],'confidence':.95,'limitations':[],'notes':''})
    return {'spec':spec,'packets':packets,'decision':{'id':'d'*24,'created_at':'2026-10-07T03:00:00Z'}}

class MaintenanceTests(unittest.TestCase):
    def test_release_date_and_preview_are_not_conflated(self):
        rows=[{'tag_name':'v2','published_at':'2026-11-01T00:00:00Z'},
            {'tag_name':'v1.1-rc','published_at':'2026-10-06T00:00:00Z','prerelease':True},
            {'tag_name':'v1','published_at':'2026-10-01T00:00:00Z'},
            {'tag_name':'draft','published_at':'2026-10-07T00:00:00Z','draft':True}]
        stable,preview=releases(rows,TODAY)
        self.assertEqual((stable['tag_name'],preview['tag_name']),('v1','v1.1-rc'))

    def test_progress_survives_deployment_and_reopens_changed_evidence(self):
        row={'id':'x','statement':'Exact statement','scope':'Exact scope','source_candidates':[], 'evidence_revision':'first'}
        first=research_spec(row,'old-release')
        self.assertEqual(first['id'],research_spec(row,'new-release')['id'])
        self.assertEqual(pending([row,row],[{'id':first['id'],'state':'complete'}],'new-release'),[])
        self.assertEqual(len(pending([{**row,'evidence_revision':'changed'}],[{'id':first['id'],'state':'complete'}],'new-release')),1)
        self.assertEqual(len(pending([row,row],[{'id':first['id'],'state':'planned'}],'new-release')),1)

    def test_passage_is_checked_against_retrieved_bytes(self):
        value=bundle()
        verify_source_snapshots(value['packets'][0],value['spec'],fetch=lambda u,a:BODY)
        with self.assertRaisesRegex(ValueError,'cited-passage-not-in'):
            verify_source_snapshots(value['packets'][0],value['spec'],fetch=lambda u,a:b'Completely different source content')

    def test_exact_fact_publication_has_history_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'data').mkdir();(root/'integration').mkdir()
            (root/'data/evidence.json').write_text('{"claims":[],"sources":[]}')
            target=root/'integration/repository-updates.md';target.write_text('# Notes\n')
            changed,outcomes=apply_verified(root,[bundle()],today=TODAY,fetch=lambda u,a:BODY)
            self.assertEqual(outcomes[0]['state'],'applied');self.assertIn('data/evidence.json',changed)
            data=json.loads((root/'data/evidence.json').read_text());self.assertEqual(data['claims'][0]['history'][0]['before']['status'],'unreviewed')
            self.assertIn('[claim:auto-',target.read_text())
            self.assertEqual(apply_verified(root,[bundle()],today=TODAY,fetch=lambda u,a:BODY)[0],[])
            updated='The documented protocol includes sequence and timestamp fields.'
            original=data['claims'][0]
            next_record={'id':original['id'],'statement':updated,'scope':original['scope'],
                'target_statement':STATEMENT,'path':'integration/repository-updates.md','record_type':'managed-claim',
                'source_candidates':['https://example.test/manual']}
            second=bundle();second['spec']=research_spec(next_record,'release-2');second['decision']['id']='e'*24
            for packet in second['packets']:
                packet.update(claim_id=original['id'],proposed_statement=updated)
                packet['sources'][0].update(passage=updated,content_sha256=hashlib.sha256(updated.encode()).hexdigest())
            changed,outcomes=apply_verified(root,[second],today=TODAY,fetch=lambda u,a:updated.encode())
            self.assertEqual(outcomes[0]['state'],'applied')
            data=json.loads((root/'data/evidence.json').read_text());self.assertEqual(data['claims'][0]['revision'],2)
            self.assertEqual(data['claims'][0]['history'][-1]['before']['statement'],STATEMENT)
            self.assertIn(updated,target.read_text());self.assertNotIn(STATEMENT,target.read_text())

    def test_changed_source_scope_mismatch_and_protected_targets_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'data').mkdir();(root/'integration').mkdir()
            (root/'data/evidence.json').write_text('{"claims":[],"sources":[]}')
            target=root/'integration/repository-updates.md';target.write_text('# Notes\n')
            for failure in ['source','scope','hold','path']:
                value=bundle();target.write_text('# Notes\n'+('publication-hold' if failure=='hold' else ''))
                if failure=='scope':value['packets'][1]['scope']='Other version'
                if failure=='path':value['spec']['path']='../secret.md'
                fetch=lambda u,a:BODY+(b' changed' if failure=='source' else b'')
                changed,outcomes=apply_verified(root,[value],today=TODAY,fetch=fetch)
                self.assertEqual(changed,[],failure);self.assertEqual(outcomes[0]['state'],'abstained',failure)

    def test_unavailable_release_keeps_previous_observation(self):
        cfg={'releases':[{'id':'test','repository':'owner/repo','sections':[]}]}
        def fail(_):raise OSError('unavailable')
        current=update_watchlist(cfg,fail,TODAY,{'items':[{'id':'test','latest':'v1','released':'2026-01-01'}]})
        self.assertEqual(current['items'][0]['latest'],'v1');self.assertEqual(current['items'][0]['status'],'unavailable')
        self.assertNotIn('<script>',cell('<script>attack</script> [link] | value'))

    def test_non_numeric_material_fact_is_in_inventory(self):
        from handbook_builder.evidence import decorate_and_inventory
        from handbook_builder.site import discover_entries
        e=discover_entries(Path(__file__).resolve().parents[1])[0]
        e.html='<p>This firmware requires a compatible driver.</p>'
        _,records,_,_=decorate_and_inventory(e,{}, {})
        self.assertEqual(len(records),1)

if __name__=='__main__':unittest.main()
