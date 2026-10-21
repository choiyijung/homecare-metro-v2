from pathlib import Path
from datetime import datetime
import re, shutil, html

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")
SERVICES_ROOT = ROOT / "services"
CSS = ROOT / "assets" / "style.css"

SERVICES = {
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

METROS = {
    "seoul":"서울",
    "gyeonggi":"경기",
    "incheon":"인천",
}

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"_backup-local-hubs-{stamp}"
BACKUP.mkdir()

def clean_text(x):
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x)
    return re.sub(r"\s+", " ", x).strip()

def direct_children(page):
    items = []
    txt = page.read_text(encoding="utf-8")

    for href, inside in re.findall(
        r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        txt,
        flags=re.I | re.S
    ):
        href = html.unescape(href.strip())

        if not re.fullmatch(r'[^/#?]+/index\.html', href, re.I):
            continue

        target = page.parent / href
        if not target.exists():
            continue

        label = clean_text(inside)
        if not label:
            continue

        if not any(a == href for a,b in items):
            items.append((href,label))

    return items

def get_heading(txt):
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", txt, re.I|re.S)
    if m:
        return clean_text(m.group(1))
    return ""

candidates = []

for p in SERVICES_ROOT.rglob("index.html"):
    rel = p.relative_to(SERVICES_ROOT)
    parts = rel.parts

    # 서비스 루트 / 서울·경기·인천 허브 제외
    if len(parts) <= 3:
        continue

    children = direct_children(p)

    # 직접 하위 지역 페이지가 실제 존재하는 페이지만 중간 허브
    if children:
        candidates.append((p, children))

print("INTERMEDIATE HUBS FOUND =", len(candidates))

updated = 0
failed = []

for p, children in candidates:
    rel = p.relative_to(SERVICES_ROOT)
    parts = rel.parts

    service_slug = parts[0]
    metro_slug = parts[1]

    service_name = SERVICES.get(service_slug, service_slug)
    metro_name = METROS.get(metro_slug, metro_slug)

    old = p.read_text(encoding="utf-8")
    old_heading = get_heading(old)

    # 예: "서울 강남구 에어컨수리"에서 지역명만 추출
    region_name = old_heading
    region_name = region_name.replace(service_name, "").strip()

    if region_name.startswith(metro_name + " "):
        region_name = region_name[len(metro_name)+1:].strip()

    if not region_name:
        region_name = parts[-2]

    # 현재 페이지에서 루트까지 상대경로 계산
    depth = len(p.parent.relative_to(ROOT).parts)
    root_prefix = "../" * depth

    # 서비스 metro 허브 상대경로
    # 현재 페이지 기준 부모 단계 계산
    metro_dir = ROOT / "services" / service_slug / metro_slug
    metro_href = Path(
        *[".."] * len(p.parent.relative_to(metro_dir).parts)
    )

    metro_back = "../" * len(p.parent.relative_to(metro_dir).parts)
    metro_back = metro_back + "index.html"

    cards = []
    for i,(href,label) in enumerate(children,1):
        cards.append(f'''
<a class="lh-card" href="{href}">
    <span>{i:02d}</span>
    <strong>{label}</strong>
    <p>{service_name} 지역 안내</p>
    <b>상세 지역 보기 →</b>
</a>''')

    cards_html = "\n".join(cards)

    backup_name = "__".join(parts[:-1]) + ".html"
    shutil.copy2(p, BACKUP / backup_name)

    body = f'''
<body class="lh-body">

<header class="lh-header">
  <a class="lh-logo" href="{root_prefix}index.html">HOMECARE <b>METRO</b></a>
  <nav>
    <a href="{root_prefix}index.html#services">서비스</a>
    <a href="{root_prefix}index.html#regions">지역</a>
  </nav>
</header>

<div class="lh-breadcrumb">
  <a href="{root_prefix}index.html">HOME</a>
  <span>/</span>
  <a href="{metro_back}">{metro_name}</a>
  <span>/</span>
  <b>{region_name}</b>
</div>

<main>

<section class="lh-hero">
  <div>
    <span class="lh-kicker">LOCAL SERVICE DIRECTORY</span>
    <h1>{metro_name} {region_name}<br><em>{service_name}</em></h1>
    <p>
      {metro_name} {region_name}에서 {service_name} 정보를 찾기 위해
      하위 지역을 세분화해 안내합니다.
    </p>
  </div>

  <aside class="lh-count">
    <span>LOCAL AREA</span>
    <strong>{len(children)}</strong>
    <p>하위 지역</p>
  </aside>
</section>

<section class="lh-directory">
  <div class="lh-title">
    <div>
      <span>01 · LOCAL DIRECTORY</span>
      <h2>동·읍·면 지역 선택</h2>
    </div>
    <p>
      원하는 세부 지역을 선택하면
      {service_name} 상세 안내 페이지로 이동합니다.
    </p>
  </div>

  <div class="lh-grid">
    {cards_html}
  </div>
</section>

<section class="lh-info">
  <div>
    <span>02 · LOCAL GUIDE</span>
    <h2>{region_name}에서도<br>지역별 환경은 다를 수 있습니다.</h2>
  </div>
  <p>
    주거 형태, 상가 여부, 건물 구조와 설비 상태에 따라
    {service_name} 확인 항목이 달라질 수 있습니다.
    실제 위치에 맞는 하위 지역 페이지에서 필요한 내용을 확인할 수 있습니다.
  </p>
</section>

</main>

<footer class="lh-footer">
  <strong>HOMECARE METRO</strong>
  <span>{metro_name} {region_name} · {service_name}</span>
</footer>

</body>
'''

    if not re.search(r"<body\b", old, re.I):
        failed.append(str(p))
        continue

    new = re.sub(
        r"<body\b[^>]*>.*?</body>",
        body,
        old,
        count=1,
        flags=re.I|re.S
    )

    p.write_text(new, encoding="utf-8")
    updated += 1


