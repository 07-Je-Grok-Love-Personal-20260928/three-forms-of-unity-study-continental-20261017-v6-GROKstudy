"""52 主日标题一致性：c_titles.HC52 = hc.html 三级标题 = hct.html 三级标题 = 各页目录 = memory.html 速记表。"""
import re,html,sys
sys.path.insert(0,'.')
from c_titles import HC52
T={n:v[0] for n,v in HC52.items()}
def rd(f): return open(f,encoding='utf-8').read()
bad=0
def chk(name,got):
    global bad
    miss=[n for n in range(1,53) if got.get(n)!=T[n]]
    print(name,'OK' if not miss else f'MISMATCH {miss[:5]} {[(got.get(n),T[n]) for n in miss[:2]]}'); bad+=bool(miss)
# 正文 L3
for f,pref in (('hc.html','hd-ld'),('hct.html','ld')):
    h=rd(f); got={}
    for m in re.finditer(r'<section class="l3[^"]*" id="'+pref+r'(\d+)"><h4 class="l3h"><span class="n3">[^<]*</span>.*?<span class="l3x">主日\d+ · (.*?)</span>',h,flags=re.S):
        got[int(m.group(1))]=html.unescape(m.group(2))
    chk(f+' 正文',got)
    # 目录（任意页的目录都应含 52 个）
    toc={}
    for m in re.finditer(r'<li class="t3"><a href="'+f+r'#'+pref+r'(\d+)"(?: data-e="[^"]*")?>[\d.]+ 主日\d+ · (.*?)</a>',h): toc[int(m.group(1))]=html.unescape(m.group(2))
    chk(f+' 目录',toc)
# 目录在其它页
for f in ('index.html','memory.html','bc.html'):
    h=rd(f); toc={}
    for m in re.finditer(r'<li class="t3"><a href="hc\.html#hd-ld(\d+)"(?: data-e="[^"]*")?>[\d.]+ 主日\d+ · (.*?)</a>',h): toc[int(m.group(1))]=html.unescape(m.group(2))
    chk(f+' 目录(hc)',toc)
# 记忆页
h=rd('memory.html'); got={}
for m in re.finditer(r'id="mm-ld(\d+)" class="mi [^"]*" data-k="hc\d+"><a href="hc.html#hd-ld\d+"><b>主日\d+</b>(.*?)<small>',h): got[int(m.group(1))]=html.unescape(m.group(2))
chk('memory.html 速记表',got)
# 罗盘 title
h=rd('hc.html'); got={int(a):html.unescape(b) for a,b in re.findall(r'<title>主日(\d+) · (.*?)</title>',h)}
chk('hc.html 罗盘',got)
sys.exit(1 if bad else 0)
