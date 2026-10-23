# -*- coding: utf-8 -*-
"""t90 后处理：9 种主题（菜单 + 顶部色点）、首屏无闪烁、预取下一页、跨页过渡、首页「一图看全」。"""
import re
NEW = [("sakura", "#fbf1f4", "🌸", "樱花粉"), ("ocean", "#031a2e", "🌊", "深海蓝"), ("amber", "#1c1108", "🍂", "秋叶琥珀"),
       ("paper", "#f4f5f7", "☁️", "云端灰白"), ("eye", "#e6f0df", "🌿", "护眼绿")]
ALLT = "night|dawn|jade|grape|" + "|".join(t for t, *_ in NEW)
META = '{night:"#070d22",dawn:"#f7f1e6",jade:"#031c1b",grape:"#150b26",' + ",".join(f'{t}:"{c}"' for t, c, *_ in NEW) + '}'
SPEC = ('<script type="speculationrules">{"prefetch":[{"source":"document","where":{"and":[{"selector_matches":".ptabs a,.pager a,#toc a,.tochome,a.vcard,#navc a"},'
        '{"not":{"selector_matches":"[href^=\\"http\\"],[href^=\\"#\\"]"}}]},"eagerness":"moderate"}]}</script>')
# t90 逐句精简（只改本站说明文字；每条须恰好命中一次）
EDITS = {("tfu", "dort"): [("下面把所有错谬原文列出（点开看开头的驳斥）；<b>不是 CCI 的目录，而是本站从“错谬反驳”页面分条列出，文字取自原文</b>。",
                            "错谬原文全列（点开看驳斥）；<b>本站从错谬反驳页面分条列出，不是 CCI 的目录，文字取自原文</b>。")],
         ("tfu", "bible"): [("；先看它们各是什么，再看三份文件里“约”字实际出现在哪里。", "；先看各指什么，再看三份文件哪里真用到约字。"),
                            ("下面是本站对 CCI 脚注的统计（按“书卷名＋章”计次，仅是粗略指示，不等于引用节数）。", "本站统计 CCI 脚注：按书卷名＋章计次，只作粗略指示，不等于引用节数。")]}
def apply(h, page, site, viz=None):
    for o, n in EDITS.get((site, page), []):
        c = h.count(o)
        if c != 1: print("t90edit MISS", site, page, c, o[:20]); continue
        h = h.replace(o, n, 1)
    ver = re.search(r'assets/t89\.css\?v=([^"]+)"', h).group(1)
    h = h.replace(f'<link rel="stylesheet" href="assets/t89.css?v={ver}">', f'<link rel="stylesheet" href="assets/t89.css?v={ver}"><link rel="stylesheet" href="assets/t90.css?v={ver}">', 1)
    h = h.replace(f'<script src="assets/t89.js?v={ver}" defer></script>', f'<script src="assets/t89.js?v={ver}" defer></script><script src="assets/t90.js?v={ver}" defer></script>', 1)
    # 首屏主题（在 CSS 之前执行，无闪烁）
    a = '/^(night|dawn|jade|grape)$/'; assert a in h, page
    h = h.replace(a, f'/^({ALLT})$/', 1)
    h = re.sub(r'var M=\{night:"#070d22",dawn:"#f7f1e6",jade:"#031c1b",grape:"#150b26"\}', 'var M=' + META, h, count=1)
    # 菜单
    m = re.search(r'(<div id="thmm"[^>]*>.*?data-theme-set="grape"[^>]*>.*?</button>)', h, re.S)
    if m:
        add = "".join(f'<button type="button" role="menuitemradio" data-theme-set="{t}" style="--sw:{c}"><i>{e}</i>{n}</button>' for t, c, e, n in NEW)
        h = h[:m.end()] + add + h[m.end():]
    m = re.search(r'(<div class="thbar"[^>]*>.*?data-theme-set="grape"[^>]*>.*?</button>)', h, re.S)
    if m:
        add = "".join(f'<button type="button" role="menuitemradio" data-theme-set="{t}" style="--sw:{c}" title="{n}"><i></i>{e}<b>{n}</b></button>' for t, c, e, n in NEW)
        h = h[:m.end()] + add + h[m.end():]
    # 预取（支持 Speculation Rules 的浏览器：悬停/按下链接时预取同站页面）
    h = h.replace('</body>', SPEC + '</body>', 1)
    if viz: h = viz(h, page)
    if page in ('index', 'index.html') and os.path.exists('data/creeds.json') and 't90viz' not in h:
        m = re.search(r'<div class="stats">(?:<div>.*?</div>)+</div>', h, re.S)
        if m: h = h[:m.end()] + viz_index('data', creeds=(site != 'tfu')) + h[m.end():]
    return h

