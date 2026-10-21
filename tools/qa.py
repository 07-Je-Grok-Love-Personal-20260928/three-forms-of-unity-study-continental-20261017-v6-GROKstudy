"""Playwright QA：每页 × 5 个宽度。检查水平溢出、被裁切的文字、JS 错误、no-JS 与 reduced-motion 下内容可见。
用法：python3 tools/qa.py [--shots] [--nojs] [--rm] [页面...]  （file:// 打开）"""
import sys,os,glob,json
from playwright.sync_api import sync_playwright
args=sys.argv[1:]; shots='--shots' in args; nojs='--nojs' in args; rm='--rm' in args; opn='--open' in args
pages=[a for a in args if a.endswith('.html')] or sorted(glob.glob('*.html'))
W=[360,390,768,1280,1440]
JS_OVER='''()=>{
 const vw=document.documentElement.clientWidth, out=[];
 const sc=(el)=>{for(let p=el;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p).overflowX; if((o==='auto'||o==='scroll')&&p.scrollWidth>p.clientWidth) return true;} return false};
 document.querySelectorAll('main *, #toc *').forEach(el=>{
   if(el.closest('svg')&&el.tagName!=='svg') return;
   const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) return;
   if(getComputedStyle(el).position==='fixed') return;
   if(r.right>vw+1||r.left<-1){ if(!sc(el)&&!el.closest('#toc')) out.push([el.tagName+'.'+(el.className&&el.className.baseVal===undefined?el.className:''),Math.round(r.left),Math.round(r.right)]); }
 });
 return {sw:document.documentElement.scrollWidth,vw:vw,over:out.slice(0,6),n:out.length};
}'''
JS_CLIP='''()=>{const out=[];document.querySelectorAll('main p,main li,main td,main th,main b,main a,main span,main h3,main h4,main small,main summary,main button').forEach(el=>{
 const cs=getComputedStyle(el); if(el.closest('svg')||el.closest('#toc')) return;
 if(el.scrollWidth>el.clientWidth+2&&(cs.overflowX==='hidden'||cs.overflowX==='clip')&&el.clientWidth>0&&getComputedStyle(el).display!=='inline') out.push(el.tagName+'.'+el.className+':'+(el.textContent||'').slice(0,20));
 });return out.slice(0,5)}'''
JS_VIS='''()=>{let n=0,bad=[];document.querySelectorAll('.reveal').forEach(e=>{const o=parseFloat(getComputedStyle(e).opacity);if(o<0.99){n++;if(bad.length<3)bad.push(e.className.slice(0,30))}});return {hidden:n,bad:bad,js:document.documentElement.classList.contains('js')}}'''
res=[];fail=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        for w in W:
            ctx=b.new_context(viewport={'width':w,'height':900},java_script_enabled=not nojs,reduced_motion='reduce' if rm else 'no-preference')
            if os.environ.get('THEME'): ctx.add_init_script("try{localStorage.setItem('ui.theme','%s')}catch(e){}"%os.environ['THEME'])
            pg=ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(300); pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",'main section.l2,main section.l3,main figure,main .icm{content-visibility:visible!important}')  # v8：测量时强制渲染 content-visibility:auto 的区块
            if opn: pg.evaluate("document.querySelectorAll('details').forEach(e=>e.open=true)")
            if not nojs:
                # 滚动一遍以触发 reveal / 进度
                h=pg.evaluate('document.documentElement.scrollHeight')
                pg.evaluate('''async(h)=>{const f=()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));for(let y=0;y<h;y+=700){window.scrollTo(0,y);await f();}}''',h)  # 单次 evaluate 内滚动，免去每步往返
                pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(200)
            ov=pg.evaluate(JS_OVER); cl=pg.evaluate(JS_CLIP); vis=pg.evaluate(JS_VIS)
            bad=[]
            if ov['sw']>ov['vw']+1: bad.append(f"页面横向溢出 sw={ov['sw']} vw={ov['vw']}")
            if ov['n']: bad.append(f"元素越界 {ov['n']}: {ov['over']}")
            if cl: bad.append(f"文字被裁切: {cl}")
            if errs: bad.append(f"JS错误: {errs[:2]}")
            if (nojs or rm) and vis['hidden']: bad.append(f"不可见元素 {vis}")
            if (nojs and vis['js']) : bad.append("no-JS 却带 js 类")
            if rm and vis['js']: bad.append("reduced-motion 却启用 reveal")
            if shots and w in (360,1280) and not nojs and not rm:
                os.makedirs('_shots',exist_ok=True); pg.screenshot(path=f'_shots/{f[:-5]}_{w}.png',full_page=True)
            tag='FAIL' if bad else 'ok'
            if bad: fail+=1; print(tag,f,w,bad)
            ctx.close()
    b.close()
print('QA',('nojs' if nojs else 'rm' if rm else 'normal'),'theme='+os.environ.get('THEME','night'),'open' if opn else 'collapsed','pages',len(pages),'widths',W,'fails',fail)
