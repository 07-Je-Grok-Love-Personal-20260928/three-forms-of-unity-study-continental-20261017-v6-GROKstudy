# -*- coding: utf-8 -*-
"""可视化：计数器、柱状图、环形图、北美地图。所有数据在构建时由 data/*.json（CCI 原文）统计，不手填。"""
import html as H,re
from core import *
from c_common import *
from c_common import _dt
from quotes import BC,DORT
from c_titles import HC52,PART_RANGE,BC_GROUPS,BC37
from geo import mapsvg
PCOL={"总纲":"#d4af37","困苦":"#e07a5f","拯救":"#5aa9e6","感恩":"#81b29a"}
def stats(items):
    return '<div class="vst reveal">'+"".join(f'<div style="--c:{c}"><i>{i}</i><b data-count="{n}">{n}</b><small>{t}</small></div>' for i,n,t,c in items)+'</div>'
def colchart(id,title,items,note="",label_every=1,unit="",legend=None,H_=220):
    """items: (标签,数值,颜色,提示,链接,标记)。纵向柱；横向在窄屏滚动，不撑破页面。"""
    n=len(items); W=1040; pl,pr,pt,pb=56,8,18,38; bw=(W-pl-pr)/n; mx=max(v for _,v,*_ in items)
    s=f'<figure class="cchart reveal"><p class="shint">← 左右滑动看全部柱子 →</p><div class="cscroll"><svg viewBox="0 0 {W} {H_}" role="img" aria-label="{H.escape(title)}">'
    for k in (0,.5,1):
        y=H_-pb-k*(H_-pt-pb); s+=f'<line x1="{pl}" y1="{y:.0f}" x2="{W-pr}" y2="{y:.0f}" class="gr"/><text x="{pl-6}" y="{y+4:.0f}" text-anchor="end" class="ax">{round(mx*k)}</text>'
    for i,(lab,v,c,tip,href,mark) in enumerate(items):
        h=v/mx*(H_-pt-pb); x=pl+i*bw; y=H_-pb-h
        r=f'<g class="cb" style="--i:{i}"><rect x="{x+bw*.1:.1f}" y="{y:.1f}" width="{bw*.8:.1f}" height="{h:.1f}" rx="3" fill="{c}"><title>{H.escape(tip)}</title></rect>'
        if mark: r+=f'<circle cx="{x+bw/2:.1f}" cy="{y-7:.1f}" r="3.6" class="mk"/>'
        r+='</g>'
        s+=(f'<a href="{href}">{r}</a>' if href else r)
        if i%label_every==0 or i==n-1: s+=f'<text x="{x+bw/2:.1f}" y="{H_-pb+16}" text-anchor="middle" class="ax">{lab}</text>'
    s+='</svg></div>'
    lg="".join(f'<span class="lg2" style="--c:{c}"><i></i>{t}</span>' for t,c in (legend or []))
    return s+f'<figcaption><b>{title}</b>{"（"+unit+"）" if unit else ""}{note and "　"+note}{lg and "<br>"+lg}</figcaption></figure>'
def donut(id,title,parts,center,sub=""):
    """parts: (标签,数值,颜色,说明)。pathLength=100，逐段描边动画。"""
    tot=sum(v for _,v,_,_ in parts); off=0; seg=""; lg=""
    for lab,v,c,d in parts:
        p=v/tot*100
        seg+=f'<circle class="dseg" cx="60" cy="60" r="40" pathLength="100" stroke="{c}" stroke-dasharray="{p-0.8:.2f} {100-p+0.8:.2f}" stroke-dashoffset="{-off:.2f}" style="--da:{p-0.8:.2f} {100-p+0.8:.2f}"><title>{H.escape(lab)}：{v}（{p:.0f}%）</title></circle>'
        lg+=f'<li style="--c:{c}"><i></i><b>{lab}</b><span>{v}　{d}</span></li>'; off+=p
    return (f'<figure class="donutw reveal"><svg viewBox="0 0 120 120" role="img" aria-label="{H.escape(title)}"><g transform="rotate(-90 60 60)">{seg}</g>'
            f'<text x="60" y="58" text-anchor="middle" class="dc1">{center}</text><text x="60" y="74" text-anchor="middle" class="dc2">{sub}</text></svg>'
            f'<figcaption><b>{title}</b><ul class="dleg">{lg}</ul></figcaption></figure>')
# ---------------- 数据 ----------------
def hc_stats():
    from quotes import HC
    from c_refx import YOUTH_LD
    rows=[]
    for n in range(1,53):
        a,b=HCRANGE[n]; ch=sum(len(HC[q][0])+len(HC[q][1]) for q in range(a,b+1))
        rows.append((n,b-a+1,ch,HC52[n][1]))
    return rows
