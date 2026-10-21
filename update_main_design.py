from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "style.css"

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f"_backup-main-{stamp}"
backup.mkdir(exist_ok=True)

shutil.copy2(INDEX, backup / "index.html")
shutil.copy2(CSS, backup / "style.css")

services = [
    ("청소", "입주청소", "이사 전·후 공간의 먼지와 오염을 정리하는 청소 안내", "move-in-cleaning"),
    ("에어컨", "에어컨수리", "냉방 불량·누수·소음·작동 이상 점검 안내", "aircon-repair"),
    ("에어컨", "에어컨설치", "신규 설치와 이전 설치 전 확인사항 안내", "aircon-install"),
    ("에어컨", "에어컨청소", "필터·열교환기·내부 오염 관리 안내", "aircon-cleaning"),
    ("에어컨", "중고에어컨매입", "제품 상태와 철거 환경을 기준으로 확인하는 매입 안내", "used-aircon-buy"),
    ("누수", "누수탐지", "배관과 주변 흔적을 확인해 원인을 찾는 점검 안내", "leak-detection"),
    ("누수", "벽누수", "벽면 얼룩·습기·도배 손상과 관련된 누수 확인", "wall-leak"),
    ("누수", "보일러누수", "난방배관과 보일러 주변 누수 증상 점검", "boiler-leak"),
    ("누수", "화장실누수", "욕실 바닥·배관·방수층 주변 누수 확인", "bathroom-leak"),
    ("배수", "하수구막힘", "배수 지연·역류·악취 발생 구간 점검 안내", "drain-clog"),
    ("배수", "변기막힘", "배수 불량과 반복 막힘 원인 확인 안내", "toilet-clog"),
    ("배수", "세면대막힘", "세면대 배수 지연과 트랩·배관 점검 안내", "sink-clog"),
    ("주방", "업소용주방후드청소", "후드·필터·덕트 주변 기름때 관리 안내", "commercial-hood-cleaning"),
]

cards = "\n".join(
    f'''<a class="hm-service-card" href="services/{slug}/index.html">
        <span class="hm-service-cat">{cat}</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <b>서비스 보기 →</b>
    </a>'''
    for cat, name, desc, slug in services
)

html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HOMECARE METRO</title>
<meta name="description" content="서울·경기·인천 생활서비스 지역 안내">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="hm-home">

<header class="hm-header">
  <div class="hm-top">SEOUL · GYEONGGI · INCHEON HOMECARE NETWORK</div>
  <div class="hm-nav">
    <a class="hm-logo" href="index.html">HOMECARE <span>METRO</span></a>
    <nav>
      <a href="#services">서비스</a>
      <a href="#regions">지역</a>
      <a href="#guide">이용안내</a>
    </nav>
  </div>
</header>

<main>
<section class="hm-hero">
  <div class="hm-hero-inner">
    <div class="hm-hero-copy">
      <span class="hm-kicker">HOME SERVICE DIRECTORY</span>
      <h1>집에서 생기는 문제,<br><em>서비스와 지역</em>으로 빠르게 찾기</h1>
      <p>
        청소부터 에어컨, 누수, 배수, 주방 관리까지.<br>
        서울·경기·인천의 시·군·구·동·읍·면 단위로 필요한 정보를 찾아볼 수 있습니다.
      </p>
      <div class="hm-hero-actions">
        <a class="hm-btn-primary" href="#services">서비스 선택</a>
        <a class="hm-btn-light" href="#regions">지역 선택</a>
      </div>
    </div>

    <div class="hm-hero-panel">
      <span class="hm-panel-label">CURRENT NETWORK</span>
      <div class="hm-stat-grid">
        <div><strong>13</strong><span>서비스</span></div>
        <div><strong>795</strong><span>세부지역</span></div>
        <div><strong>256</strong><span>서울</span></div>
        <div><strong>451</strong><span>경기</span></div>
        <div><strong>88</strong><span>인천</span></div>
        <div><strong>12,460</strong><span>페이지</span></div>
      </div>
    </div>
  </div>
</section>

<section class="hm-category-strip">
  <div>청소</div><div>에어컨</div><div>누수</div><div>배수</div><div>주방관리</div>
</section>

