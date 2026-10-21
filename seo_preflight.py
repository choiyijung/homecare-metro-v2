from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

pages = [ROOT / "index.html"]
pages += list((ROOT / "services").rglob("index.html"))
pages += list((ROOT / "regions").rglob("index.html"))
pages = sorted(set(pages))

title_missing = []
desc_missing = []
noindex = 0
indexable = 0
canonical = 0
og_title = 0
og_desc = 0

for p in pages:
    txt = p.read_text(encoding="utf-8", errors="ignore")
    head = txt.split("</head>", 1)[0]

    if not re.search(r"<title>.*?</title>", head, re.I | re.S):
        title_missing.append(p)

    if not re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']+["\']',
        head,
        re.I
    ):
        desc_missing.append(p)

    if re.search(r'noindex', head, re.I):
        noindex += 1
    else:
        indexable += 1

    if re.search(r'rel=["\']canonical["\']', head, re.I):
        canonical += 1

    if re.search(r'property=["\']og:title["\']', head, re.I):
        og_title += 1

    if re.search(r'property=["\']og:description["\']', head, re.I):
        og_desc += 1

print("=== SEO PREFLIGHT ===")
print("HTML             =", len(pages))
print("INDEXABLE        =", indexable)
print("NOINDEX          =", noindex)
print("TITLE_MISSING    =", len(title_missing))
print("DESC_MISSING     =", len(desc_missing))
print("CANONICAL        =", canonical)
print("OG_TITLE         =", og_title)
print("OG_DESCRIPTION   =", og_desc)
