import json, unicodedata as U, collections
from greek_accentuation.syllabify import syllabify
A=json.load(open('/tmp/nouns/attested.json'))
lsj=json.load(open('/home/claude/academia/tools/lsj_index.json'))
CELLS=['ns','gs','ds','as','vs','np','gp','dp','ap','vp']
ACU,CIR,GRV='́','͂','̀'
def nfc(s): return U.normalize('NFC',s)
def nfd(s): return U.normalize('NFD',s)
def strip_acc(w): return nfc(''.join(c for c in nfd(w) if c not in ACU+CIR+GRV))
def base(c): return nfd(c)[0]
def grave2acute(w): return nfc(nfd(w).replace(GRV,ACU))
def nacc(w): return sum(1 for c in nfd(w) if c in ACU+CIR)
def norm_att(lem):
    out=collections.defaultdict(collections.Counter); gens=collections.Counter()
    for k,c in A.get(lem,{}).items():
        cell,g,f=k.split('|'); cell=cell[0]+cell[1]
        if cell[1]=='d' or '’' in f or "'" in f: continue
        f=grave2acute(f)
        if nacc(f)!=1: continue
        if cell=='dp' and f.endswith('ν'): f=f[:-1]
        out[cell][f]+=c; gens[g]+=c
    return out,gens
DIPH={'αι','ει','οι','υι','αυ','ευ','ου','ηυ'}
def sylls(w): return syllabify(strip_acc(w))
def nucleus_pos(syl):
    """return index (in NFD string of syl) after which to insert accent, and is_long"""
    d=nfd(syl); bases=[(i,ch) for i,ch in enumerate(d) if U.combining(ch)==0]
    vow=[(i,ch) for i,ch in bases if ch.lower() in 'αεηιουω']
    if not vow: return None,False
    last=vow[-1]; long=False
    if len(vow)>=2:
        pair=(vow[-2][1]+vow[-1][1]).lower()
        if pair in DIPH and '̈' not in d: long=True
    v=last[1].lower()
    if v in 'ηω': long=True
    # iota subscript
    j=last[0]+1
    while j<len(d) and U.combining(d[j]):
        if d[j]=='ͅ': long=True
        j+=1
    return j,long
def put(syl,mark):
    d=nfd(syl); j,_=nucleus_pos(syl)
    # insert before iota subscript if present? canonical order handles; insert at j
    return nfc(d[:j]+mark+d[j:])
def is_long(syl, known): 
    return nucleus_pos(syl)[1] or known
def accent(word, idx_from_start, ult_long, circ_ult=False, longset=()):
    s=list(syllabify(word)); n=len(s)
    i=min(idx_from_start,n-1)
    pe=n-i  # position from end 1..
    if ult_long and pe>2: pe=2
    if pe>3: pe=3
    i=n-pe
    if pe==1: mark=CIR if circ_ult else ACU
    elif pe==2:
        pl=is_long(s[i], strip_acc(s[i]) in longset.get(i,()) if isinstance(longset,dict) else False)
        mark=CIR if (pl and not ult_long) else ACU
    else: mark=ACU
    if mark==CIR:
        j,_=nucleus_pos(s[i]); d=nfd(s[i]); k=j-1
        while k>=0 and U.combining(d[k]): k-=1
        if d[k].lower() in 'εο': mark=ACU
    s[i]=put(s[i],mark)
    return ''.join(s)
def acc_info(lem):
    s=syllabify(lem); d=[nfd(x) for x in s]
    for i,x in enumerate(d):
        if ACU in x: return i,ACU,len(s)
        if CIR in x: return i,CIR,len(s)
    return None
def longset_from(lem, att):
    L={}
    for f,c in [(lem,9)]+[(f,c) for cc in att.values() for f,c in cc.items()]:
        if c<2: continue
        for i,x in enumerate(syllabify(f)):
            if CIR in nfd(x): L.setdefault(i,set()).add(strip_acc(x))
    return L
