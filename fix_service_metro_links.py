from pathlib import Path

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")
SERVICES = ROOT / "services"

metros = ["seoul", "gyeonggi", "incheon"]

changed = 0
replace_count = 0

for service in SERVICES.iterdir():
    if not service.is_dir():
        continue

    for metro in metros:
        p = service / metro / "index.html"

        if not p.exists():
            continue

        txt = p.read_text(encoding="utf-8")
        old = txt

        n = txt.count('href="../../index.html"')

        txt = txt.replace(
            'href="../../index.html"',
            'href="../index.html"'
        )

        if txt != old:
            p.write_text(txt, encoding="utf-8")
            changed += 1
            replace_count += n

print("SERVICE METRO LINK FIX PASS")
print("FILES_CHANGED =", changed)
print("LINKS_FIXED =", replace_count)
