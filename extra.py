# -*- coding: utf-8 -*-
P = {
"crown":'<path d="M3 8l4 4 5-7 5 7 4-4-2 11H5z"/><path d="M5 19h14"/>',
"sun":'<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
"arrowup":'<path d="M12 20V5M6 11l6-6 6 6"/><path d="M5 21h14"/>',
"drop":'<path d="M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z"/>',
"cup":'<path d="M6 4h12l-1 8a5 5 0 0 1-10 0z"/><path d="M12 15v5M8 21h8"/>',
"hands":'<path d="M8 21l-3-6 3-9 2 1-1 6 3-5 2 1-2 5 2-3 2 1-3 7z"/>',
"bread":'<path d="M4 12a8 6 0 0 1 16 0v6H4z"/><path d="M9 12v3M13 12v3M17 12v3"/>',
"play":'<path d="M7 4l13 8-13 8z"/>',
"eye":'<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
"list":'<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
"check":'<path d="M4 12l5 5L20 6"/>',
"mic":'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
"book":'<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6"/>',
"dove":'<path d="M3 13c4 0 6-3 7-7 2 3 5 4 9 4-1 5-5 9-11 9H5l2-3"/><circle cx="16" cy="8" r=".8"/>',
"flame":'<path d="M12 3c1 4 6 6 6 11a6 6 0 0 1-12 0c0-3 2-4 3-6 1 2 2 3 3 3 0-3-1-5 0-8z"/>',
"shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
"scale":'<path d="M12 3v18M6 21h12M4 7h16"/><path d="M6 7l-3 6a3 3 0 0 0 6 0zM18 7l-3 6a3 3 0 0 0 6 0z"/>',
"scroll":'<path d="M7 4h11a2 2 0 0 1 2 2v1h-4"/><path d="M16 7v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1h10"/><path d="M8 9h5M8 13h5"/>',
"brain":'<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 3 5 3 3 0 0 0 5 1V5a3 3 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-3 5 3 3 0 0 1-5 1"/>',
"library":'<path d="M4 4h4v16H4zM10 4h4v16h-4z"/><path d="M16 5l3.5-1 3 15-3.5 1z"/>',
"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"map":'<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
"alert":'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
"key":'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
"leaf":'<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
"users":'<circle cx="9" cy="8" r="3"/><path d="M3 20c0-4 3-6 6-6s6 2 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c3 0 5 2 5 5"/>',
"church":'<path d="M12 2v4M10 4h4"/><path d="M6 21V11l6-5 6 5v10z"/><path d="M10 21v-5h4v5"/>',
"cross":'<path d="M12 3v18M7 8h10"/>',
"link":'<path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1"/><path d="M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/>',
"heart":'<path d="M12 20s-8-5-8-11a4 4 0 0 1 8-2 4 4 0 0 1 8 2c0 6-8 11-8 11z"/>',
"quill":'<path d="M20 4c-8 0-13 6-14 14l-2 2"/><path d="M8 14h6"/>',
"tri":'<path d="M12 3l9 16H3z"/><circle cx="12" cy="13" r="2"/>',
}
def ic(n, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{P[n]}</svg>'
def l2icon(title):
    for k,v in [("时间线","clock"),("故事","scroll"),("地理","map"),("异端","alert"),("为什么","key"),("解读","book"),("信条","scale"),("应用","leaf"),("人物","users"),("误解","alert"),("牧养","heart"),("词义","quill"),("三一","tri"),("改革者","church"),("对照","scale"),("圣约","link"),("三约","link"),("礼仪","church"),("诵读","scroll"),("信经","scroll"),("口诀","brain"),("导图","brain"),("翻卡","brain"),("自测","key"),("总结","book"),("原文","scroll"),("全文","scroll"),("比较","scale"),("三圈","tri"),("分层","book"),("交叉","link"),("陈述","church"),("转述","book"),("译本","quill"),("编号","quill"),("脚注","link"),("我属于","heart"),("使用","church"),("来源","library"),("参考网站","library"),("没有找到","alert"),("版本","clock"),("导言","book"),("分组","scroll")]:
        if k in title: return v
    return "cross"

def people(items):
    return '<div class="people">' + "".join(f'<div class="pp reveal" style="--c:{c}"><div class="pa">{n[0]}</div><div><b>{n}</b><small>{d}</small><p>{t}</p></div></div>' for n,d,t,c in items) + '</div>'
def myths(items):
    return '<div class="myths">' + "".join(f'<div class="my reveal"><p class="mx">✗ {m}</p><p class="mo">✓ {r}</p></div>' for m,r in items) + '</div>'

