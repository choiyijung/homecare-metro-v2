# -*- coding: utf-8 -*-
from pathlib import Path
import argparse, csv, html, json, re, shutil, urllib.request, zipfile

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SERVICES = json.loads((DATA / "services.json").read_text(encoding="utf-8"))
MOIS_URL = "https://www.mois.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_00147311ctH5-ah&fileSn=1"

SEOUL_SLUG = {
"종로구":"jongno-gu","중구":"jung-gu","용산구":"yongsan-gu","성동구":"seongdong-gu","광진구":"gwangjin-gu","동대문구":"dongdaemun-gu",
"중랑구":"jungnang-gu","성북구":"seongbuk-gu","강북구":"gangbuk-gu","도봉구":"dobong-gu","노원구":"nowon-gu","은평구":"eunpyeong-gu",
"서대문구":"seodaemun-gu","마포구":"mapo-gu","양천구":"yangcheon-gu","강서구":"gangseo-gu","구로구":"guro-gu","금천구":"geumcheon-gu",
"영등포구":"yeongdeungpo-gu","동작구":"dongjak-gu","관악구":"gwanak-gu","서초구":"seocho-gu","강남구":"gangnam-gu","송파구":"songpa-gu","강동구":"gangdong-gu"
}
GG_CITY_SLUG = {
"가평군":"gapyeong","과천시":"gwacheon","광명시":"gwangmyeong","광주시":"gwangju","구리시":"guri","군포시":"gunpo","김포시":"gimpo",
"고양시":"goyang","남양주시":"namyangju","동두천시":"dongducheon","부천시":"bucheon","성남시":"seongnam","수원시":"suwon","시흥시":"siheung",
"안산시":"ansan","안성시":"anseong","안양시":"anyang","양주시":"yangju","양평군":"yangpyeong","여주시":"yeoju","연천군":"yeoncheon",
"오산시":"osan","용인시":"yongin","의왕시":"uiwang","의정부시":"uijeongbu","이천시":"icheon","파주시":"paju","평택시":"pyeongtaek",
"포천시":"pocheon","하남시":"hanam","화성시":"hwaseong"
}
GU_SLUG = {
"덕양구":"deogyang-gu","일산동구":"ilsandong-gu","일산서구":"ilsanseo-gu","원미구":"wonmi-gu","소사구":"sosa-gu","오정구":"ojeong-gu",
"수정구":"sujeong-gu","중원구":"jungwon-gu","분당구":"bundang-gu","권선구":"gwonseon-gu","영통구":"yeongtong-gu","장안구":"jangan-gu","팔달구":"paldal-gu",
"단원구":"danwon-gu","상록구":"sangnok-gu","동안구":"dongan-gu","만안구":"manan-gu","기흥구":"giheung-gu","수지구":"suji-gu","처인구":"cheoin-gu",
"만세구":"manse-gu","효행구":"hyohaeng-gu","병점구":"byeongjeom-gu","동탄구":"dongtan-gu",
"강화군":"ganghwa","옹진군":"ongjin","제물포구":"jemulpo-gu","영종구":"yeongjong-gu","미추홀구":"michuhol-gu","연수구":"yeonsu-gu",
"남동구":"namdong-gu","부평구":"bupyeong-gu","계양구":"gyeyang-gu","서해구":"seohae-gu","검단구":"geomdan-gu"
}
GU_SLUG.update(SEOUL_SLUG)

def norm_town(name):
    name=name.strip()
    m=re.match(r'^([가-힣]+?)(?:제)?([0-9]+)동$',name)
    return m.group(1)+"동" if m else name

def safe_write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8")

def relprefix(path):
    return "../"*(len(path.relative_to(ROOT).parts)-1)

