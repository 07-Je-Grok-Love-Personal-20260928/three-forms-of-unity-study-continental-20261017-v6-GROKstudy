"""真实滚动性能：CDP Input.synthesizeScrollGesture（原生平滑滚动手势，手机用 touch）。
用法：python3 perf2.py DIR page.html ...   环境变量 W=390|1280  CPU=1|4  DIST=像素
输出：dcl(ms) · CLS(全程，含滚动) · fps · 掉帧(>33ms) · p95 帧时 · 长任务 · 主要位移来源"""
import sys,os,json
from playwright.sync_api import sync_playwright
d=sys.argv[1]; pages=sys.argv[2:]; W=int(os.environ.get('W','1280')); CPU=float(os.environ.get('CPU','1')); DIST=int(os.environ.get('DIST','14000'))
INIT='''window.__lt=[];window.__cls=0;window.__src={};window.__fr=[];
new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push(e.duration)}).observe({type:'longtask',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.hadRecentInput)continue;window.__cls+=e.value;for(const s of (e.sources||[]).slice(0,1)){const n=s.node;const k=n&&n.nodeType===1?(n.tagName+'.'+String(n.className).split(' ')[0]+(n.closest&&n.closest('#toc')?'@toc':'')):'?';window.__src[k]=(window.__src[k]||0)+e.value}}}).observe({type:'layout-shift',buffered:true});'''
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--enable-gpu-rasterization'])
    for f in pages:
        mob=W<600
        ctx=b.new_context(viewport={'width':W,'height':844 if mob else 900},device_scale_factor=3 if mob else 1,is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); pg.add_init_script(INIT); cdp=ctx.new_cdp_session(pg)
        if CPU>1: cdp.send('Emulation.setCPUThrottlingRate',{'rate':CPU})
        pg.goto('file://'+os.path.abspath(os.path.join(d,f)),wait_until='load')
        if os.environ.get('EXTRA_CSS'): pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",os.environ['EXTRA_CSS'])
        pg.wait_for_timeout(1200)
        ld=pg.evaluate("()=>{const n=performance.getEntriesByType('navigation')[0];return {dcl:Math.round(n.domContentLoadedEventEnd),dom:document.getElementsByTagName('*').length}}")
        pg.evaluate("()=>{window.__lt=[];window.__run=1;let last=performance.now();function f(t){window.__fr.push(t-last);last=t;if(window.__run)requestAnimationFrame(f)}requestAnimationFrame(f)}")
        h=pg.evaluate('document.documentElement.scrollHeight')
        dist=min(DIST,h-900)
        cdp.send('Input.synthesizeScrollGesture',{'x':W//2 if not mob else W//2,'y':400,'yDistance':-dist,'speed':2400,'gestureSourceType':'mouse','repeatCount':1})
        r=pg.evaluate("()=>{window.__run=0;const fr=window.__fr.slice(2);const s=fr.slice().sort((a,b)=>a-b);const tot=fr.reduce((a,b)=>a+b,0);return {fps:+(fr.length/tot*1000).toFixed(1),jank:fr.filter(x=>x>33).length,p95:+(s[Math.floor(s.length*.95)]||0).toFixed(1),frames:fr.length,lt:window.__lt.length,ltms:Math.round(window.__lt.reduce((a,b)=>a+b,0)),cls:+window.__cls.toFixed(3),src:Object.entries(window.__src).sort((a,b)=>b[1]-a[1]).slice(0,3).map(x=>x[0]+':'+x[1].toFixed(3)),y:Math.round(scrollY)}}")
        r.update(ld); out[f]=r; print(f,json.dumps(r,ensure_ascii=False),flush=True); ctx.close()
    b.close()
if os.environ.get('OUT'): json.dump(out,open(os.environ['OUT'],'w'),indent=1,ensure_ascii=False)
