# 三项联合信条 · 欧陆改革宗深读（v20261020-7）

比利时信条（BC）、海德堡要理问答（HC）、多特信经（Dort）的中文多页学习站：先从整本圣经与圣约看，再逐条深读，并附比较、签署书、威斯敏斯特对照、背诵与自测。

**三项联合信条与三大信经原文，以及全站中文引号引文，均逐字取自 [CCI《赞美手册》中文版](https://ccifellowship.org/books/book-of-praise)**（构建时由程序核对）。CCI 没有的内容，用《中国改革宗教会敬拜手册》2015 版（用户提供的 PDF）补充，逐字摘引并标明“出自《中国改革宗教会敬拜手册》2015 版 第 N 页”（tools/verify_pdf.py 核对）；两者都没有的（如多特信经的序言与结语）本站不补，见“来源”页。

## 链接（v20261020-7 · GROKstudy）

| 部署 | 地址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/three-forms-of-unity-study-continental-20261020-v7-GROKstudy/ |
| Netlify | https://three-forms-of-unity-study-continental-20261020-v7-grokstudy.netlify.app/ |
| Surge | https://three-forms-of-unity-study-continental-20261020-v7-grokstudy.surge.sh/ |
| 代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/three-forms-of-unity-study-continental-20261020-v7-GROKstudy |

Netlify 与 Surge 的域名只能用小写，所以 GROKstudy 写作 grokstudy。

**旧版本（仍在线）：** v20261017-6：[Netlify](https://three-forms-of-unity-study-continental-20261017-v6-grokstudy.netlify.app/) · [Surge](https://three-forms-of-unity-study-continental-20261017-v6-grokstudy.surge.sh/)；v20261017-5：[Netlify](https://three-forms-of-unity-study-continental-20261017.netlify.app/) · [Surge](https://three-forms-of-unity-study-continental-20261017.surge.sh/)。
**注意：** 仓库每次更名后，旧的 GitHub Pages 地址（…-20261017/、…-20261017-v6-GROKstudy/）都会失效；GitHub 只转发仓库地址，不转发 Pages。请用上表的新地址。

姊妹站（三大公教会信经）：https://three-ecumenical-creeds-study-continental-20261020-v10grokstudy.surge.sh/

## 页面

index 首页（学习路径与进度）· bible 一 全本圣经 · hc 二 海德堡 · bc 三 比利时信条 · dort 四 多特信经 · compare 五 比较与签署 · westminster 六 威斯敏斯特 · hct 七 HC 原文 · bct 八 BC 原文 · dtt 九 Dort 原文 · creedsx 十 三大信经原文 · memory 十一 记忆自测 · sources 十二 来源

## 构建与检查

```bash
python3 build.py                 # 生成全部 *.html（构建时核对所有引文）
python3 tools/verify_exact.py    # 原文库与 CCI 数据逐条对照
python3 tools/check_links.py     # 站内链接、目录锚点、重复 id
python3 tools/verify_recite.py   # 背诵版（一条一行）与 CCI 原文逐字一致
python3 tools/verify_refs.py     # 经文参考行内列表 == CCI 数据
python3 tools/check_52.py        # 52 主日标题一致
python3 tools/qa_toc.py hct.html --shots   # 目录拖拽/键盘/触摸/持久化
python3 tools/audit_all.py       # 所有引号引文 vs CCI 数据与爬取页面（自拟短语见 own.py，改为虚线“本站用语”）
python3 tools/verify_pdf.py      # 敬拜手册 2015 版摘引 == PDF 印刷正文（data/pdf/pdf2015.json，按页）
python3 tools/qa.py [--open] [--shots] [--nojs] [--rm]   # Playwright：5 个宽度、no-JS、reduced-motion
```

静态站，无构建依赖；`netlify.toml` 设置了短缓存；资源链接带 `?v=` 版本号。仓库不含 CNAME、.netrc、.env 或任何密钥。
