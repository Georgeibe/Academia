"""Extract Levan Berdzenishvili's Georgian translation of the Apology by Stephanus section.

Used with the translator's permission (26 Nov 2026).
Usage: python3 extract_georgian.py SOURCE.pdf OUT.json
"""
import json, re, sys
import pdfplumber

src, out = sys.argv[1], sys.argv[2]
text = '\n'.join((p.extract_text() or '') for p in pdfplumber.open(src).pages)
end = 'გარდა ღმრთისა.'
text = text[:text.index(end) + len(end)]
text = text[text.index('[17a]'):]

DROP = {'პირველი ნაწილი', 'სოკრატეს დაცვა', 'მეორე ნაწილი', 'მესამე ნაწილი',
        'სასამართლომ სოკრატეს სიკვდილი მიუსაჯა.'}
lines = []
for l in text.split('\n'):
    s = l.strip()
    if re.fullmatch(r'\d+', s) or s in DROP or re.match(r'(გამამტყუნებელი|სასიკვდილო) განაჩენის შემდეგ', s):
        continue
    lines.append(s)
text = ''
for s in lines:
    if text.endswith('-') and not text.endswith(' -'):
        text += s
    else:
        text += (' ' if text else '') + s

# footnote numbers glued to words or punctuation
text = re.sub(r'(?<=[ა-ჿ.,;:!?»“”—)])\d+', '', text)
text = re.sub(r'\s+', ' ', text)

parts = re.split(r'\s*\[(\d+[a-e])\]\s*', text)
keys, chunks = parts[1::2], parts[2::2]

# move a break to the nearest sentence end if one is close by
SENT = re.compile(r'[.!?;](?:\s|$)')
for i in range(1, len(chunks)):
    prev, cur = chunks[i - 1], chunks[i]
    m = SENT.search(cur)
    if m and m.end() <= 80:
        chunks[i - 1] = prev + ' ' + cur[:m.end()].strip()
        chunks[i] = cur[m.end():].strip()
        continue
    ends = list(SENT.finditer(prev))
    if ends and len(prev) - ends[-1].end() <= 80 and ends[-1].end() > 0:
        tail = prev[ends[-1].end():].strip()
        chunks[i - 1] = prev[:ends[-1].end()].strip()
        chunks[i] = (tail + ' ' + cur).strip()

res = {k: c.strip() for k, c in zip(keys, chunks)}
json.dump(res, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(res), 'sections')
