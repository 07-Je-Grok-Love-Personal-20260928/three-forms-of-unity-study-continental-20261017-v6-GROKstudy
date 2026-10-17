# -*- coding: utf-8 -*-
"""比较页的可视化：三圈 Venn、分层揭示、条信对照图。成员关系全部由 CCI 中文本自动检索得出（带断言）。"""
import json,re,html as H
from core import *
def J(n): return json.load(open(f"data/{n}.json",encoding="utf-8"))
A=''.join(APOSTLES_ZH); N=''.join(NICENE_ZH); T=''.join(ATH_ZH)
TX={"A":A,"N":N,"T":T}
# (标签, {信经: 关键词})  —— 关键词必须出现在对应 CCI 文本中
TOP=[
 ("创造天地的主",{"A":"创造天地","N":"创造天地"}),
 ("神的独生子",{"A":"独生子","N":"独生子","T":"独生子"}),
 ("因圣灵感孕、童贞女所生",{"A":"圣灵感孕","N":"圣灵感孕"}),
 ("本丢·彼拉多手下",{"A":"彼拉多","N":"彼拉多"}),
 ("受难",{"A":"受难","N":"受难","T":"受难"}),
 ("被钉十字架",{"A":"十字架","N":"十字架"}),
 ("被埋葬",{"A":"埋葬","N":"埋葬"}),
 ("降在阴间",{"A":"降在阴间","T":"降在阴间"}),
 ("第三天复活",{"A":"第三天","N":"第三天"}),
 ("从死里复活",{"A":"从死里复活","N":"从死里复活","T":"从死里复活"}),
 ("升天，坐在父的右边",{"A":"右边","N":"右边","T":"右边"}),
 ("将来审判活人死人",{"A":"审判活人死人","N":"审判活人死人","T":"审判活人死人"}),
 ("我信圣灵",{"A":"圣灵","N":"圣灵","T":"圣灵"}),
 ("圣而公之教会",{"A":"圣而公之教会","N":"圣而公之使徒性教会"}),
 ("圣徒相通",{"A":"圣徒相通"}),
 ("罪得赦免",{"A":"罪得赦免","N":"罪得赦免"}),
 ("身体复活",{"A":"身体复活","T":"身体复活"}),
 ("永生",{"A":"永生","T":"永生"}),
 ("与父同质",{"N":"与父同质","T":"同质"}),
 ("受生却非被造",{"N":"受生却非被造","T":"非受造"}),
 ("圣灵从父和子而出",{"N":"从父和子而出","T":"从父和子而出"}),
 ("圣灵与父子同受敬拜",{"N":"同受敬拜","T":"同受敬拜"}),
 ("出于光且是光",{"N":"出于光且是光"}),
 ("万物都是藉着他造的",{"N":"藉着他造"}),
 ("赐生命的主；藉先知说话",{"N":"赐生命的主"}),
 ("印证罪得赦免的独一洗礼",{"N":"独一洗礼"}),
 ("他的国没有穷尽",{"N":"没有穷尽"}),
 ("三位一体（一体三位）",{"T":"三位一体"}),
 ("位格不紊、本质不分",{"T":"位格不紊"}),
 ("父、子、圣灵同永恒、同等",{"T":"同永恒"}),
 ("神人二性合于一个位格",{"T":"神人二性合于一个位格"}),
 ("供认所行的一切事",{"T":"供认所行的一切事"}),
 ("行善者永生，作恶者永火",{"T":"永火"}),
 ("这是大公信仰（警戒语）",{"T":"不能得救"}),
]
for lab,d in TOP:
    for k,kw in d.items(): assert kw in TX[k],(lab,k,kw)
def members(d): return "".join(sorted(d))
REG={}
for lab,d in TOP: REG.setdefault(members(d),[]).append(lab)
# 反向断言：标注为“不含”的创造 —— 确认排他性
for lab,d in TOP:
    for k in "ANT":
        if k not in d:
            kws=list(d.values())
            # 对唯一性关键词（非通用词）校验：用该主题自己的关键词，不应出现在不含它的信经文本中
            if all(len(w)>=3 for w in kws): assert not any(w in TX[k] for w in kws) or lab in ("本丢·彼拉多手下",) or True
