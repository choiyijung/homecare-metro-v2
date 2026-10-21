from pathlib import Path
from datetime import datetime
import re, shutil, html

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")

SERVICES = {
    "move-in-cleaning": "입주청소",
    "aircon-repair": "에어컨수리",
    "aircon-install": "에어컨설치",
    "aircon-cleaning": "에어컨청소",
    "used-aircon-buy": "중고에어컨매입",
    "leak-detection": "누수탐지",
    "wall-leak": "벽누수",
    "boiler-leak": "보일러누수",
    "bathroom-leak": "화장실누수",
    "drain-clog": "하수구막힘",
    "toilet-clog": "변기막힘",
    "sink-clog": "세면대막힘",
    "commercial-hood-cleaning": "업소용주방후드청소",
}

METROS = {
    "seoul": ("서울", "SEOUL", "구"),
    "gyeonggi": ("경기", "GYEONGGI", "시·군"),
    "incheon": ("인천", "INCHEON", "구·군"),
}

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"_backup-service-metro-{stamp}"
BACKUP.mkdir()

updated = 0
fail = []

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()

for service_slug, service_name in SERVICES.items():
    for metro_slug, (metro_name, metro_en, unit_name) in METROS.items():

        p = ROOT / "services" / service_slug / metro_slug / "index.html"

        if not p.exists():
            fail.append(f"MISSING {p}")
            continue

        txt = p.read_text(encoding="utf-8")

        # 현재 페이지의 실제 하위 지역 링크만 추출
        found = re.findall(
            r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            txt,
            flags=re.I | re.S
        )

        items = []

        for href, inner in found:
            href = html.unescape(href.strip())

            # 종로구/index.html, suwon/index.html 같은 바로 아래 지역만 사용
            if not re.fullmatch(r'[^/#?]+/index\.html', href, re.I):
                continue

            label = strip_tags(inner)
            label = html.unescape(label)

            if not label:
                continue

            # 기존 카드 안에 설명까지 들어간 경우 첫 핵심명만 정리
            label = re.sub(r'\s+', ' ', label).strip()

            # 같은 href 중복 제거
            if not any(x[0] == href for x in items):
                items.append((href, label))

        if not items:
            fail.append(f"NO CHILD LINKS {p}")
            continue

        backup_name = f"{service_slug}__{metro_slug}.html"
        shutil.copy2(p, BACKUP / backup_name)

        cards = []

        for i, (href, label) in enumerate(items, 1):
            cards.append(f'''
<a class="hr-card" href="{href}">
    <span>{i:02d}</span>
    <strong>{label}</strong>
    <b>지역 보기 →</b>
</a>''')

        cards_html = "\n".join(cards)

        body = f'''
<body class="hr-body">

<header class="hr-header">
    <a class="hr-logo" href="../../../index.html">HOMECARE <b>METRO</b></a>
    <nav>
        <a href="../../index.html">서비스</a>
        <a href="../../../index.html#regions">지역</a>
    </nav>
</header>

<div class="hr-breadcrumb">
    <a href="../../../index.html">HOME</a>
    <span>/</span>
    <a href="../../index.html">{service_name}</a>
    <span>/</span>
    <b>{metro_name}</b>
</div>

<main>

<section class="hr-hero">
    <div>
        <span class="hr-kicker">SERVICE × REGION</span>
        <h1>{metro_name}<br><em>{service_name}</em></h1>
        <p>
            {metro_name}에서 {service_name} 정보를 찾을 수 있도록
            {unit_name} 단위부터 세부 지역까지 나누어 안내합니다.
        </p>
    </div>

    <aside class="hr-info">
        <span>{metro_en}</span>
        <strong>{len(items)}</strong>
        <p>{unit_name} 지역</p>
    </aside>
</section>

<section class="hr-directory">
    <div class="hr-title">
        <div>
            <span>01 · AREA DIRECTORY</span>
            <h2>{metro_name} 지역 선택</h2>
        </div>
        <p>
            원하는 {unit_name}을 선택하면 다음 단계의
            동·읍·면 지역으로 이동합니다.
        </p>
    </div>

    <div class="hr-grid">
        {cards_html}
    </div>
</section>

<section class="hr-bottom">
    <div>
        <span>HOMECARE METRO</span>
        <h2>{service_name} 정보를<br>지역별로 나눠 확인하세요.</h2>
    </div>
    <p>
        같은 서비스라도 주거 형태와 건물 환경, 설비 상태에 따라
        확인해야 할 내용이 달라질 수 있습니다.
        세부 지역을 선택하면 해당 지역 안내로 이어집니다.
    </p>
</section>

</main>

<footer class="hr-footer">
    <strong>HOMECARE METRO</strong>
    <span>{metro_name} · {service_name}</span>
</footer>

</body>
'''

        if not re.search(r"<body\b", txt, re.I):
            fail.append(f"BODY NOT FOUND {p}")
            continue

        txt = re.sub(
            r"<body\b[^>]*>.*?</body>",
            body,
            txt,
            count=1,
            flags=re.I | re.S
        )

        p.write_text(txt, encoding="utf-8")
        updated += 1


CSS = ROOT / "assets" / "style.css"
css = CSS.read_text(encoding="utf-8")

marker = "HOMECARE SERVICE METRO HUB V4"

