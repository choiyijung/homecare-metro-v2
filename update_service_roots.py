from pathlib import Path
from datetime import datetime
import shutil, re

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")
CSS = ROOT / "assets" / "style.css"

services = {
"move-in-cleaning": {
    "name":"입주청소","cat":"청소",
    "headline":"새 공간을 사용하기 전,\n먼저 확인해야 할 청소",
    "intro":"바닥·창틀·주방·욕실 등 공간별 오염 상태를 살펴보고 필요한 정리 범위를 확인합니다.",
    "issues":["창틀과 틈새 먼지","주방 기름·생활 오염","욕실 물때와 잔여 오염"],
    "steps":["공간 상태 확인","청소 범위 구분","구역별 작업 안내"]
},
"aircon-repair": {
    "name":"에어컨수리","cat":"에어컨",
    "headline":"냉방이 약하거나\n작동이 이상할 때",
    "intro":"냉방 불량·작동 중단·소음·누수 등 나타나는 증상을 기준으로 점검 범위를 확인합니다.",
    "issues":["찬바람이 약한 경우","작동 중 소음 발생","실내기 주변 물 떨어짐"],
    "steps":["증상 확인","기기 상태 점검","필요 작업 구분"]
},
"aircon-install": {
    "name":"에어컨설치","cat":"에어컨",
    "headline":"설치 위치와 배관 환경부터\n먼저 확인",
    "intro":"신규 설치와 이전 설치 모두 실내외기 위치, 배관 경로, 설치 공간 조건을 먼저 확인합니다.",
    "issues":["실내기 설치 위치","실외기 공간 조건","배관 이동 경로"],
    "steps":["설치환경 확인","기기·배관 점검","설치 범위 안내"]
},
"aircon-cleaning": {
    "name":"에어컨청소","cat":"에어컨",
    "headline":"필터만이 아니라\n내부 오염까지 확인",
    "intro":"필터·열교환기·송풍부 등 사용 과정에서 오염이 쌓이는 부분을 기준으로 청소 범위를 살펴봅니다.",
    "issues":["필터 먼지 증가","냄새 발생","송풍부 오염"],
    "steps":["기기 상태 확인","청소 구간 구분","세척 범위 안내"]
},
"used-aircon-buy": {
    "name":"중고에어컨매입","cat":"에어컨",
    "headline":"제품 상태와 철거 환경을\n함께 확인",
    "intro":"제품 형태·사용 상태·설치 위치와 철거 환경 등을 기준으로 중고 에어컨 확인 절차를 안내합니다.",
    "issues":["제품 형태와 연식","정상 작동 여부","철거 가능 환경"],
    "steps":["제품 정보 확인","설치상태 확인","매입·철거 범위 안내"]
},
"leak-detection": {
    "name":"누수탐지","cat":"누수",
    "headline":"보이는 물보다\n원인이 시작된 곳을 확인",
    "intro":"습기·물자국·수도 사용량 변화 등 주변 흔적을 바탕으로 누수 가능 구간을 좁혀갑니다.",
    "issues":["천장·벽면 물자국","수도 사용량 변화","바닥 주변 습기"],
    "steps":["누수 흔적 확인","배관 구간 점검","원인 범위 구분"]
},
"wall-leak": {
    "name":"벽누수","cat":"누수",
    "headline":"벽면 얼룩과 습기,\n원인을 구분해서 확인",
    "intro":"도배 변색·곰팡이·벽면 습기 등으로 나타나는 현상을 살펴 누수 가능 범위를 확인합니다.",
    "issues":["도배지 변색","벽면 습기","반복되는 곰팡이"],
    "steps":["벽면 상태 확인","주변 배관 확인","누수 범위 안내"]
},
"boiler-leak": {
    "name":"보일러누수","cat":"누수",
    "headline":"보일러와 난방배관 주변의\n누수 징후 확인",
    "intro":"보일러 본체와 연결부, 난방 배관 주변에서 나타나는 물기나 압력 변화를 기준으로 확인합니다.",
    "issues":["보일러 주변 물기","압력 변화","난방배관 누수 흔적"],
    "steps":["보일러 상태 확인","연결 배관 점검","누수 위치 구분"]
},
"bathroom-leak": {
    "name":"화장실누수","cat":"누수",
    "headline":"욕실 바닥과 배관,\n방수 구간을 나눠 확인",
    "intro":"욕실에서 발생하는 누수는 급·배수 배관과 바닥 방수 등 여러 가능성을 구분해 확인합니다.",
    "issues":["아래층 천장 물자국","욕실 바닥 습기","배관 주변 누수"],
    "steps":["욕실 상태 확인","배관·방수 구분","원인 범위 확인"]
},
"drain-clog": {
    "name":"하수구막힘","cat":"배수",
    "headline":"느린 배수와 역류,\n막힌 구간부터 확인",
    "intro":"물이 천천히 내려가거나 역류·악취가 발생할 때 배수구부터 연결 배관까지 상태를 살펴봅니다.",
    "issues":["배수가 느린 경우","물이 다시 올라오는 경우","배수구 악취 발생"],
    "steps":["배수 상태 확인","막힘 구간 점검","처리 범위 안내"]
},
"toilet-clog": {
    "name":"변기막힘","cat":"배수",
    "headline":"반복되는 변기 막힘,\n배수 상태부터 확인",
    "intro":"일시적인 막힘인지 배관 쪽 문제인지 배수 상태와 반복 여부를 기준으로 확인합니다.",
    "issues":["물이 내려가지 않음","수위가 비정상적으로 상승","막힘이 반복됨"],
    "steps":["변기 상태 확인","배수 흐름 점검","막힘 구간 구분"]
},
"sink-clog": {
    "name":"세면대막힘","cat":"배수",
    "headline":"세면대 물이 느리게 빠질 때\n트랩과 배관 확인",
    "intro":"세면대 배수구와 트랩, 연결 배관에 쌓인 이물질이나 오염 상태를 순서대로 확인합니다.",
    "issues":["배수가 느려짐","물이 고여 있음","배수구 냄새"],
    "steps":["배수구 확인","트랩 상태 점검","연결 배관 확인"]
},
"commercial-hood-cleaning": {
    "name":"업소용주방후드청소","cat":"주방",
    "headline":"후드와 필터에 쌓인\n기름 오염 관리",
    "intro":"업소용 주방 후드·필터·덕트 주변에 쌓이는 기름때와 오염 상태를 기준으로 청소 범위를 확인합니다.",
    "issues":["후드 기름때 증가","필터 오염","배기 성능 저하"],
    "steps":["후드 상태 확인","오염 구간 구분","청소 범위 안내"]
}
}

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f"_backup-service-main-{stamp}"
backup.mkdir()

