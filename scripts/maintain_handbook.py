#!/usr/bin/env python3
"""Nightly discovery, release checks, exact fact promotion and durable planning."""
import argparse
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from handbook_builder.maintenance import (GitHubReader, apply_verified, discover, emerging_watch,
    json_write, pending, render_emerging, render_watch, scheduled_records, update_watchlist)
from handbook_builder.review import extract_article_sources

def read(path, default):
    return json.loads(path.read_text()) if path.exists() else default

def private_rows(origin, token, resource):
    from urllib.parse import urlsplit, urlencode
    parsed=urlsplit(origin)
    if parsed.scheme!='https' or parsed.hostname!='uas-handbook.com' or parsed.path not in ('','/'):
        raise ValueError('Production maintenance origin must be https://uas-handbook.com')
    cursor=None;rows=[]
    for _ in range(100):
        suffix='?'+urlencode({'cursor':cursor}) if cursor else ''
        request=urllib.request.Request(origin.rstrip('/')+'/api/autonomy/'+resource+suffix,
            headers={'authorization':'Bearer '+token,'user-agent':'HandbookMaintenance/1.0'})
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):raise ValueError('Private API redirect rejected')
        with urllib.request.build_opener(NoRedirect()).open(request,timeout=20) as response:
            body=response.read(4*1024*1024+1)
            if len(body)>4*1024*1024:raise ValueError('Private response too large')
            page=json.loads(body)
        if not isinstance(page,dict) or not isinstance(page.get('rows'),list) or not all(isinstance(row,dict) for row in page['rows']):
            raise ValueError('Invalid private evidence page')
        rows.extend(page['rows']);new=page.get('next_cursor')
        if not new:return rows
        if new==cursor:raise ValueError('Nonadvancing private cursor')
        cursor=new
    raise ValueError('Private pagination exceeded bounded limit')

def private_evidence(origin, token):
    """An unavailable ledger must stop paid dispatch, not public metadata upkeep."""
    state={'configured':bool(origin and token),'connected':False,'deferred_reason':None}
    if not state['configured']:
        state['deferred_reason']='Dispatcher credentials not configured; software planning only'
        return [],[],state
    try:
        ledger=private_rows(origin,token,'ledger')
        bundles=private_rows(origin,token,'decisions')
    except (OSError,ValueError,KeyError,TypeError) as error:
        # Discard partial reads: neither duplicate detection nor publication
        # may rely on an incomplete private snapshot. Do not log response bodies.
        state.update(error_type=type(error).__name__,
            deferred_reason='Private evidence unavailable; factual publication and paid dispatch deferred')
        return [],[],state
    state['connected']=True
    return ledger,bundles,state

