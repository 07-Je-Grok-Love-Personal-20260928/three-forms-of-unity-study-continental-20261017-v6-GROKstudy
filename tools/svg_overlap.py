"""检查 SVG 地图/示意图中文字标签是否互相重叠（getBBox，用户坐标系）。"""
import sys,os
from playwright.sync_api import sync_playwright
JS='''()=>{const res=[];document.querySelectorAll('figure svg').forEach((svg,si)=>{
 const ts=[...svg.querySelectorAll('text')].map(t=>{const b=t.getBBox();return {x0:b.x,y0:b.y,x1:b.x+b.width,y1:b.y+b.height,s:t.textContent.slice(0,14)}});
 const vb=svg.viewBox.baseVal;
 for(let i=0;i<ts.length;i++){const a=ts[i];
   if(a.x0<-1||a.x1>vb.width+1||a.y0<-1||a.y1>vb.height+1) res.push(['越界',si,a.s]);
   for(let j=i+1;j<ts.length;j++){const b=ts[j];const ox=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),oy=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);
     if(ox>3&&oy>3) res.push(['重叠',si,a.s,b.s,Math.round(ox),Math.round(oy)]);}}
});return res}'''
pages=sys.argv[1:] or ['bible.html','hc.html','bc.html','dort.html','compare.html','westminster.html','memory.html']
bad=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1280,'height':900})
    for f in pages:
        pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(300); pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",'main section.l2,main section.l3,main figure,main .icm{content-visibility:visible!important}')  # v8：测量时强制渲染 content-visibility:auto 的区块
        r=pg.evaluate(JS)
        for x in r: print(f,x); bad+=1
    b.close()
print('svg problems',bad)
