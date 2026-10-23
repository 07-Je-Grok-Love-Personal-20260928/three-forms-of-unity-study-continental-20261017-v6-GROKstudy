# -*- coding: utf-8 -*-
"""t89 双层地图：概念示意图（页内 SVG，随主题变色）+ 真实地图（Natural Earth 海岸线/河流/湖泊，
本地预投影为静态 SVG 文件 assets/geo/<id>.svg；无第三方瓦片/CDN；<img loading=lazy> 懒加载；点按后才可缩放/拖动）。
地理底图数据：Natural Earth（公有领域，naturalearthdata.com），构建时从 ../ne/*.geojson 读取并裁剪简化。
投影：等距圆柱，经度按图幅中纬度余弦修正（与旧示意图相同）。"""
import json, math, os, html as _h
NE = os.environ.get("NE_DIR", "/workspace/ne")
PAL = {"gold":"#e9b949","blue":"#3b8fd9","green":"#2fa36b","purple":"#8b5cf6","red":"#e0573e","orange":"#f08a24","teal":"#14a3a3","pink":"#d6457a","gray":"#7c8796"}
RIVERS = {"Rhine","Rhein","Rhin","Nederrijn","Lek","Waal","Neckar","Main","Maas","Meuse","Schelde","Escaut","Scheldt","Danube","Donau","Duna","Dunav","Dunărea","Rhône","Rhone","Nile","Rosetta Branch","Damietta Branch","Tiber","Tevere","Po","Elbe","Thames","Jordan","Orontes","Seine","Loire","Ebro","Tajo","Tejo","Moselle","Mosel","Weser","Ems","Saône","Garonne","Euphrates","Firat","Al Furat","Tigris","Dicle","Sava","Drava","Tisza","Tisa"}
_cache = {}
def _load(n):
    if n not in _cache: _cache[n] = json.load(open(os.path.join(NE, n + ".geojson")))
    return _cache[n]
def proj(bbox, W):
    lo0, lo1, la0, la1 = bbox; mid = (la0 + la1) / 2
    sx = W / (lo1 - lo0); sy = sx / math.cos(math.radians(mid)); H = round((la1 - la0) * sy)
    return (lambda lon, lat: ((lon - lo0) * sx, (la1 - lat) * sy)), sx, sy, H
def tw(s, fs):
    w = 0
    for c in s:
        o = ord(c)
        if o > 0x2E80 or c in "（）：，、·①②③④⑤⑥⑦⑧⑨": w += fs
        elif c in " ": w += fs * .3
        elif c in "–-—.": w += fs * .5
        elif c.isdigit(): w += fs * .62
        elif c.isupper(): w += fs * .7
        else: w += fs * .56
    return w + 4
def _ring(coords, P, tol):
    out = []; lx = ly = None
    for lon, lat in coords:
        x, y = P(lon, lat)
        if lx is None or abs(x - lx) + abs(y - ly) >= tol: out.append((x, y)); lx, ly = x, y
    return out
