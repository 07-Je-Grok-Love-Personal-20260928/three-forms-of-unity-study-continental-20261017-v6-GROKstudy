# -*- coding: utf-8 -*-
"""5.9 参考站互证：只用我们真正读到的页面。每条引文构建时核对为 data/ref/*.txt（抓取副本）的逐字子串。"""
import re,html as H
from core import *
SITES={
 "ccreformed":("ccreformed.org（洛杉矶华人改革宗·恩约教会）","https://www.ccreformed.org/our-belief/","zh"),
 "canrc":("canrc.org（加拿大归正教会）","https://canrc.org/beliefs","en"),
 "urcna":("urcna.org（北美联合改革宗教会）","https://www.urcna.org/creeds","en"),
 "heritage":("heritagereformed.com（遗产改革宗教会）","https://heritagereformed.com/about-the-hrc/doctrinal-standards-and-worship/","en"),
 "reformedbeginner":("reformedbeginner.net（改革宗初学者）","https://www.reformedbeginner.net/ecumenical-creeds/","zh"),
 "wts":("wts.edu（威斯敏斯特神学院）","https://www.wts.edu/about/mission-values","en"),
 "crts":("crts.edu（改革宗神学院·台北）","https://crts.edu/en/intro/","zh"),
}
FILEOF={"heritage":"heritagereformed"}
_T={}
def txt(k):
    if k not in _T: _T[k]=re.sub(r"\s+"," ",open(f"data/ref/{FILEOF.get(k,k)}.txt",encoding="utf-8").read())
    return _T[k]
def R(site,phrase):
    """逐字引用：phrase 必须是抓取页面文字的子串（空白归一）。"""
    assert phrase in txt(site),f"R 未找到：{site}｜{phrase}"
    lang=SITES[site][2]
    return f'<q class="xq" lang="{"en" if lang=="en" else "zh"}">{H.escape(phrase,quote=False)}</q>'
def has(site,rx): return re.search(rx,txt(site)) is not None
def mark(b): return '<span class="mky">✓</span>' if b else '<span class="mkn">—</span>'
def site_a(k): return f'<a href="{SITES[k][1]}" target="_blank" rel="noopener">{SITES[k][0]}</a>'

