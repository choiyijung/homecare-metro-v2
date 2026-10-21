from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")

# 실제 운영 페이지들만 검사
pages = []

if (ROOT / "index.html").exists():
    pages.append(ROOT / "index.html")

for base in [ROOT / "services", ROOT / "regions"]:
    if base.exists():
        pages.extend(base.rglob("*.html"))

pages = sorted(set(pages))

broken = []
body_fail = []
head_fail = []
charset_fail = []
css_fail = []

checked_links = 0

skip_prefix = (
    "http://", "https://", "mailto:", "tel:", "sms:",
    "javascript:", "data:"
)

for p in pages:
    try:
        txt = p.read_text(encoding="utf-8")
    except Exception as e:
        body_fail.append((str(p), "READ_ERROR", str(e)))
        continue

    low = txt.lower()

    if low.count("<body") != 1 or low.count("</body>") != 1:
        body_fail.append((str(p), "BODY_COUNT", low.count("<body")))

    if len(re.findall(r"<head(?:\s|>)", low, re.I)) != 1 or len(re.findall(r"</head\s*>", low, re.I)) != 1:
        head_fail.append((str(p), "HEAD_COUNT"))

    if 'charset="utf-8"' not in low and "charset=utf-8" not in low:
        charset_fail.append(str(p))

    if "assets/style.css" not in low and "style.css" not in low:
        css_fail.append(str(p))

    refs = re.findall(
        r'''(?:href|src)\s*=\s*["']([^"']+)["']''',
        txt,
        flags=re.I
    )

    for ref in refs:
        ref = ref.strip()

        if (
            not ref
            or ref.startswith("#")
            or ref.lower().startswith(skip_prefix)
        ):
            continue

        u = urlsplit(ref)
        pathpart = unquote(u.path)

        if not pathpart:
            continue

        checked_links += 1

        if pathpart.startswith("/"):
            target = ROOT / pathpart.lstrip("/")
        else:
            target = p.parent / pathpart

        target = target.resolve()

        # 디렉터리 링크면 index.html 확인
        if pathpart.endswith("/") or target.is_dir():
            target = target / "index.html"

        if not target.exists():
            broken.append((str(p), ref, str(target)))

print("=== FULL SITE VERIFY ===")
print("ACTIVE_HTML       =", len(pages))
print("CHECKED_REFS      =", checked_links)
print("BROKEN_LINKS      =", len(broken))
print("BODY_FAIL         =", len(body_fail))
print("HEAD_FAIL         =", len(head_fail))
print("CHARSET_FAIL      =", len(charset_fail))
print("CSS_LINK_FAIL     =", len(css_fail))

print()
print("=== DETAIL VERIFY ===")

detail_pages = []
robots_fail = []

for service in (ROOT / "services").iterdir():
    if not service.is_dir():
        continue

    for metro in ["seoul", "gyeonggi", "incheon"]:
        base = service / metro
        if not base.exists():
            continue

        for p in base.rglob("index.html"):
            txt = p.read_text(encoding="utf-8")

            # 하위 index 링크가 없으면 최종 읍면동 상세페이지
            direct_child = False

            for href in re.findall(
                r'''href\s*=\s*["']([^"']+)["']''',
                txt,
                flags=re.I
            ):
                href = href.strip()

                # 실제 바로 아래 자식 폴더만 인정
                # ../index.html 같은 상위 이동 링크는 제외
                if (
                    not href.startswith(".")
                    and re.fullmatch(r'[^/#?]+/index\.html', href)
                ):
                    if (p.parent / href).exists():
                        direct_child = True
                        break

            if not direct_child:
                detail_pages.append(p)

                head = txt.split("</head>", 1)[0].lower()
                if "noindex" not in head or "follow" not in head:
                    robots_fail.append(str(p))

print("DETAIL_PAGES      =", len(detail_pages))
print("DETAIL_ROBOTS_FAIL=", len(robots_fail))

if broken:
    print("\n--- BROKEN SAMPLE ---")
    for x in broken[:20]:
        print(x)

if body_fail:
    print("\n--- BODY FAIL SAMPLE ---")
    for x in body_fail[:20]:
        print(x)

if head_fail:
    print("\n--- HEAD FAIL SAMPLE ---")
    for x in head_fail[:20]:
        print(x)

print()
if (
    len(pages) == 12460
    and len(detail_pages) == 10335
    and len(broken) == 0
    and len(body_fail) == 0
    and len(head_fail) == 0
    and len(charset_fail) == 0
    and len(css_fail) == 0
    and len(robots_fail) == 0
):
    print("FINAL STRUCTURE VERIFY = PASS")
else:
    print("FINAL STRUCTURE VERIFY = CHECK REQUIRED")


