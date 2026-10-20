# -*- coding: utf-8 -*-
"""v7：《中国改革宗教会 敬拜手册》2015 版（用户提供的 PDF）——逐字摘引、HC 印刷小标题、敬拜流程、与 CCI 的差异。
所有 PQ(...) 摘引在构建时断言为 PDF 印刷正文（按页）的逐字子串；tools/verify_pdf.py 再对生成页复核。
本站正文仍以 CCI 为准；PDF 只补 CCI 没有的内容，并清楚标注页码。"""
import json,re,html as H
D=json.load(open("data/pdf/pdf2015.json",encoding="utf-8"))
PAGES={int(k):v for k,v in D["pages"].items()}
BOOK="《中国改革宗教会敬拜手册》2015 版"
def _n(s): return re.sub(r"\s+","",s)
def ptext(p,span=1): return _n("".join(PAGES.get(i,"") for i in range(p,p+span+1)))
def PQ(p,phrase,span=0):
    assert _n(phrase) in ptext(p,span), f"PQ 未在 PDF 第{p}页找到：{phrase}"
    return f'<q class="pdfq" data-p="{p}" data-span="{span}">{H.escape(phrase,quote=False)}</q><span class="pdfsrc">出自{BOOK} 第 {p} 页</span>'
def label(p): return f'<span class="pdfsrc">出自{BOOK} 第 {p} 页</span>'
# ---------- HC 印刷小标题 ----------
def hc_heads_table(link=lambda n:f"主日{n}"):
    rows=[]
    for h in D["hc_heads"]:
        rows.append(f'<tr><td><b class="pdfh">{PQ(h["page"],h["t"])}</b></td><td>{link(h["ld"])} 起</td></tr>')
    return ('<div class="tw"><table class="cmp pdft"><thead><tr><th>敬拜手册里的印刷小标题（逐字）</th><th>位置</th></tr></thead><tbody>'
            +"".join(rows)+'</tbody></table></div>')
# ---------- 敬拜流程 ----------
def worship_block():
    am=[("宣告",PQ(139,"宣告：诗篇124:8")),("十诫",PQ(139,"圣约十诫（出埃及记20:2-17 或申命记5:6-21）")),("证道",PQ(139,"牧师证道（通常以唱诗回应）"))]
    pm=[("信经",PQ(140,"《使徒信经》或《尼西亚信经》（随后可唱诗）")),("唱信经",PQ(140,"会众唱《使徒信经》（赞美诗1 或2）")),
        ("读要理",PQ(140,"诵读《海德堡要理问答》（待讲解之主日）")),("讲要理",PQ(140,"牧师讲道（通常以唱诗回应）"))]
    def lane(t,ic,items,c):
        return (f'<div class="wlane" style="--c:{c}"><div class="wl-h">{ic} {t}</div><ol class="wl-s">'
                +"".join(f'<li class="reveal" style="--i:{i}"><b>{k}</b><span>{v}</span></li>' for i,(k,v) in enumerate(items))+'</ol></div>')
    return ('<div class="wflow">'+lane("上午聚会：律法在前","⚖️",am,"#5aa9e6")+lane("下午聚会：信经＋要理问答","📖",pm,"#d4af37")+'</div>'
            +'<p class="pdfnote">节选自敬拜手册“敬拜流程”（第一种流程，第 139–140 页）。第二种流程把“诵读《海德堡要理问答》”放在下午聚会第 6 项，信仰告白放在讲道之后（第 141 页）。</p>')