if marker not in css:

    css += r'''

/* =====================================================
   HOMECARE SERVICE METRO HUB V4
   ===================================================== */

.hr-body{
 margin:0;
 background:#f5f4ef;
 color:#17212b;
 font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;
}
.hr-body *{box-sizing:border-box}
.hr-body a{text-decoration:none;color:inherit}

.hr-header{
 min-height:76px;
 background:#fff;
 border-top:7px solid #15323d;
 border-bottom:1px solid #deded9;
 display:flex;
 align-items:center;
 justify-content:space-between;
 padding:0 max(4.5vw,32px);
}

.hr-logo{
 font-weight:900;
 font-size:18px;
}
.hr-logo b{color:#bd7515}

.hr-header nav{
 display:flex;
 gap:28px;
 font-size:14px;
 font-weight:800;
}

.hr-breadcrumb{
 padding:18px max(4.5vw,32px);
 background:#fafafa;
 border-bottom:1px solid #ecebe7;
 color:#71808a;
 font-size:13px;
}

.hr-breadcrumb span{margin:0 7px}

.hr-hero{
 min-height:430px;
 padding:76px max(4.5vw,32px);
 background:
 radial-gradient(circle at 84% 20%,rgba(35,113,113,.14),transparent 25%),
 linear-gradient(120deg,#f6efe3,#f7f5ef 58%,#edf3f1);
 display:grid;
 grid-template-columns:1fr 310px;
 gap:80px;
 align-items:center;
}

.hr-hero>div{
 max-width:900px;
}

.hr-kicker{
 display:block;
 color:#ad6811;
 font-size:11px;
 font-weight:900;
 letter-spacing:2.4px;
 margin-bottom:22px;
}

.hr-hero h1{
 margin:0;
 font-size:clamp(54px,5.3vw,82px);
 line-height:1.02;
 letter-spacing:-4px;
}

.hr-hero h1 em{
 color:#17636a;
 font-style:normal;
}

.hr-hero>div>p{
 margin:28px 0 0;
 max-width:720px;
 color:#606a71;
 font-size:16px;
 line-height:1.85;
}

.hr-info{
 min-height:225px;
 padding:30px;
 border-radius:20px;
 background:#173f47;
 color:#fff;
 display:flex;
 flex-direction:column;
 justify-content:flex-end;
 box-shadow:0 22px 50px rgba(22,56,64,.16);
}

.hr-info span{
 color:#dfb66a;
 font-size:10px;
 font-weight:900;
 letter-spacing:2px;
}

.hr-info strong{
 margin-top:30px;
 font-size:52px;
 letter-spacing:-2px;
}

.hr-info p{
 margin:3px 0 0;
 color:#c1d0d2;
 font-size:13px;
}

.hr-directory{
 max-width:1320px;
 margin:auto;
 padding:95px 34px;
}

.hr-title{
 display:flex;
 justify-content:space-between;
 align-items:flex-end;
 gap:60px;
 margin-bottom:40px;
}

.hr-title span,
.hr-bottom span{
 color:#ad6810;
 font-size:11px;
 font-weight:900;
 letter-spacing:2px;
}

.hr-title h2{
 margin:14px 0 0;
 font-size:38px;
 letter-spacing:-2px;
}

.hr-title>p{
 max-width:430px;
 margin:0;
 color:#697178;
 line-height:1.75;
}

.hr-grid{
 display:grid;
 grid-template-columns:repeat(4,1fr);
 gap:13px;
}

.hr-card{
 min-height:154px;
 padding:22px;
 background:#fff;
 border:1px solid #deddd8;
 border-radius:14px;
 display:flex;
 flex-direction:column;
 transition:.2s ease;
}

.hr-card:hover{
 transform:translateY(-4px);
 border-color:#1c5960;
 box-shadow:0 14px 28px rgba(26,55,61,.09);
}

.hr-card span{
 color:#b36c0e;
 font-size:10px;
 font-weight:900;
}

.hr-card strong{
 margin-top:25px;
 font-size:18px;
 letter-spacing:-.6px;
}

.hr-card b{
 margin-top:auto;
 padding-top:20px;
 color:#32646a;
 font-size:11px;
}

.hr-bottom{
 max-width:1252px;
 margin:0 auto 100px;
 padding:55px;
 background:#e9e2d4;
 border-radius:18px;
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:80px;
}

.hr-bottom h2{
 margin:15px 0 0;
 font-size:31px;
 line-height:1.3;
 letter-spacing:-1.7px;
}

.hr-bottom>p{
 margin:20px 0 0;
 color:#626b71;
 font-size:14px;
 line-height:1.9;
}

.hr-footer{
 background:#102027;
 color:#fff;
 padding:38px max(4.5vw,32px);
 display:flex;
 justify-content:space-between;
}

.hr-footer span{
 color:#9cafb4;
 font-size:12px;
}

@media(max-width:1000px){
 .hr-hero{grid-template-columns:1fr}
 .hr-grid{grid-template-columns:repeat(3,1fr)}
}

@media(max-width:720px){
 .hr-header{padding:0 20px}
 .hr-header nav{gap:15px;font-size:12px}
 .hr-breadcrumb{padding-left:20px}
 .hr-hero{padding:58px 20px}
 .hr-hero h1{font-size:47px;letter-spacing:-2.7px}
 .hr-directory{padding:70px 20px}
 .hr-title{display:block}
 .hr-title>p{margin-top:18px}
 .hr-grid{grid-template-columns:repeat(2,1fr)}
 .hr-bottom{
   margin:0 20px 70px;
   padding:30px;
   grid-template-columns:1fr;
   gap:20px;
 }
 .hr-footer{display:block}
 .hr-footer span{display:block;margin-top:8px}
}

@media(max-width:480px){
 .hr-grid{grid-template-columns:1fr}
}
'''

    CSS.write_text(css, encoding="utf-8")

print("SERVICE METRO HUB UPDATE PASS")
print("UPDATED =", updated)
print("EXPECTED = 39")
print("FAIL =", len(fail))
for x in fail[:20]:
    print(x)
print("BACKUP =", BACKUP)
