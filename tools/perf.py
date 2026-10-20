"""Perf probe: python3 perf.py DIR page.html ... -> JSON per page (TBT-ish, long tasks, CLS, scroll FPS, layout/style counts)."""
import sys,os,json,statistics
from playwright.sync_api import sync_playwright
d=sys.argv[1]; pages=sys.argv[2:]
INIT='''window.__lt=[];window.__cls=0;
try{new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push([e.startTime,e.duration])}).observe({type:'longtask',buffered:true})}catch(e){}
try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})}catch(e){}'''
SCROLL='''async(SPD)=>{const H=document.documentElement.scrollHeight-innerHeight;const fr=[];let last=performance.now();const t0=last;
window.__lt=[];
await new Promise(res=>{function f(t){fr.push(t-last);last=t;const y=(t-t0)*SPD;window.scrollTo({top:y,behavior:'instant'});if(scrollY>y-60&&t-t0<8000)requestAnimationFrame(f);else res()}requestAnimationFrame(f)});
fr.shift();const s=fr.slice().sort((a,b)=>a-b);const tot=fr.reduce((a,b)=>a+b,0);
return {frames:fr.length,fps:+(fr.length/tot*1000).toFixed(1),p95:+s[Math.floor(s.length*.95)].toFixed(1),jank:fr.filter(x=>x>33).length,lt:window.__lt.length,ltms:Math.round(window.__lt.reduce((a,b)=>a+b[1],0))}}'''
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--enable-gpu-rasterization'])
    for f in pages:
        ctx=b.new_context(viewport={'width':1280,'height':900}); pg=ctx.new_page(); pg.add_init_script(INIT)
        cdp=ctx.new_cdp_session(pg); cdp.send('Performance.enable'); cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        pg.goto('file://'+os.path.abspath(os.path.join(d,f)),wait_until='load');
        if os.environ.get('EXTRA_CSS'): pg.add_style_tag(content=os.environ['EXTRA_CSS'])
        pg.wait_for_timeout(1500)
        ld=pg.evaluate('''()=>{const n=performance.getEntriesByType('navigation')[0];const lt=window.__lt;return {dcl:Math.round(n.domContentLoadedEventEnd),load:Math.round(n.loadEventEnd),tbt:Math.round(lt.reduce((a,b)=>a+Math.max(0,b[1]-50),0)),longtasks:lt.length,dom:document.getElementsByTagName('*').length}}''')
        m0={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
        TR=os.environ.get('TRACE')=='1'
        if TR: b.start_tracing(page=pg,path='/tmp/tr.json',categories=['devtools.timeline','disabled-by-default-devtools.timeline'])
        sc=pg.evaluate(SCROLL,float(os.environ.get('SPEED','1.2')))
        if TR: b.stop_tracing()
        ev=json.load(open('/tmp/tr.json')) if TR else []
        ev=ev['traceEvents'] if isinstance(ev,dict) else ev
        agg={}
        for e in ev:
            n=e.get('name')
            if n in ('Paint','RasterTask','Layout','UpdateLayoutTree','PrePaint','Layerize','CompositeLayers','UpdateLayer') and e.get('ph')=='X': agg[n]=agg.get(n,0)+e.get('dur',0)/1000
        sc['trace_ms']={k:round(v) for k,v in sorted(agg.items())}
        m1={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
        sc['layouts']=int(m1['LayoutCount']-m0['LayoutCount']); sc['styles']=int(m1['RecalcStyleCount']-m0['RecalcStyleCount'])
        sc['layout_ms']=round((m1['LayoutDuration']-m0['LayoutDuration'])*1000); sc['style_ms']=round((m1['RecalcStyleDuration']-m0['RecalcStyleDuration'])*1000); sc['script_ms']=round((m1['ScriptDuration']-m0['ScriptDuration'])*1000)
        ld['cls']=round(pg.evaluate('window.__cls'),3)
        out[f]={'load':ld,'scroll':sc}; print(f,json.dumps(out[f]),flush=True); ctx.close()
    b.close()
json.dump(out,open(os.environ.get('OUT','/workspace/perf/out.json'),'w'),indent=1)
