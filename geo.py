# -*- coding: utf-8 -*-
"""宗教改革欧洲示意地图：按经纬度等距投影（经度按纬度余弦修正），不绘海岸线；莱茵河为示意折线。"""
import math
CITY = {
"海德堡":(8.69,49.41),"新城(诺伊施塔特)":(8.14,49.35),"施派尔":(8.44,49.32),"沃尔姆斯":(8.36,49.63),"美因茨":(8.27,49.99),"法兰克福":(8.68,50.11),
"斯特拉斯堡":(7.75,48.58),"巴塞尔":(7.59,47.56),"苏黎世":(8.54,47.38),"伯尔尼":(7.45,46.95),"日内瓦":(6.14,46.20),"维滕贝格":(12.65,51.87),
"马尔堡":(8.77,50.80),"卡塞尔":(9.50,51.32),"不来梅":(8.80,53.08),"埃姆登":(7.21,53.37),"韦瑟尔":(6.62,51.66),
"图尔奈（杜内克）":(3.39,50.61),"瓦朗谢讷":(3.52,50.36),"里尔":(3.06,50.63),"蒙斯":(3.95,50.45),"布鲁塞尔":(4.35,50.85),"安特卫普":(4.40,51.22),
"根特":(3.72,51.05),"米德尔堡":(3.61,51.50),"多德雷赫特":(4.67,51.81),"莱顿":(4.49,52.16),"海牙":(4.30,52.08),"乌得勒支":(5.12,52.09),"阿姆斯特丹":(4.90,52.37),
"阿纳海姆（洛杉矶）":(-117.91,33.84),"费城":(-75.17,39.95),"大急流城":(-85.67,42.96),"汉密尔顿（安大略）":(-79.87,43.26),"莱斯布里奇":(-112.84,49.69),"林伍德（伊利诺伊）":(-87.54,41.52),
"巴黎":(2.35,48.86),"伦敦":(-0.13,51.51),"爱丁堡":(-3.19,55.95),"科隆":(6.96,50.94),"沃尔姆斯(国会)":(8.36,49.63),
}
RHINE=[(7.59,47.56),(7.75,48.58),(8.30,49.0),(8.45,49.49),(8.27,49.99),(7.60,50.36),(6.96,50.94),(6.77,51.23),(6.62,51.66),(5.90,51.98),(5.10,51.95),(4.50,51.90),(4.05,51.95)]
def mapsvg(id, title, pts, routes=(), hl=(), bbox=(-1,14,46,54), W=1040, off=None, blobs=(), rhine=True, cap="", rtxt=()):
    lo0,lo1,la0,la1 = bbox; midlat=(la0+la1)/2
    sx = W/(lo1-lo0); sy = sx/math.cos(math.radians(midlat))
    H = int((la1-la0)*sy)
    def xy(n):
        lon,lat = CITY[n] if isinstance(n,str) else n
        return (lon-lo0)*sx, (la1-lat)*sy
    off = off or {}
    s = f'<figure class="map reveal"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{title}"><defs><linearGradient id="g{id}" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#1c3a6e" stop-opacity=".55"/><stop offset="1" stop-color="#4a3a22" stop-opacity=".35"/></linearGradient></defs>'
    s += f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#g{id})"/>'
    for gx in range(0,W,104): s += f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" class="gr"/>'
    for gy in range(0,H,104): s += f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" class="gr"/>'
    for lab,lon,lat,rx,ry,c in blobs:
        x,y = xy((lon,lat)); s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx*sx:.0f}" ry="{ry*sy:.0f}" fill="{c}" fill-opacity=".16" stroke="{c}" stroke-opacity=".5" stroke-dasharray="5 5"/><text x="{x:.0f}" y="{y-ry*sy-8:.0f}" text-anchor="middle" class="rg">{lab}</text>'
    if rhine:
        d = " ".join(("M" if i==0 else "L")+f"{xy(p)[0]:.0f},{xy(p)[1]:.0f}" for i,p in enumerate(RHINE))
        s += f'<path d="{d}" class="river"/>'
        rx_,ry_ = xy((8.30,49.0)); s += f'<text x="{rx_+10:.0f}" y="{ry_:.0f}" class="rvt">莱茵河（示意）</text>'
    for a,b in routes:
        (x1,y1),(x2,y2) = xy(a),xy(b); mx,my=(x1+x2)/2,(y1+y2)/2-min(70,abs(x2-x1)*0.18+20)
        s += f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" class="route"/>'
    for n in pts:
        x,y = xy(n); big = n in hl
        ox,oy,an = off.get(n,(14,6,'start'))
        lab = n.replace("（杜内克）","").replace("(诺伊施塔特)","") if False else n
        s += f'<g class="pt{" hl" if big else ""}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{11 if big else 7}"/><text x="{x+ox:.0f}" y="{y+oy:.0f}" text-anchor="{an}">{lab}</text></g>'
    s += f'</svg><figcaption>{title}（示意图：按经纬度投影，不绘海岸线与国界{'，莱茵河为示意折线' if rhine else ''}{'；金色虚线为叙事路线，不代表精确行程' if routes else ''}）{cap}</figcaption></figure>'
    return s
