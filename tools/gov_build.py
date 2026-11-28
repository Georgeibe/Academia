"""Build data/gov.json (verb government) from tools/gov.tsv.
gov.tsv lines: lemma|code|ru|en|ka[|form]   codes: g d a aa ag ad ai di gi i p ap dp gp dg"""
import json,sys
CODES={'g','d','a','aa','ag','ad','ai','di','gi','i','p','ap','dp','gp','dg'}
out={}; bad=[]
for n,l in enumerate(open('tools/gov.tsv',encoding='utf8'),1):
    l=l.rstrip('\n')
    if not l.strip() or l.startswith('#'): continue
    f=l.split('|')
    if len(f) not in (5,6) or f[1] not in CODES or '—' == f[3].strip(): bad.append((n,l)); continue
    out.setdefault(f[0],[]).append(f[1:5]+([f[5]] if len(f)==6 else []))
json.dump(out,open('data/gov.json','w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
print(len(out),'verbs',sum(map(len,out.values())),'lines; bad:',bad)
