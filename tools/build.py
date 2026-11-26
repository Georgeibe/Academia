"""Convert a GLAUx text into Greek Study App (GNTSP) data.

Usage: python3 build.py GLAUX_XML BOOK_NAME OUT_DIR
Produces OUT_DIR/<BOOK>.db (SQLite, same tables as GNTSP.db for text data),
OUT_DIR/<BOOK>.grk / .lex / .leb (book files), and review TSVs.
Chapters = Stephanus pages, verses = section letters (a=1 ... e=5).
"""
import re, sys, json, sqlite3, unicodedata as ud, collections, html, os, csv

SRC, BOOK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
N = lambda x: ud.normalize('NFC', x)

def strip_acc(s):
    s = ud.normalize('NFD', s.lower())
    s = ''.join(ch for ch in s if not ud.combining(ch))
    return s.replace('ς', 'σ').replace('’', '').replace("'", '')

# ---------- read GLAUx ----------
x = open(SRC, encoding='utf8').read()
W = [dict(re.findall(r'(\w+)="([^"]*)"', w)) for w in re.findall(r'<word ([^>]*)/>', x)]
W = [w for w in W if 'artificial' not in w and w.get('form') and 'postag' in w]
# crasis: GLAUx gives the first element as its own token ending in '-' (e.g. 'κα-' + 'κἀγώ').
# Drop that token and note the crasis on the full word.
_W = []
for i, w in enumerate(W):
    if w['form'].endswith('-') and i + 1 < len(W):
        W[i + 1]['crasis'] = N(w['lemma'])
        continue
    _W.append(w)
W = _W
for w in W:
    w['joined'] = w['form'].startswith('-')
    w['form'] = N(w['form']).lstrip('-')
    w['lemma'] = N(re.sub(r'\d+$', '', w['lemma']))
    sec = w.get('div_stephanus_section') or ''
    m = re.match(r'(\d+)([a-e])', sec)
    if m:   # Plato: chapter = Stephanus page, verse = section letter
        w['ch'], w['vs'] = int(m.group(1)), 'abcde'.index(m.group(2)) + 1
    else:   # book.chapter.section (e.g. Xenophon): chapter = chapter, verse = section
        m = re.match(r'\d+\.(\d+)\.(\d+)', w.get('div_section', ''))
        w['ch'], w['vs'] = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    w['speech'] = w.get('div_speech', '')

# ---------- parsing ----------
CASE = dict(n='N', g='G', d='D', a='A', v='V')
CASEW = dict(N='nominative', G='genitive', D='dative', A='accusative', V='vocative')
NUM = dict(s='S', p='P', d='D')
NUMW = dict(S='singular', P='plural', D='dual')
GEN = dict(m='M', f='F', n='N', c='C')
GENW = dict(M='masculine', F='feminine', N='neuter', C='common')
TENSE = dict(p='P', i='I', f='F', a='A', r='X', l='Y', t='Z')
TENSEW = dict(P='present', I='imperfect', F='future', A='aorist', X='perfect', Y='pluperfect', Z='future perfect')
VOICE = dict(a='A', m='M', p='P', e='M')  # middle/passive coded as M, labelled in text
VOICEW = dict(A='active', M='middle', P='passive', E='middle/passive')
MOOD = dict(i='I', s='S', o='O', m='D', n='N', p='P')
MOODW = dict(I='indicative', S='subjunctive', O='optative', D='imperative', N='infinitive', P='participle')
# sort-order digits used by GNTSP
S_T = dict(P='1', I='2', F='3', A='4', X='5', Y='6', Z='5')
S_V = dict(A='1', M='2', P='3', E='2')
S_M = dict(I='1', S='2', O='3', D='4', N='5', P='6')
S_G = dict(M='1', F='2', N='3', C='1')
S_N = dict(S='1', P='2', D='2')
S_C = dict(N='1', G='2', D='3', A='4', V='5')
S_C2 = dict(N='1', V='2', A='3', G='4', D='5')

PERSONAL = {'ἐγώ', 'σύ', 'ἡμεῖς', 'ὑμεῖς', 'αὐτός', 'ἐμαυτοῦ', 'σεαυτοῦ', 'ἑαυτοῦ', 'ἀλλήλων', 'οὗ', 'σφεῖς', 'νώ', 'σφώ'}
DEMONS = {'οὗτος', 'ὅδε', 'ἐκεῖνος', 'τοιοῦτος', 'τοσοῦτος', 'τοιόσδε', 'τοσόσδε', 'τηλικοῦτος', 'κἀκεῖνος'}
RELAT = {'ὅς', 'ὅστις', 'οἷος', 'ὅσος', 'ὁπόσος', 'ὁποῖος', 'ὅσπερ', 'ὁστισοῦν', 'ὅστισπερ'}
INTERR = {'τίς', 'ποῖος', 'πόσος', 'πότερος', 'πηλίκος'}
INDEF = {'τις'}

