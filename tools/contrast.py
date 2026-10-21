"""主题对比度检查（WCAG AA）：python3 tools/contrast.py [pages...]  逐主题统计正文文字元素的对比度。
背景按祖先 background-color 叠加估算（渐变/图片忽略，以主题底色为底）。"""
import sys,os,json
from playwright.sync_api import sync_playwright
pages=[a for a in sys.argv[1:] if a.endswith('.html')]
JS=r'''(base)=>{
function P(s){if(!s)return null;let m=s.match(/rgba?\(([^)]+)\)/);if(m){let a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return [a[0],a[1],a[2],a.length>3?a[3]:1]}
 m=s.match(/color\(srgb ([^)]+)\)/);if(m){let a=m[1].split(/[ \/]+/).filter(Boolean).map(Number);return [a[0]*255,a[1]*255,a[2]*255,a.length>3?a[3]:1]}return null}
function L(c){const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])}
function over(t,b){const a=t[3];return [t[0]*a+b[0]*(1-a),t[1]*a+b[1]*(1-a),t[2]*a+b[2]*(1-a),1]}
const B=P(base);const res={n:0,bad:0,ex:{}};
document.querySelectorAll('main p,main li,main td,main th,main span,main b,main a,main small,main h2,main h3,main h4,main summary,main dt,main dd,main i,#toc a').forEach(el=>{
 if(el.closest('svg'))return; let txt='';el.childNodes.forEach(n=>{if(n.nodeType===3)txt+=n.textContent});txt=txt.trim();if(txt.length<2)return;
 const r=el.getBoundingClientRect();if(!r.width||!r.height)return;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity<.5)return;
 if(el.closest('details:not([open])')&&!el.closest('summary'))return;
 let layers=[],gi=false;for(let p=el;p&&p!==document.body;p=p.parentElement){const ps=getComputedStyle(p);if(ps.backgroundImage!=='none'&&/gradient|url/.test(ps.backgroundImage)&&(p===el||p.getBoundingClientRect().height<120)){gi=true;break}const c=P(ps.backgroundColor);if(c&&c[3]>0){layers.push(c);if(c[3]>=1)break}}if(gi){res.grad=(res.grad||0)+1;return}
 let bg=B.slice();for(let i=layers.length-1;i>=0;i--)bg=over(layers[i],bg);
 let fg=P(cs.color);if(!fg)return;fg=over(fg,bg);
 const l1=L(fg),l2=L(bg),cr=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
 const fs=parseFloat(cs.fontSize),bold=+cs.fontWeight>=700,big=fs>=24||(bold&&fs>=18.66);
 res.n++;if(cr<(big?3:4.5)){res.bad++;const k=el.tagName+'.'+(el.className||'').toString().split(' ')[0];res.ex[k]=res.ex[k]||[0,cr.toFixed(2),txt.slice(0,16)];res.ex[k][0]++}});
return res}'''
TH={'night':'rgb(7,13,34)','dawn':'rgb(247,241,230)','jade':'rgb(3,32,30)','grape':'rgb(20,10,38)'}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for th,base in TH.items():
        n=bad=g=0;ex={}
        for f in pages:
            ctx=b.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce')
            ctx.add_init_script(f"try{{localStorage.setItem('ui.theme','{th}')}}catch(e){{}}")
            pg=ctx.new_page(); pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(250)
            pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",'main section.l2,main section.l3,main figure,main .icm{content-visibility:visible!important}')
            r=pg.evaluate(JS,base); n+=r['n']; bad+=r['bad']; g+=r.get('grad',0)
            for k,v in r['ex'].items(): ex.setdefault(k,[0,v[1],v[2],f]); ex[k][0]+=v[0]
            ctx.close()
        top=sorted(ex.items(),key=lambda x:-x[1][0])[:8]
        print(f'{th}: text elements {n}, below AA {bad} ({bad/max(n,1)*100:.2f}%); on small gradient chips skipped {g}',flush=True)
        for k,v in top: print('   ',k,v,flush=True)
    b.close()
