from pathlib import Path
from datetime import datetime
import re, shutil, html

ROOT = Path(__file__).resolve().parent
BRAND = "HOMECARE METRO"

SERVICE_NAMES = {
    "move-in-cleaning":"입주청소",
    "aircon-repair":"에어컨수리",
    "aircon-install":"에어컨설치",
    "aircon-cleaning":"에어컨청소",
    "used-aircon-buy":"중고에어컨매입",
    "leak-detection":"누수탐지",
    "wall-leak":"벽누수",
    "boiler-leak":"보일러누수",
    "bathroom-leak":"화장실누수",
    "drain-clog":"하수구막힘",
    "toilet-clog":"변기막힘",
    "sink-clog":"세면대막힘",
    "commercial-hood-cleaning":"업소용주방후드청소",
}

SERVICE_DESC = {
    "move-in-cleaning":"공간별 오염 상태와 청소 범위, 확인 순서를 안내합니다.",
    "aircon-repair":"냉방 불량·소음·누수·작동 이상 등 에어컨 점검 정보를 안내합니다.",
    "aircon-install":"실내외기 위치와 배관·배수 환경 등 설치 전 확인사항을 안내합니다.",
    "aircon-cleaning":"필터·열교환기·송풍부 등 에어컨 내부 청소 확인사항을 안내합니다.",
    "used-aircon-buy":"제품 상태와 설치·철거 환경 등 중고에어컨 매입 확인사항을 안내합니다.",
    "leak-detection":"벽·천장·바닥과 배관 주변의 누수 흔적 및 점검 정보를 안내합니다.",
    "wall-leak":"벽면 습기·변색·물자국 등 벽누수 확인사항을 안내합니다.",
    "boiler-leak":"보일러와 난방배관 주변의 누수 증상과 확인사항을 안내합니다.",
    "bathroom-leak":"욕실 배관·기구·방수 구간의 누수 확인사항을 안내합니다.",
    "drain-clog":"배수 지연·역류·악취 등 하수구 막힘 확인사항을 안내합니다.",
    "toilet-clog":"변기 수위·배수 불량·반복 막힘 등 확인사항을 안내합니다.",
    "sink-clog":"세면대 배수구·트랩·연결 배관의 막힘 확인사항을 안내합니다.",
    "commercial-hood-cleaning":"후드·필터·덕트 주변 기름 오염과 청소 범위를 안내합니다.",
}

SERVICE_IMAGE = {
    "move-in-cleaning":"01-move-in-cleaning.jpg",
    "aircon-repair":"02-aircon-repair.jpg",
    "aircon-install":"03-aircon-install.jpg",
    "aircon-cleaning":"04-aircon-cleaning.jpg",
    "used-aircon-buy":"05-used-aircon-buy.jpg",
    "leak-detection":"06-leak-detection.jpg",
    "wall-leak":"07-wall-leak.jpg",
    "boiler-leak":"08-boiler-leak.jpg",
    "bathroom-leak":"09-bathroom-leak.jpg",
    "drain-clog":"10-drain-clog.jpg",
    "toilet-clog":"11-toilet-clog.jpg",
    "sink-clog":"12-sink-clog.jpg",
    "commercial-hood-cleaning":"13-commercial-hood-cleaning.jpg",
}

def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def get_h1(txt):
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", txt, re.I|re.S)
    return clean(m.group(1)) if m else ""

def replace_title(head, title):
    if re.search(r"<title>.*?</title>", head, re.I|re.S):
        return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.I|re.S)
    return head + f"\n<title>{title}</title>"

def replace_meta_desc(head, desc):
    pat = r'<meta[^>]+name=["\']description["\'][^>]*>'
    tag = f'<meta name="description" content="{desc}">'
    if re.search(pat, head, re.I):
        return re.sub(pat, tag, head, count=1, flags=re.I)
    return head + "\n" + tag

