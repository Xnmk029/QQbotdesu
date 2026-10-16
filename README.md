# DeepSeek 仓库更新 → QQ 简报

1. 新建一个 **私有** GitHub 仓库，把本压缩包里的全部文件（含 .github 目录）传上去。
2. 仓库 Settings → Secrets and variables → Actions，添加：
   - `QQ_APPID` = 1905808650
   - `QQ_SECRET` = 你的 AppSecret
   - （可选）`DEEPSEEK_API_KEY`：有它就用 DeepSeek 把 commit 归纳成人话，没有就发原始列表
3. Actions → get-openid → Run workflow，跑起来后 3 分钟内用 QQ 私聊机器人发一句话，会自动保存到 data/openid.txt（无需再加 Secret）。
4. Actions → deepseek-watch → Run workflow 手动跑一次（第一次只建基线，不推送）。之后每天北京时间 9 点自动运行，有更新才推送。

注意：未做个人认证的机器人只有管理员（你自己）能用，私聊推送够用。