def l2():
    rows=[
     ["ccreformed",R("ccreformed","古代信经把我们连结在古代基督教会上，而三联合信条把我们连结在十六、十七世纪广大的改革宗传统中。"),"<b>两条线</b>：古代信经是<b>纵向</b>——与历代教会同一信仰；三项联合信条是<b>横向</b>——与十六、十七世纪改革宗传统同一信仰。"],
     ["ccreformed",R("ccreformed","这些文件的权威永远服于圣经"),"<b>权威次序</b>：圣经是根基，信条是从属标准。与本站以圣经为最高权威一致。"],
     ["canrc",R("canrc","We consider these creeds to be faithful summaries of the Word of God. As human documents, however, they possess human authority. Only the Word of God possesses divine authority.")+'<small class="tr">大意：我们视这些信经为神话语的忠实摘要；作为人的文件，只有人的权威；只有神的话有神的权威。（本站译）</small>',"<b>“摘要”而非“新启示”</b>：信条随时要被圣经检验。"],
     ["urcna",R("urcna","are concise and authorized statements of the essential tenets of the faith")+'<small class="tr">大意：简明、经教会授权的信仰要点陈述。（本站译）</small>',"信经的<b>定义</b>：简明（concise）、有授权（authorized）、讲要点（essential tenets）。"],
     ["urcna",R("urcna","have been approved and accepted by a large portion of the churches of Christendom")+'<small class="tr">大意：被基督教世界大部分教会认可并接受。（本站译）</small>',"「普世（ecumenical）」的含义就是<b>被广泛接受</b>，与 BC 9 的理由相合。"],
     ["heritage",R("heritage","sought to demonstrate that Reformed believers were orthodox, law-abiding Christians rather than rebels")+'<small class="tr">大意：要表明改革宗信徒是正统、守法的基督徒，而非叛乱者。（本站译）</small>',"<b>BC 为什么写</b>：在逼迫下向官长与公众自辩。"],
     ["heritage",R("heritage","organizes its 129 questions around the Romans-shaped themes of misery, redemption, and gratitude")+'<small class="tr">大意：以“罗马书式”的主题——愁苦、救赎、感恩——组织 129 问。（本站译）</small>',"<b>HC 怎么排</b>：罪·救·谢；与本站的三部分结构一致。"],
     ["heritage",R("heritage","convened to resolve the Arminian controversy that threatened the unity of the Reformed Churches in the Netherlands")+'<small class="tr">大意：为解决威胁荷兰改革宗教会合一的阿米念争论而召集。（本站译）</small>',"<b>Dort 为什么开</b>：教会合一受威胁，需要一个有权威的裁决。"],
     ["reformedbeginner",R("reformedbeginner","这些信经被西方教会几乎全部主流宗派所接纳"),"<b>“大公信经”的含义</b>。注意：该站的“大公信经”清单<b>含迦克顿定义</b>（四份），本站“三大信经”不含，原因见下。"],
     ["wts",R("wts","Reformed orthodoxy, as informed by the system of doctrine contained in the Westminster Standards, and secondarily in other Reformed confessions")+'<small class="tr">大意：改革宗正统以威斯敏斯特标准所含教义体系为主，其次才是其他改革宗信条。（本站译）</small>',"<b>英语长老会传统</b>以威斯敏斯特标准为主；本站把它作“次要比较”。"],
     ["crts",R("crts","本學院持守全球改革宗教會的信條，其中包括使徒信經、海德堡要理問答（1563）、韋斯敏斯德信條以及韋斯敏斯德大小要理問答（1643-1648）"),"华人神学教育把<b>古代信经、HC 与威斯敏斯特标准</b>并用——两个传统在华人教会里是<b>叠加</b>的关系。"]]
    t=table(["网站","原话（节录，逐字）","说明了什么 · 本站如何用"],[[site_a(k),q,w] for k,q,w in rows],"cmp xqt")
    feats=[("三大古代信经（使徒·尼西亚·亚他那修）",r"Athanasian|亚他那修"),("三项联合信条（BC·HC·Dort）",r"Three Forms|三联合|Heidelberg|海德堡"),("威斯敏斯德标准",r"Westminster|韋斯敏斯德|威斯敏斯特"),("迦克顿定义",r"Chalcedon|迦克顿")]
    ms=[]
    for k in SITES:
        ms.append([site_a(k)]+[mark(has(k,rx)) for _,rx in feats])
    mx=table(["网站"]+[f for f,_ in feats],ms,"cmp mx")
    flow_=flow([("圣经","唯一最高权威，无谬误","#a78bfa"),("古代三信经","纵向：与历代教会同一信仰","#81b29a"),("三项联合信条","横向：改革宗传统的具体回答","#d4af37"),("签署与宣讲","教会生活：签署书、主日宣讲","#5aa9e6")])
    return L2("cp-ref","5.9","参考站互证：各教会怎样表述“核心”",
      '<p>下面只用我们<b>实际读到</b>的页面（抓取副本存于 <code>data/ref/</code>；<b>每条引文在生成网页时由程序核对为页面文字的逐字子串</b>）。英文引文保持英文，大意为本站翻译并已标注。opc.org 与 canadianreformedseminary.ca 本轮抓取失败（超时／403），prca.org 此前被拦截，这三站<b>不在此引用</b>。</p>'
      +flow_+t
      +'<h4 class="qh">各站“有没有提”（程序对页面文字搜索）</h4>'+mx
      +'<p class="cn">✓ ＝ 抓取到的页面文字里出现了相应名称；— ＝ 该页面没有出现（不代表该教会不接受）。</p>'
      +key("<b>六站共识：</b>①圣经至上；②信经是“忠实的摘要”，权威从属；③古代三信经（纵向）＋大陆三项联合信条（横向）是改革宗教会的通用教义准则；④职员签署、主日宣讲，使信条进入教会生活。")
      +hard("<b>分歧：</b>迦克顿定义是否列入“大公信经”（reformedbeginner.net 列入；CCI、本站的“三大信经”不列）；威斯敏斯德标准在英语长老会传统是<b>主要</b>标准，在欧陆改革宗传统是<b>次要比较</b>。两者都不是“更正统”，是传统不同。"))