def case_num_gen(t):
    c, n, g = CASE.get(t[7]), NUM.get(t[2]), GEN.get(t[6])
    return c, n, g

def nominal(prefix, word, t, pos_txt, degree=''):
    c, n, g = case_num_gen(t)
    if not c:
        return prefix, pos_txt, '', ''
    code = prefix + c + (n or '') + (g or '')
    txt = f"{pos_txt}: {CASEW[c]} {NUMW.get(n,'')} {GENW.get(g,'')}".rstrip()
    so = S_G.get(g, '') + S_N.get(n, '') + S_C[c]
    so2 = S_G.get(g, '') + S_N.get(n, '') + S_C2[c]
    deg = {'c': ('C', 'comparative'), 's': ('S', 'superlative')}.get(degree)
    if deg:
        code += deg[0]; txt += f' ({deg[1]})'
    return code, txt, so, so2

def parse(w):
    t = w['postag'].ljust(9, '-')
    p, lem = t[0], w['lemma']
    if p == 'v':
        tn, vc, md = TENSE.get(t[3]), VOICE.get(t[5]), MOOD.get(t[4])
        if not (tn and vc and md):
            return 'V', 'verb', 'verb', '', ''
        base = f"verb: {TENSEW[tn]} {'middle/passive' if t[5]=='e' else VOICEW[vc]}"
        if md == 'N':
            return 'V' + tn + vc + 'N', f"{base} infinitive", 'verb', S_T[tn] + S_V[vc] + '5', S_T[tn] + S_V[vc] + '5'
        if md == 'P':
            c, n, g = case_num_gen(t)
            code = 'V' + tn + vc + 'P' + (c or '') + (n or '') + (g or '')
            txt = f"{base} participle, {CASEW.get(c,'')} {NUMW.get(n,'')} {GENW.get(g,'')}".rstrip(', ')
            so = S_T[tn] + S_V[vc] + '6' + S_G.get(g, '') + S_N.get(n, '') + S_C.get(c, '')
            so2 = S_T[tn] + S_V[vc] + '6' + S_G.get(g, '') + S_N.get(n, '') + S_C2.get(c, '')
            return code, txt, 'verb', so, so2
        per, n = t[1], NUM.get(t[2], 'S')
        code = 'V' + per + tn + vc + md + n
        txt = f"{base} {MOODW[md]}, {dict(zip('123',['1st','2nd','3rd'])).get(per,'')} person {NUMW[n]}"
        so = S_T[tn] + S_V[vc] + S_M[md] + S_N[n] + per
        return code, txt, 'verb', so, so
    if p == 'n':
        return (*nominal('N', w, t, 'noun')[:2], 'noun', *nominal('N', w, t, 'noun')[2:])
    if p == 'a':
        r = nominal('A', w, t, 'adjective', t[8])
        return r[0], r[1], 'adjective', r[2], r[3]
    if p == 'l':
        r = nominal('RA', w, t, 'definite article')
        return r[0], r[1], 'definite article', r[2], r[3]
    if p == 'p':
        if lem in PERSONAL and lem not in ('αὐτός',) and t[1] in '12':
            c, n = CASE.get(t[7]), NUM.get(t[2])
            if c:
                return 'RP' + c + (n or ''), f"personal pronoun: {CASEW[c]} {NUMW.get(n,'')} ", 'personal pronoun', S_N.get(n, '') + S_C[c], S_N.get(n, '') + S_C2[c]
        kind = ('RP', 'personal pronoun') if lem in PERSONAL else ('RD', 'demonstrative pronoun') if lem in DEMONS else \
               ('RR', 'relative pronoun') if lem in RELAT else ('RI', 'interrogative pronoun') if lem in INTERR else \
               ('RN', 'indefinite pronoun') if lem in INDEF else None
        if kind is None:  # ἄλλος, οὐδείς, μηδείς ... are adjectives in GNTSP
            r = nominal('A', w, t, 'adjective')
            return r[0], r[1], 'adjective', r[2], r[3]
        r = nominal(kind[0], w, t, kind[1])
        return r[0], r[1], kind[1], r[2], r[3]
    if p == 'm':
        if CASE.get(t[7]):
            r = nominal('A', w, t, 'numeral')
            return r[0], r[1], 'adjective', r[2], r[3]
        return 'A', 'numeral (indeclinable)', 'adjective', '', ''
    if p == 'd':
        return ('DC', 'adverb (comparative)', 'adverb', '', '') if t[8] == 'c' else \
               ('DS', 'adverb (superlative)', 'adverb', '', '') if t[8] == 's' else ('D', 'adverb', 'adverb', '', '')
    if p in 'bc':
        return 'C', 'conjunction', 'conjunction', '', ''
    if p == 'r':
        return 'P', 'preposition', 'preposition', '', ''
    if p == 'g':
        return 'X', 'particle', 'particle', '', ''
    if p == 'i':
        return 'I', 'interjection', 'interjection', '', ''
    return 'X', 'particle', 'particle', '', ''

