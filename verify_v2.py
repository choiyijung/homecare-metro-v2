from pathlib import Path
import json
root=Path(__file__).resolve().parent
f=root/'data'/'regions-full-20260720.json'
if not f.exists():
    raise SystemExit('먼저 build_full_regions.py를 실행하세요.')
rows=json.loads(f.read_text(encoding='utf-8'))
print('=== V2 VERIFY ===')
print('REGIONS =',len(rows))
for a in ('서울','경기','인천'):
    print(a,'=',sum(r['area']==a for r in rows))
for t in ('읍','면','동'):
    print(t,'=',sum(r['type']==t for r in rows))
print('HTML =',sum(1 for _ in root.rglob('index.html')))
print('DUPLICATE =',len(rows)-len({(r['area'],r['city'],r['gu'],r['town']) for r in rows}))
