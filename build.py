#!/usr/bin/env python3
"""index.html'e kart/görev verisini gömer, artifact demosunu ve istenirse yayın sürümünü üretir.

Kullanım:
  python3 build.py          -> index.html (geliştirme, DEV kodu dahil) + dist/demo.html
  python3 build.py --prod   -> ek olarak dist/prod/index.html: geliştirici modu tamamen çıkarılmış yayın sürümü

Geliştirici kodu şu işaretlerin arasında durur ve --prod / demo derlemesinde silinir:
  JS/CSS:  /*DEV-START*/ ... /*DEV-END*/
  HTML:    <!--DEV-START--> ... <!--DEV-END-->
"""
import json, re, sys, pathlib

root = pathlib.Path(__file__).parent
seed = json.loads((root / "data/seed.json").read_text(encoding="utf-8"))
# Demo için gerekli alanlar
seed = {
    "cards": [{k: c.get(k) for k in ("id", "type", "title", "description", "options", "effects", "budget_effect", "stat_effects")} for c in seed["cards"]],
    "missions": [{k: m.get(k) for k in ("id", "code", "title", "description", "win_condition", "target_metric", "target_value", "target_direction")} for m in seed["missions"]],
}
seed_js = json.dumps(seed, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

src = (root / "index.html").read_text(encoding="utf-8")
src, n = re.subn(r"/\*SEED\*/.*?/\*/SEED\*/", lambda _: "/*SEED*/" + seed_js + "/*/SEED*/", src, flags=re.S)
assert n == 1, "SEED bloğu bulunamadı"
(root / "index.html").write_text(src, encoding="utf-8")


def strip_dev(text: str) -> str:
    """Geliştirici modunu siler ve hiçbir iz kalmadığını doğrular."""
    a = text.count("/*DEV-START*/") + text.count("<!--DEV-START-->")
    b = text.count("/*DEV-END*/") + text.count("<!--DEV-END-->")
    assert a == b and a > 0, f"DEV işaretleri dengesiz: {a} başlangıç, {b} bitiş"
    text = re.sub(r"/\*DEV-START\*/.*?/\*DEV-END\*/\n?", "", text, flags=re.S)
    text = re.sub(r"<!--DEV-START-->.*?<!--DEV-END-->\n?", "", text, flags=re.S)
    for leftover in ("DEV_CODE", "TSDEV", "devStart", "s-dev", "devbar", "DEV-START", "DEV-END"):
        assert leftover not in text, f"Geliştirici kodu kalmış: {leftover}"
    return text


clean = strip_dev(src)

demo = clean.replace("const FORCE_DEMO=false;", "const FORCE_DEMO=true;")
demo = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/@supabase[^"]*"></script>\n?', "", demo)
demo = re.sub(r"const SURL='[^']*';", "const SURL='';", demo)
demo = re.sub(r"const SKEY='[^']*';", "const SKEY='';", demo)
# Artifact iskeleti doctype/html/head/body'yi kendisi ekler
for pat in (r"<!DOCTYPE html>\n?", r"<html[^>]*>\n?", r"</?head>\n?", r"<meta charset[^>]*>\n?",
            r"<meta name=\"viewport\"[^>]*>\n?", r"</?body>\n?", r"</html>\n?"):
    demo = re.sub(pat, "", demo, flags=re.I)
(root / "dist").mkdir(exist_ok=True)
(root / "dist/demo.html").write_text(demo, encoding="utf-8")
print("index.html (geliştirme) ve dist/demo.html hazır:", len(seed["cards"]), "kart,", len(seed["missions"]), "görev")

if "--prod" in sys.argv:
    (root / "dist/prod").mkdir(parents=True, exist_ok=True)
    (root / "dist/prod/index.html").write_text(clean, encoding="utf-8")
    print("dist/prod/index.html hazır: geliştirici modu çıkarıldı, kalıntı kontrolü geçti.")
