"""Extract H. N. Fowler's English Apology (Perseus, CC BY-SA) section by section.
Usage: python3 extract_fowler.py tlg0059.tlg002.perseus-eng2.xml OUT.json"""
import re, json, html, sys
s = open(sys.argv[1], encoding='utf8').read()
body = s[s.find('<body'):]
body = re.sub(r'<note.*?</note>', '', body, flags=re.S)
body = re.sub(r'<milestone[^>]*unit="section"[^>]*n="(\d+[a-e])"[^>]*/>', r'@@SEC \1@@', body)
body = re.sub(r'<milestone[^>]*unit="para"[^>]*/>', '@@P@@', body)
body = html.unescape(re.sub(r'<[^>]+>', ' ', body))
parts = re.split(r'@@SEC (\d+[a-e])@@', body)
sec = {}
for i in range(1, len(parts), 2):
    t = re.sub(r'\s+', ' ', parts[i + 1].replace('@@P@@', ' ¶ ')).strip()
    sec[parts[i]] = re.sub(r'(\S)\s+([,.;:!?])', r'\1\2', t)
json.dump(sec, open(sys.argv[2], 'w', encoding='utf8'), ensure_ascii=False)
print(len(sec), 'sections')
