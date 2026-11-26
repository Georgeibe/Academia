import re, glob, json, unicodedata, sys
from beta_code import beta_code_to_greek
D='/tmp/gt/lexica/CTS_XML_TEI/perseus/pdllex/grc/lsj/'
def b2g(b):
    b=re.sub(r'[\^_\d]','',b)
    g=beta_code_to_greek(b)
    g=unicodedata.normalize('NFC',g)
    # final sigma
    g=re.sub(r'σ\b','ς',g)
    return g.strip()
def clean(t):
    t=re.sub(r'<[^>]+>','',t); t=re.sub(r'\s+',' ',t).strip()
    t=t.strip(' ,;:.—-[]()')
    return t
out={}
for f in sorted(glob.glob(D+'*.xml')):
    s=open(f,encoding='utf8').read()
    for m in re.finditer(r'<entryFree[^>]*key="([^"]*)"[^>]*>(.*?)</entryFree>',s,re.S):
        key,body=m.group(1),m.group(2)
        lem=b2g(key)
        trs=[clean(x) for x in re.findall(r'<tr[^>]*>(.*?)</tr>',body,re.S)]
        trs=[t for t in trs if t and len(t)<60]
        seen=[];
        for t in trs:
            if t.lower() not in [x.lower() for x in seen]: seen.append(t)
        gl=''
        for t in seen:
            cand=(gl+', '+t) if gl else t
            if len(cand)>70 and gl: break
            gl=cand
            if len(seen)>0 and gl.count(',')>=3: break
        itypes=[b2g(x) for x in re.findall(r'<itype[^>]*>(.*?)</itype>',body[:600])]
        gen=re.findall(r'<gen[^>]*>(.*?)</gen>',body[:600])
        score=len(trs)
        rec={'gloss':gl,'itype':itypes[:3],'gen':[b2g(g) for g in gen[:1]],'score':score,'n':len(body)}
        prev=out.get(lem)
        if prev is None or rec['n']>prev['n']: out[lem]=rec
json.dump(out,open('/home/claude/plato/lsj_index.json','w'),ensure_ascii=False)
print(len(out), sum(1 for v in out.values() if v['gloss']))
for k in ['ἀγαθός','ἄγω','εἰμί','λέγω','ἀπολογέομαι','δικαστής','ὅστις','σύ','κατήγορος','φιλοσοφέω']:
    print(k, out.get(k))
