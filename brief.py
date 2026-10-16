"""读 data/updates.json，生成简报并私聊推送到 QQ。没有更新时什么都不发。"""
import json, os, urllib.request
from qqbot import send_c2c
u=json.load(open("data/updates.json"))
if u.get("baseline") or not u["items"]: print("无更新"); raise SystemExit
lines=[]
for it in u["items"]:
    lines.append(f"## {it['repo']}{'（新仓库）' if it['new_repo'] else ''}  ⭐{it['stars']}")
    if it["new_repo"] and it.get("desc"): lines.append(f"> {it['desc']}")
    for r in it["releases"]: lines.append(f"- 🚀 Release **{r['tag']}** {r.get('name') or ''} {r['url']}")
    for c in it["commits"][:10]: lines.append(f"- {c['msg']} ({c['sha']})")
    if len(it["commits"])>10: lines.append(f"- …另有 {len(it['commits'])-10} 条 commit")
    lines.append(it["url"])
raw="\n".join(lines)
md=f"# DeepSeek 仓库更新简报\n\n{raw}"
key=os.environ.get("DEEPSEEK_API_KEY")
if key:  # 可选：用 DeepSeek API 把 commit 归纳成人话
    prompt=("把下面 DeepSeek 官方 GitHub 仓库的更新写成中文简报：先一句话说最重要的变化，再按仓库归纳要点；"
            "新功能/新模型/新内核/性能优先，文档CI一笔带过；疑似未发布模型或代号单独标注“代码迹象，未官宣”；保留链接；Markdown，800字内。\n\n"+raw)
    r=urllib.request.Request("https://api.deepseek.com/chat/completions", method="POST",
        data=json.dumps({"model":"deepseek-chat","messages":[{"role":"user","content":prompt}]}).encode(),
        headers={"Content-Type":"application/json","Authorization":"Bearer "+key})
    try:
        with urllib.request.urlopen(r, timeout=120) as f: md=json.load(f)["choices"][0]["message"]["content"]
    except Exception as e: print("AI 摘要失败，改发原始列表:", e)
md=md[:1900]
oid=os.environ.get("QQ_OPENID") or open("data/openid.txt").read().strip()
print(send_c2c(oid, md))
