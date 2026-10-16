#!/usr/bin/env python3
"""DeepSeek GitHub watcher: lists deepseek-ai repos, collects new commits/releases since last run.
Output: updates.json (new items) ; state in state.json. First run = baseline only."""
import json, os, sys, urllib.request, datetime as dt
ORG="deepseek-ai"; D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
os.makedirs(D,exist_ok=True)
SF=os.path.join(D,"state.json"); OF=os.path.join(D,"updates.json")
def get(url):
    r=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"deepseek-watch",**({"Authorization":"Bearer "+os.environ["GITHUB_TOKEN"]} if os.environ.get("GITHUB_TOKEN") else {})})
    with urllib.request.urlopen(r,timeout=30) as f: return json.load(f)
now=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
state=json.load(open(SF)) if os.path.exists(SF) else None
repos=[]
for p in (1,2,3):
    page=get(f"https://api.github.com/orgs/{ORG}/repos?sort=pushed&per_page=100&page={p}")
    repos+=page
    if len(page)<100: break
if state is None:
    json.dump({"last":now,"releases":{r["name"]:None for r in repos}},open(SF,"w"),indent=1)
    json.dump({"baseline":True,"since":now,"repos":len(repos),"items":[]},open(OF,"w"),ensure_ascii=False,indent=1)
    print("baseline",len(repos)); sys.exit()
since=state["last"]; items=[]
for r in repos:
    if r.get("pushed_at","")<=since and r.get("created_at","")<=since: continue
    name=r["name"]; it={"repo":name,"url":r["html_url"],"stars":r["stargazers_count"],"desc":r.get("description"),
        "new_repo":r.get("created_at","")>since,"commits":[],"releases":[]}
    try:
        for c in get(f"https://api.github.com/repos/{ORG}/{name}/commits?since={since}&per_page=30"):
            it["commits"].append({"sha":c["sha"][:7],"msg":c["commit"]["message"].split("\n")[0][:200],
              "date":c["commit"]["committer"]["date"],"url":c["html_url"]})
        for rel in get(f"https://api.github.com/repos/{ORG}/{name}/releases?per_page=5"):
            if (rel.get("published_at") or "")>since:
                it["releases"].append({"tag":rel["tag_name"],"name":rel.get("name"),"url":rel["html_url"],"body":(rel.get("body") or "")[:1500]})
    except Exception as e: it["error"]=str(e)
    if it["commits"] or it["releases"] or it["new_repo"]: items.append(it)
state["last"]=now; json.dump(state,open(SF,"w"),indent=1)
json.dump({"baseline":False,"since":since,"until":now,"items":items},open(OF,"w"),ensure_ascii=False,indent=1)
print("items",len(items))