<section class="hm-section" id="services">
  <div class="hm-section-head">
    <div>
      <span class="hm-eyebrow">01 · SERVICE</span>
      <h2>필요한 서비스를 먼저 선택하세요</h2>
    </div>
    <p>증상과 작업 종류에 맞는 서비스를 고른 뒤 세부 지역으로 이동합니다.</p>
  </div>
  <div class="hm-service-grid">
    {cards}
  </div>
</section>

<section class="hm-region-section" id="regions">
  <div class="hm-section-head">
    <div>
      <span class="hm-eyebrow">02 · AREA</span>
      <h2>서울·경기·인천 지역 찾기</h2>
    </div>
    <p>구·시·군부터 동·읍·면까지 단계별로 지역을 선택할 수 있습니다.</p>
  </div>

  <div class="hm-region-grid">
    <a class="hm-region-card" href="regions/seoul/index.html">
      <span>SEOUL</span>
      <h3>서울</h3>
      <strong>25개 구 · 256개 세부지역</strong>
      <p>서울 전 지역의 구와 동 단위 서비스 안내</p>
      <b>서울 지역 보기 →</b>
    </a>

    <a class="hm-region-card hm-region-large" href="regions/gyeonggi/index.html">
      <span>GYEONGGI</span>
      <h3>경기</h3>
      <strong>31개 시·군 · 451개 세부지역</strong>
      <p>시·군·구와 동·읍·면까지 연결되는 지역 안내</p>
      <b>경기 지역 보기 →</b>
    </a>

    <a class="hm-region-card" href="regions/incheon/index.html">
      <span>INCHEON</span>
      <h3>인천</h3>
      <strong>2군·9구 · 88개 세부지역</strong>
      <p>인천의 구·군과 동·읍·면 단위 서비스 안내</p>
      <b>인천 지역 보기 →</b>
    </a>
  </div>
</section>

<section class="hm-guide" id="guide">
  <div class="hm-guide-title">
    <span class="hm-eyebrow">03 · HOW TO USE</span>
    <h2>복잡하지 않게<br>세 단계로 찾습니다.</h2>
  </div>
  <div class="hm-guide-steps">
    <div><span>01</span><strong>서비스 선택</strong><p>청소·에어컨·누수·배수 등 필요한 작업을 선택합니다.</p></div>
    <div><span>02</span><strong>지역 선택</strong><p>서울·경기·인천에서 시·구·동·읍·면 순으로 이동합니다.</p></div>
    <div><span>03</span><strong>상세 안내 확인</strong><p>지역별 서비스 내용과 점검 항목을 확인합니다.</p></div>
  </div>
</section>

</main>

<footer class="hm-footer">
  <div>
    <strong>HOMECARE METRO</strong>
    <p>서울 · 경기 · 인천 생활서비스 지역 안내</p>
  </div>
  <span>HOME SERVICE DIRECTORY</span>
</footer>

</body>
</html>
'''

INDEX.write_text(html, encoding="utf-8")

extra_css = r'''

/* ==================================================
   HOMECARE METRO MAIN V3
   Main-only classes: hm-
   ================================================== */

.hm-home{
  margin:0;
  background:#f4f3ee;
  color:#17212b;
  font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;
}

.hm-home *{box-sizing:border-box}
.hm-home a{text-decoration:none;color:inherit}

.hm-header{
  background:#fff;
  border-bottom:1px solid #dddcd7;
  position:relative;
  z-index:10;
}

.hm-top{
  padding:12px max(4vw,24px);
  background:#142c38;
  color:#fff;
  font-size:12px;
  font-weight:800;
  letter-spacing:1.8px;
}

.hm-nav{
  max-width:1380px;
  margin:auto;
  min-height:78px;
  padding:0 34px;
  display:flex;
  align-items:center;
  justify-content:space-between;
}

.hm-logo{
  font-size:19px;
  font-weight:900;
  letter-spacing:-.7px;
}

