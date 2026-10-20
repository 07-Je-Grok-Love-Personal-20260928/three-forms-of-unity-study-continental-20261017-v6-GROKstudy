"""核对所有敬拜手册（2015 版 PDF）摘引：<q class="pdfq" data-p=N data-span=S> 必须是第 N..N+S 页印刷正文的逐字子串，且紧跟同页码的出处标签。
用法：python3 tools/verify_pdf.py [页面...]"""
import re,json,sys,glob,html
P={int(k):v for k,v in json.load(open('data/pdf/pdf2015.json',encoding='utf-8'))['pages'].items()}
n=lambda s: re.sub(r'\s+','',s)
files=sys.argv[1:] or sorted(glob.glob('*.html'))
tot=bad=0
for f in files:
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<q class="pdfq" data-p="(\d+)" data-span="(\d+)">(.*?)</q><span class="pdfsrc">出自《中国改革宗教会敬拜手册》2015 版 第 (\d+) 页</span>',t):
        p,s,x,lab=int(m.group(1)),int(m.group(2)),html.unescape(m.group(3)),int(m.group(4))
        tot+=1; src=n(''.join(P.get(i,'') for i in range(p,p+s+1)))
        if n(x) not in src or lab!=p: bad+=1; print('BAD',f,p,x[:60])
    if t.count('class="pdfq"')!=len(re.findall(r'<q class="pdfq" data-p="\d+" data-span="\d+">.*?</q><span class="pdfsrc">',t)): bad+=1; print('BAD label missing',f)
print('pdf quotes',tot,'bad',bad); sys.exit(1 if bad else 0)
