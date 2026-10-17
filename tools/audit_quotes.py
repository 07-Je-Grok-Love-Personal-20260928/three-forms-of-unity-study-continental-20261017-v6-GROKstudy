import re,json,sys
sys.path.insert(0,'.')
files=sys.argv[1:]
corp=''
for f in ['creeds','bc','hc','dort']:
    corp+=open(f'data/{f}.json',encoding='utf-8').read()
corp=re.sub(r'⟦\d+⟧|\\n|\s','',corp)
corp=re.sub(r'[，。；：、！？“”‘’（）()\\"\'…—·]','',corp)
def norm(s): return re.sub(r'[，。；：、！？“”‘’（）()\s…—·,.;:]|<[^>]+>','',s)
bad=[]
for f in files:
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'“([^”]{5,80})”',t):
        q=m.group(1); parts=[p for p in re.split(r'……|…|\.\.\.',q) if len(norm(p))>=4]
        ok=parts and all(norm(p) in corp for p in parts)
        ctx=t[max(0,m.start()-70):m.end()+40].replace('\n',' ')
        if not ok and re.search(r'信条|信经|问\d|海德堡|多特|第\d+条|《赞美|赞美手册',ctx): bad.append((f,q,ctx))
for b in bad: print(b[0],'|',b[1],'||',b[2][:170]); 
print(len(bad))
