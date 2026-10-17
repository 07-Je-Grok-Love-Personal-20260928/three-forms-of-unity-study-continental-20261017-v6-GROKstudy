# -*- coding: utf-8 -*-
"""三大信经背诵版：把 CCI 原文（data/creeds.json）按“条/组”切成一行一句。
只做切分与分组，不改一字；tools/verify_recite.py 校验：背诵版各行（.rt）连起来 = CCI 整段原文（忽略空白）。"""
import re,html as H
def pieces(text,seps="；。！"):
    out=[];cur=""
    for ch in text:
        cur+=ch
        if ch in seps: out.append(cur);cur=""
    if cur.strip(): out.append(cur)
    return [p for p in out]
def lines(text):
    """紧凑版：一条（一点）就是一行；条内的小句保持原标点、连成一行，在窄屏自然折行。"""
    return [text.strip()]
def li(t,pn=""):
    cl="".join(f'<i class="cl">{H.escape(p,quote=False)}</i>' for p in pieces(t,"，；。！") if p)
    return f'<li><span class="rt">{cl}</span></li>'
def art(no,text_lines,cls=""):
    return f'<div class="rart {cls}"><span class="rno">{no}</span><ul class="rls">'+"".join(li(t) for t in text_lines)+'</ul></div>'

# ---------- 使徒信经：12 条 · 3 段 ----------
AP_PARTS=[("一","圣父：创造","heart",[1]),("二","圣子：降生·受死·复活·再来","cross",[2,3,4,5,6,7]),("三","圣灵、教会与末事","dove",[8,9,10,11,12])]
AP_TITLES={1:("我信神","heart","全能的父·创造天地"),2:("独生子，我主","crown","耶稣基督"),3:("感孕与降生","dove","圣灵感孕·童贞女所生"),4:("受难、受死、埋葬、降在阴间","cross","彼拉多手下·十字架"),
 5:("第三天复活","sun","从死里复活"),6:("升天，坐在父右边","arrowup","全能父神的右边"),7:("将来审判活人死人","scale","必从那里降临"),8:("我信圣灵","dove","圣灵"),
 9:("圣而公之教会，圣徒相通","church","教会·圣徒相通"),10:("罪得赦免","key","赦罪"),11:("身体复活","leaf","身体复活"),12:("永生","sun","永生·阿们")}
def apostles(C):
    P=C["apostles"]["paras"]; s=pieces(P[1]); assert len(s)==6,s
    texts={1:P[0],2:s[0],3:s[1],4:s[2],5:s[3],6:s[4],7:s[5],8:P[2],9:P[3],10:P[4],11:P[5],12:P[6]}
    return texts
# ---------- 尼西亚信经：13 节 · 4 段（对应 CCI 的 7 段） ----------
NI_PARTS=[("一","圣父","heart",[1]),("二","圣子","crown",[2,3,4,5,6,7,8]),("三","圣灵","dove",[9,10]),("四","教会、洗礼与盼望","church",[11,12,13])]
NI_TITLES={1:("独一的神，全能的父","heart","原文第1段"),2:("独一的主，神的独生子","crown","原文第2段"),3:("出于神而为神（三联句）","tri","原文第2段"),4:("受生非被造，与父同质","shield","原文第2段"),
 5:("为拯救我们：降世为人","dove","原文第3段"),6:("被钉十字架，受难、被埋葬","cross","原文第3段"),7:("照圣经复活、升天","sun","原文第3段"),8:("再来审判，他的国没有穷尽","scale","原文第3段"),
 9:("圣灵：赐生命的主","dove","原文第4段"),10:("圣灵曾藉众先知说话","quill","原文第4段"),11:("独一圣而公之使徒性教会","church","原文第5段"),12:("独一洗礼，罪得赦免","drop","原文第6段"),13:("复活与更新的世界","sun","原文第7段")}
def nicene(C):
    P=C["nicene"]["paras"]; a=pieces(P[1]); b=pieces(P[2]); c=pieces(P[3])
    assert len(a)==4 and len(b)==6 and len(c)==2,(a,b,c)
    return {1:P[0],2:a[0],3:a[1],4:a[2]+a[3],5:b[0],6:b[1]+b[2],7:b[3],8:b[4]+b[5],9:c[0],10:c[1],11:P[4],12:P[5],13:P[6]}
# ---------- 亚他那修信经：42 点 · 11 组 ----------
AT_PARTS=[("序","大公信仰的必要","key",["A"]),("一","三位一体（第3–28点）","tri",["B","C","D","E","F"]),("二","基督的位格与工作（第29–41点）","cross",["G","H","I","J"]),("结","结语","scroll",["K"])]
AT_GROUPS={"A":("大公信仰必须持守",1,2,"key"),"B":("一体三位，三位一体",3,6,"tri"),"C":("三位同等：非受造·无限·永恒·全能",7,14,"scale"),"D":("一位神，一位主",15,20,"crown"),
 "E":("位格的关系：自有·受生·发出",21,24,"link"),"F":("无先后尊卑，同受敬拜",25,28,"hands"),"G":("必须信道成肉身的基督",29,30,"cross"),"H":("既是神又是人",31,33,"dove"),
 "I":("一位基督，不混淆不转变",34,37,"shield"),"J":("受难·复活·升天·审判",38,41,"sun"),"K":("这是大公信仰",42,42,"scroll")}
def athanasian(C):
    P=C["athanasian"]["paras"]; full=" ".join(P); pts={}
    ms=list(re.finditer(r"(\d+)\)\s*",full))
    for i,m in enumerate(ms):
        e=ms[i+1].start() if i+1<len(ms) else len(full)
        pts[int(m.group(1))]=full[m.end():e].strip()
    assert sorted(pts)==list(range(1,43)),sorted(pts)
    return pts
TOOL=('<div class="rtool" data-rtool><b>背诵工具</b>'
 '<button class="btn" type="button" data-rm="show">全显</button><button class="btn ghost" type="button" data-rm="cue">首字提示</button><button class="btn ghost" type="button" data-rm="hide">全遮</button>'
 '<button class="btn" type="button" data-rplay>▶ 跟读</button><label>速度 <select data-rspeed><option value="2600">慢</option><option value="1700" selected>中</option><option value="1000">快</option></select></label>'
 '<span class="sp"></span><small>点任一行可单独揭示；无 JavaScript 时全部显示。</small></div>')
def verbatim_text(C,key):
    return "".join(C[key]["paras"])
