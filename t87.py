# -*- coding: utf-8 -*-
"""t87（2026-10-21）构建后处理，两站共用：
A 目录与正文标题的记忆图标（emoji，aria-hidden，不进入原文文字）
B 原文/背诵区：经文参考、原文页链接、学习提示默认折叠；问/答分色
C 主题切换（4 套），首屏前应用
只加标签与 class，不改任何 CCI 文字（tools/verify_exact.py 去标签后比对）。"""
import re, html as H

HC = dict(enumerate("❤️ 🪞 🍎 ⚖️ 🤝 ✝️ 💡 🔺 🌍 🛡️ 🌟 👑 🤴 👶 ⛓️ ⚰️ 🌅 ☁️ 🎺 🔥 ⛪ ♾️ 🤲 🍇 📖 💧 👪 🍞 🍷 🚫 🗝️ 🌱 🔄 1️⃣ 2️⃣ 3️⃣ ✋ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟 🙏 🌌 ✨ 🏰 🎯 🌾 🕊️ 🙌".split(), 1))
BC = dict(enumerate("☝️ 🔭 📜 📚 👑 🚧 ✅ 🔺 📖 ✝️ 🕊️ 👼 🛡️ 🍎 🧬 💎 🆘 👶 🔗 ⚖️ 🩸 🤲 🧥 🌱 🏁 🙏 ⛪ 🤝 🔍 🏛️ 📣 📏 🔏 💧 🍞 ⚔️ 🎺".split(), 1))
AP = dict(enumerate("🌍 👑 👶 ✝️ 🌅 ☁️ ⚖️ 🔥 ⛪ 🕊️ 🌱 ♾️".split(), 1))
NI = dict(enumerate("🌍 👑 💡 🔗 👶 ✝️ 🌅 🎺 🔥 📢 ⛪ 💧 🌈".split(), 1))
AT = dict(zip("ABCDEFGHIJK", "⚓ 🔺 ♾️ ☝️ 🌳 🙌 👶 🌗 🧩 ✝️ ✅".split()))
# 文档名（一级标题优先）
DOC = [("使徒信经", "🕊️"), ("尼西亚", "👑"), ("亚他那修", "🛡️"), ("海德堡", "❤️"), ("比利时", "🦁"), ("多特", "🌷"),
       ("全本圣经", "📖"), ("三大信经", "📜"), ("比较", "⚖️"), ("威斯敏斯特", "🏴"), ("记忆", "🧠"), ("来源", "📚")]
# 具体（分组/条目）在前，通用在后
KW = [
 ("错谬", "🚫"), ("使徒信经 ·|使徒信经：", "🕊️"), ("尼西亚信经 ·|尼西亚信经：", "👑"), ("亚他那修信经 ·|亚他那修信经：", "🛡️"), ("整体|一览|联合", "🧩"), ("体裁", "📐"), ("解决", "🔧"), ("小结", "📄"), ("参考网站", "🔗"), ("十诫", "📜"), ("祷告", "🙏"), ("圣餐", "🍞"), ("圣洗礼|洗礼", "💧"), ("圣言与圣礼", "📖"), ("得称为义|称义", "🤲"),
 ("圣灵神|圣灵", "🔥"), ("子神|得赎", "✝️"), ("罪和愁苦|困苦", "🪞"), ("论我们的得救|拯救", "🆘"), ("感恩", "🌱"), ("总纲|安慰", "❤️"),
 ("神与启示", "📖"), ("三位一体|一体三位|三一", "🔺"), ("创造", "🌍"), ("拣选与基督的救赎", "✝️"), ("教会", "⛪"), ("圣礼", "🔏"), ("政府|末日审判", "⚔️"),
 ("第一项", "💎"), ("第二项", "✝️"), ("第三、四项", "🌱"), ("第五项", "🛡️"),
 # 多特条目
 ("定罪|刑罚|公义所要求", "⚖️"), ("差爱子", "🎁"), ("福音的传讲|普世宣告", "📣"), ("两种结局", "🔀"), ("不信", "🌑"), ("定旨", "📜"),
 ("确信", "🔒"), ("如何教导", "📚"), ("弃绝", "🌫️"), ("婴幼|儿女", "👶"), ("赞美", "🎶"), ("满足了", "✅"), ("无限价值|无价", "💠"),
 ("有人信|其他人蒙召就", "🌟"), ("果效", "🍇"), ("拣选", "💎"), ("堕落", "🍎"), ("败坏", "🦠"), ("无能", "⛓️"), ("余光", "🕯️"), ("律法", "📜"),
 ("需要福音", "🆘"), ("福音只给", "🗺️"), ("呼召", "📯"), ("蒙召却没有", "🚪"), ("归信|重生", "🌱"), ("深不可测", "🌌"), ("礼物", "🎁"),
 ("正确态度", "🙏"), ("自由意志", "🗽"), ("罪性|软弱|严重的罪|犯罪", "🩹"), ("保守|持守", "🛡️"), ("迷失", "🧭"), ("更新", "🔄"), ("撒但", "🐍"),
 # 通用
 ("救恩史|四幕", "🎬"), ("圣约|三约|约的", "🤝"), ("基督论|基督", "✝️"), ("时间线", "🕰️"), ("地理|地图|区域", "🗺️"), ("故事线", "🎞️"), ("思维导图|导图", "🧠"),
 ("为什么|成因|为何", "❓"), ("异端", "⚠️"), ("误解", "🙅"), ("应用|牧养|使用", "🌱"), ("人物", "👤"), ("数据|篇幅|词频", "📊"), ("参考站|互证", "🔗"),
 ("拉丁|希腊|词义|译本|编号", "🔤"), ("对照|比较|对比|异同|相同与不同|同心圆|重叠", "⚖️"), ("威斯敏斯特|OPC", "🏴"), ("签署|认可|接受", "✍️"), ("敬拜|礼仪", "🎶"),
 ("口诀", "🎵"), ("翻卡", "🃏"), ("自测", "📝"), ("总结|一页", "📄"), ("计划", "📅"), ("速记|核心", "🎯"), ("逐字|CCI|原文", "📚"), ("版本", "🏷️"),
 ("方法|怎样保证", "🧪"), ("抓取", "🗄️"), ("导言|说明|总览|结构|目录|读法", "🧭"), ("逐句|逐条|逐组|逐项|分段|深读|解读|精义|专题|五问|六个角度|角度", "🔍"),
 ("圣经", "📖"), ("疑问", "❓"), ("分层|揭示|护栏", "🧱"), ("交叉引用", "🔗"), ("改革者", "🔥"), ("东方|西方", "🧭"), ("会议", "🏛️"), ("机构立场", "🏛️"),
 ("差别|差异", "↔️"), ("安息日", "🕯️"), ("教会生活", "⛪"), ("缺口|没有", "🕳️"), ("特点", "✨"), ("补充", "➕"), ("关系", "🔗")]
