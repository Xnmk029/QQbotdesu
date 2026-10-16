"""连上 QQ 网关 3 分钟，期间你用 QQ 给机器人发一句话，日志里会打印你的 user_openid。"""
import os, asyncio, json, time, urllib.request, websockets
from qqbot import token
tok=token()
req=urllib.request.Request("https://api.sgroup.qq.com/gateway", headers={"Authorization":f"QQBot {tok}"})
url=json.load(urllib.request.urlopen(req))["url"]
async def main():
    async with websockets.connect(url) as ws:
        hello=json.loads(await ws.recv()); hb=hello["d"]["heartbeat_interval"]/1000
        await ws.send(json.dumps({"op":2,"d":{"token":f"QQBot {tok}","intents":1<<25,"shard":[0,1]}}))
        end=time.time()+600; last=time.time(); seq=None
        print("已连接，请现在用 QQ 私聊机器人发任意一句话…", flush=True)
        while time.time()<end:
            if time.time()-last>hb*0.8:
                await ws.send(json.dumps({"op":1,"d":seq})); last=time.time()
            try: m=json.loads(await asyncio.wait_for(ws.recv(), 5))
            except asyncio.TimeoutError: continue
            seq=m.get("s") or seq
            if m.get("t")=="C2C_MESSAGE_CREATE":
                oid=m["d"]["author"]["user_openid"]; open("data/openid.txt","w").write(oid); print("已获取并保存 openid", flush=True); return
        raise SystemExit("10 分钟内没收到私聊消息，请重跑")
asyncio.run(main())
