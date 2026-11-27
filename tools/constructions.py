"""Detect syntactic constructions from treebank XML and add them to a site data file.
usage: constructions.py treebank.xml data/xxx.json [book]
Writes data['C'] = [[token_index, code, [member indices], [governor indices]], ...]  (token indices are 0-based into W)"""
import sys, re, json, unicodedata as U
xmlf, dataf = sys.argv[1], sys.argv[2]
book = sys.argv[3] if len(sys.argv) > 3 else None
def nfc(s): return U.normalize('NFC', s)
def base(s): return nfc(''.join(c for c in U.normalize('NFD', s) if not U.combining(c))).lower()
toks = []
for m in re.finditer(r'<word ([^>]*)/>', open(xmlf, encoding='utf8').read()):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    if book and a.get('div_book') != book: continue
    toks.append(a)
T = {t['id']: t for t in toks}
for t in toks:
    t['form'] = nfc(t['form']); t['lemma'] = nfc(t.get('lemma', ''))
    pt = t.get('postag', '---------').ljust(9, '-'); t['pt'] = pt
    r = t.get('relation', ''); t['rel'] = r.split('_')[0]
    t['kids'] = []
for t in toks:
    h = T.get(t.get('head'))
    if h: h['kids'].append(t)
def pos(t): return t['pt'][0]
def mood(t): return t['pt'][4]
def case(t): return t['pt'][7]
def tense(t): return t['pt'][3]
COORDISH = {'COORD', 'APOS', 'AuxX', 'AuxY', 'AuxG'}
def parent(t):
    """effective governor: climb over coordination nodes"""
    h = T.get(t.get('head'))
    while h is not None and h['rel'] in COORDISH and h['pt'][0] in 'cdu-' :
        h = T.get(h.get('head'))
    return h
def children(t):
    out = []
    for k in t['kids']:
        if k['rel'] in COORDISH and k['pt'][0] in 'cdu-':
            out += [x for x in k['kids'] if '_CO' in x.get('relation', '')]
        else: out.append(k)
    # shared dependents of a coordination this token belongs to
    h = T.get(t.get('head'))
    if '_CO' in t.get('relation', '') and h is not None:
        out += [x for x in h['kids'] if '_CO' not in x.get('relation', '') and x['pt'][0] not in 'u']
    return out
def kids(t, rel=None, c=None, lem=None):
    return [k for k in children(t) if (rel is None or k['rel'] in rel) and (c is None or case(k) in c) and (lem is None or k['lemma'] in lem)]
def phrase(t):
    """token + its attributive/article dependents (for highlighting a noun phrase)"""
    out = [t]
    for k in t['kids']:
        if k['rel'] in ('ATR',) and pos(k) in 'lanp' and pos(k) != 'v': out += phrase(k)
    return out
def is_inf(t): return pos(t) == 'v' and mood(t) == 'n'
def is_ptc(t): return pos(t) == 'v' and mood(t) == 'p'
TYGX = {'τυγχάνω', 'λανθάνω', 'φθάνω', 'διατελέω'}
PERC = {'οἶδα', 'ὁράω', 'αἰσθάνομαι', 'ἀκούω', 'πυνθάνομαι', 'γιγνώσκω', 'ἐπίσταμαι', 'μανθάνω', 'εὑρίσκω', 'ἐπιλανθάνομαι', 'μέμνημαι', 'ἀγγέλλω'}
ACCABS = {'ἔξεστι', 'ἔξειμι', 'δεῖ', 'πάρειμι', 'δοκέω', 'προσήκω', 'μέλω', 'πρέπω'}
NCI_GOV = {'δοκέω', 'φαίνω', 'λέγω', 'ἀγγέλλω', 'νομίζω', 'ὁμολογέω', 'ἡγέομαι', 'ὀφείλω'}
C = []
def add(t, code, members, govs=()):
    C.append((t, code, [m for m in members if m is not t], list(govs)))