# ---------- 差异 ----------
NOTABLE=[  # (doc, CCI 片段关键字, 说明)
 ("creeds","非三位非受造者","亚他那修信经第 12 点。CCI 作“非三位非受造者”，与拉丁原文 non tres increati 一致；PDF 少一个“非”字，应是排印错误。"),
 ("creeds","被钉十字架；受难","尼西亚信经：PDF“被钉上十字架上”多一个“上”，CCI 已改顺。"),
 ("bc","不可测透","BC 1：CCI“不可测透”，PDF“不可测”。"),
 ("bc","是绝对无误的","BC 4：CCI 写圣经“绝对无误”，PDF 写“绝对不可否认”。CCI 的说法更直接。"),
 ("bc","虚空的（参见","BC 7：PDF 保留诗62:9 的修辞“比虚空还要虚空”。"),
 ("bc","论万物被造，尤其是天使被造","BC 12 标题：PDF 只作“论创造”。"),
 ("bc","没有神的旨意或许可","BC 13：CCI 加上“或许可”，并把标题“眷顾”改为“护理”。"),
 ("bc","神的赦罪并不意味着","BC 15：同一意思，句子重写。"),
 ("bc","真信徒的圣会。这些","BC 27：PDF“圣洁的会众、真信徒的聚集”，CCI 合为“真信徒的圣会”。"),
 ("bc","救恩不在她之外","BC 28：PDF 作“得救之人的聚集，在她之外没有救恩”。"),
 ("bc","论政府治理我们","BC 36 标题：PDF“论民事管理”；文中“治民官长”，CCI 作“民事长官”。"),
 ("hc","喜乐地生或死","HC 2：“快乐地”改为“喜乐地”。"),
 ("hc","因始祖的悖逆和堕落而变得败坏","HC 7：CCI 把“因此”展开为“因始祖的悖逆和堕落”，并去掉“极其”。"),
 ("hc","《使徒信经》总结并教导","HC 22–24、59：PDF 作“基督教大公无疑信条”与“这些信条”，CCI 直接写《使徒信经》与“这一信经”。"),
 ("hc","活过来","HC 45：PDF“复活”，CCI“活过来”。"),
 ("hc","重新反映出他的形像","HC 86：PDF“使我们有他的形像”。"),
 ("dort","留在不信此福音","Dort 1.4：“停留在”改“留在”。"),
 ("dort","神原因用福音召我们去信的那位基督","Dort 3/4.9：PDF“藉着福音让我们认识的基督”。CCI 这句的“神原因用”读来不顺，疑似排印问题；本站仍按 CCI 收录。"),
 ("dort","情感混乱","Dort 3/4 错谬反驳 4：PDF“情感任性”。"),
 ("dort","备受折磨","Dort 5.5：PDF“良心受到重创”。"),
]
def _find(doc,key):
    for g in D["diffs"]:
        if g["doc"]==doc and key in g["cci"]: return g
    raise AssertionError(f"差异表找不到：{doc}｜{key}")
DOCN={"creeds":"三大信经","bc":"比利时信条","hc":"海德堡要理问答","dort":"多特信经"}
def diff_section():
    c=D["diff_counts"]; r=D["ratio"]
    stat="".join(f'<div class="dstat" style="--c:{col}"><b>{DOCN[d]}</b><span class="dn">{c[d].get("用词",0)}</span><small>处用词差异</small><small>另有 {c[d].get("写法",0)} 处写法差异 · 相似度 {r[d]*100:.1f}%</small></div>'
                 for d,col in [("creeds","#a78bfa"),("bc","#5aa9e6"),("hc","#81b29a"),("dort","#d4af37")])
    rows="".join(f'<tr><td>{DOCN[d]} · {H.escape(_find(d,k)["label"])}</td><td>{_find(d,k)["page"]}</td><td class="dc">{H.escape(_find(d,k)["cci"])}</td><td class="dp">{H.escape(_find(d,k)["pdf"])}</td><td>{t}</td></tr>' for d,k,t in NOTABLE)
    full="".join(f'<tr><td>{DOCN[g["doc"]]} · {H.escape(g["label"])}</td><td>{g["page"]}</td><td class="dc">{H.escape(g["cci"])}</td><td class="dp">{H.escape(g["pdf"])}</td></tr>' for g in D["diffs"] if g["kind"]=="用词")
    return (f'<p>把敬拜手册 2015 版的印刷正文（第 5–138 页，已排除页码、经文脚注、读者批注）与本站使用的 CCI 文本逐字比对。<b>本站正文不改，仍以 CCI 为准。</b>下表片段已去空格、统一全角／半角标点，仅供比对，不作引文。</p>'
            f'<div class="dstats">{stat}</div>'
            '<div class="tw"><table class="cmp dtab"><thead><tr><th>位置</th><th>页</th><th>CCI</th><th>敬拜手册 2015</th><th>说明</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
            f'<details class="rfd"><summary>展开全部 {sum(1 for g in D["diffs"] if g["kind"]=="用词")} 处用词差异</summary><div class="tw"><table class="cmp dtab"><thead><tr><th>位置</th><th>页</th><th>CCI</th><th>敬拜手册 2015</th></tr></thead><tbody>'+full+'</tbody></table></div></details>'
            f'<p class="pdfnote">没计入差异的：PDF 的书名与部分标题行 {D["diff_skipped"]["heading"]} 处、页边经文旁注 {D["diff_skipped"]["margin_ref"]} 处；“写法”指只在数字写法或标点上不同（如“400”与“四百”）。</p>')