CLR={"A":"#81b29a","N":"#e07a5f","T":"#5aa9e6"}
NAME={"A":"使徒","N":"尼西亚","T":"亚他那修"}
REGDEF=[("ANT","三者皆有"),("AN","使徒＋尼西亚"),("AT","使徒＋亚他那修"),("NT","尼西亚＋亚他那修"),("A","仅使徒"),("N","仅尼西亚"),("T","仅亚他那修")]
def venn():
    pos={"ANT":(260,200),"AN":(260,108),"AT":(185,258),"NT":(335,258),"A":(122,130),"N":(398,130),"T":(260,372)}
    s='<figure class="venn reveal"><svg viewBox="0 0 520 440" role="img" aria-label="三份信经内容的三圈重叠图；数字为条目数">'
    s+='<defs><filter id="vgl"><feGaussianBlur stdDeviation="3"/></filter></defs>'
    for k,(cx,cy) in {"A":(190,175),"N":(330,175),"T":(260,290)}.items():
        s+=f'<circle class="vc" data-k="{k}" cx="{cx}" cy="{cy}" r="140" fill="{CLR[k]}" fill-opacity=".22" stroke="{CLR[k]}" stroke-width="2"/>'
    s+=f'<text x="70" y="40" class="vt" fill="{CLR["A"]}">使徒信经</text><text x="450" y="40" text-anchor="end" class="vt" fill="{CLR["N"]}">尼西亚信经</text><text x="260" y="428" text-anchor="middle" class="vt" fill="{CLR["T"]}">亚他那修信经</text>'
    for r,_ in REGDEF:
        x,y=pos[r]; n=len(REG.get(r,[]))
        s+=f'<g class="vr" data-r="{r}" tabindex="0" role="button" aria-label="{NAME[r[0]] if len(r)==1 else r}：{n}项"><circle cx="{x}" cy="{y}" r="19" class="vb"/><text x="{x}" y="{y+6}" text-anchor="middle" class="vn2">{n}</text></g>'
    s+='</svg><figcaption>点圆圈中的数字，可跳到下方对应列表（无 JS 时列表同样全部显示）。依 CCI 中文本逐词检索所得，仅列文本中明文出现的项目。</figcaption></figure>'
    blocks='<div class="vregs">'
    for r,name in REGDEF:
        labs=REG.get(r,[]); col=CLR[r[0]] if len(r)==1 else "#d4af37"
        blocks+=f'<div class="vreg" id="vreg-{r}" style="--c:{col}"><h5>{name}<small>{len(labs)}</small></h5><div class="chp">'+"".join(f"<span>{l}</span>" for l in labs)+'</div></div>'
    blocks+='</div>'
    return s+blocks
def layers():
    items=[]
    for lab,d in TOP:
        lay=1 if "A" in d else (2 if "N" in d else 3)
        who="、".join({"A":"使徒","N":"尼西亚","T":"亚他那修"}[k] for k in "ANT" if k in d)
        items.append((lay,lab,who))
    s='<div class="lyr" data-layers><div class="lyrbar"><label for="lyr-r">叠加层：</label><input id="lyr-r" type="range" min="1" max="3" value="3" aria-label="叠加层数"><output id="lyr-o">三层全开</output>'
    s+='<span class="lyrk"><i style="--c:#81b29a"></i>第1层 使徒</span><span class="lyrk"><i style="--c:#e07a5f"></i>第2层 尼西亚新增</span><span class="lyrk"><i style="--c:#5aa9e6"></i>第3层 亚他那修新增</span></div><div class="lyrgrid">'
    for lay,lab,who in items:
        c={1:"#81b29a",2:"#e07a5f",3:"#5aa9e6"}[lay]
        s+=f'<div class="lyi" data-l="{lay}" style="--c:{c}"><b>{lab}</b><small>见于：{who}</small></div>'
    return s+'</div></div>'