for t in toks:
    if pos(t) != 'v': continue
    p = parent(t)
    pl = p['lemma'] if p else ''
    sub = kids(t, {'SBJ'})
    # --- infinitives
    if is_inf(t):
        art = [k for k in t['kids'] if k['lemma'] == 'ὁ' and k['pt'][6] == 'n' and k['pt'][2] == 's']
        if p is not None and p['lemma'] == 'πρίν':
            add(t, 'prin', [p] + [x for s in sub for x in phrase(s)], [p]); continue
        if p is not None and p['lemma'] == 'ὥστε':
            add(t, 'hoste_inf', [p] + [x for s in sub for x in phrase(s)], [p]); continue
        if art:
            add(t, 'art_inf', art + [x for s in sub for x in phrase(s)]); continue
        accs = [s for s in sub if case(s) == 'a']
        if accs:
            pn = kids(t, {'PNOM'}, 'a')
            add(t, 'aci', [x for s in accs for x in phrase(s)] + pn, [p] if p else []); continue
        pnn = kids(t, {'PNOM'}, 'n')
        personal = p is not None and (p['pt'][1] in '12' or p['pt'][2] in 'pd' or bool(kids(p, {'SBJ'}, 'n')))
        if p is not None and pos(p) == 'v' and mood(p) in 'ioms' and (pnn or (pl in NCI_GOV and personal and (pl == 'δοκέω' or p['pt'][5] == 'p'))):
            add(t, 'nci', pnn + [x for s in kids(p, {'SBJ'}, 'n') for x in phrase(s)], [p]); continue
        anx = [k for k in t['kids'] if k['lemma'] == 'ἄν']
        if anx: add(t, 'an_inf', anx, [p] if p else []); continue
        continue
    # --- participles
    if is_ptc(t):
        if p is not None and pl in TYGX and t['rel'] in ('ADV', 'ATV', 'AtvV', 'OBJ', 'PNOM'):
            add(t, 'tygx', [p], [p]); add(p, 'tygx', [t], [p]); continue
        if p is not None and pl in PERC and t['rel'] in ('OBJ', 'ATV', 'AtvV', 'OCOMP') :
            add(t, 'perc', [x for s in sub for x in phrase(s)], [p]); continue
        has_art = any(k['lemma'] == 'ὁ' for k in t['kids'])
        if case(t) == 'g' and t['rel'] in ('ADV',) and not has_art and (p is None or pos(p) == 'v'):
            gs = [s for s in sub if case(s) == 'g']
            add(t, 'gen_abs', [x for s in gs for x in phrase(s)] + kids(t, {'PNOM'}, 'g')); continue
        if case(t) == 'a' and t['rel'] == 'ADV' and t['lemma'] in ACCABS and t['pt'][2] == 's' and t['pt'][6] == 'n':
            add(t, 'acc_abs', []); continue
        if tense(t) == 'f' and t['rel'] in ('ADV', 'ATV', 'AtvV'):
            hos = [k for k in t['kids'] if k['lemma'] == 'ὡς']
            add(t, 'fut_ptc', hos, [p] if p else []); continue
        anx = [k for k in t['kids'] if k['lemma'] == 'ἄν']
        if anx: add(t, 'an_inf', anx, [p] if p else []); continue
        continue
    # --- finite verbs
    anx = [k for k in t['kids'] if k['lemma'] == 'ἄν']
    m = mood(t)
    if m == 'o':
        if anx: add(t, 'pot_opt', anx); continue
        if p is not None and p['rel'] == 'AuxC' or (p is not None and pos(p) in 'c'):
            cj = p['lemma']; gov = parent(p)
            if cj in ('ἵνα', 'ὅπως') or (cj == 'ὡς' and gov is not None and gov['lemma'] not in ('λέγω', 'εἶπον', 'φημί', 'ἀγγέλλω', 'διαβάλλω', 'ἀποκρίνομαι', 'οἶδα', 'νομίζω')):
                code = 'final_opt' if cj in ('ἵνα', 'ὅπως') else None
                if code: add(t, code, [p], [gov] if gov else []); continue
            if cj in ('ἐπεί', 'ἐπειδή', 'ὅτε', 'ὁπότε', 'ὁπόσος', 'ὅστις'):
                add(t, 'iter_opt', [p], [gov] if gov else []); continue
            SAY = {'λέγω', 'εἶπον', 'φημί', 'ἀγγέλλω', 'ἀπαγγέλλω', 'διαβάλλω', 'ἀποκρίνομαι', 'οἶδα', 'ἀκούω', 'νομίζω', 'αἰσθάνομαι', 'πυνθάνομαι', 'γιγνώσκω', 'ὁράω', 'δηλόω', 'ἐρωτάω', 'ὑπισχνέομαι', 'ἐπίσταμαι', 'ὀμνύω', 'οἴομαι', 'κηρύττω', 'ἐπιδείκνυμι', 'ἐννοέω', 'θαυμάζω'}
            if cj == 'ὅτι' or (cj == 'ὡς' and (gov is None or gov['lemma'] in SAY)):
                add(t, 'obl_opt', [p], [gov] if gov else []); continue
            if cj == 'ὡς':
                add(t, 'final_opt', [p], [gov] if gov else []); continue
            if cj == 'εἰ':
                add(t, 'ei_opt', [p], [gov] if gov else []); continue
        i0 = toks.index(t)
        near = [x for x in toks[max(0, i0 - 6):i0 + 3] if x['lemma'] == 'ἄν']
        if near and not any(pos(x) == 'v' and mood(x) in 'ios' for x in toks[toks.index(near[0]) + 1:i0] if x is not t):
            add(t, 'pot_opt', near[:1]); continue
        wish = [k for k in t['kids'] if k['lemma'] in ('εἴθε',)] or [x for x in toks[max(0, i0 - 4):i0] if x['lemma'] == 'εἴθε']
        if wish: add(t, 'wish_opt', wish); continue
        continue
    if m == 'i' and anx and tense(t) in 'ial':
        add(t, 'unreal', anx); continue
    if m == 'i' and p is not None and p['lemma'] == 'ὥστε':
        add(t, 'hoste_ind', [p]); continue
# ---- align to W
data = json.load(open(dataf))
W = data['W']
idx = {}; wi = 0
words = [t for t in toks if pos(t) not in 'u' and t['form'] not in ('', '·', ',', '.', ';')]
for t in words:
    f = base(t['form'])
    for j in range(wi, min(wi + 6, len(W))):
        if base(W[j][0]) == f:
            idx[t['id']] = j; wi = j + 1; break
miss = sum(1 for t in words if t['id'] not in idx)
out = []
seen = set()
for t, code, mem, gov in C:
    if t['id'] not in idx: continue
    i = idx[t['id']]
    if (i, code) in seen: continue
    seen.add((i, code))
    out.append([i, code, sorted({idx[m['id']] for m in mem if m and m['id'] in idx}), sorted({idx[g['id']] for g in gov if g and g['id'] in idx})])
data['C'] = sorted(out)
json.dump(data, open(dataf, 'w'), ensure_ascii=False, separators=(',', ':'))
import collections
print(dataf, 'aligned', len(idx), 'of', len(words), 'miss', miss, collections.Counter(c[1] for c in out))