def make_body(d):
    issue_html = "".join(
        f'<div class="hs-issue"><span>CHECK</span><strong>{x}</strong></div>'
        for x in d["issues"]
    )

    step_html = "".join(
        f'''<div class="hs-step">
        <span>0{i}</span>
        <strong>{x}</strong>
        <p>{d["name"]} 진행 전 필요한 내용을 단계별로 확인합니다.</p>
        </div>'''
        for i,x in enumerate(d["steps"],1)
    )

    headline = d["headline"].replace("\n","<br>")

    return f'''
<body class="hs-body">

<header class="hs-header">
  <a class="hs-logo" href="../../index.html">HOMECARE <b>METRO</b></a>
  <nav>
    <a href="../../index.html#services">서비스</a>
    <a href="../../index.html#regions">지역</a>
  </nav>
</header>

<div class="hs-breadcrumb">
  <a href="../../index.html">HOME</a>
  <span>/</span>
  <b>{d["name"]}</b>
</div>

<main>

<section class="hs-hero">
  <div class="hs-hero-copy">
    <span class="hs-cat">{d["cat"]} SERVICE</span>
    <h1>{headline}</h1>
    <p>{d["intro"]}</p>
  </div>

  <div class="hs-namebox">
    <span>SERVICE</span>
    <strong>{d["name"]}</strong>
    <p>서울 · 경기 · 인천</p>
  </div>
</section>

<section class="hs-check">
  <div class="hs-section-title">
    <span>01 · CHECK POINT</span>
    <h2>이런 상황을 먼저 확인합니다</h2>
  </div>
  <div class="hs-issues">
    {issue_html}
  </div>
</section>

<section class="hs-process">
  <div class="hs-section-title">
    <span>02 · PROCESS</span>
    <h2>{d["name"]} 확인 흐름</h2>
  </div>
  <div class="hs-step-grid">
    {step_html}
  </div>
</section>

<section class="hs-regions">
  <div class="hs-section-title hs-white">
    <span>03 · AREA SELECT</span>
    <h2>서비스 지역을 선택하세요</h2>
    <p>서울·경기·인천에서 세부 시·군·구·동·읍·면으로 이동합니다.</p>
  </div>

  <div class="hs-region-grid">
    <a href="seoul/index.html">
      <span>01 · SEOUL</span>
      <strong>서울</strong>
      <p>{d["name"]} 서울 지역 보기</p>
      <b>지역 선택 →</b>
    </a>

    <a class="hs-region-feature" href="gyeonggi/index.html">
      <span>02 · GYEONGGI</span>
      <strong>경기</strong>
      <p>{d["name"]} 경기 지역 보기</p>
      <b>지역 선택 →</b>
    </a>

    <a href="incheon/index.html">
      <span>03 · INCHEON</span>
      <strong>인천</strong>
      <p>{d["name"]} 인천 지역 보기</p>
      <b>지역 선택 →</b>
    </a>
  </div>
</section>

<section class="hs-guide">
  <div>
    <span>HOMECARE METRO</span>
    <h2>지역마다 환경이 다르기 때문에<br>세부 위치까지 나눠 안내합니다.</h2>
  </div>
  <p>
    같은 {d["name"]} 서비스라도 건물 형태와 설치 환경, 사용 상태에 따라
    확인해야 하는 부분이 달라질 수 있습니다. 원하는 지역을 선택하면
    해당 지역의 상세 안내 페이지로 이동합니다.
  </p>
</section>

</main>

<footer class="hs-footer">
  <strong>HOMECARE METRO</strong>
  <span>{d["name"]} · 서울 · 경기 · 인천</span>
</footer>

</body>
'''