css = CSS.read_text(encoding="utf-8")

if "HOMECARE LOCAL HUB V5" not in css:
    css += r'''

/* =====================================================
   HOMECARE LOCAL HUB V5
   ===================================================== */

.lh-body{
 margin:0;background:#f5f4ef;color:#17212b;
 font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;
}
.lh-body *{box-sizing:border-box}
.lh-body a{text-decoration:none;color:inherit}

.lh-header{
 min-height:76px;background:#fff;
 border-top:7px solid #15313b;
 border-bottom:1px solid #ddd;
 padding:0 max(4.5vw,32px);
 display:flex;align-items:center;justify-content:space-between
}
.lh-logo{font-weight:900;font-size:18px}
.lh-logo b{color:#bd7515}
.lh-header nav{display:flex;gap:28px;font-size:14px;font-weight:800}

.lh-breadcrumb{
 padding:18px max(4.5vw,32px);
 background:#fafafa;border-bottom:1px solid #e8e8e4;
 color:#71808a;font-size:13px
}
.lh-breadcrumb span{margin:0 7px}

.lh-hero{
 min-height:410px;
 padding:72px max(4.5vw,32px);
 display:grid;
 grid-template-columns:1fr 290px;
 gap:80px;
 align-items:center;
 background:
 radial-gradient(circle at 86% 18%,rgba(32,112,115,.13),transparent 26%),
 linear-gradient(120deg,#f7f0e3,#f7f5ef 55%,#ebf2f0)
}

.lh-kicker,.lh-title span,.lh-info span{
 display:block;color:#ad6810;font-size:11px;
 font-weight:900;letter-spacing:2px
}

.lh-hero h1{
 margin:21px 0 0;
 font-size:clamp(48px,5vw,76px);
 line-height:1.06;letter-spacing:-4px
}
.lh-hero h1 em{font-style:normal;color:#176269}

.lh-hero>div>p{
 max-width:720px;margin:27px 0 0;
 color:#606a71;font-size:16px;line-height:1.8
}

.lh-count{
 min-height:220px;padding:30px;
 border-radius:20px;background:#173f47;color:#fff;
 display:flex;flex-direction:column;justify-content:flex-end;
 box-shadow:0 22px 48px rgba(24,55,63,.17)
}
.lh-count span{font-size:10px;color:#dfb469;font-weight:900;letter-spacing:2px}
.lh-count strong{font-size:52px;margin-top:30px}
.lh-count p{margin:2px 0 0;color:#bfd0d2;font-size:13px}

.lh-directory{
 max-width:1320px;margin:auto;padding:90px 34px
}

.lh-title{
 display:flex;justify-content:space-between;
 align-items:flex-end;gap:60px;margin-bottom:38px
}
.lh-title h2{
 margin:14px 0 0;font-size:37px;letter-spacing:-2px
}
.lh-title>p{
 max-width:430px;margin:0;color:#697178;line-height:1.75
}

.lh-grid{
 display:grid;
 grid-template-columns:repeat(4,1fr);
 gap:13px
}

.lh-card{
 min-height:165px;padding:23px;
 background:#fff;border:1px solid #dddcd7;
 border-radius:14px;
 display:flex;flex-direction:column;
 transition:.2s ease
}

.lh-card:hover{
 transform:translateY(-4px);
 border-color:#1d5b61;
 box-shadow:0 14px 28px rgba(25,54,61,.09)
}

.lh-card>span{
 color:#b46c0d;font-size:10px;font-weight:900
}
.lh-card strong{
 margin-top:22px;font-size:19px;letter-spacing:-.7px
}
.lh-card p{
 margin:8px 0 0;color:#81878c;font-size:11px
}
.lh-card b{
 margin-top:auto;padding-top:18px;
 color:#285f66;font-size:11px
}

.lh-info{
 max-width:1252px;
 margin:0 auto 95px;
 background:#ebe3d5;
 border-radius:18px;
 padding:52px;
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:80px
}

.lh-info h2{
 margin:15px 0 0;
 font-size:31px;line-height:1.35;
 letter-spacing:-1.8px
}

.lh-info>p{
 margin:19px 0 0;color:#626b70;
 line-height:1.9;font-size:14px
}

.lh-footer{
 padding:38px max(4.5vw,32px);
 background:#102027;color:#fff;
 display:flex;justify-content:space-between
}
.lh-footer span{color:#9cafb4;font-size:12px}

@media(max-width:1000px){
 .lh-hero{grid-template-columns:1fr}
 .lh-grid{grid-template-columns:repeat(3,1fr)}
}

@media(max-width:720px){
 .lh-header{padding:0 20px}
 .lh-header nav{gap:14px;font-size:12px}
 .lh-breadcrumb{padding-left:20px}
 .lh-hero{padding:58px 20px}
 .lh-hero h1{font-size:45px;letter-spacing:-2.5px}
 .lh-directory{padding:70px 20px}
 .lh-title{display:block}
 .lh-title>p{margin-top:18px}
 .lh-grid{grid-template-columns:repeat(2,1fr)}
 .lh-info{
   margin:0 20px 70px;padding:30px;
   grid-template-columns:1fr;gap:20px
 }
 .lh-footer{display:block}
 .lh-footer span{display:block;margin-top:8px}
}

@media(max-width:480px){
 .lh-grid{grid-template-columns:1fr}
}
'''
    CSS.write_text(css, encoding="utf-8")

print()
print("=== LOCAL HUB UPDATE ===")
print("FOUND   =", len(candidates))
print("UPDATED =", updated)
print("FAILED  =", len(failed))
print("BACKUP  =", BACKUP)

for x in failed[:20]:
    print("FAIL:", x)
