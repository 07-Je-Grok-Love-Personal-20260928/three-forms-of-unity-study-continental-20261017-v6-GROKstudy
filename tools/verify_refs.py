"""经文参考逐条核对：页面中每个 .refs2 行内的 .rf1 文本序列 == data/*.json 中 ref 块的列表（顺序与文字完全一致）。"""
import json,re,html,sys
def blocks(f,key):
    d=json.load(open(f'data/{f}.json',encoding='utf-8'))
    if f=='bc': it=[b for a in d['articles'] for b in a['blocks']]
    elif f=='hc': it=[b for l in d['lds'] for b in l['blocks']]
    else: it=[b for h in d['heads'] for i in h['items'] for b in i['blocks']]
    return [b['x'] for b in it if b['t']=='ref']
bad=0
for f,page in (('bc','bct.html'),('hc','hct.html'),('dort','dtt.html')):
    h=open(page,encoding='utf-8').read()
    got=[[html.unescape(x) for x in re.findall(r'<span class="rf1" role="listitem"><b class="nb">\d+</b>(.*?)</span>',m)] for m in re.findall(r'<div class="refs2"[^>]*>(.*?)</div>',h,flags=re.S)]
    want=blocks(f,None); ok=got==want; bad+=not ok
    print(page,'ref blocks',len(got),'items',sum(map(len,got)),'OK' if ok else f'MISMATCH want {len(want)}')
# --- 深读页/记忆页的紧凑经文行（.refs2.rq）：按页面顺序逐条比对 data ---
def flat(lsts): return [x for l in lsts for x in l]
def rows(page):
    h=open(page,encoding='utf-8').read()
    return [[html.unescape(x) for x in re.findall(r'<span class="rf1" role="listitem"><b class="nb">\d+</b>(.*?)</span>',m)] for m in re.findall(r'<div class="refs2 rq"[^>]*>(.*?)</div>',h,flags=re.S)]
def want_blocks(f): return blocks(f,None)
hcb=want_blocks('hc'); bcb=want_blocks('bc'); dtb=want_blocks('dort')
for page,want in (('hc.html',hcb),('bc.html',bcb),('dort.html',dtb)):
    got=rows(page); ok=got==want; bad+=not ok
    print(page,'deep-dive rows',len(got),'items',sum(map(len,got)),'OK' if ok else f'MISMATCH got {len(got)} want {len(want)}')
# 记忆页：HC 按主日合并（顺序同），BC 逐条，Dort 逐条
d=json.load(open('data/hc.json',encoding='utf-8'))
hcm=[flat(b['x'] for b in l['blocks'] if b['t']=='ref') for l in d['lds']]; hcm=[x for x in hcm if x]
got=rows('memory.html'); want=hcm+bcb+dtb; ok=got==want; bad+=not ok
print('memory.html rows',len(got),'items',sum(map(len,got)),'OK' if ok else f'MISMATCH got {len(got)} want {len(want)}')
sys.exit(1 if bad else 0)