# variant lemmas of the same word -> one dictionary entry
LEMMAFIX = {'σταθμόν': 'σταθμός', 'ἄτεχνος': 'ἀτεχνῶς', 'προσδοκέω': 'προσδοκάω', 'πρόχειρον': 'πρόχειρος', 'ἢ': 'ἤ', 'μὲν': 'μέν', 'μη': 'μή', 'ὅπη': 'ὅπῃ', 'Ἀβροκόμας': 'Ἀβροκόμης',
            'Ταμῶς': 'Ταμώς', 'Ὀρόντας': 'Ὀρόντης', 'Μαρσύα': 'Μαρσύας', 'Συρηκόσιος': 'Συρακούσιος',
            'σκευόφορος': 'σκευοφόρος', 'προίημι': 'προΐημι', 'πλησίος': 'πλησίον', 'ἱππικόν': 'ἱππικός',
            'ἀντίον': 'ἀντίος', 'ὕστερον': 'ὕστερος', 'πότερον': 'πότερος', 'Πύλης': 'Πύλαι', 'μαχέομαι': 'μάχομαι',
            'σταθμόs': 'σταθμός', 'Κιλίκια': 'Κιλικία'}
for w in W:
    w['lemma'] = LEMMAFIX.get(w['lemma'], w['lemma'])
# known tagging fixes: lemma -> (pos letter, gender) for substantives tagged as adjectives
NOUNFIX = {'κατήγορος': 'm'}
# known GLAUx errors at word level: form -> (wrong lemma, right lemma, right postag or None)
FORMFIX = {
    'δοκῇ': ('δοκεύς', 'δοκέω', 'v3spsa---'),
    'ᾤμην': ('οἰμάω', 'οἴομαι', 'v1siie---'),
    'στῇ': ('στάζω', 'ἵστημι', 'v3sasa---'),
    'θεῖτο': ('θέω', 'τίθημι', 'v3saom---'),
    'δεῖ': ('δέω', 'δέω', 'v3spia---'),
    'παρέχω': ('παραχώννυμι', 'παρέχω', 'v1spia---'),
}
for w in W:
    f = FORMFIX.get(w['form'])
    if f and w['lemma'] == f[0]:
        w['lemma'] = f[1]
        if f[2]: w['postag'] = f[2]
for w in W:
    if w['lemma'] in NOUNFIX and w['postag'][0] == 'a':
        t = list(w['postag'].ljust(9, '-')); t[0] = 'n'; t[6] = NOUNFIX[w['lemma']]; t[8] = '-'
        w['postag'] = ''.join(t)
for w in W:
    if w['postag'][0] == 'u':
        w['punct'] = True
        continue
    w['code'], w['ptxt'], w['pos'], w['so'], w['so2'] = parse(w)
    if w.get('crasis'):
        w['ptxt'] = f"crasis of {w['crasis']} + {w['lemma']} · " + w['ptxt']

words = [w for w in W if not w.get('punct')]

# ---------- glosses ----------
gnt = sqlite3.connect(os.environ.get('GNTSP_DB', os.path.join(HERE, 'GNTSP.db')))  # from github.com/claypotfrog/GNTSP
NT = {N(r[0]): r for r in gnt.execute('select lemma,pos,display,gloss from dictionary')}
_lsj = os.path.join(HERE, 'lsj_index.json')
LSJ = {N(k): v for k, v in json.load(open(_lsj)).items()} if os.path.exists(_lsj) else {}
OVR = {}
ovr_path = os.path.join(HERE, 'glosses.tsv')
if os.path.exists(ovr_path):
    for row in csv.reader(open(ovr_path, encoding='utf8'), delimiter='\t'):
        if len(row) >= 3 and row[0] and not row[0].startswith('#'):
            OVR[N(row[0])] = (row[1], row[2])  # display, gloss

