# -*- coding: utf-8 -*-
"""t89 后处理：双层地图（概念图 + 真实地图）、新增史地地图、导航簇、资源引用。"""
import re, os
import rmap, maps89, hist89
NAV = ('<div id="navc"><div class="nv-l" id="nvl">'
       '<button type="button" data-nv="back" aria-label="后退（浏览器上一步）" title="后退">←</button>'
       '<button type="button" data-nv="fwd" aria-label="前进（浏览器下一步）" title="前进">→</button>'
       '<button type="button" data-nv="top" aria-label="回到页面顶部" title="顶部">⤒</button>'
       '<button type="button" data-nv="bot" aria-label="到页面底部" title="底部">⤓</button>'
       '<a href="index.html" aria-label="回到首页" title="首页">🏠</a>'
       '<button type="button" data-nv="mk" aria-pressed="true" aria-label="笔记标记开关" title="笔记标记：开/关" hidden>🖍</button>'
       '<button type="button" data-nv="leg" aria-label="跳到标记图例" title="标记图例" hidden>🔖</button></div>'
       '<button type="button" class="nv-t" aria-expanded="false" aria-controls="nvl" aria-label="页面导航：后退、前进、顶部、底部、首页" title="页面导航">🧭</button></div>')
def sec_end(h, sid):
    i = h.find(f'id="{sid}"'); assert i > 0, sid
    i = h.rfind("<section", 0, i); depth = 0; j = i
    for m in re.finditer(r"<section\b|</section>", h[i:]):
        depth += 1 if m.group(0) != "</section>" else -1
        if depth == 0: return i + m.start()
    raise ValueError(sid)
def apply(h, page, site):
    ver = re.search(r'assets/t87\.css\?v=([^"]+)"', h).group(1)
    h = h.replace(f'<link rel="stylesheet" href="assets/t87.css?v={ver}">', f'<link rel="stylesheet" href="assets/t87.css?v={ver}"><link rel="stylesheet" href="assets/t89.css?v={ver}">', 1)
    h = h.replace(f'<script src="assets/t87.js?v={ver}" defer></script>', f'<script src="assets/t87.js?v={ver}" defer></script><script src="assets/t89.js?v={ver}" defer></script>', 1)
    REG = maps89.TFU if site == "tfu" else maps89.TEC
    NEW = maps89.TFU_NEW if site == "tfu" else maps89.TEC_NEW
    out = os.path.join(os.getcwd(), "assets", "geo"); n = 0
    def wrap(m):
        nonlocal n
        fig = m.group(0); gid = re.search(r'<linearGradient id="g(\w+)"', fig).group(1)
        if gid not in REG: return fig
        n += 1
        return rmap.build(REG[gid], out, ver, fig.replace('<figure class="map reveal">', '<figure class="map in">', 1))
    h = re.sub(r'<figure class="map reveal">.*?</figure>', wrap, h, flags=re.S)
    for pg, sid, spec in NEW:
        if pg != page + ".html": continue
        e = sec_end(h, sid)
        blk = f'<h4 class="mxh">🗺️ 史地补充：{spec["title"]}</h4>' + rmap.build(spec, out, ver)
        h = h[:e] + blk + h[e:]; n += 1
    HX = (hist89.TFU if site == "tfu" else hist89.TEC).get(page + ".html")
    if HX:
        e = sec_end(h, HX["sid"]); h = h[:e] + hist89.html(HX) + h[e:]
    if "<body" in h and 'id="navc"' not in h:
        h = h.replace("</body>", NAV + "</body>", 1)
    import t90; h = t90.apply(h, page, site)
    return h, n
