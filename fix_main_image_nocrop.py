from pathlib import Path

p = Path(r"G:\homecare-metro-v1\homecare-metro-v2\assets\style.css")
css = p.read_text(encoding="utf-8")

css += r'''

/* MAIN IMAGE NO CROP */
.hm-main-visual{
  background:#f2f2ee;
  min-height:0;
}

.hm-main-visual img{
  width:100%;
  height:auto;
  min-height:0;
  max-height:none;
  object-fit:contain;
  object-position:center;
}
'''

p.write_text(css, encoding="utf-8")
print("MAIN IMAGE NO CROP PASS")
