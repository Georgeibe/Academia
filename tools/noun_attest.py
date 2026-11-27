import glob, re, unicodedata, json, collections, sys
rx=re.compile(r'<word [^>]*?form="([^"]*)"[^>]*?lemma="([^"]*)"[^>]*?postag="(n[^"]{8})"')
A=collections.defaultdict(collections.Counter)
for f in [f for f in glob.glob('/tmp/gt/glaux/xml/*.xml') if '/0016-' not in f]:
    for m in rx.finditer(open(f,encoding='utf8').read()):
        form,lem,pt=m.groups()
        form=unicodedata.normalize('NFC',form); lem=unicodedata.normalize('NFC',lem)
        num,gen,case=pt[2],pt[6],pt[7]
        if num not in 'spd' or case not in 'ngdav': continue
        A[lem][f'{case}{num}|{gen}|{form}']+=1
json.dump({k:dict(v) for k,v in A.items()},open('/tmp/nouns/attested.json','w'),ensure_ascii=False)
print(len(A))
