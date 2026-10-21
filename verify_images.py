from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parent

pages = [ROOT / "index.html"]
pages += list((ROOT / "services").rglob("*.html"))

broken = []
img_refs = 0

for p in pages:
    txt = p.read_text(encoding="utf-8")

    for src in re.findall(r'<img\b[^>]*src=["\']([^"\']+)["\']', txt, re.I):
        src = unquote(urlsplit(src).path)
        img_refs += 1

        if src.startswith("/"):
            target = ROOT / src.lstrip("/")
        else:
            target = (p.parent / src).resolve()

        if not target.exists():
            broken.append((str(p), src, str(target)))

images = list((ROOT / "assets" / "images").glob("*.*"))

print("=== IMAGE VERIFY ===")
print("IMAGE FILES =", len(images))
print("HTML IMG REFS =", img_refs)
print("BROKEN IMAGES =", len(broken))

if broken:
    print("\nBROKEN SAMPLE")
    for x in broken[:20]:
        print(x)

if len(broken) == 0:
    print("IMAGE VERIFY = PASS")
else:
    print("IMAGE VERIFY = CHECK REQUIRED")

