"""Manual source monitor. Changes open local review tasks; they never change published claims."""
import argparse
import hashlib
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch_source(url):
    request=urllib.request.Request(url,headers={"User-Agent":"HandbookSourceReview/1.0"})
    with urllib.request.urlopen(request,timeout=15) as response:
        body=response.read(4*1024*1024+1)
        if len(body)>4*1024*1024:raise ValueError("Source exceeds monitor size limit; review manually")
        return hashlib.sha256(body).hexdigest()
def inspect(source,previous,today,fetch=fetch_source):
    sid=source["id"];tasks=[]
    def task(reason,revision):
        key=hashlib.sha256((sid+reason+revision).encode()).hexdigest()[:24]
        tasks.append({"id":key,"source_id":sid,"reason":reason,"observed":today.isoformat(),"state":"needs-review","scope":"Source monitoring only; unchanged content is not verification"})
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
    today=date.today()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(lambda s:inspect(s,state["sources"].get(s["id"],{}),today),data["sources"]))
    for sid,result,tasks in results:
        state["sources"][sid]=result
        for task in tasks:state["tasks"].setdefault(task["id"],task)
    args.state.parent.mkdir(parents=True,exist_ok=True);args.state.write_text(json.dumps(state,indent=2))
    print(json.dumps({"sources":len(results),"pending_review_tasks":sum(t["state"]=="needs-review" for t in state["tasks"].values()),"state_file":str(args.state),"publication_changed":False}))
if __name__=="__main__":main()
