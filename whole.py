# -*- coding: utf-8 -*-
"""v6：每份文本的“整本圣经先行 → 圣经神学 → 圣约神学 → 欧陆改革宗读法 → 六个角度”，以及每页顶部的“本页一眼”核心条。
本站撰写的学习材料，不是 CCI 原文；引文一律走 Q()（构建时与 CCI 原文核对）。"""
from core import *

def pagecore(core, hook, hard_, key_=None):
    """页首核心条：🎯 核心 · 🧠 记忆钩 · ⚠️ 难点（· 🔑 重点）。"""
    k = f'<div class="pc4 pk"><i>🔑</i><div><b>重点</b><span>{key_}</span></div></div>' if key_ else ""
    return ('<div class="pagecore reveal" role="note" aria-label="本页一眼">'
            f'<div class="pc4 pc"><i>🎯</i><div><b>核心</b><span>{core}</span></div></div>'
            f'<div class="pc4 pm"><i>🧠</i><div><b>记忆钩</b><span>{hook}</span></div></div>'
            f'<div class="pc4 ph"><i>⚠️</i><div><b>难点</b><span>{hard_}</span></div></div>{k}</div>')

def stk(head, rows):
    """窄屏自动叠成卡片的表格（每格带小标签）。"""
    o = '<div class="tw stkw"><table class="stk"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
    for r in rows:
        o += "<tr>" + "".join(f'<td data-l="{head[i]}">{c}</td>' for i, c in enumerate(r)) + "</tr>"
    return o + "</tbody></table></div>"

def angles(rows):
    """rows: (图标, 角度, 问题, 回答, 颜色)。宽屏表格，窄屏叠成卡片。"""
    out = '<div class="angs">'
    for ico, ang, q, a, c in rows:
        out += (f'<div class="ang reveal" style="--c:{c}"><div class="ah2"><i>{ico}</i><b>{ang}</b></div>'
                f'<div class="aq"><small>要问</small>{q}</div><div class="aa"><small>答案</small>{a}</div></div>')
    return out + '</div>'

def whole_block(pid, title, intro, steps, bt_rows, ct_cards, ct_note, rr_cards, ang_rows, memo):
    """生成一个 L2：5 个 L3。pid 为 id 前缀。"""
    CUR["zero"] = 1
    l3 = L3(f"{pid}-w1", "整本圣经先行：这份文本在全书中的位置", intro + flow(steps), "book", "先整体")
    l3 += L3(f"{pid}-w2", "圣经神学：救恩史主线与代表经文",
             '<p class="sub">圣经神学看的是“神怎样一步步启示、一步步成就”。下表只列经文出处，不改写经文。</p>' +
             stk(["文本部分", "圣经主线", "代表经文"], bt_rows), "map", "主线")
    l3 += L3(f"{pid}-w3", "圣约神学：约的结构与三位一体的分工", cards(ct_cards, "g2") + note(ct_note), "link", "圣约")
    l3 += L3(f"{pid}-w4", "欧陆改革宗读法：怎样读、怎样用、与谁并读", cards(rr_cards, "g3"), "church", "改革宗")
    l3 += L3(f"{pid}-w5", "六个角度读一遍：同一份文本，六种问法", angles(ang_rows) + key(memo), "eye", "多角度")
    CUR["zero"] = 0
    return L2(f"{pid}-whole", "0", title, l3)
