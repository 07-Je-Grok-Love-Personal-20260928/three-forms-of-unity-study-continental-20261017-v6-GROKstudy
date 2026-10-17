"""目录调宽测试：鼠标拖拽、键盘、触摸(CDP)、localStorage 持久化、clamp、内容不溢出。用法：python3 tools/qa_toc.py [页面] [--shots]"""
import sys,os
from playwright.sync_api import sync_playwright
page=next((a for a in sys.argv[1:] if a.endswith('.html')),'hct.html'); shots='--shots' in sys.argv
url='file://'+os.path.abspath(page); fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
    else: print('ok  ',m)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto(url); pg.wait_for_timeout(400)
    W=lambda:pg.evaluate("Math.round(document.querySelector('#toc').getBoundingClientRect().width)")
    ML=lambda:pg.evaluate("Math.round(document.querySelector('#main').getBoundingClientRect().left)")
    OV=lambda:pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
    chk(W()==300,f'default width 300 (got {W()})')
    g=pg.locator('#tocgrip').bounding_box(); y=g['y']+g['height']/2; x=g['x']+g['width']/2
    pg.mouse.move(x,y); pg.mouse.down(); pg.mouse.move(x+150,y,steps=8); pg.mouse.move(x+300,y,steps=8); pg.mouse.up(); pg.wait_for_timeout(200)
    chk(abs(W()-600)<=3,f'drag wide -> ~600 (got {W()})'); chk(abs(ML()-W())<=1,f'main margin follows toc ({ML()})'); chk(OV()<=0,'no h-overflow wide')
    if shots: os.makedirs('_shots',exist_ok=True); pg.screenshot(path='_shots/toc_wide_1280.png')
    chk(pg.evaluate("localStorage.getItem('tfu1.tw')")==str(W()),'saved to localStorage')
    g=pg.locator('#tocgrip').bounding_box(); x=g['x']+g['width']/2
    pg.mouse.move(x,y); pg.mouse.down(); pg.mouse.move(x-700,y,steps=10); pg.mouse.up(); pg.wait_for_timeout(200)
    chk(W()==220,f'drag narrow clamps at min 220 (got {W()})'); chk(OV()<=0,'no h-overflow narrow')
    if shots: pg.screenshot(path='_shots/toc_narrow_1280.png')
    g=pg.locator('#tocgrip').bounding_box(); x=g['x']+g['width']/2
    pg.mouse.move(x,y); pg.mouse.down(); pg.mouse.move(x+1500,y,steps=10); pg.mouse.up(); pg.wait_for_timeout(200)
    chk(W()==min(680,round(1280*.6)),f'drag wide clamps at max (got {W()})')
    pg.reload(); pg.wait_for_timeout(300); chk(W()==min(680,round(1280*.6)),f'persist after reload ({W()})')
    pg.focus('#tocgrip'); pg.keyboard.press('ArrowLeft'); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(100)
    chk(W()==min(680,round(1280*.6))-32,f'keyboard ArrowLeft x2 (-32) ({W()})')
    pg.keyboard.press('Home'); chk(W()==220,'Home -> min'); pg.keyboard.press('Shift+ArrowRight'); chk(W()==284,f'Shift+Right +64 ({W()})')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(100); chk(W()==300,f'Enter resets ({W()})'); chk(pg.evaluate("localStorage.getItem('tfu1.tw')")is None,'reset clears storage')
    pg.click('#tocx'); pg.wait_for_timeout(600); chk(pg.evaluate("getComputedStyle(document.querySelector('#tocgrip')).display")=='none','grip hidden when TOC hidden'); chk(ML()==0,'main full width when hidden')
    pg.click('#tocbtn'); pg.wait_for_timeout(600); chk(ML()==300,'TOC back')
    ctx.close()
    # mobile
    ctx=b.new_context(viewport={'width':390,'height':800},has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto(url); pg.wait_for_timeout(400)
    pg.click('#tocbtn'); pg.wait_for_timeout(700)
    W=lambda:pg.evaluate("Math.round(document.querySelector('#toc').getBoundingClientRect().width)")
    chk(W()==min(330,round(390*.86)),f'mobile default {W()}')
    g=pg.locator('#tocgrip').bounding_box(); chk(g is not None and g['width']>=20,f'mobile grip visible {g}')
    cdp=ctx.new_cdp_session(pg); x=g['x']+g['width']/2; y=400
    def tp(t,xx): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[{'x':xx,'y':y}] if t!='touchEnd' else []})
    tp('touchStart',x)
    for i in range(1,9): tp('touchMove',x+i*12)
    tp('touchEnd',0); pg.wait_for_timeout(300)
    chk(W()==round(390*.94),f'touch drag widened drawer to cap 94vw ({W()})')
    chk(pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")<=0,'mobile no h-overflow')
    if shots: pg.screenshot(path='_shots/toc_mobile_390.png')
    ctx.close(); b.close()
chk(not errs,f'no js errors {errs[:1]}')
print('TOC QA fails',len(fails)); sys.exit(1 if fails else 0)
