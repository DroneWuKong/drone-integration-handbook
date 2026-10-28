"""Manual source monitor. Changes open local review tasks; they never change published claims."""
import argparse
import http.client
import hashlib
import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch_source(url):
    request=urllib.request.Request(url,headers={"User-Agent":"HandbookSourceReview/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request,timeout=15) as response:
                body=response.read(4*1024*1024+1)
                if len(body)>4*1024*1024:raise ValueError("Source exceeds monitor size limit; review manually")
                return hashlib.sha256(body).hexdigest()
        except urllib.error.HTTPError as error:
            if error.code not in (429,500,502,503,504) or attempt==2:raise
        except (http.client.RemoteDisconnected,urllib.error.URLError,TimeoutError,ConnectionError):
            if attempt==2:raise
        time.sleep(.2*(attempt+1))

def task_id(source_id,reason):
    return hashlib.sha256((source_id+"\0"+reason).encode()).hexdigest()[:24]

def merge_tasks(existing,incoming,today):
    """Keep one open task per source/reason while retaining superseded history."""
    observed_today=today.isoformat()
    groups={}
    for key,value in existing.items():
        if value.get("state")=="needs-review":
            groups.setdefault((value.get("source_id"),value.get("reason")),[]).append((key,value))
    for value in incoming:
        groups.setdefault((value["source_id"],value["reason"]),[])
    for (source_id,reason),legacy in groups.items():
        stable=task_id(source_id,reason)
        current=existing.get(stable)
        if not current or current.get("state")!="needs-review":
            seed=max((value for _,value in legacy),key=lambda value:value.get("observed",""),default={})
            current={**seed,"id":stable,"source_id":source_id,"reason":reason,"state":"needs-review"}
        observed=[value.get("observed") for _,value in legacy if value.get("observed")]
        current["first_observed"]=min(observed+[current.get("first_observed",current.get("observed",observed_today))])
        superseded=current.get("superseded_task_count",0)
        for key,value in legacy:
            if key==stable:continue
            existing[key]={**value,"state":"superseded","superseded_by":stable,"superseded_on":observed_today}
            superseded+=1
        current["superseded_task_count"]=superseded
        update=next((value for value in incoming if value["source_id"]==source_id and value["reason"]==reason),None)
        if update:
            current.update(update)
            current["first_observed"]=min(current["first_observed"],update["observed"])
            current["observation_count"]=current.get("observation_count",0)+1
        existing[stable]=current
    return existing
def inspect(source,previous,today,fetch=fetch_source):
    sid=source["id"];tasks=[]
    def task(reason,revision):
        tasks.append({"id":task_id(sid,reason),"source_id":sid,"reason":reason,"latest_revision":revision,
            "observed":today.isoformat(),"state":"needs-review","scope":"Source monitoring only; unchanged content is not verification"})
    try:
        digest=fetch(source["url"])
        if previous.get("digest") and previous["digest"]!=digest:task("source-content-changed",digest)
        result={"digest":digest,"checked":today.isoformat(),"status":"reachable"}
    except Exception as error:
        result={**previous,"checked":today.isoformat(),"status":"unavailable","error":type(error).__name__}
        task("source-unavailable",previous.get("digest","unknown"))
    age=(today-date.fromisoformat(source["accessed"])).days
    if age>=source.get("review_days",365):task("verification-due",source["accessed"])
    return sid,result,tasks
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--state",type=Path,default=ROOT/".local/source-review.json");args=p.parse_args()
    data=json.loads((ROOT/"data/evidence.json").read_text());state=json.loads(args.state.read_text()) if args.state.exists() else {"sources":{},"tasks":{}}
    today=datetime.now(timezone.utc).date()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(lambda s:inspect(s,state["sources"].get(s["id"],{}),today),data["sources"]))
    for sid,result,tasks in results:
        state["sources"][sid]=result
        merge_tasks(state["tasks"],tasks,today)
    args.state.parent.mkdir(parents=True,exist_ok=True);args.state.write_text(json.dumps(state,indent=2))
    print(json.dumps({"sources":len(results),"pending_review_tasks":sum(t["state"]=="needs-review" for t in state["tasks"].values()),"state_file":str(args.state),"publication_changed":False}))
if __name__=="__main__":main()
