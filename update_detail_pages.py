from pathlib import Path
from datetime import datetime
import hashlib, html, re, shutil

ROOT = Path(r"I:\homecare-metro-v1\homecare-metro-v2")
SERVICES_ROOT = ROOT / "services"
CSS = ROOT / "assets" / "style.css"

SPECS = {
"move-in-cleaning":{
"name":"입주청소","cat":"CLEANING",
"intro":"입주 또는 이사 전후 공간은 눈에 보이는 먼지뿐 아니라 창틀, 수납장, 주방과 욕실처럼 오염이 남기 쉬운 구역을 함께 확인하는 것이 중요합니다.",
"checks":["창틀·문틀 사이 먼지와 잔여 오염","주방 수납장과 조리 공간의 생활 오염","욕실 물때와 바닥·배수구 주변 상태"],
"steps":["공간과 오염 상태 확인","구역별 청소 범위 구분","작업 순서와 확인 항목 안내"],
"faqs":[
("어떤 공간을 먼저 확인하나요?","주방·욕실·창틀처럼 오염이 쌓이기 쉬운 구역과 바닥, 수납 공간의 상태를 함께 살펴봅니다."),
("입주 전과 이사 후 청소가 다른가요?","공간 사용 여부와 남아 있는 오염 종류에 따라 확인해야 할 구역과 작업 범위가 달라질 수 있습니다."),
("지역마다 작업 조건이 달라질 수 있나요?","건물 형태와 면적, 엘리베이터·주차 등 현장 환경에 따라 확인할 내용이 달라질 수 있습니다.")
]},
"aircon-repair":{
"name":"에어컨수리","cat":"AIR CONDITIONER",
"intro":"에어컨의 냉방 약화, 작동 중단, 소음, 누수처럼 나타나는 증상을 먼저 구분하면 점검해야 할 부분을 보다 명확하게 확인할 수 있습니다.",
"checks":["찬바람이 약하거나 냉방이 늦어지는 증상","작동 중 진동·소음 또는 갑작스러운 정지","실내기 주변 물방울이나 누수 흔적"],
"steps":["현재 증상과 작동 상태 확인","실내기·실외기 및 연결부 점검","원인 가능 구간과 필요한 작업 구분"],
"faqs":[
("찬바람이 약하면 바로 고장인가요?","필터 오염, 설정 상태, 냉매나 기기 이상 등 여러 원인이 있을 수 있어 증상 확인이 먼저 필요합니다."),
("실내기에서 물이 떨어지는 이유는 무엇인가요?","배수 문제나 결로, 설치 환경 등 여러 가능성이 있어 주변 상태와 배수 흐름을 함께 확인합니다."),
("소음만 발생해도 점검이 필요한가요?","평소와 다른 진동이나 반복적인 소음이 있다면 발생 위치와 작동 상황을 함께 확인하는 것이 좋습니다.")
]},
"aircon-install":{
"name":"에어컨설치","cat":"AIR CONDITIONER",
"intro":"에어컨 설치는 기기만 옮기는 작업이 아니라 실내기와 실외기 위치, 배관 경로, 배수 조건과 설치 공간을 함께 확인해야 합니다.",
"checks":["실내기와 실외기 설치 위치","배관·전선·배수호스 이동 경로","벽면과 실외기 주변 작업 공간"],
"steps":["설치 위치와 주변 환경 확인","제품 형태와 배관 조건 점검","설치 범위와 필요한 작업 구분"],
"faqs":[
("이전 설치도 같은 과정을 거치나요?","기존 제품 철거 상태와 새 설치 위치를 함께 확인해야 하므로 신규 설치와 확인 항목이 일부 다를 수 있습니다."),
("배관 길이는 왜 확인하나요?","실내기와 실외기의 거리와 이동 경로에 따라 필요한 배관 조건이 달라질 수 있기 때문입니다."),
("실외기 위치도 중요한가요?","통풍과 작업 공간, 설치 안전성에 영향을 줄 수 있어 실외기 주변 환경을 함께 확인합니다.")
]},
"aircon-cleaning":{
"name":"에어컨청소","cat":"AIR CONDITIONER",
"intro":"에어컨 내부에는 사용하면서 먼지와 습기가 쌓일 수 있어 필터뿐 아니라 열교환기와 송풍부 등 오염 구간을 나누어 확인합니다.",
"checks":["필터와 흡입구에 쌓인 먼지","송풍구 안쪽의 오염과 냄새","열교환기 주변 먼지와 습기 흔적"],
"steps":["제품 형태와 오염 상태 확인","세척이 필요한 내부 구간 구분","청소 범위와 관리 방법 안내"],
"faqs":[
("필터만 청소하면 충분한가요?","사용 환경에 따라 내부 열교환기나 송풍부에도 오염이 남을 수 있어 상태 확인이 필요합니다."),
("냄새가 나는 이유는 무엇인가요?","내부 습기와 먼지, 오염 등이 원인이 될 수 있어 냄새가 발생하는 위치와 내부 상태를 함께 살펴봅니다."),
("청소 주기는 모두 같나요?","사용 빈도와 설치 장소, 실내 환경에 따라 오염 속도가 달라질 수 있습니다.")
]},
"used-aircon-buy":{
"name":"중고에어컨매입","cat":"AIR CONDITIONER",
"intro":"중고 에어컨은 제품 형태와 연식뿐 아니라 정상 작동 여부, 설치 위치와 철거 환경까지 함께 확인해야 매입 가능 여부를 판단하기 쉽습니다.",
"checks":["제품 종류·모델·사용 상태","전원과 냉방 등 기본 작동 여부","실내외기 위치와 철거 가능 환경"],
"steps":["제품 정보와 상태 확인","설치 위치와 철거 조건 확인","매입 가능 범위와 진행 방식 안내"],
"faqs":[
("어떤 정보를 준비하면 좋나요?","제품 전체 모습과 모델 정보, 설치 위치, 정상 작동 여부를 확인하면 상태 파악에 도움이 됩니다."),
("설치된 상태에서도 확인할 수 있나요?","설치 위치와 철거 환경을 함께 확인해야 하므로 현재 설치 상태 정보가 중요합니다."),
("모든 에어컨이 매입 가능한가요?","제품 상태와 연식, 설치 환경 등에 따라 가능 여부가 달라질 수 있습니다.")
]},
"leak-detection":{
"name":"누수탐지","cat":"LEAK",
"intro":"누수는 실제 물이 보이는 위치와 원인이 시작된 위치가 다를 수 있어 벽·천장·바닥의 흔적과 배관 구간을 함께 확인해야 합니다.",
"checks":["벽이나 천장에 번지는 물자국","수도 사용량이나 계량기 변화","바닥·배관 주변의 반복적인 습기"],
"steps":["누수 흔적과 발생 위치 확인","급수·난방 등 배관 가능 구간 점검","원인 후보와 확인 범위 구분"],
"faqs":[
("물이 보이는 곳이 누수 지점인가요?","물은 구조물이나 배관을 따라 이동할 수 있어 보이는 위치와 실제 원인이 다를 수 있습니다."),
("계량기도 확인해야 하나요?","급수 계통 누수가 의심되는 경우 사용하지 않는 상태에서 계량기 변화를 확인하는 것이 도움이 될 수 있습니다."),
("탐지 전에 무엇을 확인하면 좋나요?","처음 발견한 위치와 시기, 물 사용과의 관계, 반복 여부를 확인하면 원인 범위를 좁히는 데 도움이 됩니다.")
]},
"wall-leak":{
"name":"벽누수","cat":"LEAK",
"intro":"벽면 변색이나 습기, 도배지 들뜸은 외부 유입·배관·결로 등 원인이 다양할 수 있어 주변 환경과 함께 구분해서 살펴봅니다.",
"checks":["도배지 변색과 들뜸","벽면이 반복적으로 젖거나 차가운 상태","곰팡이 또는 물자국이 넓어지는 현상"],
"steps":["벽면 손상과 습기 범위 확인","주변 배관·외벽 조건 점검","누수 가능 구간과 원인 구분"],
"faqs":[
("곰팡이가 있으면 모두 누수인가요?","결로나 환기 문제도 비슷한 현상을 만들 수 있어 습기 발생 위치와 패턴을 함께 확인해야 합니다."),
("벽지가 젖었다 마르면 괜찮은가요?","반복 여부와 범위 변화가 중요하므로 발생 시기와 주변 물 사용 상황을 확인하는 것이 좋습니다."),
("외벽에서도 물이 들어올 수 있나요?","창호와 외벽 균열 등 외부 유입 가능성도 있어 건물 구조와 발생 위치를 함께 살펴봅니다.")
]},
"boiler-leak":{
"name":"보일러누수","cat":"LEAK",
"intro":"보일러 주변 물기나 압력 변화는 본체 연결부와 난방배관 등 여러 지점에서 발생할 수 있어 위치와 증상을 나누어 확인합니다.",
"checks":["보일러 본체 또는 연결부 주변 물기","보일러 압력이 반복적으로 변하는 현상","난방 배관 주변 바닥의 습기"],
"steps":["보일러와 연결부 상태 확인","난방배관과 주변 누수 흔적 점검","누수 가능 위치와 작업 범위 구분"],
"faqs":[
("압력이 떨어지면 누수인가요?","여러 원인이 있을 수 있으므로 압력 변화와 함께 배관 및 연결부 상태를 확인해야 합니다."),
("바닥만 젖어도 난방배관 문제일 수 있나요?","배관 위치와 물기 발생 패턴에 따라 가능성이 있으므로 주변 구간을 함께 확인합니다."),
("보일러 아래 물이 고이면 어떻게 하나요?","사용 상태와 물이 발생한 위치를 확인하고 연결부나 배수 계통 등 원인을 구분하는 과정이 필요합니다.")
]},
"bathroom-leak":{
"name":"화장실누수","cat":"LEAK",
"intro":"화장실 누수는 급수배관, 배수관, 바닥 방수와 기구 연결부 등 여러 원인이 있을 수 있어 물 사용 상황과 발생 위치를 함께 확인합니다.",
"checks":["아래층 천장에 생기는 물자국","욕실 바닥이나 벽면의 반복적인 습기","세면대·변기·샤워기 주변 연결부 물기"],
"steps":["누수 발생 위치와 물 사용 상황 확인","배관·기구·방수 가능 구간 점검","원인 범위와 필요한 작업 구분"],
"faqs":[
("아래층에 물이 새면 욕실 방수 문제인가요?","배수관이나 급수관 등 다른 원인도 가능하므로 물 사용 상황과 발생 위치를 같이 확인해야 합니다."),
("물을 쓸 때만 새는 것도 단서가 되나요?","특정 기구 사용과 누수 발생이 연결된다면 원인 구간을 좁히는 데 도움이 됩니다."),
("타일이 멀쩡해도 누수가 생길 수 있나요?","표면 상태와 내부 배관·방수 상태는 다를 수 있어 겉모습만으로 판단하기 어렵습니다.")
]},
"drain-clog":{
"name":"하수구막힘","cat":"DRAIN",
"intro":"하수구가 천천히 내려가거나 역류하고 냄새가 나는 경우 배수구 입구부터 연결 배관까지 막힘 가능 구간을 순서대로 확인합니다.",
"checks":["물이 평소보다 천천히 빠지는 현상","사용할 때 물이 다시 올라오는 역류","배수구 주변에서 반복되는 악취"],
"steps":["배수 속도와 역류 여부 확인","배수구·트랩·배관 구간 점검","막힘 위치와 처리 범위 구분"],
"faqs":[
("물이 조금씩 내려가면 괜찮은가요?","부분적으로 막힌 경우에도 배수 속도가 점점 느려질 수 있어 반복 여부를 확인하는 것이 좋습니다."),
("악취도 막힘과 관련이 있나요?","배관 내 오염이나 트랩 상태 등 여러 원인이 있어 배수 상태와 함께 확인합니다."),
("여러 배수구가 동시에 느리면 무엇을 봐야 하나요?","공통으로 연결되는 배관 구간의 상태를 함께 확인할 필요가 있습니다.")
]},
"toilet-clog":{
"name":"변기막힘","cat":"DRAIN",
"intro":"변기 막힘은 이물질뿐 아니라 배수관 내부 상태와 반복적인 배수 불량 등 원인이 다를 수 있어 물이 내려가는 모습을 먼저 확인합니다.",
"checks":["물을 내려도 수위가 높게 유지되는 현상","배수 후 물이 다시 올라오는 현상","같은 증상이 반복적으로 발생하는 경우"],
"steps":["변기 수위와 배수 반응 확인","이물질·배관 가능 구간 점검","막힘 위치와 처리 방법 구분"],
"faqs":[
("물이 조금씩 내려가면 막힌 건가요?","정상보다 배수 시간이 길다면 부분 막힘 가능성이 있어 반복되는지 확인하는 것이 좋습니다."),
("여러 번 물을 내리면 해결될까요?","수위가 계속 올라가는 상태에서는 추가 사용으로 넘침이 생길 수 있어 상태 확인이 우선입니다."),
("변기가 자주 막히는 이유는 무엇인가요?","사용 습관뿐 아니라 배관 구조나 내부 상태 등도 영향을 줄 수 있습니다.")
]},
"sink-clog":{
"name":"세면대막힘","cat":"DRAIN",
"intro":"세면대 배수가 느려질 때는 배수구 주변 오염부터 트랩과 연결 배관까지 물 흐름을 방해하는 구간을 순서대로 확인합니다.",
"checks":["물이 세면대에 오래 고이는 현상","배수구에서 물이 천천히 내려가는 상태","배수구 주변 냄새나 이물질"],
"steps":["배수구와 물 흐름 확인","트랩과 연결부 상태 점검","막힘 가능 구간과 작업 범위 구분"],
"faqs":[
("세면대만 느리면 어디를 봐야 하나요?","세면대 배수구와 바로 아래 트랩부터 확인해 연결 배관 쪽으로 범위를 넓혀볼 수 있습니다."),
("머리카락도 원인이 되나요?","비누 찌꺼기나 머리카락 등이 함께 쌓이면 배수 흐름이 줄어들 수 있습니다."),
("냄새와 막힘이 같이 생길 수 있나요?","배관 내부 오염과 트랩 상태에 따라 두 증상이 함께 나타날 수 있습니다.")
]},
"commercial-hood-cleaning":{
"name":"업소용주방후드청소","cat":"KITCHEN",
"intro":"업소용 후드는 조리 과정에서 발생하는 기름 입자가 필터와 후드 내부, 덕트 주변에 쌓일 수 있어 오염 범위를 나누어 확인합니다.",
"checks":["후드 표면과 내부의 끈적한 기름때","필터에 누적된 기름과 먼지","배기 성능 저하 또는 주변 오염"],
"steps":["후드·필터 오염 상태 확인","청소가 필요한 구간과 구조 파악","작업 범위와 관리 항목 안내"],
"faqs":[
("필터만 청소하면 되나요?","사용 환경에 따라 후드 내부와 연결 구간에도 기름 오염이 쌓일 수 있어 전체 상태를 확인하는 것이 좋습니다."),
("주방 사용량에 따라 차이가 큰가요?","조리 방식과 사용 시간, 기름 사용량에 따라 오염 속도와 범위가 달라질 수 있습니다."),
("청소 전에 무엇을 확인해야 하나요?","후드 크기와 형태, 필터 수량, 작업 공간과 주변 설비 상태를 확인하면 범위 파악에 도움이 됩니다.")
]}
}

