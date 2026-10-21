# -*- coding: utf-8 -*-
"""共用构件：目录登记、L1/L2、卡片、表格、时间线、地图。"""

from extra import *
import html as H
V = "v20261021-10"
CUR = {"f": None, "n": 0, "c2": 0}
PEND = []
PEND3 = []
TOC = []  # (l1id, l1title, [(id,title)])

def L1(id, num, title, ico, lead, body):
    TOC.append((id, f"{num}、{title}", PEND[:], CUR["f"])); PEND.clear()
    return f'<section class="l1" id="{id}"><header class="l1h reveal"><span class="ico">{ic(ico,"ic big")}</span><div><div class="kick">第{num}部分</div><h2>{num}、{title}</h2><p class="lead">{lead}</p></div></header>{body}</section>'
SEC = set(['bi-refx', 'rx-bible', 'hcd-ppl', 'hcd-use', 'rx-hc', 'bcd-ppl', 'bcd-use', 'bcd-feat', 'rx-bc', 'dd-co', 'dd-miss', 'dd-ppl', 'dd-use', 'rx-dort', 'cp-use', 'rx-compare', 'cp-ref', 'wm-inst', 'wm-time', 'wm-sab', 'rx-west', 'mem-rf', 'rx-memory', 'src-cci', 'src-refx', 'src-ver', 'src-method'])
def L2(id, num, title, body):
    if id.endswith("-whole") or id == "hcd-angles":
        num = f'{CUR["n"]}.0'  # v6：导读区块不占用既有编号，保持全站既有“见 x.y”引用不变
    else:
        CUR["c2"] += 1; num = f'{CUR["n"]}.{CUR["c2"]}'
    kids = PEND3[:]; PEND3.clear()
    PEND.append((id, f"{num} {title}", kids))
    cls = "l2 reveal"
    if id in SEC:
        cls += " sec"
        body = f'<details class="secd"><summary>展开：{title}<small>辅助内容 · 默认折叠</small></summary><div class="secb">{body}</div></details>'
    return f'<section class="{cls}" id="{id}"><h3><span class="n">{num}</span>{ic(l2icon(title))}{title}</h3>{body}</section>'
def L3(id, title, body, icon="cross", tag="", cls="", sub="", bar=None):
    """三级标题：编号 = 所属二级编号 + 序号（所属二级尚未登记，故用 c2+1）。返回 <section class=l3>。"""
    k = len(PEND3) + 1; num = f'{CUR["n"]}.{0 if CUR.get("zero") else CUR["c2"]+1}.{k}'
    PEND3.append((id, f"{num} {title}"))
    t = f'<span class="l3t">{tag}</span>' if tag else ""
    s = f'<small class="l3s">{sub}</small>' if sub else ""
    return f'<section class="l3 reveal {cls}" id="{id}"><h4 class="l3h"><span class="n3">{num}</span>{ic(icon,"ic sm")}<span class="l3x">{title}</span>{s}{t}</h4>{body}</section>'
def key(t): return f'<div class="call key"><b>🔑 重点</b>{t}</div>'
def hard(t): return f'<div class="call hard"><b>⚠️ 难点</b>{t}</div>'
def note(t): return f'<div class="call note"><b>📌 说明</b>{t}</div>'
def app(t): return f'<div class="call app"><b>🌱 应用</b>{t}</div>'
def cards(items, cls="g3"):
    return f'<div class="grid {cls}">' + "".join(f'<div class="card" style="--c:{c}"><div class="ct"><span>{i}</span>{t}</div><p>{p}</p></div>' for i,t,p,c in items) + '</div>'
def table(head, rows, cls=""):
    if head and head[0]=="异端": rows=[[ic("alert","ic sm hz")+r[0]]+list(r[1:]) for r in rows]
    return f'<div class="tw"><table class="{cls}"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>" + "".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows) + "</tbody></table></div>"
def timeline(items):
    return '<ol class="tl reveal">' + "".join(f'<li class="reveal" style="--c:{c}"><div class="yr">{ic("church" if "会议" in t else "clock","ic sm")}{y}</div><div class="tb"><b>{t}</b><p>{p}</p></div></li>' for y,t,p,c in items) + "</ol>"
def story(items):
    return '<div class="story">' + "".join(f'<div class="st reveal"><div class="sn">{n+1}</div><b>{t}</b><p>{p}</p></div>' for n,(t,p) in enumerate(items)) + "</div>"
def flow(steps):
    return '<div class="flow">' + '<span class="arr">➜</span>'.join(f'<div class="fs" style="--c:{c}"><b>{t}</b><small>{s}</small></div>' for t,s,c in steps) + "</div>"
def exeg(rows):
    out = '<div class="exeg">'
    for ph, mean, scr, conf, k, h in rows:
        out += f'<details class="ex reveal"><summary><span class="q">“{ph}”</span></summary><div class="exb"><p><i>释义</i>{mean}</p><p><i>经文</i>{scr}</p><p><i>信条</i>{conf}</p>' + (f'<p class="k"><i>重点</i>{k}</p>' if k else "") + (f'<p class="h"><i>难点</i>{h}</p>' if h else "") + '</div></details>'
    return out + '</div><div class="exctl"><button class="btn" data-open=".exeg">全部展开</button><button class="btn ghost" data-close=".exeg">全部收起</button></div>'

from geo import mapsvg
