# 三项联合信条 · 欧陆改革宗深读

**版本标签：three-forms-of-unity-study-continental-20261020-v7-CCstudy**（页脚版本 v20261020-7）

比利时信条（BC）、海德堡要理问答（HC）、多特信经（Dort）的中文多页学习站：先从整本圣经与圣约看，再逐条深读，并附比较、签署书、威斯敏斯特对照、背诵与自测。

**三项联合信条与三大信经原文，以及全站中文引号引文，均逐字取自 [CCI《赞美手册》中文版](https://ccifellowship.org/books/book-of-praise)**（构建时由程序核对）。CCI 没有的内容，用《中国改革宗教会敬拜手册》2015 版（用户提供的 PDF）补充，逐字摘引并标明“出自《中国改革宗教会敬拜手册》2015 版 第 N 页”（tools/verify_pdf.py 核对）；两者都没有的（如多特信经的序言与结语）本站不补，见“来源”页。

## 当前版本链接（v7）

| 部署 | 地址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/three-forms-of-unity-study-continental-GROKstudy/ |
| Netlify | https://three-forms-of-unity-study-continental-20261020-v7-ccser.netlify.app/ |
| Surge | https://three-forms-of-unity-study-continental-20261020-v7-ccser.surge.sh/ |
| 代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/three-forms-of-unity-study-continental-GROKstudy |

命名：仓库名只含主题（…-GROKstudy，以后不再改名）；Netlify / Surge 域名为“主题-日期-版本-ccser”（这两处只能小写），每个版本一个新域名，旧域名继续在线。

姊妹站（三大公教会信经）：https://three-ecumenical-creeds-study-continental-20261020-v10-ccser.surge.sh/

## 版本记录

| 版本 | 更新内容 | 仍可访问的链接 |
|---|---|---|
| **v7 · v20261020-7**（当前） | 用敬拜手册 2015 版补 CCI 缺的内容（HC 11 个印刷小标题、主日敬拜流程），并与 CCI 逐字比对，差异列在来源页（正文仍用 CCI）；六份文件各加五步动画故事线（起因→危机→会议→文本→果效，每步带出处）与思维导图；记忆页加 7 个常见疑问；39 处自拟短语去掉引号，改为虚线“本站用语”；按文件区分配色。 | 见上表 |
| v6 · v20261017-6 | 全站字号体系（根字号 16.5–17.5px，小字 ≥14px）；每页“本页一眼”；BC、Dort 导读区块（整本圣经、圣经神学、圣约神学、改革宗读法、六角度）；辅助区块默认折叠；SVG 动画时间轴。 | 旧版本：[Netlify](https://three-forms-of-unity-study-continental-20261017-v6-grokstudy.netlify.app/) · [Surge](https://three-forms-of-unity-study-continental-20261017-v6-grokstudy.surge.sh/) |
| v5 · v20261017-5 | 每个主日、BC 条、Dort 项加“核心一句 · 记忆钩 · 为何重要”；核心速记总表；参考站互证；HC/BC/Dort 篇幅数据图与北美地图。 | 旧版本：[Netlify](https://three-forms-of-unity-study-continental-20261017.netlify.app/) · [Surge](https://three-forms-of-unity-study-continental-20261017.surge.sh/)（v1–v5 共用这两个域名，现显示 v5） |
| v4 · v20261017-4 | 深读页与记忆页加紧凑经文参考行（780 条，程序核对）；重点/难点标签。 | 同上（已被 v5 覆盖） |
| v3 · v20261017-3 | 目录可拖拽调宽；背诵版一条一行；经文参考行内编号；三信经深度对比；参考站互证。 | 同上（已被覆盖） |
| v2 · v20261017-2 | 三级/四级目录（52 主日、37 条、多特各项）；信经背诵版；52 主日罗盘；“已背熟”勾选。 | 同上（已被覆盖） |
| v1 · v20261017-1 | 首版：十二部分、52 主日、37 条、多特 63 条目、威斯敏斯特对照、记忆与 52 周计划。 | 同上（已被覆盖） |

**GitHub Pages 注意：** 仓库曾两次更名（…-20261017 → …-20261017-v6-GROKstudy → …-20261020-v7-GROKstudy → 现名），旧的 Pages 地址都已失效；GitHub 只转发仓库地址，不转发 Pages。请用上表的 Pages 地址。

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
