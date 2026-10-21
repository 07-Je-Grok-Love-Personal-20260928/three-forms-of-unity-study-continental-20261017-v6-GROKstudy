"""一次性把 styles.css 的硬编码颜色改成主题变量（t87）。幂等：已处理则跳过。用法：python3 tools/themeize.py assets/styles.css"""
import re,sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
if '/*themeized*/' in s: print('already'); sys.exit()
s=s.replace('rgba(255,255,255,','rgba(var(--W),')
s=re.sub(r'rgba\((?:9,16,40|10,18,44|13,24,56|20,32,70|7,13,34|10,22,52),','rgba(var(--D),',s)
s=s.replace('rgba(212,175,55,','rgba(var(--A),').replace('rgba(243,217,139,','rgba(var(--A2),')
s=re.sub(r'(background(?:-color)?:[^;}]*?)#(?:0b1636|0d1838)\b',r'\1var(--pnl)',s)
s=re.sub(r'(background(?:-color)?:[^;}]*?)#14224b\b',r'\1var(--pnl2)',s)
n=0
def col(m):
    global n
    v=m.group(2).strip(); imp=''
    if v.endswith('!important'): v=v[:-10].strip(); imp='!important'
    if v in('inherit','currentColor','currentcolor','transparent','unset','initial') or 'color-mix' in v: return m.group(0)
    n+=1
    if v.lower() in('#fff','#ffffff'): return m.group(1)+'var(--hi)'+imp
    return m.group(1)+f'color-mix(in srgb,{v},var(--dkc) var(--dk))'+imp
s=re.sub(r'((?<![\w-])color:)([^;}]+)',col,s)
s='/*themeized*/'+s
open(f,'w',encoding='utf-8').write(s); print('themeized colors',n)
