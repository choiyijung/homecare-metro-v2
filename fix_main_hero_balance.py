from pathlib import Path

CSS = Path(r"G:\homecare-metro-v1\homecare-metro-v2\assets\style.css")
css = CSS.read_text(encoding="utf-8")

css += r'''

/* =====================================================
   HOME MAIN HERO BALANCE V9
   ===================================================== */

.hm-hero{
  padding-top:70px;
  padding-bottom:66px;
}

.hm-hero-inner{
  max-width:1320px;
  grid-template-columns:minmax(0,1.05fr) minmax(480px,.95fr);
  gap:55px;
}

.hm-hero h1{
  max-width:760px;
  font-size:clamp(44px,4.15vw,63px);
  line-height:1.08;
  letter-spacing:-3.4px;
  word-break:keep-all;
}

.hm-hero-copy>p{
  margin-top:27px;
  font-size:16px;
  line-height:1.8;
}

.hm-main-visual{
  width:100%;
  height:440px;
  min-height:440px;
  max-height:440px;
  border-radius:22px;
  overflow:hidden;
}

.hm-main-visual img{
  width:100%;
  height:100%;
  min-height:440px;
  max-height:440px;
  object-fit:cover;
  object-position:center;
}

.hm-network-strip{
  margin-top:-30px;
}

.hm-category-strip{
  margin-top:18px;
}

@media(max-width:1100px){
  .hm-hero-inner{
    grid-template-columns:minmax(0,1fr) minmax(400px,.85fr);
    gap:38px;
  }

  .hm-hero h1{
    font-size:clamp(42px,4.4vw,56px);
  }

  .hm-main-visual,
  .hm-main-visual img{
    height:390px;
    min-height:390px;
    max-height:390px;
  }
}

@media(max-width:900px){
  .hm-hero-inner{
    grid-template-columns:1fr;
  }

  .hm-hero h1{
    max-width:720px;
    font-size:clamp(40px,7vw,56px);
  }

  .hm-main-visual,
  .hm-main-visual img{
    height:auto;
    min-height:0;
    max-height:none;
  }

  .hm-main-visual img{
    aspect-ratio:16/9;
    object-fit:cover;
  }
}
'''

CSS.write_text(css, encoding="utf-8")
print("MAIN HERO BALANCE PASS")
