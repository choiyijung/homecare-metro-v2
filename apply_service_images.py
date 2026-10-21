from pathlib import Path
from datetime import datetime
import re, shutil

ROOT = Path(r"G:\homecare-metro-v1\homecare-metro-v2")
SERVICES = ROOT / "services"
IMG = ROOT / "assets" / "images"
CSS = ROOT / "assets" / "style.css"

IMAGES = {
    "move-in-cleaning": "01-move-in-cleaning.jpg",
    "aircon-repair": "02-aircon-repair.jpg",
    "aircon-install": "03-aircon-install.jpg",
    "aircon-cleaning": "04-aircon-cleaning.jpg",
    "used-aircon-buy": "05-used-aircon-buy.jpg",
    "leak-detection": "06-leak-detection.jpg",
    "wall-leak": "07-wall-leak.jpg",
    "boiler-leak": "08-boiler-leak.jpg",
    "bathroom-leak": "09-bathroom-leak.jpg",
    "drain-clog": "10-drain-clog.jpg",
    "toilet-clog": "11-toilet-clog.jpg",
    "sink-clog": "12-sink-clog.jpg",
    "commercial-hood-cleaning": "13-commercial-hood-cleaning.jpg",
}

# 이미지 13장 존재 확인
missing = [name for name in IMAGES.values() if not (IMG / name).exists()]

if missing:
    print("STOP - IMAGE MISSING")
    for x in missing:
        print(x)
    raise SystemExit

print("IMAGE FILES = 13 / PASS")

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"_backup-before-service-images-{stamp}"
BACKUP.mkdir()

updated = 0
already = 0
fail = []

for p in SERVICES.rglob("index.html"):

    rel = p.relative_to(SERVICES)
    parts = rel.parts

    if not parts:
        continue

    slug = parts[0]

    if slug not in IMAGES:
        continue

    txt = p.read_text(encoding="utf-8")

    if 'class="service-photo-card"' in txt:
        already += 1
        continue

    depth = len(p.parent.relative_to(ROOT).parts)
    prefix = "../" * depth
    img_src = f"{prefix}assets/images/{IMAGES[slug]}"

    photo = f'''
<div class="service-photo-card">
  <img src="{img_src}" alt="" loading="lazy">
</div>
'''

    old = txt

    # 서비스 루트
    if 'class="hs-namebox"' in txt:
        txt = re.sub(
            r'<div class="hs-namebox">.*?</div>',
            photo,
            txt,
            count=1,
            flags=re.S
        )

    # 광역 서비스 허브
    elif 'class="hr-info"' in txt:
        txt = re.sub(
            r'<aside class="hr-info">.*?</aside>',
            photo,
            txt,
            count=1,
            flags=re.S
        )

    # 시/구/군 중간허브
    elif 'class="lh-count"' in txt:
        txt = re.sub(
            r'<aside class="lh-count">.*?</aside>',
            photo,
            txt,
            count=1,
            flags=re.S
        )

    # 동/읍/면 상세
    elif 'class="hd-servicebox"' in txt:
        txt = re.sub(
            r'<aside class="hd-servicebox">.*?</aside>',
            photo,
            txt,
            count=1,
            flags=re.S
        )

    else:
        fail.append(str(p))
        continue

    if txt != old:
        backup = BACKUP / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, backup)

        p.write_text(txt, encoding="utf-8")
        updated += 1


css = CSS.read_text(encoding="utf-8")

marker = "HOMECARE SERVICE PHOTO V7"

if marker not in css:
    css += r'''

/* =====================================================
   HOMECARE SERVICE PHOTO V7
   ===================================================== */

.service-photo-card{
  width:100%;
  min-height:260px;
  height:100%;
  max-height:390px;
  border-radius:22px;
  overflow:hidden;
  background:#dfe7e5;
  box-shadow:0 24px 52px rgba(22,55,63,.17);
}

.service-photo-card img{
  display:block;
  width:100%;
  height:100%;
  min-height:260px;
  max-height:390px;
  object-fit:cover;
  object-position:center;
}

.hs-hero .service-photo-card{
  min-height:300px;
}

.hs-hero .service-photo-card img{
  min-height:300px;
}

.hr-hero .service-photo-card,
.lh-hero .service-photo-card{
  min-height:230px;
}

.hr-hero .service-photo-card img,
.lh-hero .service-photo-card img{
  min-height:230px;
}

.hd-hero .service-photo-card{
  min-height:270px;
}

.hd-hero .service-photo-card img{
  min-height:270px;
}

@media(max-width:900px){
  .service-photo-card,
  .service-photo-card img{
    min-height:240px;
    max-height:340px;
  }
}
'''

    CSS.write_text(css, encoding="utf-8")

print()
print("=== SERVICE IMAGE APPLY ===")
print("UPDATED =", updated)
print("ALREADY =", already)
print("FAIL    =", len(fail))
print("BACKUP  =", BACKUP)

if fail:
    print("\nFAIL SAMPLE")
    for x in fail[:20]:
        print(x)
