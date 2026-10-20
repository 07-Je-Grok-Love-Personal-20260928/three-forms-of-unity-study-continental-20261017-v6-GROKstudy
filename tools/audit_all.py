"""核对网页中所有中文引号引文是否为 CCI 数据/爬取页面的逐字子串（含 data/*.json 与 /workspace/cci_crawl/corpus.json）。
用法：python3 tools/audit_all.py [页面...]；默认检查所有非原文库页面。最短 8 个有效字才检查。"""
import re,json,sys,glob,html
def strip(t):
    t=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',t); t=re.sub(r'<[^>]+>','',t); return html.unescape(t)
def norm(s): return re.sub(r'[\s，。；：、！？“”‘’「」『』"\'（）()…—–·,.;:﹑\u200b\xa0\-\*\[\]⟦⟧]|\\n','',s)
corp=''
for f in glob.glob('data/*.json')+glob.glob('data/ref/*.txt'): corp+=open(f,encoding='utf-8').read()
try:
    for v in json.load(open('/workspace/cci_crawl/corpus.json')).values(): corp+=v['text']
except Exception as e: print('no crawl corpus',e)
corp=norm(re.sub(r'⟦\d+⟧','',corp))
PDFC=norm(''.join(json.load(open('data/pdf/pdf2015.json',encoding='utf-8'))['pages'].values()))
pdfq=0
files=sys.argv[1:] or ['index.html','bible.html','hc.html','bc.html','dort.html','compare.html','westminster.html','memory.html','sources.html']
bad=0
for f in files:
    t=open(f,encoding='utf-8').read()
    t=re.sub(r'<q class="en"[^>]*>.*?</q>','',t)
    t=re.sub(r'<q class="pdfq"[^>]*>.*?</q>','',t)
    t=re.sub(r'<td class="d[cp]">.*?</td>','',t)  # 差异表：规范化比对片段，不是引文  # 由 tools/verify_pdf.py 单独核对
    for m in re.finditer(r'“([^”]{4,200})”',t):
        q=strip(m.group(1)); parts=[p for p in re.split(r'……|…|\.\.\.',q) if len(norm(p))>=8]
        if parts and not all(norm(p) in corp for p in parts) and all(norm(p) in corp or norm(p) in PDFC for p in parts): pdfq+=1; continue
        if parts and not all(norm(p) in corp for p in parts):
            bad+=1; ctx=strip(t[max(0,m.start()-40):m.end()+20]).replace('\n',' ')
            print(f,'|',q[:90],'||',ctx[:110])
print('PDF-only quotes (in 敬拜手册 2015 text)',pdfq); print('unmatched',bad)
