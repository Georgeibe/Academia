"""Export a converted text (SQLite from build.py) to the website's JSON.

Usage: python3 export_site.py BOOK.db glosses_ru.tsv eng.json rus.json OUT.json [ID] [SCHEME]
(use - for a missing translation; SCHEME is 'stephanus' (17a, 17b ...) or 'section' (1.1, 1.2 ...))
"""
import sqlite3, json, re, sys, csv
db, ru_path, eng_path, rus_path, out = sys.argv[1:6]
TEXT_ID = sys.argv[6] if len(sys.argv) > 6 else 'apology'
SCHEME = sys.argv[7] if len(sys.argv) > 7 else 'stephanus'
c = sqlite3.connect(db)

RU = {r[0]: r[1] for r in csv.reader(open(ru_path, encoding='utf8'), delimiter='\t') if r and not r[0].startswith('#')}
ENG = json.load(open(eng_path, encoding='utf8')) if eng_path != '-' else {}
RUS = json.load(open(rus_path, encoding='utf8')) if rus_path != '-' else {}

POS_RU = {'noun': 'существительное', 'adjective': 'прилагательное', 'verb': 'глагол', 'adverb': 'наречие',
          'conjunction': 'союз', 'preposition': 'предлог', 'particle': 'частица', 'interjection': 'междометие',
          'definite article': 'артикль', 'personal pronoun': 'личное местоимение', 'demonstrative pronoun': 'указательное местоимение',
          'relative pronoun': 'относительное местоимение', 'interrogative pronoun': 'вопросительное местоимение',
          'indefinite pronoun': 'неопределённое местоимение', 'numeral': 'числительное'}
CASE = dict(N='им. п.', G='род. п.', D='дат. п.', A='вин. п.', V='зват. п.')
NUM = dict(S='ед. ч.', P='мн. ч.', D='дв. ч.')
GEN = dict(M='муж. р.', F='жен. р.', N='ср. р.', C='общ. р.')
TENSE = dict(P='настоящее время', I='имперфект', F='будущее время', A='аорист', X='перфект', Y='плюсквамперфект', Z='будущее совершенное')
TENSE_G = dict(P='настоящего времени', I='имперфекта', F='будущего времени', A='аориста', X='перфекта', Y='плюсквамперфекта', Z='будущего совершенного')
VOICE = dict(A='действительный залог', M='средний залог', P='страдательный залог', E='средне-страдательный залог')
VOICE_G = dict(A='действ. залога', M='сред. залога', P='страд. залога', E='средне-страд. залога')
MOOD = dict(I='изъявительное наклонение', S='сослагательное наклонение (конъюнктив)', O='желательное наклонение (оптатив)', D='повелительное наклонение')

def cng(s):
    out = []
    for ch, tab in zip(s, (CASE, NUM, GEN)):
        if ch in tab: out.append(tab[ch])
    return ' '.join(out)

def ru_parse(code, en):
    pre = ''
    m = re.match(r'crasis of (\S+) \+ (\S+) · (.*)', en)
    if m:
        pre = f'красис: {m.group(1)} + {m.group(2)} · '; en = m.group(3)
    if code.startswith('V') and len(code) > 3:
        vc = lambda v: 'E' if 'middle/passive' in en else v
        if code[1] in '123':
            per, tn, v, md, n = code[1:6]
            return pre + f'глагол: {TENSE[tn]}, {VOICE[vc(v)]}, {MOOD[md]}, {per}-е лицо {NUM[n]}'
        tn, v, md = code[1], code[2], code[3]
        if md == 'N':
            return pre + f'глагол: инфинитив {TENSE_G[tn]} {VOICE_G[vc(v)]}'
        return pre + f'глагол: причастие {TENSE_G[tn]} {VOICE_G[vc(v)]}, {cng(code[4:])}'.rstrip(', ')
    kind = en.split(':')[0].replace(' (comparative)', '').replace(' (superlative)', '').replace(' (indeclinable)', '')
    word = POS_RU.get(kind, kind)
    if 'numeral' in en: word = 'числительное'
    deg = ' (сравнительная степень)' if 'comparative' in en else ' (превосходная степень)' if 'superlative' in en else ''
    if ':' in en:
        tail = code[2:] if code.startswith('R') else code[1:]
        return pre + f'{word}: {cng(tail[:3])}{deg}'
    return pre + word + deg

P, Pi, W = [], {}, []
def pidx(code, en):
    k = (code, en)
    if k not in Pi:
        Pi[k] = len(P); P.append([en.strip(), ru_parse(code, en)])
    return Pi[k]

L, Li = [], {}
for lem, pos, disp, gl, cnt in c.execute('select lemma,pos,display,gloss,count from dictionary order by count desc'):
    Li[lem] = len(L)
    L.append([lem, disp, pos, gl.replace('<cr>', '\n'), RU.get(lem, '').replace('<cr>', '\n'), cnt])

for wid, w, lem, pt, pc in c.execute('select wordID,word,lemma,parsetxt,parsecode from entries order by wordID'):
    tense = mood = ''
    if pc.startswith('V') and len(pc) > 3:
        tense, mood = (pc[2], pc[4]) if pc[1] in '123' else (pc[1], pc[3])
    W.append([w, Li[lem], pidx(pc, pt), tense, mood])

pages = []
for (ch,) in c.execute('select distinct chapter from verses order by chapter'):
    secs = []
    for vs, text in c.execute('select verse,text from verses where chapter=? order by verse', (ch,)):
        secs.append([vs, text])
    pages.append([ch, secs])
# word id ranges per section, from the .grk-equivalent ordering: words are in text order
ids_by_sec = []
wi = 0
for ch, secs in pages:
    for s in secs:
        text = s[1]; ids = []; cur = 0
        while wi < len(W):
            j = text.find(W[wi][0], cur)
            if j < 0: break
            ids.append(wi + 1); cur = j + len(W[wi][0]); wi += 1
        s.append([ids[0], ids[-1]] if ids else [0, -1])
assert wi == len(W), (wi, len(W))

tr = {'en': {}, 'ru': {}}
for ch, secs in pages:
    for vs, text, rng in secs:
        key = f'{ch}{"abcde"[vs-1]}' if SCHEME == 'stephanus' else f'{ch}.{vs}'
        if key in ENG: tr['en'][key] = ENG[key]
        if key in RUS: tr['ru'][key] = RUS[key]

data = {'id': TEXT_ID, 'scheme': SCHEME, 'pages': pages, 'W': W, 'L': L, 'P': P, 'tr': tr}
json.dump(data, open(out, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('words', len(W), 'lemmas', len(L), 'parse forms', len(P), 'en sections', len(tr['en']), 'ru sections', len(tr['ru']))