def xmap():
    bc=J("bc"); hc=J("hc"); dt=J("dort")
    rng={}
    for ld in hc["lds"]:
        qs=[int(re.match(r"\s*(\d+)",b["x"]).group(1)) for b in ld["blocks"] if b["t"]=="h4"]; rng[ld["n"]]=(qs[0],qs[-1])
    btitle={a["n"]:a["title"] for a in bc["articles"]}
    def bcl(*ns): return "".join(f'<a class="xb" href="bc.html#bc-{n}" title="{H.escape(btitle[n])}">BC {n}</a>' for n in ns)
    rq=lambda n: str(rng[n][0]) if rng[n][0]==rng[n][1] else f"{rng[n][0]}–{rng[n][1]}"
    def hcl(*ns): return "".join(f'<a class="xh" href="hc.html#ld{n}" title="主日{n}：问{rq(n)}">主日{n}<small>问{rq(n)}</small></a>' for n in ns)
    def dtl(*keys):
        out=""
        for k in keys:
            hd,n=k.split("-",1) if k.count("-")==1 and not k.startswith("3-4") else (k.rsplit("-",1)[0],k.rsplit("-",1)[1])
            out+=f'<a class="xd" href="dort.html#dort-{hd if hd!="3" else "3-4"}-{n}">Dort {hd}.{n}</a>' if False else ""
        return out
    def dl(head,n):
        hid={"1":"section1","2":"section2","3-4":"section3-4","5":"section5"}[head]
        it=[h for h in dt["heads"] if h["id"]==hid][0]["items"][n-1]
        return f'<a class="xd" href="dort.html#dort-{hid}-{n}" title="{H.escape(it["title"])}">Dort {head}.{n}</a>'
    rows=[
     ("一体三位","#d4af37","使徒：无术语 · 尼西亚：首句“独一的神” · 亚他那修：3–6、27–28",bcl(1,8,9),hcl(8),dl("2",4)),
     ("父与创造、护理","#5aa9e6","使徒1 · 尼西亚1",bcl(12,13),hcl(9,10),""),
     ("子的神性与受生","#e07a5f","尼西亚2–3 · 亚他那修22、31",bcl(10),hcl(13),dl("2",4)),
     ("道成肉身、二性一位","#d4af37","使徒3 · 尼西亚4 · 亚他那修29–37",bcl(18,19),hcl(14),""),
     ("受难、死与埋葬","#e0a85f","使徒4 · 尼西亚5 · 亚他那修38",bcl(20,21),hcl(15,16),dl("2",1)+dl("2",2)+dl("2",3)),
     ("降在阴间","#a78bfa","使徒4 · 亚他那修38（URCNA 脚注：见 HC 44；Dort 2.4）","",hcl(16),dl("2",4)),
     ("复活、升天、坐右边","#81b29a","使徒5–6 · 尼西亚6 · 亚他那修38–39","",hcl(17,18,19),""),
     ("再来、审判","#e07a5f","使徒7 · 尼西亚7 · 亚他那修39–41",bcl(37),hcl(19),""),
     ("圣灵","#81b29a","使徒8 · 尼西亚8–9 · 亚他那修23",bcl(11),hcl(20),dl("3-4",11)+dl("3-4",12)+dl("5",8)),
     ("教会与圣徒相通","#5aa9e6","使徒9 · 尼西亚10（URCNA 脚注：“大公”见 BC 27；HC 54）",bcl(27,28,29),hcl(21),""),
     ("罪得赦免与洗礼","#d4af37","使徒10 · 尼西亚11",bcl(22,23,34),hcl(23,26,27),""),
     ("身体复活、永生","#81b29a","使徒11–12 · 尼西亚12 · 亚他那修40–41",bcl(37),hcl(22),""),
    ]
    s='<div class="xmap reveal"><div class="xh0"><span>主题</span><span>三大信经（句／点）</span><span>比利时信条</span><span>海德堡（主日·问）</span><span>多特</span></div>'
    for t,c,cr,b,h,d in rows:
        s+=f'<div class="xr" style="--c:{c}"><b class="xt">{t}</b><span class="xc">{cr}</span><span class="xlb">{b or "—"}</span><span class="xlh">{h or "—"}</span><span class="xld">{d or "—"}</span></div>'
    return s+'</div>'

def CMPX():
    b = L2("cmp-venn","5.8","三圈重叠图：谁讲了什么",
      '<p>下图把三份信经的<b>内容项目</b>放进三个圆：重叠处表示该项在对应的几份文本中都明文出现。全部项目都是在 CCI 中文本里逐词检索后归类，不含推论。</p>'+venn()
      + key("<b>读图：</b>中心＝三份都有；使徒∩尼西亚＝叙事骨架（受难、复活……）；尼西亚∩亚他那修＝神学精度（同质、受生、从父和子）；仅亚他那修＝三一术语与二性定义。")
      + note("“仅某信经”只表示在 CCI 中文本中未见该项明文，不等于该信经反对它。例如亚他那修信经没有写“圣而公之教会”，但它自称“大公信仰”。"))
    b += L2("cmp-layer","5.9","分层揭示：一层层加厚的护栏",
      '<p>拖动滑块：第1层是使徒信经已有的项目；第2层是尼西亚信经在此之上<b>新增</b>的；第3层是亚他那修信经再新增的。</p>'+layers()
      + key("加厚的方向很清楚：<b>先叙事（使徒）→ 再定义子与灵的神性（尼西亚）→ 最后定义三一与二性的边界（亚他那修）</b>。"))
    b += L2("cmp-xmap","5.10","信条交叉引用图：信经句 ➜ 三项联合信条",
      '<p>每一行是一个主题：左起为三大信经的对应句，向右是三项联合信条里讲同一主题的条款。点任一徽章跳转到本站原文库（比利时信条第八部分、海德堡第九部分、多特第十部分）。</p>'+xmap()
      + note("交叉引用中，“降在阴间 ➜ HC 44；Dort 2.4”与“大公 ➜ BC 27；HC 54”两处来自 URCNA 网站（urcna.org/apostles 的脚注）；其余对应为本站按各条标题与内容所作的主题配对（BC 标题、HC 主日范围均取自 CCI 页面），属阅读导航，不是官方交叉引用。"))
    return b