KWC = [(re.compile(p), e) for p, e in KW]
DOCC = [(re.compile(p), e) for p, e in DOC]
FALL = {1: "📘", 2: "🔹", 3: "▫️"}

def emo(i, title, lvl):
    t = H.unescape(re.sub(r"<[^>]+>", "", title))
    m = re.search(r"(?:^|-)ld(\d+)$", i) or (re.search(r"主日(\d+) · ", t) if lvl == 3 else None)
    if m and 1 <= int(m.group(1)) <= 52: return HC[int(m.group(1))]
    m = re.match(r"(?:bcd-a|bc-)(\d+)$", i)
    if m: return BC[int(m.group(1))]
    m = re.match(r"(?:ap-a|apx-)(\d+)$", i)
    if m and int(m.group(1)) in AP: return AP[int(m.group(1))]
    m = re.match(r"(?:ni-a|nix-)(\d+)$", i)
    if m and int(m.group(1)) in NI: return NI[int(m.group(1))]
    m = re.match(r"(?:at-g|atx-)([A-K])$", i)
    if m: return AT[m.group(1)]
    if lvl == 1:
        for r, e in DOCC:
            if r.search(t): return e
    t2 = re.sub(r"^[\d.]+\s*", "", t)
    t2 = re.sub(r"^第[一二三四五六七八九十百\d]+条\s*", "", t2)
    for r, e in KWC:
        if r.search(t2): return e
    return FALL.get(lvl, "🔹")

def te(e): return f'<span class="te" aria-hidden="true">{e}</span>'

def _toc(nav):
    def lvl_of(pos):
        k = nav.rfind('<li class="t', 0, pos)
        return int(nav[k + 12]) if k >= 0 else 2
    out = []; last = 0
    for m in re.finditer(r'<a href="([^"#]*)#([^"]+)">(.*?)</a>', nav):
        lv = lvl_of(m.start())
        out.append(nav[last:m.start()]); out.append(f'<a href="{m.group(1)}#{m.group(2)}">{te(emo(m.group(2), m.group(3), lv))}{m.group(3)}</a>'); last = m.end()
    out.append(nav[last:])
    return "".join(out).replace('href="index.html">🏠 首页', 'href="index.html">' + te("🏠") + '首页')