def upsert_property(head, prop, content):
    pat = rf'<meta[^>]+property=["\']{re.escape(prop)}["\'][^>]*>'
    tag = f'<meta property="{prop}" content="{content}">'
    if re.search(pat, head, re.I):
        return re.sub(pat, tag, head, count=1, flags=re.I)
    return head + "\n" + tag

pages = [ROOT / "index.html"]
pages += list((ROOT / "services").rglob("index.html"))
pages += list((ROOT / "regions").rglob("index.html"))
pages = sorted(set(pages))

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"_backup-before-seo-{stamp}"
BACKUP.mkdir()

updated = 0
service_pages = 0
region_pages = 0
main_pages = 0

for p in pages:
    txt = p.read_text(encoding="utf-8")
    rel = p.relative_to(ROOT)

    if "</head>" not in txt.lower():
        continue

    h1 = get_h1(txt)

    # ===== 메인 =====
    if p == ROOT / "index.html":
        title = "서울 경기 인천 홈케어 생활서비스 | HOMECARE METRO"
        desc = "서울·경기·인천의 입주청소, 에어컨, 누수, 배수, 주방관리 서비스를 지역별로 찾을 수 있는 홈케어 안내 사이트입니다."
        og_image = "assets/images/00-main-homecare.jpg"
        main_pages += 1

    # ===== 서비스 페이지 =====
    elif rel.parts[0] == "services":
        slug = rel.parts[1]
        service = SERVICE_NAMES.get(slug, "")
        extra = SERVICE_DESC.get(slug, "서비스 확인사항과 지역별 안내 정보를 제공합니다.")

        location = h1.replace(service, "").strip() if service else h1
        location = re.sub(r"\s+", " ", location).strip()

        if location:
            title = f"{location} {service} | {BRAND}"
            desc = f"{location} {service} 안내. {extra}"
        else:
            title = f"{service} 서울 경기 인천 지역 안내 | {BRAND}"
            desc = f"서울·경기·인천 {service} 안내. {extra}"

        depth = len(p.parent.relative_to(ROOT).parts)
        prefix = "../" * depth
        og_image = prefix + "assets/images/" + SERVICE_IMAGE[slug]
        service_pages += 1

    # ===== 지역 전용 페이지 =====
    else:
        location = h1 if h1 else "서울 경기 인천"
        title = f"{location} 홈케어 생활서비스 지역 안내 | {BRAND}"
        desc = f"{location}의 청소, 에어컨, 누수, 배수 등 생활서비스 지역 정보를 단계별로 확인할 수 있습니다."

        depth = len(p.parent.relative_to(ROOT).parts)
        prefix = "../" * depth
        og_image = prefix + "assets/images/00-main-homecare.jpg"
        region_pages += 1

    # 너무 긴 공백 정리
    title = re.sub(r"\s+", " ", title).strip()
    desc = re.sub(r"\s+", " ", desc).strip()

    # 백업
    bp = BACKUP / rel
    bp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, bp)

    # head/body 분리
    m = re.search(r"(?is)^(.*?</head>)(.*)$", txt)
    if not m:
        continue

    full_head = m.group(1)
    rest = m.group(2)

    # </head> 전 내용만 수정
    head_content = re.sub(r"(?is)</head>\s*$", "", full_head)

    head_content = replace_title(head_content, title)
    head_content = replace_meta_desc(head_content, desc)
    head_content = upsert_property(head_content, "og:title", title)
    head_content = upsert_property(head_content, "og:description", desc)
    head_content = upsert_property(head_content, "og:type", "website")
    head_content = upsert_property(head_content, "og:image", og_image)

    new_txt = head_content + "\n</head>" + rest
    p.write_text(new_txt, encoding="utf-8")
    updated += 1

print("=== SEO META APPLY ===")
print("TOTAL    =", len(pages))
print("UPDATED  =", updated)
print("MAIN     =", main_pages)
print("SERVICE  =", service_pages)
print("REGION   =", region_pages)
print("CANONICAL= SKIPPED (DOMAIN NOT SET)")
print("ROBOTS   = PRESERVED")
print("BACKUP   =", BACKUP)
