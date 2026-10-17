# -*- coding: utf-8 -*-
import html as H
from core import *
def deep(items, open_first=False):
    """items: (title, color, [(label, html), ...]) → 可展开的“五问”深读卡片。"""
    out='<div class="dps">'
    for n,(t,c,rows) in enumerate(items):
        out+=f'<details class="dp reveal" style="--c:{c}"{" open" if open_first and n==0 else ""}><summary><b>{t}</b></summary><div class="dpb">'+"".join(f'<div class="dpr"><span class="dpl">{l}</span><div class="dpt">{x}</div></div>' for l,x in rows)+'</div></details>'
    return out+'</div><div class="exctl"><button class="btn" data-open=".dps">全部展开</button><button class="btn ghost" data-close=".dps">全部收起</button></div>'
def hc3(parts):
    """HC 三部分动画结构条：parts=[(标题,问数,副题,颜色,链接)]。宽度按问数比例。"""
    tot=sum(p[1] for p in parts)
    out='<div class="hc3 reveal" role="img" aria-label="海德堡要理问答三部分结构：按问数比例"><div class="h3bar">'
    for t,n,s,c,u in parts:
        out+=f'<a class="h3s" href="{u}" style="--n:{n};--c:{c}"><b>{t}</b><small>{s}</small><em>{n}问</em></a>'
    out+='</div><div class="h3ax"><span>问1</span><span>问129</span></div></div>'
    return out
