# -*- coding: utf-8 -*-
"""t90 后处理：9 种主题（菜单 + 顶部色点）、首屏无闪烁、预取下一页、跨页过渡、首页「一图看全」。"""
import re
NEW = [("sakura", "#fbf1f4", "🌸", "樱花粉"), ("ocean", "#031a2e", "🌊", "深海蓝"), ("amber", "#1c1108", "🍂", "秋叶琥珀"),
       ("paper", "#f4f5f7", "☁️", "云端灰白"), ("eye", "#e6f0df", "🌿", "护眼绿")]
ALLT = "night|dawn|jade|grape|" + "|".join(t for t, *_ in NEW)
META = '{night:"#070d22",dawn:"#f7f1e6",jade:"#031c1b",grape:"#150b26",' + ",".join(f'{t}:"{c}"' for t, c, *_ in NEW) + '}'
SPEC = ('<script type="speculationrules">{"prefetch":[{"source":"document","where":{"and":[{"selector_matches":".ptabs a,.pager a,#toc a,.tochome,a.vcard,#navc a"},'
        '{"not":{"selector_matches":"[href^=\\"http\\"],[href^=\\"#\\"]"}}]},"eagerness":"moderate"}]}</script>')
def apply(h, page, site, viz=None):
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
    return h
