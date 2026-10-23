# -*- coding: utf-8 -*-
"""生成 assets/t90.css：新增 5 个主题（浅色族复用晨光暖白的全部覆盖规则；深色族沿用青绿/葡萄的模式）
+ t90static.css（性能、视觉、标记、排版）。用法：python3 gen90.py → shared89/t90.css"""
import re, os
H = os.path.dirname(os.path.abspath(__file__))
SRC = [open('/workspace/shared87/t87.css').read(), open(os.path.join(H, 't89.css')).read()]
def rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S); out = []
    def block(s, media):
        j = 0
        while j < len(s):
            k = s.find('{', j)
            if k < 0: break
            sel = s[j:k].strip(); depth = 1; m = k + 1
            while depth and m < len(s):
                if s[m] == '{': depth += 1
                elif s[m] == '}': depth -= 1
                m += 1
            body = s[k + 1:m - 1]
            if sel.startswith('@media') or sel.startswith('@supports'): block(body, sel)
            elif not sel.startswith('@'): out.append((media, sel, body))
            j = m
    block(css, None); return out
ALL = [r for c in SRC for r in rules(c)]
LIGHT = ['sakura', 'paper', 'eye']; DARK = ['ocean', 'amber']
LSEL = 'html:is(' + ','.join(f'[data-theme={t}]' for t in LIGHT) + ')'
T = {
 'sakura': dict(bg='#fbf1f4', bg2='#f5e2ea', W='90,28,52', D='255,250,252', A='194,64,122', A2='164,40,98', gold='#c0457c', gold2='#b23a72', tx='#2e2a33', mut='#5f5462', hi='#1a0f15', dk='64%', gtx='#8a1f52', dkc='#1a0610', pnl='#fff8fb', pnl2='#f8e7ef', gb='rgba(194,64,122,.28)', f='#2a64b0', g='#2f7d5b', s='#c0457c', qc='#8a1f52', ac='#2a2630', qbg='rgba(194,64,122,.1)', abg='rgba(255,255,255,.7)', abd='#2f7d5b', mkhl='rgba(255,160,196,.5)', halo='#fdf5f8'),
 'paper':  dict(bg='#f4f5f7', bg2='#e8ebef', W='28,38,58', D='255,255,255', A='52,86,140', A2='38,68,120', gold='#3a5a8e', gold2='#33517f', tx='#262b36', mut='#545c6b', hi='#0e121a', dk='64%', gtx='#1d3a68', dkc='#05080f', pnl='#ffffff', pnl2='#eef1f5', gb='rgba(52,86,140,.26)', f='#2a64b0', g='#2f7d5b', s='#3a5a8e', qc='#1d3a68', ac='#232833', qbg='rgba(52,86,140,.09)', abg='rgba(255,255,255,.8)', abd='#2f7d5b', mkhl='rgba(255,214,60,.5)', halo='#f7f8fa'),
 'eye':    dict(bg='#e6f0df', bg2='#d9e8d0', W='26,56,28', D='246,251,242', A='52,116,58', A2='38,96,44', gold='#3b7a3e', gold2='#336b35', tx='#23302a', mut='#4a5c4f', hi='#0c160e', dk='64%', gtx='#1e4d21', dkc='#061006', pnl='#f3f9ef', pnl2='#e2eedb', gb='rgba(52,116,58,.28)', f='#25609f', g='#2f6f4f', s='#3b7a3e', qc='#1e4d21', ac='#212c25', qbg='rgba(52,116,58,.1)', abg='rgba(255,255,255,.55)', abd='#8a5a00', mkhl='rgba(255,214,60,.5)', halo='#eef5e9'),
 'ocean':  dict(bg='#031a2e', bg2='#062a48', D='4,30,54', A='90,186,250', A2='180,224,255', gold='#5ab8f5', gold2='#b4e1ff', pnl='#062a48', pnl2='#0a3658', gb='rgba(90,186,250,.26)', qc='#a6e3ff', abd='#e0b86a', mut='#a8c2d8', f='#7cc8ff', g='#7fd6b0', qbg='rgba(90,186,250,.13)', mkhl='rgba(255,214,90,.28)'),
 'amber':  dict(bg='#1c1108', bg2='#2b1a0c', D='40,24,11', A='240,160,70', A2='255,214,160', gold='#f0a448', gold2='#ffd6a0', pnl='#2b1a0c', pnl2='#3a2412', gb='rgba(240,160,70,.28)', qc='#ffcf94', abd='#7fd6c2', mut='#cfb89c', f='#86c8ff', g='#9fd6a6', qbg='rgba(240,160,70,.14)', mkhl='rgba(255,200,80,.3)'),
}
IMG = {
 'sakura': 'radial-gradient(1100px 700px at 85% -10%,#ffd3e2 0,transparent 60%),radial-gradient(900px 600px at -10% 45%,#f3e6f7 0,transparent 55%)',
 'paper': 'radial-gradient(1100px 700px at 85% -10%,#ffffff 0,transparent 60%),radial-gradient(900px 600px at -10% 45%,#e1e7f0 0,transparent 55%)',
 'eye': 'radial-gradient(1100px 700px at 85% -10%,#f1f7d6 0,transparent 60%),radial-gradient(900px 600px at -10% 45%,#cfe5d2 0,transparent 55%)',
 'ocean': 'radial-gradient(1100px 700px at 85% -10%,#0b4a7a 0,transparent 60%),radial-gradient(900px 600px at -10% 45%,#0a3a4a 0,transparent 55%)',
 'amber': 'radial-gradient(1100px 700px at 85% -10%,#5a3210 0,transparent 60%),radial-gradient(900px 600px at -10% 45%,#4a2414 0,transparent 55%)'}
