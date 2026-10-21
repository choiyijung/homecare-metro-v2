from pathlib import Path
import re

p = Path(r"G:\homecare-metro-v1\homecare-metro-v2\index.html")
txt = p.read_text(encoding="utf-8")

txt, n = re.subn(
    r'<section class="hm-network-strip">.*?</section>',
    '',
    txt,
    count=1,
    flags=re.S
)

p.write_text(txt, encoding="utf-8")

print("NETWORK STRIP REMOVE =", n)