def correction_candidates(bundles, current):
    records=[];by_id={r['id']:r for r in current}
    for bundle in bundles:
        spec=bundle['spec'];original=by_id.get(spec['claim_id'])
        if not original or original['statement']!=spec.get('target_statement',spec['statement']):continue
        for packet in bundle.get('packets',[]):
            proposed=packet.get('proposed_statement','').strip();scope=packet.get('scope','').strip()
            if not proposed or not scope or (proposed==spec['statement'] and scope==spec.get('scope','')):continue
            if packet.get('confidence',0)<.75 or not packet.get('sources'):continue
            records.append({**original,'statement':proposed,'target_statement':original['statement'],'scope':scope,
                'source_candidates':sorted(set(original.get('source_candidates',[])+[s['url'] for s in packet['sources']])),
                'evidence_revision':spec.get('evidence_revision',''),'record_type':original['record_type']})
            break
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh',action='store_true',help='Read public release/repository metadata')
    parser.add_argument('--apply',action='store_true',help='Apply only independently verified exact facts')
    args=parser.parse_args();today=date.today()
    config=read(ROOT/'data/maintenance-config.json',{})
    changed=[];candidates=[];observations=[]
    if args.refresh:
        reader=GitHubReader(os.environ.get('GITHUB_TOKEN',''))
        status=update_watchlist(config,reader,today,read(ROOT/'data/update-status.json',{}))
        emerging=emerging_watch(config,reader,today,read(ROOT/'data/emerging-watch.json',{}))
        discovery_config={**config,'repositories':config['repositories']+[
            {'repository':p['repository'],'paths':['README.md']} for p in emerging['projects'][:3]
            if p['repository'] not in {r['repository'] for r in config['repositories']}]}
        candidates,observations=discover(discovery_config,reader,today)
        for path,value in [('data/update-status.json',status),('data/emerging-watch.json',emerging)]:json_write(ROOT/path,value);changed.append(path)
        for path,value in [('field/update-status.md',render_watch(status)),('integration/emerging-technology-watch.md',render_emerging(emerging))]:(ROOT/path).write_text(value);changed.append(path)
        json_write(ROOT/'.local/autonomy/discovery.json',{'records':candidates,'observations':observations})
    else:
        candidates=read(ROOT/'.local/autonomy/discovery.json',{}).get('records',[])
    snapshot=read(ROOT/'site/assets/reference-data.json',{})
    registry=read(ROOT/'data/evidence.json',{})
    sources=registry['sources'];source_state=read(ROOT/'.local/source-review.json',{})
    records=scheduled_records(snapshot,sources,source_state,today,read(ROOT/'data/update-status.json',{}).get('items',[]))
    leads=extract_article_sources(ROOT,records)
    for record in records:
        record['article_source_candidates']=leads.get(record['path'],[])
        import hashlib
        urls=set(record.get('source_candidates',[])+record['article_source_candidates'])
        fingerprints={s['url']:source_state.get('sources',{}).get(s['id'],{}).get('digest','unknown') for s in sources if s['url'] in urls}
        watched=read(ROOT/'data/update-status.json',{}).get('items',[])
        versions={x['id']:x.get('latest') for x in watched if record['path'] in x['sections']}
        if fingerprints or versions:record['evidence_revision']=hashlib.sha256(json.dumps({'sources':fingerprints,'versions':versions},sort_keys=True).encode()).hexdigest()
    records+=candidates
    origin=os.environ.get('AUTONOMY_DISPATCH_URL','').strip();token=os.environ.get('AUTONOMY_REVIEW_TOKEN','').strip()
    ledger,bundles,private_state=private_evidence(origin,token)
    if private_state.get('error_type'):
        print('::warning::Private evidence unavailable ('+private_state['error_type']+'); public metadata upkeep continues, paid dispatch is deferred.',file=sys.stderr)
    if args.apply:
        applied,outcomes=apply_verified(ROOT,bundles,today=today);changed+=applied
        json_write(ROOT/'.local/autonomy/publication-summary.json',{'outcomes':outcomes,'changed':applied})
    if args.refresh:
        from datetime import timedelta
        status['repositories']=observations
        status['sources']=[{'title':s['title'],'url':s['url'],'accessed':s['accessed'],
            'checked':source_state.get('sources',{}).get(s['id'],{}).get('checked','not attempted'),
            'status':source_state.get('sources',{}).get(s['id'],{}).get('status','not checked'),
            'due':(date.fromisoformat(s['accessed'])+timedelta(days=s.get('review_days',365))).isoformat()}
            for s in read(ROOT/'data/evidence.json',{})['sources']]
        json_write(ROOT/'data/update-status.json',status)
        (ROOT/'field/update-status.md').write_text(render_watch(status))
    # Corrected wording is independently rechecked; the first model suggestion
    # never becomes a public patch. Stable ledger identities prevent repeats.
    records+=correction_candidates(bundles,records)
    dispatch_blocked=private_state['configured'] and not private_state['connected']
    queue={'release':snapshot['release'],'records':[] if dispatch_blocked else pending(records,ledger,snapshot['release'])}
    json_write(ROOT/'.local/autonomy/maintenance-queue.json',queue)
    json_write(ROOT/'.local/autonomy/changed-files.json',sorted(set(changed)))
    print(json.dumps({'release_checks':len(config['releases']) if args.refresh else 0,
        'repository_candidates':len(candidates),'pending_records':len(queue['records']),
        'durable_specs':len(ledger),'changed_files':len(set(changed)),
        'private_ledger_connected':private_state['connected'],
        'research_deferred_reason':private_state['deferred_reason'],
        'paid_research_started':False},indent=2))
if __name__=='__main__':main()