def viz_hc():
    from c_refx import YOUTH_LD,YOUTH_Q
    rows=hc_stats(); nq=sum(r[1] for r in rows)
    q_items=[(str(n),k,PCOL[p],f"主日 {n}｜{HC52[n][0]}：{k} 问（问{HCRANGE[n][0]}–{HCRANGE[n][1]}）"+("；恩约教会宣信必背" if n in YOUTH_LD else ""),f"#hd-ld{n}",n in YOUTH_LD) for n,k,ch,p in rows]
    c_items=[(str(n),ch,PCOL[p],f"主日 {n}｜{HC52[n][0]}：{ch} 字（问与答，不含脚注）","#hd-ld%d"%n,n in YOUTH_LD) for n,k,ch,p in rows]
    longest=max(rows,key=lambda r:r[2]); shortest=min(rows,key=lambda r:r[2]); mostq=max(rows,key=lambda r:r[1])
    parts=[("总纲+困苦",11,"#e07a5f","问1–11"),("拯救",74,"#5aa9e6","问12–85"),("感恩",44,"#81b29a","问86–129")]
    leg=[("总纲",PCOL["总纲"]),("困苦",PCOL["困苦"]),("拯救",PCOL["拯救"]),("感恩",PCOL["感恩"])]
    body=('<p>下面的图表由 CCI 中文本在构建时<b>逐主日统计</b>（不是手填）。金色圆点＝恩约教会青少年宣信要求背诵的问答所在主日（来源见 2.x 参考站互证）；点柱子跳到对应主日。</p>'
      +stats([("📖",52,"个主日","#d4af37"),("❓",nq,"问","#5aa9e6"),("🧭",3,"大部分（罪·救·谢）","#81b29a"),("📌",len(YOUTH_Q),"个宣信必背问","#e07a5f")])
      +colchart("hcq","每个主日有几问",q_items,legend=leg,unit="问",label_every=3,note=f"最多的是主日{mostq[0]}（{mostq[1]} 问）：{HC52[mostq[0]][0]}。")
      +colchart("hcc","每个主日有多长",c_items,legend=leg,unit="字",label_every=3,note=f"最长主日{longest[0]}（{longest[2]} 字），最短主日{shortest[0]}（{shortest[2]} 字）。")
      +donut("hcp","三部分占多少问",parts,"129","问",)
      +key("<b>读图：</b>第二部分（得救）占 74 问、近六成；而“感恩”部分（44 问）是十诫与主祷文——篇幅上，感恩几乎与“愁苦＋总纲”（11 问）的四倍相当。记忆时先背“罪 11 · 救 74 · 谢 44”这组数字。"))
    return L2("hc-viz","?","数据图：129 问怎样分布在 52 个主日",body)
def viz_bc():
    items=[]; col={}
    for g,lab,c,lo,hi,_ in BC_GROUPS:
        for n in range(lo,hi+1): col[n]=(c,lab)
    for n in range(1,38):
        ln=len(BC[n]); items.append((str(n),ln,col[n][0],f"第{n}条 · {BC37[n][0]}：{ln} 字（{col[n][1]}）",f"#bcd-a{n}",n in (8,9,10,11)))
    longest=max(range(1,38),key=lambda n:len(BC[n])); shortest=min(range(1,38),key=lambda n:len(BC[n]))
    parts=[(lab,hi-lo+1,c,f"第{lo}–{hi}条") for g,lab,c,lo,hi,_ in BC_GROUPS]
    gs=sorted([(lab,sum(len(BC[n]) for n in range(lo,hi+1)),f"{lo}–{hi}") for g,lab,c,lo,hi,_ in BC_GROUPS],key=lambda t:-t[1])
    top2=sorted(range(1,38),key=lambda n:-len(BC[n]))[:2]
    body=('<p>37 条按七群着色；金色圆点＝第 8–11 条（三位一体与基督、圣灵的神性），也是与三大信经直接重叠的核心段。字数为 CCI 中文本正文（不含脚注）。</p>'
      +stats([("📜",37,"条","#5aa9e6"),("🧩",7,"群","#d4af37"),("📏",len(BC[longest]),f"字 · 最长第{longest}条","#e07a5f"),("✂️",len(BC[shortest]),f"字 · 最短第{shortest}条","#81b29a")])
      +colchart("bcl","37 条的篇幅",items,legend=[(lab,c) for g,lab,c,*_ in BC_GROUPS],unit="字",label_every=1,note=f"最长的是第{longest}条《{BCT[longest]}》，最短的是第{shortest}条《{BCT[shortest]}》。")
      +donut("bcg","七群各占几条",parts,"37","条")
      +key(f"<b>读图：</b>按总字数，最长的两群是“{gs[0][0]}”（{gs[0][1]} 字，第{gs[0][2]}条）与“{gs[1][0]}”（{gs[1][1]} 字，第{gs[1][2]}条）；“{gs[-1][0]}”最短（{gs[-1][1]} 字）。单条最长的是第{top2[0]}条，其次是第{top2[1]}条。"))
    return L2("bc-viz","?","数据图：37 条的篇幅与七群",body)