def _d(rings, close=True):
    s = []
    for r in rings:
        if len(r) < (3 if close else 2): continue
        s.append("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in r) + ("Z" if close else ""))
    return "".join(s)
def base(bbox, W, fine=False):
    from shapely.geometry import shape, box, mapping
    P, sx, sy, H = proj(bbox, W)
    lo0, lo1, la0, la1 = bbox; pad = 1.0
    B = box(lo0 - pad, la0 - pad, lo1 + pad, la1 + pad)
    tol_deg = (0.5 if fine else 0.9) / sx
    def polys(name, minarea=0):
        rings = []
        for f in _load(name)["features"]:
            g = shape(f["geometry"])
            if not g.intersects(B): continue
            g = g.intersection(B).simplify(tol_deg, preserve_topology=True)
            if g.is_empty: continue
            for p in (g.geoms if hasattr(g, "geoms") else [g]):
                if p.geom_type != "Polygon" or p.area < minarea: continue
                rings.append(_ring(p.exterior.coords, P, 0.6))
                for i in p.interiors: rings.append(_ring(i.coords, P, 0.6))
        return rings
    land = polys("ne_10m_land" if fine else "ne_50m_land", (2.5 / sx) ** 2)
    lakes = polys("ne_10m_lakes" if fine else "ne_50m_lakes", (5 / sx) ** 2)
    riv = []
    src = "ne_10m_rivers_lake_centerlines" if fine else "ne_50m_rivers_lake_centerlines"
    for f in _load(src)["features"]:
        nm = (f["properties"].get("name") or "")
        if nm not in RIVERS and (f["properties"].get("name_en") or "") not in RIVERS: continue
        g = shape(f["geometry"])
        if not g.intersects(B): continue
        g = g.intersection(B).simplify(tol_deg)
        for l in (g.geoms if hasattr(g, "geoms") else [g]):
            if l.geom_type == "LineString": riv.append(_ring(l.coords, P, 0.8))
    return P, sx, sy, H, _d(land), _d(lakes), _d(riv, False)
def spread(mk, P, rh, rn):
    """标记点互相避让：真实位置过近（如君士坦丁堡与迦克墩相距约 5 km）时，后者沿 8 个方向外移，并以细线连回真实位置。"""
    pos = {}
    for m in mk:
        x, y = P(*m["ll"]); r = rh if m.get("hl") else rn
        def ok(px, py): return all(math.hypot(px - a, py - b) >= r + c + 5 for a, b, c in pos.values())
        if not ok(x, y):
            for k in (1, 1.6, 2.3):
                hit = None
                for ang in (-90, -45, 0, 45, 90, 135, 180, -135):
                    d = (r * 2 + 8) * k; px, py = x + d * math.cos(math.radians(ang)), y + d * math.sin(math.radians(ang))
                    if ok(px, py): hit = (px, py); break
                if hit: x, y = hit; break
        pos[m["k"]] = (x, y, r)
    return pos
# ---------- 标签避让 ----------
class Placer:
    def __init__(s, W, H): s.W, s.H, s.boxes = W, H, []
    def free(s, b, m=3):
        x0, y0, x1, y1 = b
        if x0 < 4 or y0 < 4 or x1 > s.W - 4 or y1 > s.H - 4: return False
        return all(x1 + m <= a[0] or a[2] + m <= x0 or y1 + m <= a[1] or a[3] + m <= y0 for a in s.boxes)
    def add(s, b): s.boxes.append(b)
    def label(s, x, y, r, text, fs):
        w = tw(text, fs); asc, dsc = fs * .88, fs * .24
        for d in (r + 5, r + 16, r + 30, r + 46):
            for an, dx, dy in (("start", d, fs * .34), ("end", -d, fs * .34), ("middle", 0, -d * .8), ("middle", 0, d * .8 + fs * .7),
                               ("start", d * .75, -d * .62), ("end", -d * .75, -d * .62), ("start", d * .75, d * .62 + fs * .5), ("end", -d * .75, d * .62 + fs * .5)):
                bx = x + dx; by = y + dy
                x0 = bx if an == "start" else bx - w if an == "end" else bx - w / 2
                b = (x0, by - asc, x0 + w, by + dsc)
                if s.free(b): s.add(b); return bx, by, an, d > r + 16
        return None
# ---------- 真实地图（静态 SVG 文件） ----------
def real_svg(spec, W=1000):
    P, sx, sy, H, land, lakes, riv = base(spec["bbox"], W, spec.get("fine", False))
    fs = spec.get("fs", 19)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="\'Noto Sans CJK SC\',\'PingFang SC\',\'Microsoft YaHei\',\'Source Han Sans SC\',sans-serif">',
         '<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6f5"/><stop offset="1" stop-color="#a9d0ea"/></linearGradient>',
         '<linearGradient id="ld" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf4e2"/><stop offset="1" stop-color="#efe2c0"/></linearGradient>']
    cols = sorted({PAL[r[2]] for r in spec.get("routes", ())})
    for c in cols: o.append(f'<marker id="a{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="{c}"/></marker>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sea)"/>')
    st = 1 if (spec["bbox"][1] - spec["bbox"][0]) <= 10 else 5 if (spec["bbox"][1] - spec["bbox"][0]) <= 40 else 10
    g = []
    lo0, lo1, la0, la1 = spec["bbox"]
    for lon in range(math.ceil(lo0 / st) * st, int(lo1) + 1, st): x, _ = P(lon, la1); g.append(f"M{x:.0f},0V{H}")
    for lat in range(math.ceil(la0 / st) * st, int(la1) + 1, st): _, y = P(lo0, lat); g.append(f"M0,{y:.0f}H{W}")
    o.append(f'<path d="{"".join(g)}" stroke="#ffffff" stroke-opacity=".55" stroke-width="1" stroke-dasharray="2 5" fill="none"/>')
    o.append(f'<path d="{land}" fill="url(#ld)" stroke="#a9946a" stroke-width="1" stroke-linejoin="round" fill-rule="evenodd"/>')
    if lakes: o.append(f'<path d="{lakes}" fill="#bcdcf0" stroke="#7fb0d4" stroke-width=".7"/>')
    if riv: o.append(f'<path d="{riv}" fill="none" stroke="#4f97cf" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" opacity=".85"/>')
    pl = Placer(W, H)
    # 保留区：比例尺（左下）、指北针（右上）
    km = 111.32 * math.cos(math.radians((la0 + la1) / 2)) / sx  # km per px
    nice = min((100, 200, 250, 500, 1000, 2000), key=lambda k: abs(k / km - W * .16)); bl = nice / km
    pl.add((10, H - 46, 26 + bl + 60, H - 6)); pl.add((W - 52, 6, W - 6, 62))
    for reg in spec.get("regions", ()):
        lab, lon, lat, rx, ry, c = reg; x, y = P(lon, lat)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx * sx:.0f}" ry="{ry * sy:.0f}" fill="{PAL[c]}" fill-opacity=".16" stroke="{PAL[c]}" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="6 5"/>')
    for ln in spec.get("lines", ()):
        lab, pts, c = ln; d = "M" + " ".join(f"{P(*p)[0]:.0f},{P(*p)[1]:.0f}" for p in pts)
        o.append(f'<path d="{d}" fill="none" stroke="{PAL[c]}" stroke-width="2.2" stroke-dasharray="9 6" opacity=".85"/>')
    mk = spec["markers"]; pos = spread(mk, P, 13, 11)
    for m in mk:
        x, y, r = pos[m["k"]]; pl.add((x - r - 1, y - r - 1, x + r + 1, y + r + 1))
        tx, ty = P(*m["ll"])
        if abs(tx - x) + abs(ty - y) > 1: o.append(f'<path d="M{tx:.0f},{ty:.0f}L{x:.0f},{y:.0f}" stroke="#3a3020" stroke-width="1.5"/><circle cx="{tx:.0f}" cy="{ty:.0f}" r="3" fill="#3a3020"/>'); pl.add((tx - 4, ty - 4, tx + 4, ty + 4))
    cw = tw("Natural Earth 底图 · 等距圆柱投影 · 本站绘制", 12)
    cred = None
    for bx0, by0, an in ((W - 10 - cw, H - 24, "end"), (W - 10 - cw, 76, "end"), (12, 10, "start"), (12, H - 66, "start")):
        b_ = (bx0, by0, bx0 + cw, by0 + 18)
        if pl.free(b_, 2): pl.add(b_); cred = (bx0 + cw if an == "end" else bx0, by0 + 14, an); break
    cred = cred or (W - 10, H - 10, "end")
    for a, b, c, *rest in spec.get("routes", ()):
        (x1, y1, r1), (x2, y2, r2) = pos[a], pos[b]
        L = math.hypot(x2 - x1, y2 - y1) or 1; ux, uy = (x2 - x1) / L, (y2 - y1) / L
        x1, y1, x2, y2 = x1 + ux * (r1 + 2), y1 + uy * (r1 + 2), x2 - ux * (r2 + 4), y2 - uy * (r2 + 4)
        bend = (rest[0] if rest else .18) * L; mx, my = (x1 + x2) / 2 + uy * bend, (y1 + y2) / 2 - ux * bend
        o.append(f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{PAL[c]}" stroke-width="3" stroke-dasharray="8 5" stroke-linecap="round" marker-end="url(#a{PAL[c][1:]})" opacity=".9"/>')
    T = []
    halo = 'paint-order="stroke" stroke="#fffaf0" stroke-width="4" stroke-linejoin="round"'
    order = sorted(range(len(mk)), key=lambda i: (not mk[i].get("hl"), i))
    for i in order:
        m = mk[i]; x, y, r = pos[m["k"]]
        lab = m["n"] + ((" " + m["y"]) if m.get("ylab") else "")
        res = pl.label(x, y, r, lab, fs)
        if not res:
            lab = m["n"]; res = pl.label(x, y, r, lab, fs)
        if not res: m["_nolab"] = True; continue
        bx, by, an, far = res
        if far:
            T.append(f'<path d="M{x:.0f},{y:.0f}L{bx:.0f},{by - fs * .3:.0f}" stroke="#5a4a30" stroke-width="1" opacity=".6"/>')
        T.append(f'<text x="{bx:.1f}" y="{by:.1f}" text-anchor="{an}" font-size="{fs}" font-weight="{800 if m.get("hl") else 600}" fill="#1f1a12" {halo}>{_h.escape(lab)}</text>')
    for reg in spec.get("regions", ()):
        lab, lon, lat, rx, ry, c = reg; x, y = P(lon, lat)
        res = pl.label(x, y - ry * sy * .2, 0, lab, fs - 3)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" font-size="{fs - 3}" font-weight="700" fill="{_dark(PAL[c])}" {halo}>{_h.escape(lab)}</text>')
    for lab, lon, lat in spec.get("water", ()):
        x, y = P(lon, lat); w = tw(lab, fs - 2); b = (x - w / 2, y - fs, x + w / 2, y + 4)
        if pl.free(b): pl.add(b); T.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="{fs - 2}" font-style="italic" fill="#2b6a9a" letter-spacing="2" {halo.replace("#fffaf0", "#d6ebf7")}>{_h.escape(lab)}</text>')
    for ln in spec.get("lines", ()):
        lab, pts, c = ln; x, y = P(*pts[len(pts) // 2])
        res = pl.label(x, y, 4, lab, fs - 4)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" font-size="{fs - 4}" font-weight="700" fill="{_dark(PAL[c])}" {halo}>{_h.escape(lab)}</text>')
    o += T
    for i, m in enumerate(mk):
        x, y, r = pos[m["k"]]; c = PAL[m.get("c", "blue")]
        if m.get("hl"): o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r + 5}" fill="none" stroke="{c}" stroke-width="2.5" opacity=".55"/>')
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}" stroke="#ffffff" stroke-width="2.5"/>')
        o.append(f'<text x="{x:.0f}" y="{y + 4.6:.1f}" text-anchor="middle" font-size="13" font-weight="800" fill="{ink(c)}">{i + 1}</text>')
    # 比例尺 + 指北针 + 出处
    o.append(f'<g transform="translate(18,{H - 18})"><rect x="-8" y="-24" width="{bl + 70:.0f}" height="34" rx="8" fill="#fffaf0" opacity=".8"/><path d="M0,0H{bl:.0f}" stroke="#2a2118" stroke-width="3"/><path d="M0,-6V4M{bl:.0f},-6V4" stroke="#2a2118" stroke-width="2"/><text x="{bl + 8:.0f}" y="4" font-size="14" fill="#2a2118">{nice} km</text></g>')
    o.append(f'<g transform="translate({W - 29},34)"><circle r="20" fill="#fffaf0" opacity=".85"/><path d="M0,-15L6,6L0,2L-6,6z" fill="#c0392b"/><text y="15" text-anchor="middle" font-size="11" font-weight="800" fill="#2a2118">N</text></g>')
    o.append(f'<text x="{cred[0]:.0f}" y="{cred[1]:.0f}" text-anchor="{cred[2]}" font-size="12" fill="#3d4a57" {halo.replace("stroke-width=\"4\"", "stroke-width=\"3\"")}>Natural Earth 底图 · 等距圆柱投影 · 本站绘制</text>')
    o.append('</svg>')
    hs = [(m, (pos[m["k"]][0] / W * 100, pos[m["k"]][1] / H * 100)) for m in mk]
    return "".join(o), W, H, hs
def ink(c):
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda v: v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    L = .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
    return "#1a1206" if (L + .05) / .0625 > 1.05 / (L + .05) else "#ffffff"
def _dark(c):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return "#%02x%02x%02x" % (int(r * .55), int(g * .55), int(b * .55))
# ---------- 概念示意图（新地图用；页内 SVG，主题色） ----------
def concept_svg(spec, W=1040):
    P, sx, sy, H = proj(spec["cbbox"] if "cbbox" in spec else spec["bbox"], W)
    fs = 21
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{_h.escape(spec["title"])}（概念图）"><defs><linearGradient id="g{spec["id"]}" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#1c3a6e" stop-opacity=".55"/><stop offset="1" stop-color="#4a3a22" stop-opacity=".35"/></linearGradient>']
    cols = sorted({PAL[r[2]] for r in spec.get("routes", ())})
    for c in cols: o.append(f'<marker id="c{spec["id"]}{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="{c}"/></marker>')
    o.append(f'</defs><rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#g{spec["id"]})"/>')
    o.append("".join(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" class="gr"/>' for gx in range(0, W, 104)) + "".join(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" class="gr"/>' for gy in range(0, H, 104)))
    pl = Placer(W, H); T = []
    for lab, lon, lat, rx, ry, c in spec.get("regions", ()):
        x, y = P(lon, lat)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx * sx:.0f}" ry="{ry * sy:.0f}" fill="{PAL[c]}" fill-opacity=".16" stroke="{PAL[c]}" stroke-opacity=".55" stroke-dasharray="5 5"/>')
    for lab, pts, c in spec.get("lines", ()):
        d = "M" + " ".join(f"{P(*p)[0]:.0f},{P(*p)[1]:.0f}" for p in pts)
        o.append(f'<path d="{d}" fill="none" stroke="{PAL[c]}" stroke-width="2" stroke-dasharray="9 6" opacity=".7"/>')
    mk = spec["markers"]; pos = spread(mk, P, 15, 12)
    for m in mk:
        x, y, r = pos[m["k"]]; pl.add((x - r - 2, y - r - 2, x + r + 2, y + r + 2))
        tx, ty = P(*m["ll"])
        if abs(tx - x) + abs(ty - y) > 1: o.append(f'<path d="M{tx:.0f},{ty:.0f}L{x:.0f},{y:.0f}" class="ldr"/>')
    n = 0
    for a, b, c, *rest in spec.get("routes", ()):
        (x1, y1, r1), (x2, y2, r2) = pos[a], pos[b]
        L = math.hypot(x2 - x1, y2 - y1) or 1; ux, uy = (x2 - x1) / L, (y2 - y1) / L
        x1, y1, x2, y2 = x1 + ux * (r1 + 3), y1 + uy * (r1 + 3), x2 - ux * (r2 + 5), y2 - uy * (r2 + 5)
        bend = (rest[0] if rest else .18) * L; mx, my = (x1 + x2) / 2 + uy * bend, (y1 + y2) / 2 - ux * bend
        o.append(f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" class="route cr" style="stroke:{PAL[c]}" marker-end="url(#c{spec["id"]}{PAL[c][1:]})"/>')
    for i in sorted(range(len(mk)), key=lambda i: (not mk[i].get("hl"), i)):
        m = mk[i]; x, y, r = pos[m["k"]]
        lab = m.get("cl") or (m["n"] + " " + m["y"])
        res = pl.label(x, y, r, lab, fs) or pl.label(x, y, r, m["n"], fs)
        if not res: continue
        bx, by, an, far = res
        if far: T.append(f'<path d="M{x:.0f},{y:.0f}L{bx:.0f},{by - 6:.0f}" class="ldr"/>')
        T.append(f'<text x="{bx:.0f}" y="{by:.0f}" text-anchor="{an}" class="cml{" hl" if m.get("hl") else ""}">{_h.escape(lab)}</text>')
    for lab, lon, lat, rx, ry, c in spec.get("regions", ()):
        x, y = P(lon, lat); res = pl.label(x, y - ry * sy - 4, 0, lab, 20)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" class="rg">{_h.escape(lab)}</text>')
    for lab, pts, c in spec.get("lines", ()):
        x, y = P(*pts[len(pts) // 2]); res = pl.label(x, y, 4, lab, 18)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" class="rg" style="font-size:18px">{_h.escape(lab)}</text>')
    o += T
    for i, m in enumerate(mk):
        x, y, r = pos[m["k"]]; c = PAL[m.get("c", "blue")]
        o.append(f'<g class="cpt{" hl" if m.get("hl") else ""}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" style="fill:{c}"/><text x="{x:.0f}" y="{y + 5:.0f}" text-anchor="middle" class="cmn" style="fill:{ink(c)}">{i + 1}</text></g>')
    o.append('</svg>')
    return "".join(o)
# ---------- HTML ----------
def legend(spec):
    li = []
    for i, m in enumerate(spec["markers"]):
        li.append(f'<li style="--c:{PAL[m.get("c", "blue")]};--t:{ink(PAL[m.get("c", "blue")])}" data-i="{i}" tabindex="0"><b class="rn">{i + 1}</b><span class="rmt"><b>{_h.escape(m["n"])}</b>{(" <i>" + _h.escape(m["en"]) + "</i>") if m.get("en") else ""} · <em>{_h.escape(m["y"])}</em>：{m["t"]}</span></li>')
    return f'<ol class="rm-leg">{"".join(li)}</ol>'
def real_html(spec, svgW, svgH, hs, ver):
    t = _h.escape(spec["title"])
    b = "".join(f'<button type="button" class="rm-hs" style="left:{x:.2f}%;top:{y:.2f}%" data-i="{i}" aria-label="{i + 1} {_h.escape(m["n"])}"></button>' for i, (m, (x, y)) in enumerate(hs))
    return (f'<figure class="rmap"><div class="rmw"><div class="rmv"><div class="rm-in" style="aspect-ratio:{svgW}/{svgH}">'
            f'<img src="assets/geo/{spec["id"]}.svg?v={ver}" width="{svgW}" height="{svgH}" loading="lazy" decoding="async" alt="{t}（真实地图：Natural Earth 海岸线与河流，标注 {len(hs)} 个地点）">{b}</div></div>'
            f'<button type="button" class="rm-go" aria-label="开启地图缩放与拖动">🔍 点按开启缩放 / 拖动</button>'
            f'<div class="rm-ctl"><button type="button" data-z="1" aria-label="放大">＋</button><button type="button" data-z="-1" aria-label="缩小">－</button><button type="button" data-z="0" aria-label="复位">⟲</button><button type="button" data-z="x" aria-label="结束缩放，恢复页面滚动">✕</button></div>'
            f'<div class="rm-tip" role="status" aria-live="polite"></div></div>'
            f'<figcaption>{t}（真实地图：Natural Earth 公有领域底图，本地静态文件，无第三方瓦片；编号见下表；{spec.get("rcap", "路线为示意方向，不代表精确行程")}）</figcaption>{legend(spec)}</figure>')
def pair(mid, concept_html, real, title):
    return (f'<div class="mapx" id="mx-{mid}" data-l="c"><div class="mx-tabs" role="tablist" aria-label="{_h.escape(title)}：地图图层">'
            f'<button type="button" role="tab" aria-selected="true" data-l="c">🎨 概念图</button><button type="button" role="tab" aria-selected="false" data-l="r">🗺️ 真实地图 · 可缩放</button></div>'
            f'<div class="mx-c">{concept_html}</div><div class="mx-r">{real}</div></div>')
def new_concept(spec):
    steps = spec.get("steps")
    st = ""
    if steps: st = '<ol class="msteps">' + "".join(f'<li style="--c:{PAL[c]}"><b>{_h.escape(y)}</b> {_h.escape(t)}</li>' for y, t, c in steps) + '</ol>'
    return f'<figure class="map in cmap">{concept_svg(spec)}<figcaption>{_h.escape(spec["title"])}（概念图：按经纬度投影的城市位置，不绘海岸线；编号与真实地图、下方列表一致；箭头为示意方向）</figcaption></figure>{st}'
def build(spec, outdir, ver, concept_html=None):
    svg, W, H, hs = real_svg(spec)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, spec["id"] + ".svg"), "w").write(svg)
    c = concept_html if concept_html is not None else new_concept(spec)
    return pair(spec["id"], c, real_html(spec, W, H, hs, ver), spec["title"])