lemcount = collections.Counter(w['lemma'] for w in words)
lempos = {}
for w in words:
    lempos.setdefault(w['lemma'], collections.Counter())[w['pos']] += 1

dictionary = {}
review = []
for lem, cnt in lemcount.most_common():
    pos = lempos[lem].most_common(1)[0][0]
    src = ''
    if lem in OVR:
        display, gloss = OVR[lem]; src = 'manual'
        if pos == 'verb' and not gloss.startswith(('(', 'it ', 'I ')) and not display.startswith(('ἀπολογητέον',)):
            # match GNTSP style: verbs glossed in the 1st person ("I say")
            gloss = ('I am ' + gloss[3:]) if gloss.startswith('be ') else ('I ' + gloss)
    elif lem in NT:
        display, gloss = NT[lem][2], NT[lem][3]; src = 'GNTSP'
    elif lem in LSJ and LSJ[lem]['gloss']:
        e = LSJ[lem]
        display = lem + (', ' + ', '.join(e['itype']) if e['itype'] else '') + (', ' + e['gen'][0] if e['gen'] else '')
        gloss = e['gloss']; src = 'LSJ'
    else:
        display, gloss, src = lem, '', 'none'
    dictionary[lem] = (lem, pos, strip_acc(lem), display, gloss, cnt, '0')
    review.append((lem, pos, cnt, src, display, gloss))

with open(os.path.join(OUT, f'{BOOK}_gloss_review.tsv'), 'w', encoding='utf8') as f:
    f.write('lemma\tpos\tcount\tsource\tdisplay\tgloss\n')
    for r in review:
        f.write('\t'.join(map(str, r)) + '\n')

# ---------- database ----------
dbp = os.path.join(OUT, f'{BOOK}.db')
if os.path.exists(dbp):
    os.remove(dbp)
db = sqlite3.connect(dbp)
for name in ('entries', 'dictionary', 'verses', 'books', 'chapters', 'search'):
    sql = gnt.execute("select sql from sqlite_master where name=?", (name,)).fetchone()[0]
    db.execute(sql)
for name in ('entries_lemma_index', 'entries_word_index', 'entries_normword_index', 'search_lookup_index',
             'search_normword_index', 'dictionary_lookup_index'):
    db.execute(gnt.execute("select sql from sqlite_master where name=?", (name,)).fetchone()[0])

START = 1
for i, w in enumerate(words):
    w['id'] = START + i
    nw = w['form'].lower() if w['form'][:1].isupper() and w['pos'] != 'noun' else w['form']
    # normword: accent-normalized form (grave -> acute)
    w['norm'] = N(ud.normalize('NFD', w['form']).replace('̀', '́'))
    db.execute('insert into entries values (?,?,?,?,?,?,?,?)',
               (w['id'], w['ptxt'], w['code'], w['form'], w['norm'], w['lemma'], w['so'], w['so2']))
db.executemany('insert into dictionary values (?,?,?,?,?,?,?)', dictionary.values())
db.execute('insert into books values (?,?,?,?)', (1, BOOK, words[0]['id'], words[-1]['id']))
bych = collections.OrderedDict()
for w in words:
    bych.setdefault(w['ch'], []).append(w['id'])
for ch, ids in bych.items():
    db.execute('insert into chapters values (?,?,?,?)', (1, ch, ids[0], ids[-1]))
seen = set()
for w in words:
    k = (strip_acc(w['form']), w['lemma'], w['norm'])
    if k not in seen:
        seen.add(k); db.execute('insert into search values (?,?,?)', k)

# verses (with punctuation)
NOSPACE_BEFORE = set(',.;:·’)]»!?')
verses = collections.OrderedDict()
for w in W:
    if w['ch'] == 0:
        continue
    verses.setdefault((w['ch'], w['vs']), []).append(w)
for (ch, vs), ws in verses.items():
    text = ''
    for w in ws:
        f = w['form']
        if text and not w['joined'] and not (w.get('punct') and f[:1] in NOSPACE_BEFORE) and not text.endswith(('(', '«')):
            text += ' '
        text += f
    real = [w for w in ws if not w.get('punct')]
    db.execute('insert into verses values (?,?,?,?,?,?,?)', (1, ch, vs, text,
               ' ' + ' '.join(w['lemma'] for w in real) + ' ', ' ' + ' '.join(w['norm'] for w in real) + ' ',
               ' ' + ' '.join(w['code'] for w in real) + ' '))
