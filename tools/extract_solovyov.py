"""Extract M. S. Solovyov's Russian Apology (public domain; text as printed on plato.today,
from the 1990 'Mysl' reprint of the 1899-1903 edition), split by Stephanus sections.
Editorial headings and A. A. Takho-Godi's notes (still in copyright) are left out.
Usage: python3 extract_solovyov.py plato.today.pdf OUT.json"""
import pdfplumber, re, json, sys

pdf = pdfplumber.open(sys.argv[1])
lines, prev_last = [], None
for pn, p in enumerate(pdf.pages):
    words = p.extract_words(extra_attrs=['fontname'])
    rows, marks = {}, []
    for w in words:
        if 200 <= w['x0'] < 240:
            marks.append((w['top'], w['text'])); continue
        if w['x0'] < 240: continue
        key = next((k for k in rows if abs(k - w['top']) < 3), w['top'])
        rows.setdefault(key, []).append(w)
    ls = []
    for top in sorted(rows):
        ws = sorted(rows[top], key=lambda w: w['x0'])
        ls.append({'top': top, 'toks': [w['text'] for w in ws], 'bold': 'Bold' in ws[0]['fontname'], 'mark': None})
    if ls and prev_last and ls[0]['toks'] == prev_last: ls = ls[1:]   # line repeated across PDF pages
    if ls: prev_last = ls[-1]['toks']
    for top, m in marks:
        if ls: min(ls, key=lambda l: abs(l['top'] - (top - 3)))['mark'] = m
    for k, l in enumerate(ls):
        l['gap'] = (l['top'] - ls[k - 1]['top']) if k else 0
    lines += ls

# body: from the first line after the title to the translator credit
start = next(i for i, l in enumerate(lines) if l['mark'] == '17')
end = next(i for i, l in enumerate(lines) if ' '.join(l['toks']).startswith('Перевод М'))
lines = lines[start:end]
lines = [l for l in lines if not l['bold'] and not ' '.join(l['toks']).startswith(('* Все подзаголовки', 'издательские добавления'))]

# stray section letters printed inside the text (look-alike Cyrillic): (line text fragment, token) -> exact split point
STRAY = [('с выдавая', 'с'), ('от в кого', 'в'), ('за с обучение', 'с'), ('дела с справедливые', 'с'),
         ('поступать с иначе', 'с'), ('меня на в', 'в'), ('думал , с что', 'с'), ('ну в вот', 'в'),
         ('считая с себя', 'с'), ('не а всем', 'а')]
for i, l in enumerate(lines):
    s = ' '.join(l['toks'])
    for frag, tok in STRAY:
        if frag in s:
            j = frag.split().index(tok)
            k0 = next(k for k in range(len(l['toks'])) if ' '.join(l['toks'][k:k + len(frag.split())]) == frag)
            l['stray'] = k0 + j

# assign tokens to sections
secs, order, cur, page = {}, [], None, None
for i, l in enumerate(lines):
    split_at = 0
    if l['mark']:
        m = l['mark']
        if m.isdigit(): page, key = int(m), f'{m}a'
        else: key = f'{page}{m}'
        # use an exact stray letter on this or a neighbouring line when there is one
        for d in (0, -1, 1):
            if 0 <= i + d < len(lines) and 'stray' in lines[i + d]:
                if d == 0: split_at = l['stray']
                elif d == -1:
                    prev = lines[i - 1]; tail = prev['toks'][prev['stray'] + 1:]
                    secs[cur] = secs[cur][:len(secs[cur]) - len(tail)]; secs.setdefault(key, []).extend(tail)
                    del prev['stray']
                break
    toks = l['toks']
    if 'stray' in l and l['mark']:
        before, after = toks[:split_at], toks[split_at + 1:]
        del l['stray']
    elif 'stray' in l:   # stray belongs to the next line's marker
        before, after = toks[:l['stray']], toks[l['stray'] + 1:]
        if cur: secs[cur].extend(before + ['@@CUT@@'] + after)
        continue
    else:
        before, after = ([], toks) if l['mark'] else (toks, [])
    if cur and before: secs[cur].extend((['¶'] if l['gap'] > 25 else []) + before)
    if l['mark']:
        cur = key; order.append(key); secs.setdefault(cur, []).extend(after)
    elif cur and after: secs[cur].extend(after)
# resolve a stray that belongs to the following marker (case d == +1)
for k_i, k in enumerate(order):
    if '@@CUT@@' in secs[k]:
        c = secs[k].index('@@CUT@@'); nxt = order[k_i + 1]
        secs[nxt] = secs[k][c + 1:] + secs[nxt]; secs[k] = secs[k][:c]

def clean(toks):
    s = ' '.join(toks)
    s = re.sub(r'\[\s*\d+\s*\]', '', s)
    s = re.sub(r'\s+-\s+', '-', s)
    s = re.sub(r'\s+([,.;:!?)\]»…])', r'\1', s)
    s = re.sub(r'([(\[«])\s+', r'\1', s)
    out, q = [], 0
    for part in re.split(r'(")', s):
        if part == '"':
            q ^= 1; out.append('«' if q else '»')
        else: out.append(part)
    s = ''.join(out)
    s = re.sub(r'«\s+', '«', s); s = re.sub(r'\s+»', '»', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

res = {k: clean(secs[k]) for k in order}
json.dump(res, open(sys.argv[2], 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(res), 'sections', order[:3], order[-3:])

# The margin marks only give the line on which a section starts; move each break to the nearest
# sentence end (or clause end) within a few words, so sections don't stop mid-phrase.
def adjust(a, b):
    joined = a + ' ' + b; pos = len(a)
    def best(pat, win):
        cands = [m.end() for m in re.finditer(pat, joined) if abs(m.end() - pos) <= win]
        return min(cands, key=lambda c: abs(c - pos)) if cands else None
    c = best(r'[.!?;]»?(?=\s)', 90) or best(r'[:,–]\s?(?=\s)', 45)
    if c is None: return a, b
    return joined[:c].strip(), joined[c:].strip().lstrip('¶ ').strip()
keys = list(res)
for i in range(len(keys) - 1):
    res[keys[i]], res[keys[i + 1]] = adjust(res[keys[i]], res[keys[i + 1]])
res = {k: re.sub(r'\s+-\s+', '-', v.replace(' ¶ ', ' ').replace('¶', '')).strip() for k, v in res.items()}
json.dump(res, open(sys.argv[2], 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('adjusted')
