# -*- coding: utf-8 -*-
"""短引文：全部取自 data/*.json（CCI 原文），去掉脚注标记 ⟦n⟧ 后逐字引用。"""
import json,re
def _L(n): return json.load(open(f"data/{n}.json",encoding="utf-8"))
def strip(s): return re.sub(r"⟦\d+⟧","",s)
_bc,_hc,_dt=_L("bc"),_L("hc"),_L("dort")
SRC="华人改革宗《赞美手册》（Book of Praise）中文版，ccifellowship.org"
def bc_paras(n): return [strip(b["x"]) for b in _bc["articles"][n-1]["blocks"] if b["t"]=="p"]
BC={n:"　".join(bc_paras(n)) for n in range(1,38)}
HC={}
for ld in _hc["lds"]:
    bl=ld["blocks"]
    for i,b in enumerate(bl):
        if b["t"]=="h4":
            m=re.match(r"\s*(\d+)\s*[.．]\s*问\s*[：:]\s*(.*)",b["x"]); n=int(m.group(1))
            a=bl[i+1]["x"]; a=re.sub(r"^答\s*[：:]\s*","",strip(a))
            HC[n]=(m.group(2),a)
DORT={}
for h in _dt["heads"]:
    for it in h["items"]:
        DORT[f'{h["num"]}.{it["n"]}']="　".join(strip(b["x"]) for b in it["blocks"] if b["t"]=="p")