# ---------- 首页「一图看全」：由 CCI 数据实时统计（本站统计） ----------
import json, os
def _txt(blocks):
    return sum(len(re.sub(r'⟦\d+⟧|\s', '', b.get('x', ''))) for b in blocks if isinstance(b, dict) and isinstance(b.get('x', ''), str) and b.get('t') != 'ref')
def _bars(rows, unit):
    mx = max(v for _, v, _ in rows)
    return '<ul class="t90bars">' + ''.join(
        f'<li><span>{n}</span><span class="bar" aria-hidden="true"><i style="--v:{v/mx:.3f};--c:var({c})"></i></span><em>{v:,}{unit}</em></li>' for n, v, c in rows) + '</ul>'
def _axis(pts, lo=None, hi=None):
    out, prev = [], None
    for y, n, c in pts:
        y0 = int(str(y)[:4]); gap = f'<small>距上一项 {y0-prev} 年</small>' if prev else ''
        out.append(f'<li style="--c:var({c})"><b>{y}</b><span>{n}</span>{gap}</li>'); prev = y0
    return '<ol class="t90tl">' + ''.join(out) + '</ol>'
def viz_index(datadir, creeds=False):
    J = lambda f: json.load(open(os.path.join(datadir, f + '.json'), encoding='utf-8'))
    bc, hc, dt = J('bc'), J('hc'), J('dort')
    # 与比较页／总览页的字数图同一算法（quotes.py：CCI 中文本正文，不含脚注）
    import quotes as Q
    nhc = sum(len(Q.HC[q][0]) + len(Q.HC[q][1]) for q in Q.HC); nbc = sum(len(Q.BC[n]) for n in Q.BC); ndt = sum(len(v) for v in Q.DORT.values())
    rows = [('比利时信条', nbc, '--gold'), ('海德堡要理问答', nhc, '--f'), ('多特信经（含驳谬）', ndt, '--g')]
    if creeds:
        cr = J('creeds'); ct = lambda k: len(re.sub(r"\s|\d+\)", "", "".join(cr[k]['paras'])))
        rows = [('使徒信经', ct('apostles'), '--qc'), ('尼西亚信经', ct('nicene'), '--qc'), ('亚他那修信经', ct('athanasian'), '--qc')] + rows
    # 海德堡三部：各部起始问＝该部标题所在主日的第一问（第一部标题在第 1 主日第 2 问之后，故从第 3 问起）
    qn = lambda l: [int(m.group(1)) for b in l['blocks'] if b.get('t') == 'h4' for m in [re.match(r'(\d+)\s*[．.]\s*问', b.get('x', ''))] if m]
    allq = sorted(q for l in hc['lds'] for q in qn(l))
    st = {}
    for l in hc['lds']:
        g = l.get('group') or ''
        for key in ('第一部', '第二部', '第三部'):
            if g.startswith(key): st[key] = 3 if key == '第一部' else min(qn(l))
    b1, b2, b3 = st['第一部'], st['第二部'], st['第三部']
    parts = {'引言 安慰': sum(q < b1 for q in allq), '第一部 罪与愁苦': sum(b1 <= q < b2 for q in allq),
             '第二部 得救': sum(b2 <= q < b3 for q in allq), '第三部 感恩': sum(q >= b3 for q in allq)}
    prow = [(k, v, c) for (k, v), c in zip(parts.items(), ['--mut', '--abd', '--f', '--g'])]
    pts = [(1561, '比利时信条', '--gold'), (1563, '海德堡', '--f'), ('1618–19', '多特会议', '--g')]
    lo, hi = 1555, 1625
    if creeds: pts = [(325, '尼西亚', '--qc'), (381, '君士坦丁堡', '--qc')] + pts; lo, hi = 300, 1650
    return ('<section class="t90viz t90-in" aria-label="一图看全"><h3>📊 一图看全：原文篇幅与年代</h3>'
            '<p class="sub">本站统计：字数＝CCI 中文本正文（不含脚注），与<a href="compare.html">比较页</a>的字数图同一算法；年代为各文件定稿或会议年份。</p>'
            + _bars(rows, ' 字') + '<h3 style="margin-top:16px">🔢 海德堡要理问答各部问数</h3>' + _bars(prow, ' 问')
            + '<h3 style="margin-top:16px">🗓️ 年代刻度</h3>' + _axis(pts, lo, hi) + '</section>')
