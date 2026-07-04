from pathlib import Path
import re
text = Path('index-v3.html').read_text(encoding='utf-8')
keys = set(re.findall(r'data-key="([^"]+)"', text)) | set(re.findall(r'data-placeholder="([^"]+)"', text)) | set(re.findall(r'data-aria="([^"]+)"', text))
start = text.index('const translations = {')
brace = 0
for i,ch in enumerate(text[start:], start):
    if ch == '{':
        brace += 1
    elif ch == '}':
        brace -= 1
    if brace == 0:
        end = i+1
        break
block = text[start:end]
seg_re = re.compile(r'(en|ar)\s*:\s*\{(.*?)\}(?=\s*,\s*(?:en|ar)\s*:\s*\{|\s*\})', re.S)
sections = {m.group(1): m.group(2) for m in seg_re.finditer(block)}
for lang in ['en','ar']:
    data = {}
    if lang in sections:
        data = {m.group(1): m.group(2) for m in re.finditer(r"([A-Za-z0-9_]+)\s*:\s*'((?:[^'\\]|\\.)*)'", sections[lang])}
    print(f"--- {lang} ---")
    print('entries', len(data))
    if lang == 'en':
        bad = [k for k,v in data.items() if re.search('[\u0600-\u06FF]', v)]
        print('en with arabic text', bad)
    else:
        bad = [k for k,v in data.items() if re.search('[A-Za-z]', v) and not re.search('[\u0600-\u06FF]', v)]
        print('ar with english-only', bad)
    missing = [k for k in sorted(keys) if k not in data]
    print('missing keys', missing)
    print()
print('all keys count', len(keys))
PYPATH = Path('index-v3.html')
