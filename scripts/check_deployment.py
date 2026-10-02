"""Verify an exact deployed handbook release and its advertised capabilities."""

import argparse
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

COMMIT=re.compile(r"^[0-9a-f]{40}$")
RELEASE=re.compile(r"^[0-9a-f]{20}$")

def http_fetch(url):
    request=urllib.request.Request(url,headers={"User-Agent":"HandbookDeploymentCheck/1.0"})
    with urllib.request.urlopen(request,timeout=20) as response:
        return response.read().decode("utf-8"),response.headers.get("content-type","")

def verify(base_url,expected_commit,require_storage=False,require_attachments=False,fetch=http_fetch):
    if not COMMIT.fullmatch(expected_commit):raise ValueError("Expected commit must be a full lowercase Git SHA")
    base=base_url.rstrip("/")
    paths=("/release.json","/assets/reference-data.json","/api/capabilities","/reference.html")
    with ThreadPoolExecutor(max_workers=len(paths)) as pool:
        raw=dict(zip(paths,pool.map(lambda path:fetch(base+path),paths)))
    def get(path,json_expected=False):
        body,content_type=raw[path]
        if json_expected:
            try:return json.loads(body)
            except json.JSONDecodeError as error:raise ValueError(f"{path} did not return JSON") from error
        return body
    marker=get("/release.json",True)
    data=get("/assets/reference-data.json",True)
    capabilities=get("/api/capabilities",True)
    reference=get("/reference.html")
    if marker.get("commit")!=expected_commit:raise ValueError("Deployment commit does not match expected commit")
    if not RELEASE.fullmatch(marker.get("release", "")):raise ValueError("Invalid release marker")
    if data.get("commit")!=expected_commit or data.get("release")!=marker["release"]:raise ValueError("Public data snapshot does not match release marker")
    if marker["release"] not in reference:raise ValueError("Reference page does not identify the release")
    for name in ("submission","review","attachments"):
        if not isinstance(capabilities.get(name),bool):raise ValueError("Invalid capability response")
    if require_storage and not (capabilities["submission"] and capabilities["review"]):raise ValueError("Durable submission/review is not enabled")
    if require_attachments and not capabilities["attachments"]:raise ValueError("Attachment storage is not enabled")
    return {"base_url":base,"release":marker["release"],"commit":expected_commit,"capabilities":capabilities,"exact_release_verified":True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url")
    parser.add_argument("--expected-commit",required=True)
    parser.add_argument("--require-storage",action="store_true")
    parser.add_argument("--require-attachments",action="store_true")
    args=parser.parse_args()
    print(json.dumps(verify(args.base_url,args.expected_commit,args.require_storage,args.require_attachments),indent=2))

if __name__=="__main__":main()
