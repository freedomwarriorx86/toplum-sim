#!/usr/bin/env python3
"""Mobil uygulama için dış kaynakları (supabase-js, Google Fonts) vendor/ klasörüne indirir.
Uygulama bu sayede yazı tipleri ve kütüphane için CDN'e muhtaç kalmaz. Bir kez çalıştırmak yeter."""
import pathlib, re, urllib.request

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "vendor"; (out / "fonts").mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

src = (root / "index.html").read_text(encoding="utf-8")
sb = re.search(r'<script src="(https://cdn\.jsdelivr\.net/npm/@supabase[^"]+)"', src).group(1)
(out / "supabase.min.js").write_bytes(get(sb))
font_css_url = re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)"', src).group(1).replace("&amp;", "&")
css = get(font_css_url).decode()
for i, u in enumerate(dict.fromkeys(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
    name = f"f{i}.woff2"; (out / "fonts" / name).write_bytes(get(u)); css = css.replace(u, f"fonts/{name}")
(out / "fonts.css").write_text(css, encoding="utf-8")
print("vendor/ hazır:", sb, "ve", css.count("@font-face"), "font-face")
