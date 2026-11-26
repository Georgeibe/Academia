"""Take one book of a GLAUx text and replace its automatic lemmas and parsing with Vanessa Gorman's
hand-checked treebank wherever the two line up word for word.

Usage: python3 merge_gorman.py GLAUX.xml BOOK OUT.xml GORMAN1.xml [GORMAN2.xml ...]
Writes a GLAUx-style XML (only <word .../> lines) for that book."""
import re, sys, difflib, unicodedata as ud, html, collections

src, book, out, gfiles = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
attrs = lambda s: dict(re.findall(r'(\w+)="([^"]*)"', s))
def key(f):
    f = ud.normalize('NFD', ud.normalize('NFC', f).lower()).replace('̀', '́')
    return ud.normalize('NFC', f).replace('’', "'").replace('ʼ', "'").strip('-')

x = open(src, encoding='utf8').read()
G = [attrs(w) for w in re.findall(r'<word ([^>]*)/>', x)]
G = [w for w in G if w.get('div_book') == book and w.get('form') and 'artificial' not in w and 'postag' in w]

T = []
for f in gfiles:
    for w in re.findall(r'<word ([^>]*)/>', open(f, encoding='utf8').read()):
        a = attrs(w)
        if a.get('form') and a.get('postag') and not a.get('artificial') and a['form'] != '[0]':
            T.append(a)

a, b = [key(w['form']) for w in G], [key(w['form']) for w in T]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
changed = matched = 0
diffs = collections.Counter()
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal': continue
    for i, j in zip(range(i1, i2), range(j1, j2)):
        g, t = G[i], T[j]
        lem = ud.normalize('NFC', re.sub(r'\d+$', '', t.get('lemma', ''))) or g['lemma']
        g['lemma'] = ud.normalize('NFC', g['lemma'])
        if (g['lemma'], g['postag']) != (lem, t['postag']):
            changed += 1
            if g['postag'][0] != t['postag'][0]: diffs['part of speech'] += 1
            elif g['lemma'] != lem: diffs['lemma'] += 1
            else: diffs['parsing'] += 1
        g['lemma'], g['postag'] = lem, t['postag']
        g['source'] = 'gorman'
        matched += 1

with open(out, 'w', encoding='utf8') as f:
    f.write('<words>\n')
    for w in G:
        f.write('<word ' + ' '.join(f'{k}="{html.escape(v, quote=True)}"' for k, v in w.items()) + '/>\n')
    f.write('</words>\n')
print(f'GLAUx words {len(G)}, Gorman words {len(T)}, matched {matched}, corrected {changed}', dict(diffs))
