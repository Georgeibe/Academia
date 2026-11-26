"""Extract a Perseus translation divided into book/chapter/section <div>s (e.g. Brownson's Anabasis).
Usage: python3 extract_perseus_sections.py TRANSLATION.xml BOOK OUT.json
Keys are "chapter.section" (e.g. "1.1"); notes are dropped."""
import re, json, html, sys
from lxml import etree
src, book, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = etree.parse(src)
ns = {'t': 'http://www.tei-c.org/ns/1.0'}
res = {}
for b in t.iterfind('.//t:div[@subtype="book"]', ns):
    if b.get('n') != book: continue
    for ch in b.iterfind('t:div[@subtype="chapter"]', ns):
        for sec in ch.iterfind('t:div[@subtype="section"]', ns):
            for n in list(sec.iterfind('.//t:note', ns)):
                parent, prev = n.getparent(), n.getprevious()
                if n.tail:   # keep the text that follows the note
                    if prev is not None: prev.tail = (prev.tail or '') + n.tail
                    else: parent.text = (parent.text or '') + n.tail
                parent.remove(n)
            s = ' '.join(sec.itertext())
            s = re.sub(r'\s+', ' ', s).strip()
            s = re.sub(r'\s+([,.;:!?])', r'\1', s)
            res[f"{ch.get('n')}.{sec.get('n')}"] = s
json.dump(res, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(res), 'sections')