METRO_KR = {"seoul":"서울","gyeonggi":"경기","incheon":"인천"}

def clean_text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

def get_h1(txt):
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", txt, re.I|re.S)
    return clean_text(m.group(1)) if m else ""

def has_direct_child(p):
    txt = p.read_text(encoding="utf-8")
    for href in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']', txt, re.I):
        if re.fullmatch(r'[^/#?]+/index\.html', html.unescape(href.strip()), re.I):
            if (p.parent / html.unescape(href.strip())).exists():
                return True
    return False

leaves = []

for p in SERVICES_ROOT.rglob("index.html"):
    rel = p.relative_to(SERVICES_ROOT)
    parts = rel.parts

    # 최소 services/service/metro/지역/index.html 이상의 페이지
    if len(parts) < 4:
        continue

    service_slug = parts[0]
    metro_slug = parts[1]

    if service_slug not in SPECS or metro_slug not in METRO_KR:
        continue

    if not has_direct_child(p):
        leaves.append(p)

print("LEAF PAGES FOUND =", len(leaves))
print("EXPECTED =", 13 * 795)

if len(leaves) != 13 * 795:
    raise SystemExit("STOP: 예상 상세페이지 수와 다릅니다. 파일을 수정하지 않습니다.")

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"_backup-detail-pages-{stamp}"
BACKUP.mkdir()