def _old_longset(lem, att):
    """syllable indices (from start) known long via a circumflex in lemma or attested forms"""
    L=set(); st=strip_acc(lem)
    forms=[lem]+[f for c in att.values() for f in c]
    for f in forms:
        s=syllabify(f)
        for i,x in enumerate(s):
            if CIR in nfd(x): L.add(i)
    return L
def recessive_idx(word, ult_long):
    n=len(syllabify(word)); return max(0,n-(2 if ult_long else 3))
# endings: (ending, ultima_long)
SYNC={'πατήρ':'πατήρ πατρός πατρί πατέρα πάτερ πατέρες πατέρων πατράσι πατέρας πατέρες',
'μήτηρ':'μήτηρ μητρός μητρί μητέρα μῆτερ μητέρες μητέρων μητράσι μητέρας μητέρες',
'θυγάτηρ':'θυγάτηρ θυγατρός θυγατρί θυγατέρα θύγατερ θυγατέρες θυγατέρων θυγατράσι θυγατέρας θυγατέρες',
'γαστήρ':'γαστήρ γαστρός γαστρί γαστέρα γαστέρ γαστέρες γαστέρων γαστράσι γαστέρας γαστέρες',
'ἀνήρ':'ἀνήρ ἀνδρός ἀνδρί ἄνδρα ἄνερ ἄνδρες ἀνδρῶν ἀνδράσι ἄνδρας ἄνδρες'}
def gen_paradigm(lem, gs, g, att):
    if lem in SYNC: return 3,'πατήρ',dict(zip(CELLS,SYNC[lem].split()))
    L=strip_acc(lem); G=strip_acc(gs) if gs else None
    ai=acc_info(lem)
    if not ai: return None
    ia,am,nsyl=ai; oxy = ia==nsyl-1
    if am==CIR and ia==nsyl-1 and (L[-1] in 'αη' or L.endswith('ους')): return None
    ns_top = att.get('ns') and att['ns'].most_common(1)[0]
    if ns_top and ns_top[1]>=3 and strip_acc(ns_top[0])!=L: return None
    LS=longset_from(lem,att)
    F={}
    def P(st,ends,circ_cells=(),gp_circ=False):
        for c,(e,ul) in zip(CELLS,ends):
            if e is None: continue
            w=st+e
            cu = oxy and c in circ_cells
            if gp_circ and c=='gp':
                F[c]=accent(w,len(syllabify(w))-1,True,True); continue
            F[c]=accent(w,ia,ul,cu,LS)
    S,Lg=False,True
    O2=('gs','ds','gp','dp')
    # 2nd declension
    if G and G.endswith('ου') and L.endswith('ος') and g in 'mf':
        P(L[:-2],[('ος',S),('ου',Lg),('ῳ',Lg),('ον',S),('ε',S),('οι',S),('ων',Lg),('οις',Lg),('ους',Lg),('οι',S)],O2)
        return 2,'λόγος',F
    if G and G.endswith('ου') and L.endswith('ον') and g=='n':
        P(L[:-2],[('ον',S),('ου',Lg),('ῳ',Lg),('ον',S),('ον',S),('α',S),('ων',Lg),('οις',Lg),('α',S),('α',S)],O2)
        return 2,'δῶρον',F
    pl1=[('αι',S),('ων',Lg),('αις',Lg),('ας',Lg),('αι',S)]
    if g=='f' and L[-1] in 'ηα' and G and G[-2:] in ('ης','ας'):
        st=L[:-1]; v=L[-1]; gv=G[-2]
        if v=='η': sg=[('η',Lg),('ης',Lg),('ῃ',Lg),('ην',Lg),('η',Lg)]; typ='τιμή'
        elif gv=='α': sg=[('α',Lg),('ας',Lg),('ᾳ',Lg),('αν',Lg),('α',Lg)]; typ='χώρα'
        else: sg=[('α',S),('ης',Lg),('ῃ',Lg),('αν',S),('α',S)]; typ='θάλαττα'
        if gv=='α' and (ia==nsyl-3 or (am==CIR and ia==nsyl-2)): sg=[('α',S),('ας',Lg),('ᾳ',Lg),('αν',S),('α',S)]; typ='ἀλήθεια'
        # short-alpha nouns: nom accent may be antepenult; persistent idx handles
        P(st,sg+pl1,O2,True)
        return 1,typ,F
    if g=='m' and L[-2:] in ('ης','ας') and G and G.endswith('ου'):
        st=L[:-2]; v=L[-2]
        va = not lem[0].isupper() and v=='η' and (L.endswith('της') or L.endswith('πωλης') or L.endswith('αρχης'))
        sg=[(v+'ς',Lg),('ου',Lg),('ῃ' if v=='η' else 'ᾳ',Lg),(v+'ν',Lg),('α' if va else v,S if va else Lg)]
        P(st,sg+pl1,O2,True)
        if va and not lem[0].isupper(): 
            w=st+'α'; F['vs']=accent(w,ia,False,False,LS) if not oxy else F['vs']
        return 1,('στρατιώτης' if v=='η' else 'νεανίας'),F
    if not G: return None
    if L.endswith('ος') and g!='n' and not G.endswith('ου'): return None
    if L.endswith('ις') and G.endswith('εως'):
        st=L[:-2]
        ends=[('ις',S),('εως',S),('ει',Lg),('ιν',S),('ι',S),('εις',Lg),('εων',S),('εσι',S),('εις',Lg),('εις',Lg)]
        for c,(e,ul) in zip(CELLS,ends):
            w=st+e; n=len(syllabify(w))
            if c in ('gs','gp'): F[c]=accent(w,len(syllabify(st))-1 if len(syllabify(st))>0 else 0,False,False,LS)
            else: F[c]=accent(w,recessive_idx(w,ul),ul,False,LS)
        F['ns']=lem
        return 3,'πόλις',F
    if L.endswith('κλης') and G.endswith('κλεους'):
        st=L[:-4]
        F.update(dict(zip(CELLS[:5],[lem,nfc(st+'κλέους'),nfc(st+'κλεῖ'),nfc(st+'κλέα'),accent(st+'κλεις',recessive_idx(st+'κλεις',True),True,False,LS)])))
        return 3,'Περικλῆς',F
    if L.endswith('ευς') and G.endswith('εως'):
        st=L[:-3]
        for c,e in zip(CELLS,['εύς','έως','εῖ','έα','εῦ','εῖς','έων','εῦσι','έας','εῖς']): F[c]=nfc(st+e)
        return 3,'βασιλεύς',F
    if g=='n' and L.endswith('ος') and G.endswith('ους'):
        st=L[:-2]
        ends=[('ος',S),('ους',Lg),('ει',Lg),('ος',S),('ος',S),('η',Lg),('ων',Lg),('εσι',S),('η',Lg),('η',Lg)]
        for c,(e,ul) in zip(CELLS,ends):
            w=st+e
            F[c]= accent(w,len(syllabify(w))-1,True,True) if c=='gp' else accent(w,recessive_idx(w,ul),ul,False,LS)
        F['ns']=F['as']=F['vs']=lem
        return 3,'γένος',F
    if g in 'mf' and L.endswith('ης') and G.endswith('ους') and not lem[0].isupper():
        st=L[:-2]
        ends=[('ης',Lg),('ους',Lg),('ει',Lg),('η',Lg),('ες',S),('εις',Lg),('ων',Lg),('εσι',S),('εις',Lg),('εις',Lg)]
        for c,(e,ul) in zip(CELLS,ends):
            w=st+e; F[c]=accent(w,ia,ul,False,LS) if c=='gp' else accent(w,recessive_idx(w,ul),ul,False,LS)
        F['ns']=lem
        return 3,'τριήρης',F
    if g=='m' and L.endswith('ης') and G.endswith('ους'):
        st=L[:-2]
        for c,(e,ul) in zip(CELLS[:5],[('ης',Lg),('ους',Lg),('ει',Lg),('η',Lg),('ες',S)]):
            w=st+e; F[c]=accent(w,recessive_idx(w,ul),ul,False,LS)
        F['ns']=lem
        return 3,'Σωκράτης',F
    if G.endswith('ος') and not G.endswith('ους'):
        st=G[:-2]; nm=g=='n'
        mono = nsyl==1
        s2=st
        for a,b in [('οντ','ου'),('αντ','α'),('εντ','ει'),('υντ','υ')]:
            if s2.endswith(a): s2=s2[:-len(a)]+b; dp=s2+'σι'; break
        else:
            if s2[-1] in 'κγχ': dp=s2[:-1]+'ξι'
            elif s2[-1] in 'πβφ': dp=s2[:-1]+'ψι'
            elif s2[-1] in 'τδθν': dp=s2[:-1]+'σι'
            else: dp=s2+'σι'
        ends={'gs':(st+'ος',S),'ds':(st+'ι',S),'as':(st+'α',S),'np':(st+('α' if nm else 'ες'),S),
              'gp':(st+'ων',Lg),'dp':(dp,S),'ap':(st+('α' if nm else 'ας'),S)}
        GI=acc_info(gs)  # accent of genitive is reliable (attested)
        gox = GI and GI[0]==GI[2]-1
        if gox: mono=True
        for c,(w,ul) in ends.items():
            if mono and c in ('gs','ds','gp','dp'):
                F[c]=accent(w,len(syllabify(w))-1,True,c=='gp')
            elif mono:
                n=len(syllabify(w)); F[c]=accent(w,n-2,ul,False,LS)
            elif GI:
                # keep accent syllable of genitive (same stem syllable count)
                idx=GI[0]
                F[c]=accent(w,idx,ul,False,LS)
            else:
                F[c]=accent(w,ia,ul,False,LS)
        F['ns']=lem; F['vs']=lem
        if not oxy and L[-2:] in ('ις','υς') and not nm: F['vs']=nfc(lem[:-1])
        if nm: F['as']=lem
        F['vp']=F['np']
        if not nm and not oxy and L[-2:] in ('ις','υς') and (st[-1] in 'τδθ' or st[-1] in 'ιυ'):
            w=L[:-1]+'ν'; F['as']=accent(w,ia,False,False,LS)
        if st.endswith('ματ'): typ='-ματ-'
        elif st.endswith('ντ'): typ='-ντ-'
        else: typ='-'+st[-1]+'-'
        return 3,typ,F
    return None

