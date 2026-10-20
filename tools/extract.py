# 用 PyMuPDF 抽取印刷正文：只保留 SimSun/Calibri 字体，并排除与用户批注（FreeText 内容）相同的文字。
import pymupdf,json
d=pymupdf.open('/workspace/uploads/t83u.pdf')
notes=[]
for i,p in enumerate(d):
    cont=' '.join((a.info.get('content') or '') for a in p.annots() if a.type[1] in ('FreeText','Text'))
    cn=''.join(cont.split())
    for a in p.annots():
        if a.type[1] in ('FreeText','Text') and (a.info.get('content') or '').strip(): notes.append({'page':i+2,'text':a.info['content'].replace('\r','\n')})
    out=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            s=''
            for sp in l['spans']:
                t=sp['text']; tn=''.join(t.split())
                if ('SimSun' in sp['font'] or 'Calibri' in sp['font']) and not (tn and tn in cn): s+=t
            if s.strip(): out.append(s)
    open(f'p{i+1}.txt','w').write('\n'.join(out)+'\n')
json.dump(notes,open('user_notes.json','w'),ensure_ascii=False,indent=0)
print(len(notes),'user notes')
