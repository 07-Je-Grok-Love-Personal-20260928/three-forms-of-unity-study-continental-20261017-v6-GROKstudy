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
 ("错谬", "🚫"), ("使徒信经 ·|使徒信经：", "🕊️"), ("尼西亚信经 ·|尼西亚信经：", "👑"), ("亚他那修信经 ·|亚他那修信经：", "🛡️"), ("整体|一览|联合", "🧩"), ("体裁", "📐"), ("解决", "🔧"), ("小结", "📄"), ("参考网站", "🔗"), ("脚注", "📎"), ("十诫", "📜"), ("祷告", "🙏"), ("圣餐", "🍞"), ("圣洗礼|洗礼", "💧"), ("圣言与圣礼", "📖"), ("得称为义|称义", "🤲"),
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
        out.append(nav[last:m.start()]); out.append(f'<a href="{m.group(1)}#{m.group(2)}" data-e="{emo(m.group(2), m.group(3), lv)}">{m.group(3)}</a>'); last = m.end()  # t88：图标用 ::before 渲染，目录少约 490 个节点
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
    h = re.sub(r'<h4 class="qh">(\s*\d+[.．]\s*问[：:])', r'<h4 class="qh qq">\1', h)
    h = re.sub(r'<p class="ex">(答：)', r'<p class="ex qa">\1', h)
    return h

def _fold(h):
    def rf(m):
        n = m.group(0).count('class="rf1"')
        return f'<details class="rfx"><summary>📖 经文参考 · {n} 条</summary>{m.group(0)}</details>'
    h = re.sub(r'<div class="refs2" role="list" aria-label="经文参考">.*?</div>', rf, h, flags=re.S)
    h = re.sub(r'<p class="src">((?:(?!</p>).)*?class="srcl"(?:(?!</p>).)*)</p>',
               lambda m: f'<details class="rfx rsrc"><summary>🔗 原文页 · 学习课程</summary><p class="src">{m.group(1)}</p></details>', h, flags=re.S)
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

# ===== D · 图标记忆地图 + 问答结构图 =====
def _tile(href, e, num, title, col, i):
    return f'<a class="icm-t" href="{href}" style="--c:{col};--i:{i}" data-e="{e}"><b>{num}</b><small>{H.escape(title)}</small></a>'
def map_hc(pref):
    from c_titles import HC52, PART_COL
    t = "".join(_tile(f"{pref}{n}", HC[n], n, HC52[n][0], PART_COL[HC52[n][1]], n) for n in range(1, 53))
    key = "".join(f'<span style="--c:{c}"><i></i>{k}</span>' for k, c in PART_COL.items())
    return f'<div class="icm reveal"><div class="icm-h"><b>🧩 图标记忆地图 · 52 主日一图看完</b><span class="icm-k">{key}</span></div><div class="icm-g">{t}</div><p class="icm-n">先记图标，再记标题：看到 ❤️ 想到唯一的安慰，看到 🪞 想到律法这面镜子。点任一格跳到该主日。图标与主日标题为本站学习辅助。</p></div>'
def map_bc(pref):
    from c_titles import BC37, BC_GROUPS
    col = {n: c for _, _, c, lo, hi, _ in BC_GROUPS for n in range(lo, hi + 1)}
    t = "".join(_tile(f"{pref}{n}", BC[n], n, BC37[n][0], col[n], n) for n in range(1, 38))
    key = "".join(f'<span style="--c:{c}"><i></i>{g}</span>' for _, g, c, _, _, _ in BC_GROUPS)
    return f'<div class="icm reveal"><div class="icm-h"><b>🧩 图标记忆地图 · 比利时信条 37 条</b><span class="icm-k">{key}</span></div><div class="icm-g">{t}</div><p class="icm-n">七种颜色＝七群；图标是记忆钩（本站学习辅助）。点任一格跳到该条。</p></div>'
def map_creeds(ap, ni, at):
    import creedlib as CL
    a = "".join(_tile(f"{ap}{n}", AP[n], n, CL.AP_TITLES[n][0], "#5aa9e6", n) for n in range(1, 13))
    b = "".join(_tile(f"{ni}{n}", NI[n], n, CL.NI_TITLES[n][0], "#d4af37", n) for n in range(1, 14))
    c = "".join(_tile(f"{at}{k}", AT[k], f"{v[1]}–{v[2]}" if v[1] != v[2] else v[1], v[0], "#81b29a", i) for i, (k, v) in enumerate(CL.AT_GROUPS.items(), 1))
    return (f'<div class="icm reveal"><div class="icm-h"><b>🧩 图标记忆地图 · 三大信经</b><span class="icm-k"><span style="--c:#5aa9e6"><i></i>使徒 12 条</span><span style="--c:#d4af37"><i></i>尼西亚 13 节</span><span style="--c:#81b29a"><i></i>亚他那修 11 组</span></span></div>'
            f'<h5 class="icm-s">🕊️ 使徒信经 · 洗礼的信经</h5><div class="icm-g">{a}</div><h5 class="icm-s">👑 尼西亚信经 · 会议的信经</h5><div class="icm-g">{b}</div><h5 class="icm-s">🛡️ 亚他那修信经 · 教学的信经</h5><div class="icm-g">{c}</div>'
            '<p class="icm-n">一条一图：🌍 创造主 → 👑 独生子 → 👶 降生 → ✝️ 受难 → 🌅 复活 → ☁️ 升天 → ⚖️ 审判 → 🔥 圣灵 → ⛪ 教会 → 🕊️ 赦罪 → 🌱 复活 → ♾️ 永生。图标为本站学习辅助。</p></div>')
