import json, glob, sys, collections
sys.path.insert(0,'/tmp/nouns')
from gen import *
nouns={}
for f in sorted(glob.glob('/home/claude/academia/data/*.json')):
    d=json.load(open(f))
    for l in d['L']:
        if l[2]=='noun': nouns[l[0]]=l[1]
ART={'ὁ':'m','ἡ':'f','τό':'n','οἱ':'m','αἱ':'f','τά':'n','ὁ/ἡ':'c'}
out={}; stats=collections.Counter(); mism=[]
for lem,head in nouns.items():
    parts=[p.strip() for p in head.split(',')]
    att,gens=norm_att(lem)
    g=None
    if parts[-1] in ART: g=ART[parts[-1]]
    elif lem in lsj and lsj[lem]['gen'] and lsj[lem]['gen'][0] in ART: g=ART[lsj[lem]['gen'][0]]
    elif gens: g=gens.most_common(1)[0][0]
    if g=='c': g=gens.most_common(1)[0][0] if gens else 'm'
    if g not in ('m','f','n'): g='m'
    gs = att['gs'].most_common(1)[0][0] if att['gs'] else None
    if not gs and len(parts)>=3:
        gs=recon_gs(lem,parts[1])
    if False:
        e=parts[1]
        # reconstruct from ending: if ending full word (starts like lemma) use it
        if strip_acc(e)[:2]==strip_acc(lem)[:2]: gs=e
        else:
            el=strip_acc(e); Ls=strip_acc(lem)
            # replace lemma ending by matching first letter of ending
            for i in range(len(Ls)-1,0,-1):
                if Ls[i]==el[0]:
                    gs=None; break
    if not gs:
        Ls=strip_acc(lem); e=None
        if Ls.endswith('ευς'): e='εως'
        elif Ls.endswith('κλης'): gs=nfc(Ls[:-4]+'κλέους')
        elif Ls.endswith('ος') and g in 'mf': e='ου'
        elif Ls.endswith('ον') and g=='n': e='ου'
        elif Ls.endswith('η') and g=='f': e='ης'
        elif Ls.endswith('α') and g=='f': e='ας' if Ls[-2] in 'ειρ' else 'ης'
        elif Ls.endswith('ας') and g=='m': e='ου'
        elif Ls.endswith('ης') and g=='m':
            e='ους' if any(Ls.endswith(x) for x in ('γενης','κρατης','σθενης','φανης','μηδης','μενης','πειθης','φερνης')) else 'ου'
        if e: gs=recon_gs(lem,e)
    r=gen_paradigm(lem,gs,g,att)
    proper=lem[0].isupper()
    forms=[];st=''
    for c in CELLS:
        gf=r[2].get(c) if r else None
        at=att.get(c,collections.Counter())
        top=at.most_common(1)[0] if at else None
        if gf and gf in at: f,s=gf,'a'; stats['agree']+=1
        elif top and top[1]>=2:
            f,s=top[0],'a'
            if gf: stats['disagree']+=1; mism.append((lem,c,gf,top))
        elif gf: f,s=gf,'g'; stats['gen']+=1
        elif top: f,s=top[0],'a'
        else: f,s='', '-'
        forms.append(f); st+=s
    forms[9]=forms[5]; st=st[:9]+st[5]
    plur_att=sum(att.get(c,collections.Counter()).total() for c in ('np','gp','dp','ap','vp'))
    if proper and plur_att<2:
        for i in range(5,10): forms[i]=''; st=st[:i]+'-'+st[i+1:]
    if r: decl,typ=r[0],r[1]
    else:
        G=strip_acc(gs) if gs else ''
        Ls=strip_acc(lem)
        if not G and Ls[-2:] in ('αι',): G='ης'
        elif not G and Ls[-2:] in ('οι',): G='ου'
        elif not G and Ls[-2:] in ('ες',): G='ος'
        decl = 2 if G.endswith('ου') and not (strip_acc(lem).endswith('ης') or strip_acc(lem).endswith('ας')) else 1 if G.endswith('ου') or G.endswith('ης') or G.endswith('ας') else 3 if G else 0
        typ=''
        stats['nogen']+=1
    if decl==0:
        Ls=strip_acc(lem)
        if Ls.endswith('α') and g=='n': decl=2
        elif Ls[-1] in 'ξψρ' or Ls[-2:] in ('ων','ις','ας','ης','υς','ος','ους','εις','ους') or Ls.endswith('ν'): decl=3
    if st.count('-')==10: forms=[]; st=''
    out[lem]=[decl,typ,g,'|'.join(forms),st]
json.dump(out,open('/home/claude/academia/data/nouns.json','w'),ensure_ascii=False,separators=(',',':'))
print(stats)
import random; random.seed(1)
for m in random.sample(mism,min(40,len(mism))): print(m)
