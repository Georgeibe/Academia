#!/usr/bin/env python3
"""Inject Georgian glosses (tools/gloss_ka.json) and Russian gloss corrections
(tools/gloss_ru_fixes.json) into the lemma tables of data/*.json.

L entry: [lemma, display, pos, glossEN, glossRU, count, glossKA]
Run after export_site.py:  python3 tools/apply_glosses.py
"""
import json, glob, os
here = os.path.dirname(os.path.abspath(__file__))
ka = json.load(open(os.path.join(here, 'gloss_ka.json'), encoding='utf-8'))
ru = json.load(open(os.path.join(here, 'gloss_ru_fixes.json'), encoding='utf-8'))
for f in sorted(glob.glob(os.path.join(here, '..', 'data', '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    if 'L' not in d:
        continue
    nka = nru = 0
    for l in d['L']:
        if l[0] in ru and l[4] != ru[l[0]]:
            l[4] = ru[l[0]]; nru += 1
        g = ka.get(l[0], '')
        if len(l) < 7:
            l.append(g)
        else:
            l[6] = g
        nka += bool(g)
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(os.path.basename(f), 'lemmas', len(d['L']), 'ka', nka, 'ru fixed', nru)


# ---------- Georgian parse labels: P entry [en, ru] -> [en, ru, ka] ----------
POS = {'verb': 'ზმნა', 'noun': 'არსებითი სახელი', 'adjective': 'ზედსართავი სახელი', 'adverb': 'ზმნიზედა',
       'preposition': 'წინდებული', 'conjunction': 'კავშირი', 'particle': 'ნაწილაკი', 'interjection': 'შორისდებული',
       'definite article': 'არტიკლი', 'numeral': 'რიცხვითი სახელი', 'personal pronoun': 'პირის ნაცვალსახელი',
       'demonstrative pronoun': 'ჩვენებითი ნაცვალსახელი', 'relative pronoun': 'მიმართებითი ნაცვალსახელი',
       'interrogative pronoun': 'კითხვითი ნაცვალსახელი', 'indefinite pronoun': 'განუსაზღვრელობითი ნაცვალსახელი'}
CASE = {'nominative': 'სახ. ბრ.', 'genitive': 'ნათ. ბრ.', 'dative': 'მიც. ბრ.', 'accusative': 'ბრალდ. ბრ.', 'vocative': 'წოდ. ბრ.'}
NUM = {'singular': 'მხ. რ.', 'plural': 'მრ. რ.', 'dual (dualis)': 'ორობითი რიცხვი (dualis)'}
GEN = {'masculine': 'მამრ. სქ.', 'feminine': 'მდედრ. სქ.', 'neuter': 'საშ. სქ.', 'common': 'საერთო სქ.'}
DEG = {'(comparative)': '(შედარებითი ხარისხი)', '(superlative)': '(აღმატებითი ხარისხი)', '(indeclinable)': '(უბრუნველი)'}
TENSE = {'present': 'აწმყო', 'imperfect': 'იმპერფექტი', 'future': 'მყოფადი', 'aorist': 'აორისტი', 'perfect': 'პერფექტი',
         'pluperfect': 'პლუსკვამპერფექტი', 'future perfect': 'მყოფად-პერფექტი'}
VOICE = {'active': 'მოქმედებითი გვარი', 'middle': 'საშუალი გვარი', 'passive': 'ვნებითი გვარი', 'middle/passive': 'საშუალ-ვნებითი გვარი'}
MOOD = {'indicative': 'თხრობითი კილო', 'subjunctive': 'კავშირებითი კილო (კონიუნქტივი)', 'optative': 'ნატვრითი კილო (ოპტატივი)',
        'imperative': 'ბრძანებითი კილო', 'infinitive': 'ინფინიტივი', 'participle': 'მიმღეობა'}
PERS = {'1st': 'I პირი', '2nd': 'II პირი', '3rd': 'III პირი'}


def nominal(s):
    """'accusative dual (dualis) masculine (comparative)' -> Georgian"""
    out, s = [], ' ' + s + ' '
    for src in (CASE, NUM, GEN, DEG):
        for k, v in src.items():
            if ' ' + k + ' ' in s:
                out.append((s.index(' ' + k + ' '), v)); s = s.replace(' ' + k + ' ', ' ' * (len(k) + 2), 1)
    if s.strip():
        raise ValueError('unparsed nominal: ' + s)
    return ' '.join(v for _, v in sorted(out))


def verbal(s):
    """'future perfect middle infinitive' -> Georgian"""
    w = s.split()
    vi = next(i for i, x in enumerate(w) if x in VOICE)
    return f"{TENSE[' '.join(w[:vi])]}, {VOICE[w[vi]]}, {MOOD[' '.join(w[vi + 1:])]}"


def person(s):
    w = s.split()
    return PERS[w[0]] + ' ' + NUM[' '.join(w[2:])]


def parse_ka(en):
    if en.startswith('crasis of '):
        a, b = en[len('crasis of '):].split(' · ', 1)
        return 'კრაზისი: ' + a + ' · ' + parse_ka(b)
    if ':' not in en:
        for k, v in DEG.items():
            if en.endswith(' ' + k):
                return POS[en[:-len(k) - 1]] + ' ' + v
        return POS[en]
    head, rest = en.split(': ', 1)
    parts = [x.strip() for x in rest.split(', ')]
    if head == 'verb':
        out = [verbal(parts[0])]
        for x in parts[1:]:
            out.append(person(x) if x[:3] in ('1st', '2nd', '3rd') else nominal(x))
        return POS[head] + ': ' + ', '.join(out)
    return POS[head] + ': ' + ', '.join(nominal(x) for x in parts)


for f in sorted(glob.glob(os.path.join(here, '..', 'data', '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    if 'P' not in d:
        continue
    for p in d['P']:
        g = parse_ka(p[0])
        if len(p) < 3:
            p.append(g)
        else:
            p[2] = g
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(os.path.basename(f), 'parses', len(d['P']))