.hm-logo span{color:#c47b18}

.hm-nav nav{
  display:flex;
  gap:28px;
  font-size:14px;
  font-weight:800;
}

.hm-hero{
  padding:82px 34px 72px;
  background:
    radial-gradient(circle at 84% 15%,rgba(197,131,33,.16),transparent 24%),
    linear-gradient(125deg,#f5efe2 0%,#f6f4ed 45%,#e9f1ef 100%);
}

.hm-hero-inner{
  max-width:1320px;
  margin:auto;
  display:grid;
  grid-template-columns:minmax(0,1.35fr) minmax(330px,.65fr);
  gap:70px;
  align-items:center;
}

.hm-kicker,.hm-eyebrow{
  display:block;
  color:#ac6710;
  font-size:12px;
  font-weight:900;
  letter-spacing:2.2px;
  margin-bottom:20px;
}

.hm-hero h1{
  margin:0;
  max-width:820px;
  font-size:clamp(46px,5.2vw,78px);
  line-height:1.05;
  letter-spacing:-4px;
}

.hm-hero h1 em{
  color:#155d63;
  font-style:normal;
}

.hm-hero-copy>p{
  margin:30px 0 0;
  color:#56616a;
  font-size:18px;
  line-height:1.85;
}

.hm-hero-actions{
  display:flex;
  gap:12px;
  margin-top:34px;
}

.hm-btn-primary,.hm-btn-light{
  padding:15px 22px;
  border-radius:9px;
  font-size:14px;
  font-weight:900;
}

.hm-btn-primary{
  background:#183e46;
  color:#fff!important;
}

.hm-btn-light{
  background:#fff;
  border:1px solid #d9d7cf;
}

.hm-hero-panel{
  background:#173e46;
  color:#fff;
  padding:28px;
  border-radius:22px;
  box-shadow:0 24px 55px rgba(20,44,56,.18);
}

.hm-panel-label{
  display:block;
  color:#dcb66e;
  font-size:11px;
  font-weight:900;
  letter-spacing:2px;
  margin-bottom:22px;
}

.hm-stat-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:1px;
  overflow:hidden;
  border:1px solid rgba(255,255,255,.16);
}

.hm-stat-grid div{
  min-height:108px;
  padding:21px;
  background:rgba(255,255,255,.04);
  display:flex;
  flex-direction:column;
  justify-content:center;
}

.hm-stat-grid strong{
  font-size:28px;
  letter-spacing:-1px;
}

.hm-stat-grid span{
  margin-top:6px;
  color:#cdd9da;
  font-size:12px;
}

.hm-category-strip{
  max-width:1320px;
  margin:-22px auto 0;
  position:relative;
  display:grid;
  grid-template-columns:repeat(5,1fr);
  background:#fff;
  border:1px solid #dddcd6;
  border-radius:12px;
  overflow:hidden;
  box-shadow:0 15px 30px rgba(31,42,48,.07);
}

.hm-category-strip div{
  padding:18px;
  text-align:center;
  font-weight:900;
  font-size:14px;
  border-right:1px solid #e5e3dd;
}

.hm-category-strip div:last-child{border-right:0}

.hm-section,.hm-region-section,.hm-guide{
  max-width:1320px;
  margin:auto;
  padding:100px 34px;
}

.hm-section-head{
  display:flex;
  justify-content:space-between;
  align-items:end;
  gap:40px;
  margin-bottom:42px;
}

.hm-section-head h2,.hm-guide h2{
  margin:0;
  font-size:38px;
  letter-spacing:-2px;
}

.hm-section-head>p{
  max-width:470px;
  margin:0;
  color:#687078;
  line-height:1.75;
}

.hm-service-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px;
}

.hm-service-card{
  min-height:210px;
  padding:26px;
  background:#fff;
  border:1px solid #dfddd7;
  border-radius:16px;
  transition:.22s ease;
  display:flex;
  flex-direction:column;
}

.hm-service-card:hover{
  transform:translateY(-5px);
  border-color:#174c53;
  box-shadow:0 16px 34px rgba(25,55,61,.1);
}

.hm-service-cat{
  color:#b66e0d;
  font-size:11px;
  font-weight:900;
}

.hm-service-card h3{
  margin:18px 0 11px;
  font-size:21px;
  letter-spacing:-1px;
}

.hm-service-card p{
  margin:0;
  color:#70777c;
  font-size:13px;
  line-height:1.65;
}

