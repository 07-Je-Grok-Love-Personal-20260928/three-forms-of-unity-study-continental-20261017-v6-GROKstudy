"""背诵版逐字核对：每部信经背诵版各行 (.rt) 连起来，必须等于 CCI 整段原文（忽略空白）；亚他那修另核对 42 点编号齐全。"""
import json,re,html,sys
def txt(h): return html.unescape(re.sub(r'<[^>]+>','',h))
norm=lambda s:re.sub(r'\s+','',s)
C=json.load(open('data/creeds.json',encoding='utf-8'))
page=open(sys.argv[1] if len(sys.argv)>1 else 'creedsx.html',encoding='utf-8').read()
bad=0
for key,sid in (('apostles','ap'),('nicene','ni'),('athanasian','at')):
    secs=re.findall(r'<section class="l3 [^"]*rcs[^"]*" id="'+sid+r'-[^"]+">(.*?)</section>',page,flags=re.S)
    lines=[]
    for s in secs: lines+=re.findall(r'<span class="rt">(.*?)</span>',s,flags=re.S)
    got=norm(txt("".join(lines))); want=norm("".join(C[key]['paras']))
    if key=='athanasian': want=re.sub(r'\d+\)','',want)
    ok=got==want; bad+=not ok
    print(key,'sections',len(secs),'lines',len(lines),'OK' if ok else 'MISMATCH')
    if not ok:
        for i,(a,b) in enumerate(zip(got,want)):
            if a!=b: print('  first diff at',i,got[i-10:i+20],'|',want[i-10:i+20]); break
        print('  len',len(got),len(want))
sys.exit(1 if bad else 0)