def shell(title,desc,body,prefix):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc[:155])}">
<meta name="robots" content="noindex,follow">
<link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><div class="top"><div class="wrap">SEOUL · GYEONGGI · INCHEON HOMECARE NETWORK</div></div>
<header class="header"><div class="wrap"><a class="brand" href="{prefix}index.html">HOME<span>CARE</span> METRO</a>
<nav class="nav"><a href="{prefix}index.html#services">서비스</a><a href="{prefix}index.html#regions">지역</a></nav></div></header>
{body}
<footer class="footer"><div class="wrap"><strong>HOMECARE METRO</strong><br>서울 · 경기 · 인천 생활설비 지역 안내</div></footer>
<script src="{prefix}assets/app.js"></script></body></html>'''

def cards(items):
    return '<div class="localgrid">' + ''.join(
        f'<a class="local" href="{html.escape(href)}">{html.escape(name)}</a>' for name,href in items
    ) + '</div>'

def area_label(r):
    return " ".join(x for x in [r["area"],r.get("city",""),r.get("gu",""),r["town"]] if x)

def region_parent_dir(r,service_slug=None):
    root=ROOT/("services" if service_slug else "regions")
    if service_slug: root=root/service_slug
    if r["area"]=="서울":
        return root/"seoul"/SEOUL_SLUG[r["gu"]]
    if r["area"]=="경기":
        d=root/"gyeonggi"/GG_CITY_SLUG[r["city"]]
        if r["gu"]: d=d/GU_SLUG[r["gu"]]
        return d
    if r["area"]=="인천":
        return root/"incheon"/GU_SLUG[r["gu"]]
    raise ValueError(r)

def download_zip(target):
    print("공식 주소코드 다운로드 중...")
    req=urllib.request.Request(MOIS_URL,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=90) as resp:
        target.write_bytes(resp.read())
    if target.stat().st_size < 100000:
        raise RuntimeError("다운로드 파일 크기가 비정상적으로 작습니다.")
    print("다운로드 완료:",target.stat().st_size,"bytes")

def read_admin_text(zip_path):
    work=ROOT/"_official-address-code"
    if work.exists(): shutil.rmtree(work)
    work.mkdir()
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(work)
    candidates=[p for p in work.rglob("*") if p.is_file() and p.name.upper().startswith("KIKCD_H.20260720") and p.suffix.lower() not in {".xls",".xlsx"}]
    if not candidates:
        raise RuntimeError("KIKcd_H.20260720 행정동 파일을 찾지 못했습니다.")
    f=max(candidates,key=lambda p:p.stat().st_size)
    b=f.read_bytes()
    for enc in ("cp949","utf-8"):
        try:
            t=b.decode(enc)
            if all(k in t for k in ("서울특별시","경기도","인천광역시")):
                print("행정동 원본:",f.name,"/ 인코딩:",enc)
                return t
        except UnicodeDecodeError:
            pass
    raise RuntimeError("행정동 파일 인코딩 판별 실패")

def parse(text):
    rows=[]
    for line in text.splitlines():
        if "서울특별시" in line:
            m=re.search(r'서울특별시\s+(?P<gu>[가-힣]+구)\s+(?P<town>[가-힣0-9.]+(?:읍|면|동))(?:\s|$)',line)
            if m: rows.append(("서울","",m["gu"],m["town"]))
        elif "경기도" in line:
            m=re.search(r'경기도\s+(?P<city>[가-힣]+(?:시|군))(?:\s+(?P<gu>[가-힣]+구))?\s+(?P<town>[가-힣0-9.]+(?:읍|면|동))(?:\s|$)',line)
            if m: rows.append(("경기",m["city"],m["gu"] or "",m["town"]))
        elif "인천광역시" in line:
            m=re.search(r'인천광역시\s+(?P<gu>[가-힣]+(?:구|군))\s+(?P<town>[가-힣0-9.]+(?:읍|면|동))(?:\s|$)',line)
            if m and m["gu"] in GU_SLUG: rows.append(("인천","",m["gu"],m["town"]))
    grouped={}
    for area,city,gu,raw in rows:
        town=norm_town(raw)
        grouped.setdefault((area,city,gu,town),set()).add(raw)
    out=[]
    for (area,city,gu,town),raws in sorted(grouped.items()):
        out.append({"area":area,"city":city,"gu":gu,"town":town,"type":town[-1],"raw_names":sorted(raws)})
    return out

def validate(rows):
    errors=[]
    for r in rows:
        if r["area"]=="서울" and r["gu"] not in SEOUL_SLUG: errors.append(r)
        if r["area"]=="경기" and r["city"] not in GG_CITY_SLUG: errors.append(r)
        if r["area"]=="경기" and r["gu"] and r["gu"] not in GU_SLUG: errors.append(r)
        if r["area"]=="인천" and r["gu"] not in GU_SLUG: errors.append(r)
    if errors:
        print("매핑 오류 샘플:",errors[:20])
        raise RuntimeError("상위지역 매핑 오류: "+str(len(errors)))
    if len(rows)!=len({(r["area"],r["city"],r["gu"],r["town"]) for r in rows}):
        raise RuntimeError("읍면동 중복 발생")

def replace_parent_index(parent,title,intro,items):
    p=parent/"index.html"
    prefix=relprefix(p)
    body=f'''<main><div class="wrap crumb"><a href="{prefix}index.html">HOME</a> / 지역</div>
