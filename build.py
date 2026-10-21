# -*- coding: utf-8 -*-
"""生成全站静态页面。用法：python3 build.py"""
import json,re,html as H
from core import *
import core
from c_common import *
import pdf15,storymap
import c_bible,c_hc,c_bc,c_dort,c_compare,c_west,c_mem,c_src,libs

SITE="三项联合信条 · 欧陆改革宗深读"
PAGES=[("index","index.html","首页","home"),("bible","bible.html","一 全本圣经","book"),("hc","hc.html","二 海德堡","heart"),("bc","bc.html","三 比利时信条","scroll"),
 ("dort","dort.html","四 多特信经","scale"),("compare","compare.html","五 比较与签署","link"),("westminster","westminster.html","六 威斯敏斯特","scale"),
 ("hct","hct.html","七 HC 原文","scroll"),("bct","bct.html","八 BC 原文","scroll"),("dtt","dtt.html","九 Dort 原文","scroll"),("creedsx","creedsx.html","十 三大信经","scroll"),
 ("memory","memory.html","十一 记忆自测","brain"),("sources","sources.html","十二 来源","library")]
if "home" not in P: P["home"]=P["book"]
PARTS={"bible":c_bible.part_bible,"hc":c_hc.part_hc,"bc":c_bc.part_bc,"dort":c_dort.part_dort,"compare":c_compare.part_compare,"westminster":c_west.part_westminster,
 "hct":libs.part_hct,"bct":libs.part_bct,"dtt":libs.part_dtt,"creedsx":libs.part_creedsx,"memory":c_mem.part_mem}
FILE={k:f for k,f,_,_ in PAGES}; LABEL={k:t for k,_,t,_ in PAGES}
BODY={}
L1N={"bible":1,"hc":2,"bc":3,"dort":4,"compare":5,"westminster":6,"hct":7,"bct":8,"dtt":9,"creedsx":10,"memory":11,"sources":12}
for k,_,_,_ in PAGES[1:]:
    core.CUR["f"]=FILE[k]; core.CUR["n"]=L1N[k]; core.CUR["c2"]=0
    if k=="sources": BODY[k]=c_src.part_src(BODY)
    else: BODY[k]=PARTS[k]()
TOC=core.TOC
IDS={}
for k,h in BODY.items():
    for i in re.findall(r'\bid="([^"]+)"',h): IDS.setdefault(i,FILE[k])
UNRES=[]
def rewrite(k,h):
    own=set(re.findall(r'\bid="([^"]+)"',h))
    def f(m):
        i=m.group(1)
        if i in own or i=="": return m.group(0)
        if i in IDS: return f'href="{IDS[i]}#{i}"'
        UNRES.append((k,i)); return m.group(0)
    return re.sub(r'href="#([^"]*)"',f,h)
def toc_html(cur):
    t='<nav id="toc" aria-label="目录"><div class="tochead"><b>目录</b><button id="tocx" class="btn ghost" aria-label="隐藏目录" type="button">✕</button></div>'
    t+='<a class="tochome'+(' on' if cur=="index" else '')+'" href="index.html">🏠 首页 · 学习路径与进度</a><ol>'
    for id,title,subs,f in TOC:
        page=[k for k,ff in FILE.items() if ff==f][0]
        def sub(s):
            sid,st,kids=s
            if not kids: return f'<li class="t2"><a href="{f}#{sid}">{st}</a></li>'
            return (f'<li class="t2 has closed"><div class="t2r"><a href="{f}#{sid}">{st}</a><button class="tg2" type="button" aria-label="展开或收起三级标题" aria-expanded="false">▾</button></div><ol>'
                    +"".join(f'<li class="t3"><a href="{f}#{i}">{tt}</a></li>' for i,tt in kids)+"</ol></li>")
        t+=f'<li class="t1{" cur" if page==cur else " closed"}" data-page="{page}"><div class="t1r"><a href="{f}#{id}">{title}</a><button class="tg" type="button" aria-label="展开或收起" aria-expanded="{"true" if page==cur else "false"}">▾</button></div><ol>'+"".join(sub(s) for s in subs)+"</ol></li>"
    return t+"</ol></nav>"
