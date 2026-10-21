from pathlib import Path
from datetime import datetime
import re, shutil

ROOT = Path(r"G:\homecare-metro-v1\homecare-metro-v2")
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "style.css"
IMG = ROOT / "assets" / "images" / "00-main-homecare.jpg"

if not IMG.exists():
    raise SystemExit("STOP: 00-main-homecare.jpg 파일이 없습니다.")

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f"_backup-main-image-{stamp}"
backup.mkdir()

shutil.copy2(INDEX, backup / "index.html")
shutil.copy2(CSS, backup / "style.css")

txt = INDEX.read_text(encoding="utf-8")

# 기존 오른쪽 CURRENT NETWORK 패널 교체
new_visual = '''
<div class="hm-main-visual">
  <img src="assets/images/00-main-homecare.jpg" alt="" loading="eager">
</div>
'''

txt = re.sub(
    r'<div class="hm-hero-panel">.*?</div>\s*</div>',
    new_visual + '\n  </div>',
    txt,
    count=1,
    flags=re.S
)

# 기존 카테고리 스트립 앞에 통계바 삽입
stats = '''
<section class="hm-network-strip">
  <div><strong>13</strong><span>서비스</span></div>
  <div><strong>795</strong><span>세부지역</span></div>
  <div><strong>256</strong><span>서울</span></div>
  <div><strong>451</strong><span>경기</span></div>
  <div><strong>88</strong><span>인천</span></div>
  <div><strong>12,460</strong><span>페이지</span></div>
</section>
'''

if 'class="hm-network-strip"' not in txt:
    txt = txt.replace(
        '<section class="hm-category-strip">',
        stats + '\n<section class="hm-category-strip">',
        1
    )

INDEX.write_text(txt, encoding="utf-8")

css = CSS.read_text(encoding="utf-8")

if "HOMECARE MAIN IMAGE V8" not in css:
    css += r'''

/* =====================================================
   HOMECARE MAIN IMAGE V8
   ===================================================== */

.hm-main-visual{
  width:100%;
  min-height:420px;
  border-radius:22px;
  overflow:hidden;
  box-shadow:0 24px 55px rgba(20,44,56,.18);
  background:#dfe7e5;
}

.hm-main-visual img{
  display:block;
  width:100%;
  height:100%;
  min-height:420px;
  object-fit:cover;
  object-position:center;
}

.hm-network-strip{
  max-width:1320px;
  margin:-28px auto 0;
  position:relative;
  z-index:3;
  display:grid;
  grid-template-columns:repeat(6,1fr);
  background:#173f47;
  color:#fff;
  border-radius:14px;
  overflow:hidden;
  box-shadow:0 18px 40px rgba(23,55,63,.16);
}

.hm-network-strip div{
  min-height:92px;
  padding:18px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  border-right:1px solid rgba(255,255,255,.12);
}

.hm-network-strip div:last-child{
  border-right:0;
}

.hm-network-strip strong{
  font-size:23px;
  line-height:1;
}

.hm-network-strip span{
  margin-top:7px;
  color:#c8d7da;
  font-size:11px;
}

@media(max-width:900px){
  .hm-main-visual,
  .hm-main-visual img{
    min-height:340px;
  }

  .hm-network-strip{
    margin:-18px 20px 0;
    grid-template-columns:repeat(3,1fr);
  }
}

@media(max-width:560px){
  .hm-main-visual,
  .hm-main-visual img{
    min-height:260px;
  }

  .hm-network-strip{
    grid-template-columns:repeat(2,1fr);
  }
}
'''

    CSS.write_text(css, encoding="utf-8")

print("MAIN IMAGE APPLY PASS")
print("BACKUP =", backup)