.hm-service-card b{
  margin-top:auto;
  padding-top:24px;
  font-size:12px;
  color:#245b61;
}

.hm-region-section{
  max-width:none;
  padding-left:max(34px,calc((100% - 1320px)/2 + 34px));
  padding-right:max(34px,calc((100% - 1320px)/2 + 34px));
  background:#172c34;
  color:#fff;
}

.hm-region-section .hm-section-head{
  max-width:1320px;
  margin-left:auto;
  margin-right:auto;
}

.hm-region-section .hm-section-head>p{color:#b6c4c7}

.hm-region-grid{
  max-width:1320px;
  margin:auto;
  display:grid;
  grid-template-columns:1fr 1.25fr 1fr;
  gap:16px;
}

.hm-region-card{
  min-height:330px;
  padding:32px;
  border:1px solid rgba(255,255,255,.17);
  border-radius:18px;
  background:rgba(255,255,255,.045);
  display:flex;
  flex-direction:column;
}

.hm-region-card:hover{background:rgba(255,255,255,.09)}

.hm-region-card>span{
  font-size:11px;
  font-weight:900;
  letter-spacing:2px;
  color:#dfb56d;
}

.hm-region-card h3{
  margin:32px 0 10px;
  font-size:48px;
  letter-spacing:-3px;
}

.hm-region-card strong{font-size:15px}

.hm-region-card p{
  color:#b9c5c7;
  line-height:1.7;
  font-size:13px;
}

.hm-region-card b{
  margin-top:auto;
  font-size:13px;
}

.hm-region-large{
  background:#f1e8d8;
  color:#17212b;
}

.hm-region-large p{color:#5d6468}

.hm-guide{
  display:grid;
  grid-template-columns:.75fr 1.25fr;
  gap:90px;
}

.hm-guide-steps{
  border-top:1px solid #cfcfc9;
}

.hm-guide-steps>div{
  display:grid;
  grid-template-columns:70px 180px 1fr;
  gap:20px;
  padding:28px 0;
  border-bottom:1px solid #cfcfc9;
  align-items:start;
}

.hm-guide-steps span{
  color:#ae6a12;
  font-size:12px;
  font-weight:900;
}

.hm-guide-steps strong{font-size:17px}

.hm-guide-steps p{
  margin:0;
  color:#697177;
  line-height:1.65;
  font-size:14px;
}

.hm-footer{
  padding:45px max(5vw,34px);
  background:#111d22;
  color:#fff;
  display:flex;
  justify-content:space-between;
  align-items:end;
}

.hm-footer strong{font-size:20px}
.hm-footer p{margin:7px 0 0;color:#a9b4b7;font-size:13px}
.hm-footer>span{color:#7f9296;font-size:10px;letter-spacing:2px}

@media(max-width:1000px){
  .hm-hero-inner{grid-template-columns:1fr}
  .hm-service-grid{grid-template-columns:repeat(2,1fr)}
  .hm-region-grid{grid-template-columns:1fr}
  .hm-guide{grid-template-columns:1fr}
}

@media(max-width:650px){
  .hm-nav{padding:0 20px}
  .hm-nav nav{gap:13px;font-size:12px}
  .hm-hero{padding:58px 20px}
  .hm-hero h1{font-size:43px;letter-spacing:-2.8px}
  .hm-hero-copy>p{font-size:15px}
  .hm-category-strip{
    margin:-12px 18px 0;
    grid-template-columns:repeat(2,1fr);
  }
  .hm-category-strip div{border-bottom:1px solid #e5e3dd}
  .hm-section,.hm-region-section,.hm-guide{padding:72px 20px}
  .hm-section-head{display:block}
  .hm-section-head>p{margin-top:18px}
  .hm-service-grid{grid-template-columns:1fr}
  .hm-guide-steps>div{grid-template-columns:42px 1fr}
  .hm-guide-steps p{grid-column:2}
  .hm-footer{display:block}
  .hm-footer>span{display:block;margin-top:25px}
}

'''

with CSS.open("a", encoding="utf-8") as f:
    f.write(extra_css)

print("MAIN DESIGN UPDATE PASS")
print("BACKUP =", backup)
print("INDEX =", INDEX)
print("CSS =", CSS)
