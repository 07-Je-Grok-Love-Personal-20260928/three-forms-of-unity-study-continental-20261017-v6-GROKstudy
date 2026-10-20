# -*- coding: utf-8 -*-
"""共用：引用核对（Q）、链接助手、数据装载。所有 Q(...) 摘引都在构建时断言为 CCI 原文的逐字子串。"""
import json,re,html as H
from quotes import BC,HC,DORT,strip
def J(n): return json.load(open(f"data/{n}.json",encoding="utf-8"))
IB=J("ib_summ")
_hc=J("hc"); _bc=J("bc"); _dt=J("dort")
HCLD={}   # 问号 → 主日
HCRANGE={}
for ld in _hc["lds"]:
    qs=[int(re.match(r"\s*(\d+)",b["x"]).group(1)) for b in ld["blocks"] if b["t"]=="h4"]
    HCRANGE[ld["n"]]=(qs[0],qs[-1])
    for q in qs: HCLD[q]=ld["n"]
BCT={a["n"]:a["title"] for a in _bc["articles"]}
BCT={n:re.sub(r"^第.+?条\s*","",t) for n,t in BCT.items()}
DTITLE={}
for h in _dt["heads"]:
    for it in h["items"]:
        DTITLE[(h["num"],it["n"])]=re.sub(r"^第.+?条\s*","",it["title"])
HEADID={"1":"section1","2":"section2","3-4":"section3-4","5":"section5"}
def ibk(n):
    if n in (26,27): return "26-27"
    if n in (28,29,30): return "28-29-30"
    if n in (36,37): return "36-37"
    return str(n)
CCI="https://ccifellowship.org"
def _text(ref):
    k,v=ref.split(" ",1)
    if k=="BC": return BC[int(v)]
    if k=="HC":  # 问号
        q,a=HC[int(v)]; return q+"　"+a
    if k=="DORT": return DORT[v]
    raise KeyError(ref)
def Q(ref,phrase):
    """摘引 CCI 原文：phrase 必须是原文子串（忽略脚注标记）。返回带中文引号的 HTML。"""
    t=_text(ref)
    assert phrase in t, f"Q 摘引未在原文中找到：{ref}｜{phrase}"
    return "“"+H.escape(phrase,quote=False)+"”"
def QI(n,phrase):
    s=IB[ibk(n)][0] if n in range(1,53) else None
    assert phrase in s, f"QI 未找到：{n}｜{phrase}"
    return "“"+H.escape(phrase,quote=False)+"”"
def bl(n,t=None): return f'<a href="#bc-{n}" title="{H.escape(BCT[n])}">{t or "BC "+str(n)}</a>'
def bls(a,b): return f'<a href="#bc-{a}">BC {a}</a>–<a href="#bc-{b}">{b}</a>'
def hl(n,t=None): return f'<a href="#ld{n}">{t or "主日"+str(n)}</a>'
def hq(q,t=None):
    n=HCLD[q]; return f'<a href="#ld{n}" title="主日{n}">{t or "HC "+str(q)}</a>'
def hqs(a,b): return f'<a href="#ld{HCLD[a]}">HC {a}</a>–{b}'
def dl(h,n=None,t=None):
    if n is None: h,n=h.rsplit(".",1)
    n=int(n)
    return f'<a href="#dort-{HEADID[h]}-{n}" title="多特 {h}.{n}">{t or "Dort "+h+"."+str(n)}</a>'
def dre(h,t=None): return dl(h,len(next(x for x in _dt["heads"] if x["num"]==h)["items"]),t or f"Dort {h} 驳")
def A(u,t): return f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
def ibl(n,t=None):
    return A(f"{CCI}/books/i-belong/{ibk(n)}",t or f"CCI《我属于》{ibk(n)}")
def ibsum(n):
    s=IB[ibk(n)]; return s[0] if s else ""
def oa(u,t): return A(u,t)
CREEDS_SITE="https://three-ecumenical-creeds-study-continental-20261020-v11-grokser.surge.sh/"
MISC=J("cci_misc")
def M(key,phrase):
    t=MISC[key]["text"]; assert phrase in t, f"M 未找到：{key}｜{phrase}"
    return "“"+H.escape(phrase,quote=False)+"”"
def mu(key,t=None): return A(MISC[key]["url"],t or MISC[key]["title"])
