# -*- coding: utf-8 -*-
"""
기존 서울·경기·인천 사이트의 지역 폴더를 읽어 regions.json의 동·읍·면 children을 채우는 보조 도구.
사용 예:
  python import_regions_from_reference.py --source "D:\기존지역사이트" --output "data\regions-imported.json"

주의:
- 기존 사이트 구조가 사이트마다 다르므로 이 파일은 '읽기 전용 추출'만 합니다.
- 원본 파일은 수정하지 않습니다.
- 추출 결과를 검토한 뒤 regions.json으로 교체하세요.
"""
from pathlib import Path
import argparse, json

SEOUL_GU = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
GYEONGGI_MUNI = ['가평군', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '고양시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시']
INCHEON_GU = ['강화군', '옹진군', '제물포구', '영종구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서해구', '검단구']
GG_GU = {'고양시': ['고양덕양구', '고양일산동구', '고양일산서구'], '부천시': ['부천원미구', '부천소사구', '부천오정구'], '성남시': ['성남수정구', '성남중원구', '성남분당구'], '수원시': ['수원권선구', '수원영통구', '수원장안구', '수원팔달구'], '안산시': ['안산단원구', '안산상록구'], '안양시': ['안양동안구', '안양만안구'], '용인시': ['용인기흥구', '용인수지구', '용인처인구'], '화성시': ['화성만세구', '화성효행구', '화성병점구', '화성동탄구']}

def dirs(p):
    if not p.exists(): return []
    return sorted([x.name for x in p.iterdir() if x.is_dir() and (x/"index.html").exists()])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--output", default="data/regions-imported.json")
    a=ap.parse_args()
    root=Path(a.source)
    out={"서울":{"children":{}},"경기":{"children":{}},"인천":{"children":{}}}

    for gu in SEOUL_GU:
        p=root/gu
        out["서울"]["children"][gu]={"children":dirs(p)}

    for city in GYEONGGI_MUNI:
        if city in GG_GU:
            out["경기"]["children"][city]={"children":{}}
            for gu_folder in GG_GU[city]:
                p=root/gu_folder
                out["경기"]["children"][city]["children"][gu_folder]={"children":dirs(p)}
        else:
            p=root/city
            out["경기"]["children"][city]={"children":dirs(p)}

    for gu in INCHEON_GU:
        # 2026 인천 개편명과 과거 원본 폴더명이 다를 수 있으므로 결과 확인 필수
        p=root/gu
        out["인천"]["children"][gu]={"children":dirs(p)}

    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print("추출 완료:", a.output)

if __name__=="__main__": main()
