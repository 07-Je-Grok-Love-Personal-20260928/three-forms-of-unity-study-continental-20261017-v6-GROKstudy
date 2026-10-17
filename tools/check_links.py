import re,glob,os,sys
pages={f:open(f,encoding='utf-8').read() for f in glob.glob('*.html')}
ids={f:set(re.findall(r'\bid="([^"]+)"',h)) for f,h in pages.items()}
bad=0;n=0
for f,h in pages.items():
    for m in re.finditer(r'href="([^"]+)"',h):
        u=m.group(1)
        if u.startswith(('http','mailto:')): continue
        n+=1
        file,_,frag=u.partition('#')
        file=file or f
        if file.startswith('assets/'):
            if not os.path.exists(file.split('?')[0]): print('missing asset',f,u); bad+=1
            continue
        if file not in pages: print('missing page',f,u); bad+=1; continue
        if frag and frag not in ids[file]: print('missing id',f,u); bad+=1
    # toc direct child of body
    if not re.search(r'<body[^>]*>\s*<div id="prog"></div><nav id="toc"',h): print('toc not direct child',f); bad+=1
    dup=[i for i in ids[f] if len(re.findall(r'\bid="%s"'%re.escape(i),h))>1]
    if dup: print('dup ids',f,dup[:5]); bad+=1
print('links checked',n,'bad',bad)
