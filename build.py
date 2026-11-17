#!/usr/bin/env python3
"""index.html'e kart/görev verisini gömer ve artifact için demo.html üretir.

Kullanım: python3 build.py
- data/seed.json  -> index.html içindeki /*SEED*/.../*/SEED*/ bloğu
- dist/demo.html  -> FORCE_DEMO=true, Supabase betiği ve anahtarları çıkarılmış sürüm
"""
import json, re, pathlib

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

demo = src.replace("const FORCE_DEMO=false;", "const FORCE_DEMO=true;")
demo = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/@supabase[^"]*"></script>\n?', "", demo)
demo = re.sub(r"const SURL='[^']*';", "const SURL='';", demo)
demo = re.sub(r"const SKEY='[^']*';", "const SKEY='';", demo)
# Artifact iskeleti doctype/html/head/body'yi kendisi ekler
for pat in (r"<!DOCTYPE html>\n?", r"<html[^>]*>\n?", r"</?head>\n?", r"<meta charset[^>]*>\n?",
            r"<meta name=\"viewport\"[^>]*>\n?", r"</?body>\n?", r"</html>\n?"):
    demo = re.sub(pat, "", demo, flags=re.I)
(root / "dist").mkdir(exist_ok=True)
(root / "dist/demo.html").write_text(demo, encoding="utf-8")
print("index.html ve dist/demo.html hazır:", len(seed["cards"]), "kart,", len(seed["missions"]), "görev")
