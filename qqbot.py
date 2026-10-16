import json, os, urllib.request
APPID=os.environ.get("QQ_APPID",""); SECRET=os.environ.get("QQ_SECRET","")
API="https://api.sgroup.qq.com"
def _post(url, body, headers=None):
    r=urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type":"application/json", **(headers or {})})
    with urllib.request.urlopen(r, timeout=30) as f: return json.load(f)
def token():
    d=_post("https://bots.qq.com/app/getAppAccessToken", {"appId":APPID, "clientSecret":SECRET})
    if "access_token" not in d: raise SystemExit(f"获取 token 失败: {d}")
    return d["access_token"]
def send_c2c(openid, md, tok=None):
    tok=tok or token()
    return _post(f"{API}/v2/users/{openid}/messages", {"msg_type":2, "markdown":{"content":md}},
                 {"Authorization":f"QQBot {tok}"})
