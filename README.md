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
- `data/cleanup_rooms.sql`: iki günden eski odaları her gece silen pg_cron görevi (Supabase’de kurulu)
- `data/leaderboard.sql`: liderlik tablosu (`game_results`, odalardan bağımsız, temizlikte silinmez) ve yetkilerin tur sütunu
- `data/role_actions.sql`: rol yetkileri (eylem puanı) kayıt tablosu. Tablo yoksa oyun yetki panelini gizler.

## Denge

`tools/balance-sim.js` botlarla binlerce oyun oynatır ve görev başarı oranlarını basar. Görev eşikleri `index.html` içindeki `MISSION_RULE` tablosunda, ilçenin başlangıç değerine göre tanımlıdır; hedef her görev için yaklaşık %40–50 başarı.

Not: RLS kuralları prototip aşamasında herkese açık. Linki yalnızca test ekibiyle paylaş.

## Mobil uygulama (Capacitor)

Android projesi `android/` klasöründe. Web içeriği `python3 build.py --app` ile `dist/app/` altına üretilir: geliştirici modu çıkarılır, supabase-js ve yazı tipleri `vendor/` klasöründen yerel yüklenir (`tools/fetch_vendor.py` bunları indirir).

```sh
npm install
export JAVA_HOME=~/.local/opt/jdk-21 ANDROID_HOME=~/.local/opt/android-sdk   # JDK 21 + Android SDK 36
npm run apk        # -> android/app/build/outputs/apk/debug/app-debug.apk
```

İkon ve açılış ekranı kaynakları `assets/` altında; değiştirdikten sonra `npx capacitor-assets generate --android`.
Gradle 8.14 JDK 25 ile çalışmaz, JDK 21 kullan.
