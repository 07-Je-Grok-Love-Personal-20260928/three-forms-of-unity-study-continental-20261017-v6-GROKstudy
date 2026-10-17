import json,re,html
def page(f):
    h=open(f,encoding='utf-8').read(); h=re.sub(r'<sup class="fn">\d+</sup>','',h); h=re.sub(r'<[^>]+>','',h); return html.unescape(h)
def clean(s): return re.sub(r'⟦\d+⟧','',s)
tot=0;bad=0
def chk(f,texts):
    global tot,bad; p=page(f)
    for t in texts:
        tot+=1
        if clean(t) not in p: bad+=1; print('MISSING',f,clean(t)[:50])
c=json.load(open('data/creeds.json',encoding='utf-8'))
chk('creedsx.html',[x for k in('apostles','nicene','athanasian') for x in c[k]['paras']])
bc=json.load(open('data/bc.json',encoding='utf-8')); chk('bct.html',[b['x'] for a in bc['articles'] for b in a['blocks'] if b['t'] in('p','h4')]); print('bc articles',len(bc['articles']))
hc=json.load(open('data/hc.json',encoding='utf-8')); chk('hct.html',[b['x'] for l in hc['lds'] for b in l['blocks'] if b['t'] in('p','h4')]); print('hc LDs',len(hc['lds']),'Qs',sum(1 for l in hc['lds'] for b in l['blocks'] if b['t']=='h4'))
dt=json.load(open('data/dort.json',encoding='utf-8')); chk('dtt.html',[b['x'] for h in dt['heads'] for i in h['items'] for b in i['blocks'] if b['t'] in('p','h4')]); print('dort items',sum(len(h['items']) for h in dt['heads']))
print('texts checked',tot,'missing',bad)