updated = 0

for p in leaves:
    rel = p.relative_to(SERVICES_ROOT)
    parts = rel.parts
    service_slug = parts[0]
    metro_slug = parts[1]
    spec = SPECS[service_slug]
    service = spec["name"]

    txt = p.read_text(encoding="utf-8")
    heading = get_h1(txt)

    location = heading.replace(service, "").strip()
    if not location:
        location = " ".join(parts[1:-1])

    # deterministic variation
    hv = int(hashlib.sha256((service_slug + "|" + location).encode("utf-8")).hexdigest()[:8],16)
    starters = [
        f"{location}에서 {service} 관련 내용을 찾을 때는 현재 나타나는 증상과 현장 환경을 함께 확인하는 것이 좋습니다.",
        f"{location} {service}는 겉으로 보이는 현상만 보기보다 발생 위치와 반복 여부를 함께 살펴보는 것이 중요합니다.",
        f"{location}에서 {service}가 필요한 상황이라면 먼저 현재 상태를 정리하고 확인해야 할 구간을 나누어 보는 것이 도움이 됩니다.",
        f"{location}의 건물 형태와 사용 환경에 따라 {service} 확인 항목은 달라질 수 있어 현장 상태를 기준으로 살펴보는 것이 좋습니다."
    ]
    starter = starters[hv % len(starters)]

    checks = "".join(
        f'''<article class="hd-check">
        <span>0{i}</span>
        <strong>{x}</strong>
        <p>{location} 현장에서 해당 항목이 나타나는지 먼저 확인합니다.</p>
        </article>'''
        for i,x in enumerate(spec["checks"],1)
    )

    steps = "".join(
        f'''<li><span>{i:02d}</span><div><strong>{x}</strong>
        <p>{location}의 실제 상태를 기준으로 필요한 범위를 순서대로 확인합니다.</p></div></li>'''
        for i,x in enumerate(spec["steps"],1)
    )

    faqs = "".join(
        f'''<details class="hd-faq">
        <summary>{q}</summary>
        <p>{a}</p>
        </details>'''
        for q,a in spec["faqs"]
    )

    depth = len(p.parent.relative_to(ROOT).parts)
    root_prefix = "../" * depth

    parent_href = "../index.html"

    safe_backup = "__".join(parts[:-1]) + ".html"
    shutil.copy2(p, BACKUP / safe_backup)

    body = f'''
<body class="hd-body">

<header class="hd-header">
  <a class="hd-logo" href="{root_prefix}index.html">HOMECARE <b>METRO</b></a>
  <nav>
    <a href="{root_prefix}index.html#services">서비스</a>
    <a href="{root_prefix}index.html#regions">지역</a>
  </nav>
</header>

<div class="hd-breadcrumb">
  <a href="{root_prefix}index.html">HOME</a>
  <span>/</span>
  <a href="{parent_href}">상위 지역</a>
  <span>/</span>
  <b>{location}</b>
</div>

<main>

<section class="hd-hero">
  <div class="hd-hero-copy">
    <span class="hd-kicker">{spec["cat"]} · LOCAL SERVICE</span>
    <h1>{location}<br><em>{service}</em></h1>
    <p>{starter}</p>
  </div>

  <aside class="hd-servicebox">
    <span>SERVICE</span>
    <strong>{service}</strong>
    <p>{location}</p>
  </aside>
</section>

<section class="hd-intro">
  <div>
    <span>01 · OVERVIEW</span>
    <h2>{location}에서<br>먼저 확인할 내용</h2>
  </div>
  <p>{spec["intro"]}</p>
</section>

<section class="hd-checks">
  {checks}
</section>

<section class="hd-process">
  <div class="hd-heading">
    <span>02 · CHECK PROCESS</span>
    <h2>{service} 확인 흐름</h2>
  </div>
  <ol>{steps}</ol>
</section>

<section class="hd-local">
  <div>
    <span>03 · LOCAL POINT</span>
    <h2>{location} 현장 환경도<br>함께 살펴봅니다.</h2>
  </div>
  <p>
    같은 {service} 문제라도 아파트, 빌라, 단독주택, 상가 등 건물 형태와
    설비 배치에 따라 확인해야 할 부분이 달라질 수 있습니다.
    따라서 {location}에서도 증상 발생 위치와 사용 환경을 함께 확인해
    필요한 범위를 구분하는 과정이 중요합니다.
  </p>
</section>

<section class="hd-faq-section">
  <div class="hd-heading">
    <span>04 · FAQ</span>
    <h2>{service} 자주 확인하는 내용</h2>
  </div>
  <div class="hd-faq-list">
    {faqs}
  </div>
</section>

<section class="hd-return">
  <div>
    <span>AREA DIRECTORY</span>
    <h2>다른 세부 지역도 확인할 수 있습니다.</h2>
  </div>
  <a href="{parent_href}">상위 지역으로 돌아가기 →</a>
</section>

</main>

<footer class="hd-footer">
  <strong>HOMECARE METRO</strong>
  <span>{location} · {service}</span>
</footer>

</body>
'''

    new = re.sub(
        r"<body\b[^>]*>.*?</body>",
        body,
        txt,
        count=1,
        flags=re.I|re.S
    )

    p.write_text(new, encoding="utf-8")
    updated += 1