count = 0

for slug,d in services.items():
    p = ROOT / "services" / slug / "index.html"

    if not p.exists():
        print("MISSING:", p)
        continue

    shutil.copy2(p, backup / f"{slug}.html")

    txt = p.read_text(encoding="utf-8")

    if not re.search(r"<body\b", txt, re.I):
        print("BODY NOT FOUND:", slug)
        continue

    txt = re.sub(
        r"<body\b[^>]*>.*?</body>",
        make_body(d),
        txt,
        count=1,
        flags=re.I | re.S
    )

    p.write_text(txt, encoding="utf-8")
    count += 1

css_add = r'''

/* =====================================================
   HOMECARE SERVICE ROOT V3
   ===================================================== */

.hs-body{
 margin:0;background:#f5f4ef;color:#17212b;
 font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;
}
.hs-body *{box-sizing:border-box}
.hs-body a{text-decoration:none;color:inherit}

.hs-header{
 height:78px;background:#fff;border-top:7px solid #16313c;
 border-bottom:1px solid #ddd;
 display:flex;align-items:center;justify-content:space-between;
 padding:0 max(4.5vw,32px)
}
.hs-logo{font-weight:900;font-size:18px}
.hs-logo b{color:#bd7515}
.hs-header nav{display:flex;gap:28px;font-weight:800;font-size:14px}

.hs-breadcrumb{
 padding:18px max(4.5vw,32px);
 background:#fafafa;color:#71808b;font-size:13px
}
.hs-breadcrumb span{margin:0 7px}

.hs-hero{
 padding:82px max(4.5vw,32px);
 min-height:480px;
 background:
 radial-gradient(circle at 85% 20%,rgba(30,111,113,.12),transparent 28%),
 linear-gradient(120deg,#f7f0e3,#f6f5ef 55%,#ecf2f0);
 display:grid;grid-template-columns:1.35fr .65fr;
 gap:70px;align-items:center
}
.hs-hero-copy{max-width:820px}
.hs-cat{
 display:block;color:#b46d0d;font-size:12px;font-weight:900;
 letter-spacing:2.4px;margin-bottom:22px
}
.hs-hero h1{
 margin:0;font-size:clamp(48px,5.2vw,78px);
 line-height:1.08;letter-spacing:-4px
}
.hs-hero-copy>p{
 max-width:720px;margin:28px 0 0;color:#59666e;
 font-size:17px;line-height:1.85
}
.hs-namebox{
 min-height:270px;padding:34px;border-radius:22px;
 background:#173f47;color:#fff;display:flex;
 flex-direction:column;justify-content:flex-end;
 box-shadow:0 25px 50px rgba(21,50,58,.18)
}
.hs-namebox span{font-size:11px;color:#deb265;font-weight:900;letter-spacing:2px}
.hs-namebox strong{font-size:35px;margin-top:42px;letter-spacing:-2px}
.hs-namebox p{margin:8px 0 0;color:#bfd0d2;font-size:13px}

.hs-check,.hs-process,.hs-guide{
 max-width:1320px;margin:auto;padding:95px 34px
}
.hs-section-title span{
 display:block;color:#ad6811;font-size:11px;
 font-weight:900;letter-spacing:2px;margin-bottom:14px
}
.hs-section-title h2{
 margin:0;font-size:36px;letter-spacing:-2px
}
.hs-issues{
 display:grid;grid-template-columns:repeat(3,1fr);
 margin-top:40px;border-top:1px solid #cecfc9
}
.hs-issue{
 padding:30px 24px;border-bottom:1px solid #cecfc9;
 border-right:1px solid #cecfc9
}
.hs-issue:first-child{border-left:1px solid #cecfc9}
.hs-issue span{
 display:block;color:#b16a0c;font-size:10px;
 font-weight:900;letter-spacing:1.5px;margin-bottom:30px
}
.hs-issue strong{font-size:20px}

.hs-process{
 padding-top:35px
}
.hs-step-grid{
 display:grid;grid-template-columns:repeat(3,1fr);
 gap:15px;margin-top:38px
}
.hs-step{
 background:#fff;border:1px solid #deddd7;
 border-radius:15px;padding:28px;min-height:200px
}
.hs-step span{
 display:block;color:#b16b0e;font-weight:900;
 font-size:12px;margin-bottom:35px
}
.hs-step strong{font-size:20px}
.hs-step p{color:#778087;font-size:13px;line-height:1.7;margin:14px 0 0}

.hs-regions{
 background:#152f39;color:#fff;
 padding:95px max(4.5vw,32px)
}
.hs-regions>.hs-section-title,
.hs-region-grid{max-width:1252px;margin-left:auto;margin-right:auto}
.hs-white span{color:#e3b667}
.hs-white p{color:#b9c9cc;margin-top:14px}

.hs-region-grid{
 display:grid;grid-template-columns:1fr 1.2fr 1fr;
 gap:15px;margin-top:40px
}
.hs-region-grid>a{
 min-height:300px;padding:30px;border-radius:18px;
 border:1px solid rgba(255,255,255,.16);
 display:flex;flex-direction:column;
 background:rgba(255,255,255,.04)
}
.hs-region-grid>a:hover{background:rgba(255,255,255,.09)}
.hs-region-grid span{
 font-size:10px;letter-spacing:2px;
 color:#e0b466;font-weight:900
}
.hs-region-grid strong{
 margin-top:45px;font-size:45px;letter-spacing:-3px
}
.hs-region-grid p{color:#b9c9cb;font-size:13px}
.hs-region-grid b{margin-top:auto;font-size:12px}
.hs-region-grid .hs-region-feature{
 background:#eee5d5;color:#17212b
}
.hs-region-grid .hs-region-feature p{color:#62696e}

.hs-guide{
 display:grid;grid-template-columns:1fr 1fr;gap:80px
}
.hs-guide>div>span{
 font-size:10px;font-weight:900;color:#ae6810;letter-spacing:2px
}
.hs-guide h2{
 font-size:34px;line-height:1.3;letter-spacing:-2px
}
.hs-guide>p{
 margin:24px 0 0;color:#667078;line-height:1.9;font-size:15px
}

.hs-footer{
 padding:38px max(4.5vw,32px);
 background:#101f25;color:#fff;
 display:flex;justify-content:space-between
}
.hs-footer span{color:#9cafb4;font-size:12px}

@media(max-width:900px){
 .hs-hero{grid-template-columns:1fr}
 .hs-issues,.hs-step-grid,.hs-region-grid{grid-template-columns:1fr}
 .hs-guide{grid-template-columns:1fr}
}

@media(max-width:620px){
 .hs-header{padding:0 20px}
 .hs-header nav{gap:14px;font-size:12px}
 .hs-breadcrumb{padding-left:20px}
 .hs-hero{padding:58px 20px;min-height:auto}
 .hs-hero h1{font-size:43px;letter-spacing:-2.5px}
 .hs-check,.hs-process,.hs-guide{padding:70px 20px}
 .hs-regions{padding:70px 20px}
 .hs-issues{display:block}
 .hs-issue{border-left:1px solid #cecfc9}
 .hs-footer{display:block}
 .hs-footer span{display:block;margin-top:8px}
}

'''

css = CSS.read_text(encoding="utf-8")

if "HOMECARE SERVICE ROOT V3" not in css:
    with CSS.open("a",encoding="utf-8") as f:
        f.write(css_add)

print("SERVICE ROOT UPDATE PASS")
print("UPDATED =", count)
print("BACKUP =", backup)
