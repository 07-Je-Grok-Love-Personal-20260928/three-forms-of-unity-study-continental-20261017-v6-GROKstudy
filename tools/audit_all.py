import re,json,sys,glob,html
sys.path.insert(0,'/workspace/cci_crawl')
def strip(t):
    t=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',t); t=re.sub(r'<[^>]+>','',t); return html.unescape(t)
def norm(s): return re.sub(r'[\s，。；：、！？“”‘’「」『』（）()…—·,.;:﹑,\u200b\xa0\-\*\[\]⟦⟧\d]|\\n|<[^>]+>','',s)
corp=''
for f in glob.glob('data/*.json'): corp+=open(f,encoding='utf-8').read()
for f in glob.glob('/workspace/cci_crawl/raw/*'): corp+=strip(open(f,encoding='utf-8',errors='ignore').read())
for f in glob.glob('/workspace/ref_crawl/*.html'): corp+=strip(open(f,encoding='utf-8',errors='ignore').read())
for f in glob.glob('/workspace/ref_crawl/*.json')+glob.glob('/workspace/ref_crawl/*.txt'): corp+=open(f,encoding='utf-8',errors='ignore').read()
corp=norm(corp)
bad=0
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'“([^”]{4,120})”',t):
        q=m.group(1); parts=[p for p in re.split(r'……|…|\.\.\.',q) if len(norm(p))>=4]
        if parts and not all(norm(p) in corp for p in parts):
            bad+=1; print(f,'|',q)
print('unmatched',bad)