def qa_chart(nq, nref):
    return ('<div class="qac reveal" role="img" aria-label="问答结构图"><div class="qac-h"><b>🔎 问答结构图：每一问都是同一个形状</b></div><div class="qac-f">'
            '<div class="qac-s q"><i>Q</i><b>问</b><small>金色左条 · 粗体</small></div><span class="qac-a">➜</span>'
            '<div class="qac-s a"><i>A</i><b>答</b><small>绿色左条 · 背诵主体</small></div><span class="qac-a">➜</span>'
            '<div class="qac-s r"><i>📖</i><b>经文参考</b><small>默认折叠 · 点开核对</small></div><span class="qac-a">➜</span>'
            '<div class="qac-s l"><i>🔗</i><b>原文页 · 课程</b><small>默认折叠</small></div></div>'
            f'<div class="qac-n"><span><b>{nq}</b>问</span><span><b>52</b>主日</span><span><b>{nref}</b>条经文参考</span><span><b>3</b>部分：罪 · 救 · 谢</span></div>'
            '<p class="icm-n">背诵法：遮住答，只看问 → 说出答 → 点开 📖 核对出处。</p></div>')

YEAR = re.compile(r'(?<![\d.:：\-–])((?:1[0-9]{3}|20[0-2][0-9])(?:[–-](?:1[0-9]{3}|[0-9]{2}))?\s?年?|[3-9][0-9]{2}\s?年)(?![\d:：])')
PROT = re.compile(r'<(script|style|svg|nav|a|h[1-6]|button|summary|th|code|title|select|label|textarea)\b[^>]*>.*?</\1>', re.S)
def mark_years(h):
    i = h.find('<main'); j = h.rfind('</main>')
    body = h[i:j]; keep = []
    def stash(m): keep.append(m.group(0)); return f'\x00{len(keep)-1}\x00'
    body = PROT.sub(stash, body)
    n = [0]
    def sub_txt(seg):
        if seg.startswith('<'): return seg
        def y(m): n[0] += 1; return f'<span class="mk-d">{m.group(1)}</span>'
        return YEAR.sub(y, seg)
    body = "".join(sub_txt(x) for x in re.split(r'(<[^>]+>)', body))
    body = re.sub('\x00(\\d+)\x00', lambda m: keep[int(m.group(1))], body)
    return h[:i] + body + h[j:], n[0]

def extras(h, page, site):
    """site: 'tfu' 或 'tec'。在页面第一个 L2 之前插入图标地图/结构图；深读页加年份虚线标记。"""
    blk = ""
    if site == "tfu":
        if page == "hct": blk = qa_chart(h.count('class="qh qq"'), h.count('class="rf1"')) + map_hc("#ld")
        elif page == "bct": blk = map_bc("#bc-")
        elif page == "creedsx": blk = map_creeds("#ap-a", "#ni-a", "#at-g")
        elif page == "memory": blk = map_hc("hc.html#hd-ld") + map_bc("bc.html#bcd-a") + map_creeds("creedsx.html#ap-a", "creedsx.html#ni-a", "creedsx.html#at-g")
    else:
        if page == "hc": blk = qa_chart(h.count('class="qh qq"'), h.count('class="rf1"')) + map_hc("#ld")
        elif page == "bc": blk = map_bc("#bc-")
        elif page == "creeds": blk = map_creeds("#ap-a", "#ni-a", "#at-g")
        elif page == "memory": blk = map_creeds("apostles.html#apx-", "nicene.html#nix-", "athanasian.html#atx-") + map_hc("hc.html#ld")
    if blk:
        k = h.find('<section class="l2', h.find('<main'))
        h = h[:k] + blk + h[k:]
    n = 0
    if 'class="mklegend"' in h:
        h, n = mark_years(h)
        h = h.replace('<span class="lg lg-def">定义框</span>', '<span class="mk-d">1563 年</span><span class="lg lg-def">定义框</span>', 1)
    return h, n
