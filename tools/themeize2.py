"""t88：SVG 的 fill/stroke 也接入主题（浅色主题下文字压暗、描边光晕变浅），去掉浅色主题的“夜色底”图示。幂等。"""
import re,sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
if '/*themeized2*/' in s: print('already'); sys.exit()
def lum(h):
    h=h.lstrip('#'); h=''.join(c*2 for c in h) if len(h)==3 else h[:6]
    r,g,b=(int(h[i:i+2],16)/255 for i in (0,2,4)); return .2126*r+.7152*g+.0722*b
n=[0]
def fx(m):
    p,v=m.group(1),m.group(2)
    if lum(v)<.25:
        if p=='stroke': n[0]+=1; return f'stroke:var(--halo,{v})'
        return m.group(0)
    if lum(v)<.45: return m.group(0)   # 中等饱和色（强调色）保持
    n[0]+=1
    if v.lower() in('#fff','#ffffff'): return f'{p}:var(--hi)'
    return f'{p}:color-mix(in srgb,{v},var(--dkc) var(--dk))'
s=re.sub(r'(?<![\w-])(fill|stroke):(#[0-9a-fA-F]{3,6})\b',fx,s)
s='/*themeized2*/'+s; open(f,'w',encoding='utf-8').write(s); print('svg colours themeized',n[0])