css = CSS.read_text(encoding="utf-8")

if "HOMECARE DETAIL PAGE V6" not in css:
    css += r'''

/* =====================================================
   HOMECARE DETAIL PAGE V6
   ===================================================== */

.hd-body{
 margin:0;background:#f5f4ef;color:#17212b;
 font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;
}
.hd-body *{box-sizing:border-box}
.hd-body a{text-decoration:none;color:inherit}

.hd-header{
 min-height:76px;background:#fff;
 border-top:7px solid #15313b;
 border-bottom:1px solid #ddd;
 padding:0 max(4.5vw,32px);
 display:flex;align-items:center;justify-content:space-between
}
.hd-logo{font-weight:900;font-size:18px}
.hd-logo b{color:#bd7515}
.hd-header nav{display:flex;gap:28px;font-weight:800;font-size:14px}

.hd-breadcrumb{
 padding:18px max(4.5vw,32px);
 background:#fafafa;border-bottom:1px solid #e8e8e4;
 color:#72808a;font-size:13px
}
.hd-breadcrumb span{margin:0 7px}

.hd-hero{
 min-height:470px;
 padding:78px max(4.5vw,32px);
 display:grid;grid-template-columns:1fr 330px;
 gap:80px;align-items:center;
 background:
 radial-gradient(circle at 85% 18%,rgba(31,111,113,.14),transparent 27%),
 linear-gradient(120deg,#f7efe2,#f7f5ef 56%,#eaf2f0)
}

.hd-kicker,.hd-intro span,.hd-heading span,.hd-local span{
 display:block;color:#ad6810;font-size:11px;
 font-weight:900;letter-spacing:2px
}

.hd-hero h1{
 margin:22px 0 0;
 font-size:clamp(50px,5.2vw,80px);
 line-height:1.04;letter-spacing:-4px
}
.hd-hero h1 em{font-style:normal;color:#176269}

.hd-hero-copy>p{
 max-width:760px;margin:28px 0 0;
 color:#5f6970;font-size:16px;line-height:1.9
}

.hd-servicebox{
 min-height:245px;padding:31px;border-radius:20px;
 background:#173f47;color:#fff;
 display:flex;flex-direction:column;justify-content:flex-end;
 box-shadow:0 23px 50px rgba(23,55,63,.17)
}
.hd-servicebox span{
 color:#dfb56a;font-size:10px;font-weight:900;letter-spacing:2px
}
.hd-servicebox strong{
 margin-top:38px;font-size:30px;letter-spacing:-1.5px
}
.hd-servicebox p{margin:7px 0 0;color:#c0d0d2;font-size:13px}

.hd-intro,.hd-local{
 max-width:1252px;margin:auto;
 padding:92px 34px 48px;
 display:grid;grid-template-columns:.8fr 1.2fr;
 gap:90px
}
.hd-intro h2,.hd-local h2{
 margin:15px 0 0;font-size:35px;
 line-height:1.3;letter-spacing:-2px
}
.hd-intro>p,.hd-local>p{
 margin:25px 0 0;color:#626c72;
 line-height:1.95;font-size:15px
}

.hd-checks{
 max-width:1252px;margin:auto;
 display:grid;grid-template-columns:repeat(3,1fr);
 border-top:1px solid #cfcec8;
 border-left:1px solid #cfcec8
}
.hd-check{
 min-height:210px;padding:28px;
 border-right:1px solid #cfcec8;
 border-bottom:1px solid #cfcec8
}
.hd-check>span{
 display:block;color:#b16a0c;
 font-size:11px;font-weight:900;margin-bottom:34px
}
.hd-check strong{font-size:19px;line-height:1.45}
.hd-check p{color:#7a8186;font-size:12px;line-height:1.7}

.hd-process{
 max-width:1252px;margin:auto;padding:105px 34px
}
.hd-heading h2{
 margin:15px 0 0;font-size:36px;letter-spacing:-2px
}
.hd-process ol{
 list-style:none;margin:40px 0 0;padding:0;
 border-top:1px solid #cdcec8
}
.hd-process li{
 display:grid;grid-template-columns:90px 1fr;
 gap:20px;padding:27px 0;
 border-bottom:1px solid #cdcec8
}
.hd-process li>span{
 color:#b16a0d;font-size:12px;font-weight:900
}
.hd-process strong{font-size:18px}
.hd-process li p{
 margin:8px 0 0;color:#747c81;font-size:13px;line-height:1.7
}

.hd-local{
 max-width:none;
 padding-left:max(34px,calc((100% - 1252px)/2 + 34px));
 padding-right:max(34px,calc((100% - 1252px)/2 + 34px));
 background:#eae3d6
}

.hd-faq-section{
 max-width:1252px;margin:auto;padding:100px 34px
}
.hd-faq-list{margin-top:38px}
.hd-faq{
 border-top:1px solid #cccdc7;padding:0
}
.hd-faq:last-child{border-bottom:1px solid #cccdc7}
.hd-faq summary{
 cursor:pointer;padding:24px 4px;
 font-size:17px;font-weight:900;list-style:none
}
.hd-faq summary::-webkit-details-marker{display:none}
.hd-faq p{
 margin:0;padding:0 4px 25px;
 color:#697278;font-size:14px;line-height:1.8
}

.hd-return{
 max-width:1252px;margin:0 auto 100px;
 padding:38px 44px;border-radius:16px;
 background:#173f47;color:#fff;
 display:flex;justify-content:space-between;align-items:center;gap:30px
}
.hd-return span{
 color:#dfb469;font-size:10px;font-weight:900;letter-spacing:2px
}
.hd-return h2{margin:9px 0 0;font-size:23px}
.hd-return>a{
 padding:13px 18px;border-radius:8px;
 background:#fff;color:#17343b;font-size:12px;font-weight:900
}

.hd-footer{
 padding:38px max(4.5vw,32px);
 background:#102027;color:#fff;
 display:flex;justify-content:space-between
}
.hd-footer span{color:#9cafb4;font-size:12px}

@media(max-width:900px){
 .hd-hero{grid-template-columns:1fr}
 .hd-intro,.hd-local{grid-template-columns:1fr;gap:20px}
 .hd-checks{grid-template-columns:1fr}
}

@media(max-width:650px){
 .hd-header{padding:0 20px}
 .hd-header nav{gap:14px;font-size:12px}
 .hd-breadcrumb{padding-left:20px}
 .hd-hero{padding:58px 20px;min-height:auto}
 .hd-hero h1{font-size:44px;letter-spacing:-2.6px}
 .hd-intro,.hd-local,.hd-process,.hd-faq-section{padding:70px 20px}
 .hd-checks{margin:0 20px}
 .hd-process li{grid-template-columns:45px 1fr}
 .hd-return{margin:0 20px 70px;padding:28px;display:block}
 .hd-return>a{display:inline-block;margin-top:22px}
 .hd-footer{display:block}
 .hd-footer span{display:block;margin-top:8px}
}
'''
    CSS.write_text(css, encoding="utf-8")


# ===== VERIFY =====
robots_fail = []
body_hashes = {}
detail_count = 0

for p in leaves:
    txt = p.read_text(encoding="utf-8")
    detail_count += 1

    head = txt.split("</head>",1)[0].lower()
    if "noindex" not in head or "follow" not in head:
        robots_fail.append(str(p))

    m = re.search(r"<body\b[^>]*>(.*?)</body>", txt, re.I|re.S)
    if m:
        h = hashlib.sha256(m.group(1).encode("utf-8")).hexdigest()
        body_hashes.setdefault(h,0)
        body_hashes[h] += 1

duplicate_bodies = sum(v-1 for v in body_hashes.values() if v > 1)

print()
print("=== DETAIL PAGE UPDATE ===")
print("FOUND =", len(leaves))
print("UPDATED =", updated)
print("EXPECTED =", 13 * 795)
print("ROBOTS_FAIL =", len(robots_fail))
print("DUPLICATE_BODY =", duplicate_bodies)
print("UNIQUE_BODY =", len(body_hashes))
print("BACKUP =", BACKUP)