MK = {'sakura': ('rgba(255,150,190,.5)', '#b8233f', '#8a3a00', '#b23a72'), 'paper': ('rgba(255,210,40,.5)', '#b8233f', '#7a4300', '#33517f'),
      'eye': ('rgba(255,206,40,.55)', '#b0233a', '#7a4300', '#336b35'), 'ocean': ('rgba(255,214,90,.4)', '#ff95a6', '#ffc685', '#ffd166'),
      'amber': ('rgba(255,200,80,.38)', '#ff9d9d', '#ffc98a', '#ffd166')}
TOC = {'sakura': ('#f6b9d0', '#fbdde9'), 'paper': ('#c9d6ea', '#e3eaf5'), 'eye': ('#b9dbb4', '#d9ecd4')}
META = {'night': '#070d22', 'dawn': '#f7f1e6', 'jade': '#031c1b', 'grape': '#150b26', 'sakura': '#fbf1f4', 'paper': '#f4f5f7', 'eye': '#e6f0df', 'ocean': '#031a2e', 'amber': '#1c1108'}
def build():
    o = ['/* t90：由 gen90.py 生成——请改 gen90.py / t90static.css */']
    for media, sel, body in ALL:
        if 'data-theme=dawn' not in sel: continue
        if re.fullmatch(r'html\[data-theme=dawn\](\s+body)?', sel) and body.strip().startswith('--'): continue
        r = sel.replace('html[data-theme=dawn]', LSEL) + '{' + body + '}'
        o.append(f'{media}{{{r}}}' if media else r)
    o.append('html[data-theme=ocean] .map stop:nth-child(-n+2){stop-color:#145a8c}')
    o.append('html[data-theme=amber] .map stop:nth-child(-n+2){stop-color:#7a4a1a}')
    for t, v in T.items():
        o.append(f'html[data-theme={t}]{{' + ';'.join(f'--{k}:{x}' for k, x in v.items()) + '}')
        o.append(f'html[data-theme={t}] body{{--bgimg:{IMG[t]},linear-gradient(180deg,var(--bg),var(--bg2) 50%,var(--bg))}}')
        hl, x, ref, u = MK[t]
        o.append(f'html[data-theme={t}]{{--c-hl:{hl};--c-x:{x};--c-ref:{ref};--mk-u:{u}}}')
        if t in TOC:
            a, b = TOC[t]
            o.append(f'html[data-theme={t}] #toc a.on{{background:linear-gradient(90deg,{a},{b})!important}}')
    o.append(open(os.path.join(H, 't90static.css')).read())
    return '\n'.join(o) + '\n'
if __name__ == '__main__':
    open(os.path.join(H, 't90.css'), 'w').write(build()); print('t90.css', len(build()))