def tabs(cur):
    return '<nav class="ptabs" aria-label="页面导航">'+"".join(f'<a href="{f}"{" class=on aria-current=page" if k==cur else ""}>{t}</a>' for k,f,t,_ in PAGES)+'</nav>'
def pager(cur):
    ks=[k for k,_,_,_ in PAGES]; i=ks.index(cur); out='<nav class="pager" aria-label="上一页下一页">'
    if i>0: out+=f'<a class="pg prev" href="{FILE[ks[i-1]]}"><small>← 上一页</small><b>{LABEL[ks[i-1]]}</b></a>'
    else: out+='<span></span>'
    if i<len(ks)-1: out+=f'<a class="pg next" href="{FILE[ks[i+1]]}"><small>下一页 →</small><b>{LABEL[ks[i+1]]}</b></a>'
    return out+'</nav>'
DESC={"index":"三项联合信条（比利时信条、海德堡要理问答、多特信经）的欧陆改革宗中文深读：CCI 原文逐字收录，圣经与圣约视角、时间线、地图、动画图示、比较、背诵与自测。"}
def page(cur,body):
    n={k:len(re.findall(r'<section class="l2',h)) for k,h in BODY.items()}
    title=LABEL[cur]+" · "+SITE if cur!="index" else "三项联合信条 · 欧陆改革宗深读（比利时信条·海德堡要理问答·多特信经）"
    desc=DESC.get(cur) or re.sub(r'<[^>]+>','',re.search(r'<p class="lead">(.*?)</p>',body).group(1))+" "+SITE+"。"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} {V}</title><meta name="description" content="{H.escape(desc[:150])}"><meta name="theme-color" content="#070d22"><script>try{{var de=document.documentElement;de.classList.add("jsok");if(localStorage.getItem("mk.off")==="1")de.classList.add("mkoff");var s=de.style,a=+localStorage.getItem("tfu1.tw"),m=+localStorage.getItem("tfu1.twm"),w=innerWidth;if(a>=220&&a<=Math.min(680,w*.6))s.setProperty("--tw",a+"px");if(m>=240&&m<=Math.min(560,w*.94))s.setProperty("--twm",m+"px")}}catch(e){{}}</script><link rel="stylesheet" href="assets/styles.css?v={V}"></head><body data-page="{cur}" data-total="{n.get(cur,0)}">