<section class="hero"><div class="wrap"><div class="kicker">LOCAL DIRECTORY</div><h1>{html.escape(title)}</h1><p>{html.escape(intro)}</p></div></section>
<section class="section"><div class="wrap"><h2>동·읍·면 선택</h2><p class="lead">{len(items)}개 세부 지역을 확인할 수 있습니다.</p>{cards(items)}</div></section></main>'''
    safe_write(p,shell(title,intro,body,prefix))

def make_leaf(r,service=None):
    parent=region_parent_dir(r,service["slug"] if service else None)
    p=parent/r["town"]/"index.html"
    prefix=relprefix(p)
    loc=area_label(r)
    if service:
        title=f"{loc} {service['name']}"
        desc=f"{loc} {service['name']} 지역 안내 페이지입니다. 현장 조건과 필요한 작업 범위를 확인할 수 있도록 구성했습니다."
        h1=f"{loc} {service['name']}"
        body2='<div class="notice">현장 방문 전 증상·위치·작업 범위를 확인한 뒤 상담하는 구조입니다. 최종 SEO 문구는 마지막 단계에서 적용합니다.</div>'
    else:
        title=f"{loc} 홈케어 지역"
        desc=f"{loc}의 홈케어 서비스 지역 안내입니다."
        h1=loc
        body2='<div class="grid">'+''.join(
            f'<a class="card" href="{prefix}services/{s["slug"]}/index.html"><small>{s["group"]}</small><h3>{s["name"]}</h3><p>{s["short"]}</p></a>'
            for s in SERVICES)+'</div>'
    body=f'''<main><div class="wrap crumb"><a href="{prefix}index.html">HOME</a> / {html.escape(loc)}</div>
<section class="hero"><div class="wrap"><div class="kicker">LOCAL AREA</div><h1>{html.escape(h1)}</h1><p>{html.escape(desc)}</p></div></section>
<section class="section"><div class="wrap"><h2>{'지역 서비스 안내' if service else '서비스 선택'}</h2>{body2}</div></section></main>'''
    safe_write(p,shell(title,desc,body,prefix))

def build(rows):
    (DATA/"regions-full-20260720.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    with (DATA/"regions-full-20260720.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["area","city","gu","town","type","raw_names"])
        w.writeheader()
        for r in rows:
            x=dict(r); x["raw_names"]=",".join(x["raw_names"]); w.writerow(x)
    groups={}
    for r in rows:
        groups.setdefault((r["area"],r["city"],r["gu"]),[]).append(r)
    for items in groups.values():
        sample=items[0]
        label=" ".join(x for x in [sample["area"],sample["city"],sample["gu"]] if x)
        parent=region_parent_dir(sample)
        links=[(r["town"],r["town"]+"/index.html") for r in sorted(items,key=lambda x:(x["type"],x["town"]))]
        replace_parent_index(parent,f"{label} 홈케어 지역",f"{label}의 동·읍·면 단위 지역을 선택하세요.",links)
        for r in items: make_leaf(r)
    for i,s in enumerate(SERVICES,1):
        print(f"[{i}/{len(SERVICES)}] {s['name']} 생성")
        for items in groups.values():
            sample=items[0]
            label=" ".join(x for x in [sample["area"],sample["city"],sample["gu"]] if x)
            parent=region_parent_dir(sample,s["slug"])
            links=[(r["town"],r["town"]+"/index.html") for r in sorted(items,key=lambda x:(x["type"],x["town"]))]
            replace_parent_index(parent,f"{label} {s['name']}",f"{label}의 동·읍·면별 {s['name']} 지역을 선택하세요.",links)
            for r in items: make_leaf(r,s)
    paths=[]
    for f in ROOT.rglob("index.html"):
        rel=f.relative_to(ROOT).as_posix()
        paths.append("/"+rel[:-10])
    (ROOT/"sitemap-paths.txt").write_text("\n".join(sorted(set(paths)))+"\n",encoding="utf-8")
    print("\n=== V2 생성 완료 ===")
    for a in ("서울","경기","인천"):
        print(a,":",sum(r["area"]==a for r in rows))
    print("읍:",sum(r["type"]=="읍" for r in rows),"면:",sum(r["type"]=="면" for r in rows),"동:",sum(r["type"]=="동" for r in rows))
    print("서비스:",len(SERVICES))
    print("전체 HTML:",sum(1 for _ in ROOT.rglob("index.html")))
    print("최종 SEO: 미적용 / 상세페이지 noindex,follow")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--zip",help="이미 받은 행정안전부 주소코드 ZIP")
    args=ap.parse_args()
    if args.zip:
        z=Path(args.zip).resolve()
        if not z.is_file(): raise SystemExit("ZIP 파일 없음: "+str(z))
    else:
        z=ROOT/"_official-address-code-20260720.zip"
        if not z.exists(): download_zip(z)
    text=read_admin_text(z)
    rows=parse(text)
    validate(rows)
    print("파싱 완료:",len(rows))
    build(rows)

if __name__=="__main__":
    main()
