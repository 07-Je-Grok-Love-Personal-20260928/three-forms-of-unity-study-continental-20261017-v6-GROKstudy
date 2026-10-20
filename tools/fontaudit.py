"""字号审计：列出渲染后 <14px 的文字（HTML 取 computed；SVG 文字乘以缩放）。用法：python3 tools/fontaudit.py [--min 14] [页面...]"""
import sys,os,glob,collections
from playwright.sync_api import sync_playwright
a=sys.argv[1:]; mn=14
if '--min' in a: i=a.index('--min'); mn=float(a[i+1]); del a[i:i+2]
pages=[x for x in a if x.endswith('.html')] or sorted(glob.glob('*.html'))
JS='''(mn)=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.textContent.trim(); if(!t) continue; const el=n.parentElement; if(!el||['SCRIPT','STYLE'].includes(el.tagName)) continue;
 const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) continue;
 let fs=parseFloat(getComputedStyle(el).fontSize);
 const svg=el.closest('svg'); if(svg&&el.getScreenCTM){const m=el.getScreenCTM(); if(m) fs=fs*Math.sqrt(m.a*m.a+m.b*m.b)}
 if(fs<mn){ let c=el; let k=el.tagName+'.'+(el.getAttribute('class')||'').split(' ')[0]; let q=el.parentElement; while(q&&!q.getAttribute('class')) q=q.parentElement; if(q&&!el.getAttribute('class')) k+='<'+q.tagName+'.'+q.getAttribute('class').split(' ')[0]; if(svg) k='svg:'+k; out.push([k,Math.round(fs*10)/10,t.slice(0,16)]);}}
return out}'''
agg=collections.defaultdict(lambda:[99,0,''])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        for w in (390,1280):
            pg=b.new_context(viewport={'width':w,'height':900}).new_page(); pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(250); pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",'main section.l2,main section.l3{content-visibility:visible!important}')  # v8：测量时强制渲染 content-visibility:auto 的区块
            for k,fs,t in pg.evaluate(JS,mn):
                e=agg[(k,w)]; e[0]=min(e[0],fs); e[1]+=1; e[2]=e[2] or f+':'+t
for (k,w),(fs,n,s) in sorted(agg.items(),key=lambda x:x[1][0]): print(f'{w:5} {fs:5} x{n:<4} {k:34} {s}')
print('distinct',len(agg))