<div id="prog"></div>{toc_html(cur)}<div id="tocgrip" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度（左右方向键微调，双击还原）" title="拖动调整目录宽度；双击还原" tabindex="0"></div><button id="tocbtn" class="fab" aria-label="显示目录" aria-controls="toc" type="button">☰ 目录</button>
<main id="main">{tabs(cur)}{'' if cur=='index' else f'<p class="readchip">本页已读 <b id="pgread">0</b> / {n.get(cur,0)} 个小节</p>'}{'<div class="secbar"><b>🎯 阅读建议</b><span>先读彩色标记；“辅助”区块默认折叠。</span><button class="btn ghost" type="button" data-secall="open">展开全部辅助</button><button class="btn ghost" type="button" data-secall="close">收起全部辅助</button></div>' if 'class="secd"' in body else ''}{body}{pager(cur)}<footer class="foot"><p>{SITE} · <b>{V}</b></p><p>以圣经为最高权威；信条与信经为从属标准。三项联合信条与三大信经原文取自 <a href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">CCI《赞美手册》中文版</a>。姊妹站：<a href="{CREEDS_SITE}" target="_blank" rel="noopener">三大公教会信经 · 欧陆改革宗深读</a>。</p></footer></main>
<script>window.TEC={json.dumps({"v":V,"pages":[{"k":k,"f":f,"t":t,"n":n.get(k,0)} for k,f,t,_ in PAGES[1:]]},ensure_ascii=False)}</script>
<script src="assets/app.js?v={V}" defer></script></body></html>'''
def index_body():
    hc=J("hc"); nq=sum(1 for l in hc["lds"] for b in l["blocks"] if b["t"]=="h4")
    bcn=len(J("bc")["articles"]); dn=sum(len(h["items"]) for h in J("dort")["heads"])
    desc={"bible":"救恩史四幕、圣约框架、三份文件如何成为一个整体","hc":"52 主日 · 罪·救·谢 · 本质与应用 · 时间线与地图","bc":"37 条七群 · 德布利的故事 · 11 张深读卡","dort":"1618–19 · 4 项 · 34 条错谬反驳 · TULIP 术语说明",
      "compare":"体裁、问题、对照表、签署书与 BC 9","westminster":"WCF/WLC/WSC 十五个主题的对读","hct":"129 问逐字全文（CCI）","bct":"37 条逐字全文（CCI）","dtt":"63 个条目逐字全文（CCI）",
      "creedsx":"三大信经 CCI 原文附录","memory":"口诀、导图、翻卡、15 题自测、52 周计划","sources":"哪些逐字、哪些转述、哪些 CCI 没有"}
    icon={k:i for k,_,_,i in PAGES}
    steps="".join(f'<a class="step" href="{FILE[k]}" data-pg="{k}" style="--i:{n}"><span class="sno">{n+1}</span><span class="si">{ic(icon[k],"ic big")}</span><b>{LABEL[k]}</b><small>{desc[k]}</small><span class="bar"><i></i></span><em class="pc" data-pc="{k}">未读</em></a>' for n,(k,_,_,_) in enumerate(PAGES[1:]))
    hero=f'''<header class="hero"><div class="hin"><div class="badge">欧陆改革宗 · 三项联合信条</div><h1>三项联合信条<br><span>比利时信条 · 海德堡要理问答 · 多特信经</span></h1><p>先看整本圣经与圣约，再逐条深入三份文件：为什么写、怎么写、写了什么、今天怎样用。三项联合信条与所有引文<b>逐字取自 CCI《赞美手册》中文版</b>。</p>
<div class="trio"><a href="bc.html" class="tri" style="--c:#5aa9e6"><i>{ic("scroll","ic big")}</i><b>比利时信条</b><small>1561 · 告白 · 37 条</small></a><a href="hc.html" class="tri" style="--c:#81b29a"><i>{ic("heart","ic big")}</i><b>海德堡要理问答</b><small>1563 · 问答 · 52 主日</small></a><a href="dort.html" class="tri" style="--c:#d4af37"><i>{ic("scale","ic big")}</i><b>多特信经</b><small>1618–19 · 裁决 · 4 项</small></a></div>
<div class="stats"><div><b data-count="{bcn}">{bcn}</b><small>条比利时信条</small></div><div><b data-count="{nq}">{nq}</b><small>问海德堡要理问答</small></div><div><b data-count="{dn}">{dn}</b><small>个多特条目</small></div><div><b data-count="34">34</b><small>条错谬反驳</small></div></div>
<div class="hbtn"><a class="btn" href="bible.html">开始阅读：全本圣经视角</a><a class="btn ghost" href="hc.html#hcd-struct">HC 三部分</a><a class="btn ghost" href="dort.html#dd-tulip">TULIP 与多特</a></div></div></header>'''
    prog='''<section class="l1" id="path"><header class="l1h reveal"><span class="ico">'''+ic("map","ic big")+'''</span><div><div class="kick">学习路径</div><h2>十二站学习路径与进度</h2><p class="lead">建议顺序：先读圣经，再读三份文件的深读页，然后比较与对照，最后读原文库、背诵与自测。进度只保存在你的浏览器里（localStorage），不上传。</p></div></header>
