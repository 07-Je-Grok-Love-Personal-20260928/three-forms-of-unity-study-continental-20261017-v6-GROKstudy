# -*- coding: utf-8 -*-
"""共用构件：目录登记、L1/L2、卡片、表格、时间线、地图。"""

from extra import *
import html as H
V = "v20261017-1"
CUR = {"f": None}
PEND = []
TOC = []  # (l1id, l1title, [(id,title)])

def L1(id, num, title, ico, lead, body):
    TOC.append((id, f"{num}、{title}", PEND[:], CUR["f"])); PEND.clear()
    return f'<section class="l1" id="{id}"><header class="l1h reveal"><span class="ico">{ic(ico,"ic big")}</span><div><div class="kick">第{num}部分</div><h2>{num}、{title}</h2><p class="lead">{lead}</p></div></header>{body}</section>'
def L2(id, num, title, body):
    PEND.append((id, f"{num} {title}"))
    return f'<section class="l2 reveal" id="{id}"><h3><span class="n">{num}</span>{ic(l2icon(title))}{title}</h3>{body}</section>'
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