SVG = re.compile(r'<svg class="ic[^"]*"[^>]*>.*?</svg>', re.S)
def _body(h):
    h = re.sub(r'(<section class="l1" id="([^"]+)"><header class="l1h[^"]*"><span class="ico">.*?</span><div><div class="kick">[^<]*</div><h2>)(.*?)(</h2>)',
               lambda m: m.group(1) + te(emo(m.group(2), m.group(3), 1)) + m.group(3) + m.group(4), h, flags=re.S)
    h = re.sub(r'(<section class="l2[^"]*" id="([^"]+)"><h3><span class="n">[^<]*</span>)(.*?)(</h3>)',
               lambda m: m.group(1) + te(emo(m.group(2), m.group(3), 2)) + SVG.sub('', m.group(3), 1) + m.group(4), h, flags=re.S)
    h = re.sub(r'(<section class="l3[^"]*" id="([^"]+)"><h4 class="l3h"><span class="n3">[^<]*</span>)(.*?<span class="l3x">)(.*?)(</span>)',
               lambda m: m.group(1) + te(emo(m.group(2), m.group(4), 3)) + SVG.sub('', m.group(3), 1) + m.group(4) + m.group(5), h, flags=re.S)
    return h

def _qa(h):
    h = re.sub(r'<h4 class="qh">(\s*\d+\.\s*问：)', r'<h4 class="qh qq">\1', h)
    h = re.sub(r'<p class="ex">(答：)', r'<p class="ex qa">\1', h)
    return h

def _fold(h):
    def rf(m):
        n = m.group(0).count('class="rf1"')
        return f'<details class="rfx"><summary><span class="rxs">📖 经文参考</span><small>{n} 条 · 点开</small></summary>{m.group(0)}</details>'
    h = re.sub(r'<div class="refs2" role="list" aria-label="经文参考">.*?</div>', rf, h, flags=re.S)
    h = re.sub(r'<p class="src">((?:(?!</p>).)*?class="srcl"(?:(?!</p>).)*)</p>',
               lambda m: f'<details class="rfx rsrc"><summary><span class="rxs">🔗 原文页 · 学习课程</span><small>点开</small></summary><p class="src">{m.group(1)}</p></details>', h, flags=re.S)
    h = re.sub(r'<div class="cws ([^"]*)">(.*?</div>)</div>',
               lambda m: f'<details class="rfx rtip"><summary><span class="rxs">💡 学习提示</span><small>核心一句 · 记忆钩 · 为何重要</small></summary><div class="cws {m.group(1)}">{m.group(2)}</div></details>', h, flags=re.S)
    return h

BAR = ('<div class="rxbar" role="group" aria-label="背诵版折叠"><b>🎙️ 干净背诵版</b><span>经文参考、原文链接与学习提示默认折叠，需要时点开。</span>'
       '<button class="btn" type="button" data-rx="open">📖 展开全部</button><button class="btn ghost" type="button" data-rx="close">🙈 全部收起</button>'
       '<span class="qaleg"><i class="qb">Q</i>问 <i class="ab">A</i>答</span></div>')
THEMES = [("night", "🌌", "深夜星空", "#070d22"), ("dawn", "🌅", "晨光暖白", "#f7f1e6"), ("jade", "🏞️", "青绿山水", "#031c1b"), ("grape", "🍇", "葡萄紫韵", "#150b26")]
INIT = ('<script>try{var T=localStorage.getItem("ui.theme");if(T&&/^(night|dawn|jade|grape)$/.test(T)){document.documentElement.setAttribute("data-theme",T);'
        'var M={night:"#070d22",dawn:"#f7f1e6",jade:"#031c1b",grape:"#150b26"};document.querySelector(\'meta[name="theme-color"]\').setAttribute("content",M[T])}}catch(e){}</script>')
def switcher():
    return ('<div id="thm"><button id="thmb" class="fab2" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="thmm" title="切换主题配色">🎨<span>主题</span></button>'
            '<div id="thmm" role="menu" aria-label="主题配色">' + "".join(
                f'<button type="button" role="menuitemradio" data-theme-set="{k}" style="--sw:{c}"><i>{e}</i>{n}</button>' for k, e, n, c in THEMES) + '</div></div>')

def post(h, fold=False):
    h = h.replace('<link rel="stylesheet" href="assets/styles.css', INIT + '<link rel="stylesheet" href="assets/styles.css', 1)
    ver = re.search(r'assets/styles\.css\?v=([^"]+)"', h).group(1)
    h = h.replace('<link rel="stylesheet" href="assets/styles.css?v=' + ver + '">', '<link rel="stylesheet" href="assets/styles.css?v=' + ver + '"><link rel="stylesheet" href="assets/t87.css?v=' + ver + '">', 1)
    h = h.replace('<script src="assets/app.js?v=' + ver + '" defer></script>', '<script src="assets/app.js?v=' + ver + '" defer></script><script src="assets/t87.js?v=' + ver + '" defer></script>', 1)
    a = h.find('<nav id="toc"'); b = h.find('</nav>', a)
    h = h[:a] + _toc(h[a:b]) + h[b:]
    main = h.find('<main id="main">')
    h = h[:main] + _body(h[main:])
    h = _qa(h)
    if fold:
        h = _fold(h)
        if 'class="rfx' in h:
            k = h.find('<section class="l1"')
            h = h[:k] + BAR + h[k:]
    h = h.replace('<button id="tocbtn"', switcher() + '<button id="tocbtn"', 1)
    return h