<div class="progbox reveal"><div class="ring2" id="ringbox"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="rb"/><circle cx="60" cy="60" r="52" class="rf" id="ringf" pathLength="100" stroke-dasharray="0 100"/></svg><div class="rt"><b id="ringn">0%</b><small>已读小节</small></div></div><div class="pinfo"><p>已读 <b id="readn">0</b> / <b id="readt">0</b> 个小节（滚动到小节即记为已读）。自测最近得分：<b id="quizs">未做</b>。</p><p><button class="btn ghost" id="resetp" type="button">清除进度</button></p></div></div>
<div class="steps">'''+steps+'''</div></section>'''
    vis=[("🗺️","SVG 地图与路线","海德堡、图尔奈、低地国家、多德雷赫特、日内瓦与苏黎世等地图。","hc.html#hcd-geo"),("🧭","时间线","每份文件一条动画时间线。","bc.html#bcd-tl"),("🏗️","HC 三部分动画结构条","按问数比例画出罪·救·谢。","hc.html#hcd-struct"),
         ("🧩","BC 37 条地图","七群着色的方块，点任一块跳到原文。","bc.html#bcd-map"),("🌷","TULIP ↔ 抗辩派五点","分层面板：抗辩派 vs 多特的回答。","dort.html#dd-tulip"),("📋","主题×文件对照表","十四个主题，三份文件的链接矩阵。","compare.html#cp-xmap"),
         ("📜","签署书","CCI 签署书原文与结构分解。","compare.html#cp-sub"),("🧠","思维导图 · 翻卡 · 自测","口诀、24 张翻卡、15 题自测、52 周计划。","memory.html#mem-mind"),("↔️","可拖宽的目录","拖目录右缘的金色手柄调宽（宽度会记住）；手机上抽屉也能拉宽；方向键微调，双击还原。","index.html#idx-vis"),("🔤","背诵版一条一行","使徒·尼西亚·亚他那修：一条（一点）一行，小句连读；全显、首字提示、全遮、跟读。","creedsx.html#cr-ap"),("🔍","三信经深度对比","总表、问题→信经流程、时间线与地图、同异矩阵、为何是三份。","creedsx.html#cr-cmp"),("🌐","参考站互证","七个教会与神学院页面的逐字引文与“有没有提”矩阵。","compare.html#cp-ref"),("⚖️","威斯敏斯特对照","十五个主题的“实质同／措辞异／强调异”。","westminster.html#wm-table")]
    v="".join(f'<a class="card vcard" href="{u}" style="--c:#d4af37"><div class="ct"><span>{i}</span>{t}</div><p>{p}</p></a>' for i,t,p,u in vis)
    guide='''<section class="l2 reveal" id="idx-vis"><h3><span class="n">·</span>'''+ic("cross")+'''本站的视觉与互动工具</h3><div class="grid g3">'''+v+'''</div>
'''+key("<b>读法：</b>每个深读页先给“整本圣经的位置”，再给“逐条的局部”。左侧目录可以收起；没有 JavaScript 时所有内容仍然全部可见。颜色约定：<span class=hl-f>蓝＝父</span>、<span class=hl-s>金＝子</span>、<span class=hl-g>绿＝圣灵</span>。")+note("三项联合信条原文来自 CCI；讲解、图表与比较是本站的学习材料。哪些是逐字、哪些是转述、哪些 CCI 上没有，见"+'<a href="sources.html">第十二部分</a>。')+'</section>'
    return hero+prog+guide
BODY["index"]=index_body()
core.CUR["f"]="index.html"
import own,t87
import notes,trim
DEEP={"bible","hc","bc","dort","compare","westminster","memory"}; RECITE={"creedsx"}
MKS={};CUT={}
for k,f,_,_ in PAGES:
    h=own.mark(rewrite(k,BODY[k]))
    h,c=trim.cut(k,h); CUT[k]=c
    out=page(k,h)
    out,st=notes.apply(out,deep=k in DEEP,recite=k in RECITE); MKS[k]=st
    out=t87.post(out,fold=k in {"hct","bct","dtt","creedsx"})
    open(f,"w",encoding="utf-8").write(out)
trim.check()
print("marks",{k:v for k,v in MKS.items() if v}); print("trim chars",CUT,sum(CUT.values()))
own.check()
if UNRES: print("WARN unresolved links:",sorted(set(UNRES))[:40],len(UNRES))
print("built",[(f,round(len(open(f,encoding="utf-8").read())/1024)) for _,f,_,_ in PAGES])
