# -*- coding: utf-8 -*-
"""《中国改革宗教会敬拜手册》2015 版（PDF） vs CCI 数据：逐字差异。
页码一律用 PDF 印刷页码（= PDF 物理页 + 1）。输出 pdf_diff.json。"""
import json,re,sys,difflib,time
SITE=sys.argv[1] if len(sys.argv)>1 else '/workspace/three-forms-of-unity-study-continental-20261017'
def J(n): return json.load(open(f'{SITE}/data/{n}.json',encoding='utf-8'))
P='/workspace/pdf2015/p%d.txt'
FN=re.compile(r'^[（(]\d+[）)]\s*[\u4e00-\u9fff]{1,3}\s*\d+\s*[:：]\s*\d+')
REFONLY=re.compile(r'^[\u4e00-\u9fff]{1,3}\s*\d+[:：][\d\-,;；，\s:\u4e00-\u9fff]*$')
def lines(a,b):
    out=[]
    for pg in range(a,b+1):
        L=open(P%pg,encoding='utf-8').read().replace('\f','').split('\n')
        prev_fn=False
        for l in L:
            s=l.strip()
            if not s or re.fullmatch(r'\d{1,3}',s): continue
            if FN.match(s): prev_fn=True; continue
            if prev_fn and REFONLY.match(s) and len(re.findall(r'[\u4e00-\u9fff]',s))<=8: continue
            prev_fn=False
            out.append((pg+1,s))   # 印刷页码
    return out
PUN=str.maketrans({',':'，',';':'；',':':'：','(':'（',')':'）','!':'！','?':'？','•':'·','﹑':'、','．':'.'})
def norm_keep(s):
    s=re.sub(r'⟦\d+⟧','',s); s=re.sub(r'[（(]\d+[）)]','',s); s=s.translate(PUN)
    return re.sub(r'\s+','',s)
def pdf_stream(a,b):
    txt='';pages=[]
    for pg,s in lines(a,b):
        n=norm_keep(s); txt+=n; pages+= [pg]*len(n)
    return txt,pages
def cci_units(doc):
    U=[]
    if doc=='creeds':
        c=J('creeds')
        for k,t in [('apostles','使徒信经'),('nicene','尼西亚信经'),('athanasian','亚他那修信经')]:
            U.append((k,t,c[k]['intro'])); U.append((k,t,''.join(c[k]['paras'])))
    if doc=='bc':
        b=J('bc'); U.append(('intro','导言',''.join(b['intro'])))
        for a in b['articles']: U.append((f"bc-{a['n']}",a['title'],a['title']+''.join(x['x'] for x in a['blocks'] if x['t']=='p')))
    if doc=='hc':
        h=J('hc'); U.append(('intro','导言',''.join(h['intro'])))
        for l in h['lds']: U.append((f"ld{l['n']}",f"主日{l['n']}",f"主日{l['n']}"+''.join(x['x'] for x in l['blocks'] if x['t']!='ref')))
    if doc=='dort':
        d=J('dort'); U.append(('intro','导言',''.join(d['intro'])))
        for h in d['heads']:
            U.append((h['id'],h['title'],h['title']))
            for it in h['items']:
                tt='' if it['title']=='错谬反驳' else it['title']
                U.append((f"dort-{h['id']}-{it['n']}",h['num']+' '+it['title'],tt+''.join(x['x'] for x in it['blocks'] if x['t']=='p')))
    return U
RANGE={'creeds':(4,9),'bc':(10,46),'hc':(47,93),'dort':(94,137)}
def run(doc):
    U=cci_units(doc); ctext='';cmap=[]
    for i,(uid,lab,t) in enumerate(U):
        n=norm_keep(t); ctext+=n; cmap+=[i]*len(n)
    ptext,pmap=pdf_stream(*RANGE[doc])
    t0=time.time()
    sm=difflib.SequenceMatcher(None,ctext,ptext,autojunk=False)
    # 分块加速：按单元首 10 字锚点
    ops=sm.get_opcodes()
    res=[]
    for tag,i1,i2,j1,j2 in ops:
        if tag=='equal': continue
        a=ctext[i1:i2]; b=ptext[j1:j2]
        u=U[cmap[min(i1,len(cmap)-1)]]
        pg=pmap[min(j1,len(pmap)-1)]
        core=lambda s: re.sub(r'[\d\W_a-zA-Z]','',s)
        kind='标点/数字' if core(a)==core(b) else '用词'
        res.append({'doc':doc,'unit':u[0],'label':u[1],'cci':a,'pdf':b,'page':pg,'kind':kind,
                    'i1':i1,'i2':i2,'j1':j1,'j2':j2,'cctx':ctext[max(0,i1-10):i2+10],'pctx':ptext[max(0,j1-10):j2+10]})
    sim=sm.ratio()
    print(doc,'len',len(ctext),len(ptext),'ratio',round(sim,4),'ops',len(res),'words',sum(r['kind']=='用词' for r in res),round(time.time()-t0,1),'s',file=sys.stderr)
    return res,sim,ctext,ptext
if __name__=='__main__':
    out={'source':'《中国改革宗教会 敬拜手册》2015 版（用户提供 PDF，245 页）','pages_note':'页码为印刷页码','docs':{}}
    for d in ['creeds','bc','hc','dort']:
        r,s,a,b=run(d); out['docs'][d]={'ratio':s,'cci_chars':len(a),'pdf_chars':len(b),'diffs':r,'ctext':a,'ptext':b}
    json.dump(out,open('/workspace/pdf2015/pdf_diff.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