def recon_gs(lem, ending):
    """build genitive singular from dictionary ending like 'ου', 'ης', 'ακος'"""
    L=strip_acc(lem); e=strip_acc(ending).replace('-','')
    ai=acc_info(lem)
    if not ai or not e: return None
    ia,am,nsyl=ai; oxy= ia==nsyl-1
    if e in ('η','α','ον','ή','ά','όν','ος') and L.endswith('ος'): e='ου'
    if e=='ου' and L[-2:] in ('ος','ον','ης','ας'): w=L[:-2]+'ου'; ul=True; c=oxy
    elif e in ('ης','ας') and L[-1] in 'ηα': w=L[:-1]+e; ul=True; c=oxy
    elif e=='εως' and L.endswith('ις'): w=L[:-2]+'εως'; return accent(w,len(syllabify(L[:-2]))-1,False,False)
    elif e=='εως' and L.endswith('ευς'): return nfc(L[:-3]+'έως')
    elif e=='ους' and L[-2:] in ('ος','ης'): w=L[:-2]+'ους'; ul=True; c=False
    else:
        stem=None
        for i in range(len(L)-1,-1,-1):
            if L[i]==e[0] and (i<len(L)-1 or L[i] in 'αεηιουω'): stem=L[:i]; break
        if stem is None: return None
        w=stem+e; ul=e.endswith('ως'); c=False
        if nsyl==1: return accent(w,len(syllabify(w))-1,True,False)
    return accent(w,ia,ul,c)