db.commit()

# ---------- book files (.grk/.lex/.leb) ----------
def ent(s):
    return ''.join(c if ord(c) < 128 else f'&#{ord(c)};' for c in s)

def verb_wrap(w, s):
    c = w['code']
    if not c.startswith('V') or len(c) < 4:
        return s
    if c[1] in '123':
        per, tn, vc, md, n = c[1], c[2], c[3], c[4], c[5]
        pn = int(per) + (3 if n in 'PD' else 0)
        return f'<P{pn}><M{md}><V{vc if vc!="E" else "M"}><T{tn if tn!="Z" else "X"}>{s}</T{tn if tn!="Z" else "X"}></V{vc if vc!="E" else "M"}></M{md}></P{pn}>'
    tn, vc, md = c[1], c[2], c[3]
    V = vc if vc != 'E' else 'M'; T = tn if tn != 'Z' else 'X'
    return f'<V{V}><M{md}><T{T}>{s}</T{T}></M{md}></V{V}>'

STEPH = any(w.get('div_stephanus_section') for w in W)
lab = lambda vs: 'abcde'[vs - 1] if STEPH else str(vs)

def book_file(kind):
    out = []
    bypage = collections.OrderedDict()
    for (ch, vs), ws in verses.items():
        bypage.setdefault(ch, []).append((vs, ws))
    first = True
    for ch, vlist in bypage.items():
        meta = ' '.join(f'{ch}:{vs} ' + ' '.join(str(w['id']) for w in ws if not w.get('punct')) for vs, ws in vlist)
        spans = []
        for vs, ws in vlist:
            num = f'<b><font size="30" color="#969696">{ch}</font><font color="#969696">{lab(vs) if STEPH else ':' + lab(vs)}</font></b>' if vs == vlist[0][0] \
                else f'<b><font color="#969696">{lab(vs)}</font></b>'
            parts, cur = [], ''
            for w in ws:
                f = w['form'] if kind == 'grk' else (w['lemma'] if not w.get('punct') else w['form'])
                sep = '' if (not cur and not parts) or w['joined'] or (w.get('punct') and w['form'][:1] in NOSPACE_BEFORE) else ' '
                if kind == 'grk' and not w.get('punct') and w['code'].startswith('V'):
                    parts.append(cur + sep); cur = ''
                    parts.append(verb_wrap(w, ent(f)))
                    continue
                cur += sep + ent(f)
            parts.append(cur)
            if kind == 'grk':
                # split into spans at each verb, like GNTSP
                body = ''.join(parts)
                segs = re.split(r'(<P\d>.*?</P\d>|<V[AMP]><M[NP]>.*?</M[NP]></V[AMP]>)', body)
                html_s, buf = '', f'<span metadata="{ch}:{vs}">' + ('  ' if vs == vlist[0][0] else '') + num + ' '
                for sgm in segs:
                    buf += sgm
                    if sgm.startswith(('<P', '<V')):
                        html_s += buf + '</span>'; buf = f'<span metadata="{ch}:{vs}">'
                html_s += buf + '</span>'
                spans.append(html_s)
            else:
                spans.append(f'<span metadata="{ch}:{vs}">' + num + ' ' + ''.join(parts) + ' </span>')
        if kind == 'leb':
            out.append(f'<p spacebelow="5" metadata="{ch}:{vlist[0][0]}"><span metadata="{ch}:{vlist[0][0]}"> </span></p>')
        elif kind == 'grk':
            out.append(f'<p metadata="{meta}" spacebelow="5">' + ''.join(spans) + '</p>')
        else:
            out.append('<p> ' + ''.join(spans) + '</p> ')
    open(os.path.join(OUT, f'{BOOK}.{kind}'), 'w', encoding='utf8').write('\n'.join(out))

for k in ('grk', 'lex', 'leb'):
    book_file(k)

# ---------- summary ----------
src_count = collections.Counter(r[3] for r in review)
tok_src = collections.Counter()
for r in review:
    tok_src[r[3]] += r[2]
print(json.dumps({'words': len(words), 'lemmas': len(review), 'pages': len(bych), 'verses': len(verses),
                  'gloss_sources_lemmas': src_count, 'gloss_sources_tokens': tok_src,
                  'verbs': sum(1 for w in words if w['code'].startswith('V'))}, ensure_ascii=False, default=dict))