def viz_dort():
    from c_dort import ERR
    cols={"section1":"#d4af37","section2":"#5aa9e6","section3-4":"#e07a5f","section5":"#81b29a"}
    items=[]
    for h in _dt["heads"]:
        for it in h["items"]:
            err=it is h["items"][-1]; ln=sum(len(strip(b["x"])) for b in it["blocks"] if b["t"]=="p")
            items.append((f'{h["num"]}.{it["n"]}'.replace("3-4","3-4"),ln,("#a05a4a" if err else cols[h["id"]]),f'第{h["num"]}项 第{it["n"]}条{"（错谬反驳）" if err else ""}：{ln} 字',"",False))
    nerr=sum(len(v) for v in ERR.values())
    parts=[(f'第{h["num"]}项',len(h["items"]),cols[h["id"]],f'{len(h["items"])-1} 条＋反驳') for h in _dt["heads"]]
    body=('<p>每项的“错谬反驳”（红褐色柱）都是该项最长的条目（本图已逐项核对），因为它把抗辩派的错谬逐条列出再驳斥；柱标签＝项.条。</p>'
      +stats([("⚖️",len(_dt["heads"]),"项教义","#d4af37"),("📑",sum(len(h["items"]) for h in _dt["heads"]),"个条目","#5aa9e6"),("🚫",nerr,"条被驳斥的错谬","#e07a5f"),("🕯️",8,"国 · 26 名代表（reformedbeginner.net）","#81b29a")])
      +colchart("dtl","63 个条目的篇幅",items,legend=[("第1项","#d4af37"),("第2项","#5aa9e6"),("第3–4项","#e07a5f"),("第5项","#81b29a"),("错谬反驳","#a05a4a")],unit="字",label_every=4)
      +donut("dtp","四项各占多少条目",parts,str(sum(len(h["items"]) for h in _dt["heads"])),"条目")
      +key("<b>读图：</b>第一项条目最多（19 个，含错谬反驳），第二项最少（10 个）；每项都以“错谬反驳”收尾——正反两面是 Dort 的体例（PRCA 页同说：真理“既被正面也被负面地界定”，见参考站互证）。"))
    return L2("dt-viz","?","数据图：63 个条目与错谬反驳",body)
def viz_overview():
    from quotes import HC
    hcn=sum(len(HC[q][0])+len(HC[q][1]) for q in HC); bcn=sum(len(BC[n]) for n in BC); dn=sum(len(v) for v in DORT.values())
    bars_=[("比利时信条（37 条）",bcn,"#5aa9e6"),("海德堡要理问答（129 问）",hcn,"#81b29a"),("多特信经（含驳谬）",dn,"#d4af37")]
    mx=max(v for _,v,_ in bars_)
    bh='<div class="bars reveal" role="img" aria-label="三份文件字数对比"><p class="bt">三份文件的篇幅（CCI 中文本正文字数，不含脚注）</p>'+"".join(f'<div class="br"><span class="bl">{l}</span><span class="bk"><i style="--w:{v/mx*100:.1f}%;--c:{c}"></i></span><b class="bv">{v}</b></div>' for l,v,c in bars_)+'</div>'
    pts=["阿纳海姆（洛杉矶）","费城","大急流城","汉密尔顿（安大略）","莱斯布里奇","林伍德（伊利诺伊）"]
    m=mapsvg("na","今天用三项联合信条的机构：本站在参考页上读到的 6 个地点",pts,hl=("阿纳海姆（洛杉矶）","汉密尔顿（安大略）"),bbox=(-124,-68,28,54),rhine=False,
      off={"阿纳海姆（洛杉矶）":(14,6,'start'),"费城":(-14,18,'end'),"大急流城":(-14,-8,'end'),"汉密尔顿（安大略）":(14,-10,'start'),"莱斯布里奇":(14,6,'start'),"林伍德（伊利诺伊）":(-14,22,'end')},
      cap="。地点与出处：阿纳海姆＝恩约教会（ccreformed.org 页脚地址）；汉密尔顿＝加拿大归正教会神学院 1969 年开学（canadianreformedseminary.ca/about/history）；莱斯布里奇＝加拿大归正教会第一个教会 1950 年建立（canrc.org/history）；林伍德＝URCNA 1996 年首届总会（urcna.org/about）；大急流城＝Heritage Reformed 的神学院所在（heritagereformed.com）；费城＝威斯敏斯特神学院 1929 年首堂课（wts.edu/about/history）")
    body=('<p>三份文件文体不同、篇幅也不同：BC 是告白、HC 是问答、Dort 是裁决。下面用 CCI 中文本的字数把它们放在一起，再用地图看今天谁在用它们。</p>'
      +stats([("📜",37,"条告白","#5aa9e6"),("❓",129,"问问答","#81b29a"),("⚖️",63,"个裁决条目","#d4af37"),("🔗",3,"份古代信经：BC 第9条接受","#e07a5f")])
      +bh+m
      +note("地图只标本站在参考页文字里<b>真实读到</b>的地点；北美以外的教会（荷兰、台北等）此处不绘。"))
    return L2("cp-viz","?","数据图与地图：三份文件的篇幅，与今天谁在用",body)
