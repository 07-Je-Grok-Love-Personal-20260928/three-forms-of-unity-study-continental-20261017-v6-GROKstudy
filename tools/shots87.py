import sys,os
from playwright.sync_api import sync_playwright
d=sys.argv[1]; out=sys.argv[2]; jobs=sys.argv[3:]  # page:theme:width[:mode]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for j in jobs:
        parts=j.split(':'); f,th,w=parts[0],parts[1],int(parts[2]); mode=parts[3] if len(parts)>3 else ''
        ctx=b.new_context(viewport={'width':w,'height':860 if w>500 else 800},device_scale_factor=1)
        ctx.add_init_script(f"try{{localStorage.setItem('ui.theme','{th}')}}catch(e){{}}")
        pg=ctx.new_page(); frag=''
        if '#' in f: f,frag=f.split('#')
        pg.goto('file://'+os.path.abspath(os.path.join(d,f))); pg.wait_for_timeout(500)
        if frag: pg.evaluate("i=>{const e=document.getElementById(i);if(e){e.scrollIntoView();setTimeout(()=>e.scrollIntoView(),200)}}",frag); pg.wait_for_timeout(600)
        if mode=='toc': pg.click('#tocbtn'); pg.wait_for_timeout(600)
        if mode=='menu': pg.click('#thmb'); pg.wait_for_timeout(400)
        if mode=='open': pg.evaluate("document.querySelectorAll('details.rfx').forEach(e=>e.open=true)"); pg.wait_for_timeout(300)
        name=f"{out}/{os.path.basename(d)[:5]}_{f[:-5]}{('-'+frag) if frag else ''}_{th}_{w}{('_'+mode) if mode else ''}.png"
        pg.screenshot(path=name); print(name); ctx.close()
    b.close()
