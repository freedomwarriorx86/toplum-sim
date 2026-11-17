# Toplum Simülasyonu

Kurgusal bir Türk ilçesinde geçen, 2–6 kişilik, gerçek zamanlı sosyoekonomik strateji oyunu.
Vanilla JS, tek dosya (`index.html`) + Supabase (veritabanı ve gerçek zamanlı senkron).

## Çalıştırma

- **Yerelde:** `python3 -m http.server 8080` → http://localhost:8080
- **Botlu demo:** adrese `?demo` ekle (ör. `index.html?demo`). Supabase gerekmez.
- **Canlı test:** GitHub Pages bu depodaki `index.html`'i yayınlar; her `git push` sonrası 1–2 dakikada güncellenir.

## Geliştirme akışı

1. `index.html` dosyasını düzenle.
2. `python3 build.py` çalıştır: kart/görev verisini (`data/seed.json`) dosyaya gömer ve artifact demosunu (`dist/demo.html`) üretir.
3. `git commit` + `git push`.

## Veritabanı

- `data/seed_cards.sql`: kart içerikleri
- `data/apply_card_effects.sql`: kart etkilerini tek UPDATE ile uygulayan fonksiyon
- `data/rooms_roles.sql`: odanın rol havuzu sütunu

Not: RLS kuralları prototip aşamasında herkese açık. Linki yalnızca test ekibiyle paylaş.
