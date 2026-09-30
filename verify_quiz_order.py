from pathlib import Path
import re, sys

root = Path(r'c:\Users\David\Desktop\Dorfquiz Ammerndorf')
expected_keys = ['buergerhaus','dreschhaus','kirchturm','muehle','ortsarrest','marktplatz','rathaus','feuerwehr','bahnhofsplatz']
expected_titles = [
    'Das Bürgerhaus',
    'Das Dreschmaschinenhaus',
    'Die Sankt Peter und Paul Kirche',
    'Die Ammerndorfer Mühle',
    'Der Ortsarrest / das alte Feuerwehrhaus',
    'Der Marktplatz',
    'Das Rathaus',
    'Die Freiwillige Feuerwehr Ammerndorf',
    'Der Bahnhofsplatz',
]

ok = True

for name in ['dorfquiz/index.html', 'index-qr-only.html']:
    text = (root / name).read_text(encoding='utf-8')
    match = re.search(r"const STATION_KEYS = \[(.*?)\];", text, re.S)
    if not match:
        print(f'MISSING_KEYS:{name}')
        ok = False
        continue
    actual = re.findall(r"'([^']+)'", match.group(1))
    print(f'{name} keys: {",".join(actual)}')
    if actual != expected_keys:
        print(f'KEY_ORDER_MISMATCH:{name}')
        ok = False

for i, title in enumerate(expected_titles, start=1):
    page = root / f'station-qr-{i}.html'
    text = page.read_text(encoding='utf-8')
    if title not in text:
        print(f'TITLE_MISMATCH:{page.name}')
        ok = False
    if f'key={expected_keys[i - 1]}' not in text:
        print(f'KEY_MISMATCH:{page.name}')
        ok = False

if (root / 'station-qr-10.html').exists() or (root / 'dorfquiz' / 'station-qr-10.html').exists():
    print('EXTRA_STATION_FILE_PRESENT')
    ok = False

print('verification=passed' if ok else 'verification=failed')
raise SystemExit(0 if ok else 1)
