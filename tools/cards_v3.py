#!/usr/bin/env python3
"""v3 kart içeriği: olay kartlarına tepki seçenekleri ve 8 yeni kriz kartı.
data/seed.json'u günceller ve veritabanına uygulanacak data/seed_cards_v3.sql dosyasını yazar."""
import json, pathlib, uuid

root = pathlib.Path(__file__).resolve().parent.parent
seed_p = root / "data/seed.json"
seed = json.loads(seed_p.read_text(encoding="utf-8"))

def o(label, cost, effects, icon="", desc=None):
    d = {"label": label, "cost": cost, "icon": icon, "effects": effects}
    if desc: d["desc"] = desc
    return d

# Olay kendiliğinden olur (taban etki), oyuncu ek olarak tepkisini seçer
EVENT_OPTIONS = {
  "Bağ Bozumu Festivali": [o("Festivali bir hafta uzat",-25000,{"social":3},"🍇"), o("Sponsorluğu iş insanına ver",15000,{"suspicion":4,"businessman_cash":40000},"🤝","Kasaya para girer, afişlerde onun adı yazar."), o("Planlandığı gibi bitir",0,{},"✓")],
  "Bakanlık Hibesi": [o("Hibeyi doğrudan okullara aktar",-60000,{"education":5},"🏫"), o("Hibeyi kasada tut",0,{},"🏦"), o("Tablet ihalesini tanıdık firmaya ver",0,{"education":1,"suspicion":8,"businessman_cash":70000},"📦")],
  "Basında Yolsuzluk Haberi": [o("Basın toplantısıyla açıklama yap",-5000,{"social":2,"suspicion":-4},"🎙️"), o("Gazeteye dava aç",-15000,{"social":-2,"suspicion":-6},"⚖️","Haber susar, basın özgürlüğü tartışması başlar."), o("Sessiz kal",0,{},"🤐")],
  "Bisiklet Yolu Bağışı": [o("Bisiklet paylaşım sistemi kur",-30000,{"transport":3,"health":2},"🚲"), o("Açılış töreni düzenle",-5000,{"social":2},"🎀"), o("Yolun bir kısmını otoparka çevir",10000,{"transport":-2,"health":-1,"businessman_cash":20000},"🅿️")],
  "Çete Kavgası": [o("Sahil yoluna aydınlatma ve kamera",-40000,{"security":5},"💡"), o("Gençlik merkezinde gece programı",-25000,{"social":3,"security":2},"🏀"), o("Olayı küçümse",0,{"social":-2},"🙈")],
  "Deprem Tatbikatı": [o("Okullarda güçlendirme taraması başlat",-50000,{"security":3,"education":2},"🏗️"), o("Tatbikatı her yıl tekrarla",-10000,{"security":2},"📅"), o("Raporu rafa kaldır",0,{},"🗄️")],
  "Doğa Turizmi Projesi": [o("Parkurlara rehberli tur koy",-15000,{"social":2,"health":1},"🥾"), o("Vadide otel inşaatına izin ver",40000,{"health":-2,"suspicion":5,"businessman_cash":80000},"🏨"), o("Doğal hâlinde bırak",0,{},"🌲")],
  "Doktor İstifaları": [o("Doktorlara lojman ve prim ver",-60000,{"health":5},"🏠"), o("Özel hastaneyle sevk anlaşması yap",-20000,{"health":3,"suspicion":5,"businessman_cash":50000},"🏥"), o("Bakanlıktan atama bekle",0,{"social":-2},"⏳")],
  "Genç Girişimci Fuarı": [o("Kazananlara belediye ofisi ver",-20000,{"education":2,"social":2},"🏢"), o("Fuarı iş insanının şirketine devret",10000,{"suspicion":4,"businessman_cash":60000},"💼"), o("Teşekkür et, kapat",0,{},"👋")],
  "Kanalizasyon Taştı": [o("Hattı baştan yenile",-70000,{"health":5,"social":1},"🔧"), o("Geçici pompa getir",-15000,{"health":2},"🚰"), o("Esnafa vergi indirimi yap",-20000,{"social":3},"🧾")],
  "Okulda Yangın": [o("Konteyner sınıf kur",-35000,{"education":4},"📦"), o("Öğrencileri komşu okula taşı",-5000,{"education":2,"transport":-2},"🚌"), o("Tüm okullarda yangın denetimi",-25000,{"security":3,"education":1},"🧯")],
  "Sosyal Medyada Viral Video": [o("Zabıta memurunu ödüllendir",-5000,{"social":2},"🏅"), o("Videoyu tanıtım kampanyasına çevir",-20000,{"social":3,"suspicion":-3},"📣"), o("Gündemi kendi hâline bırak",0,{},"📱")],
  "Tarımsal Destek Programı": [o("Üretici kooperatifi kur",-25000,{"social":3,"health":1},"🌾"), o("Ürünü okul yemeklerine al",-20000,{"health":2,"education":1},"🥕"), o("Desteği iş insanının çiftliğine yönlendir",0,{"social":-2,"suspicion":7,"businessman_cash":60000},"🚜")],
  "Tekstil Fabrikası Kapandı": [o("İşsizlere meslek kursu aç",-40000,{"social":4,"education":2},"🧵"), o("Binayı teşvikle yeni yatırımcıya ver",-20000,{"social":2,"businessman_cash":90000},"🏭"), o("Bekle ve gör",0,{"social":-2},"⏳")],
  "Toplu İşten Çıkarma": [o("Geçici istihdam programı başlat",-50000,{"social":5},"👷"), o("Firmayla arabuluculuk yap",-5000,{"social":2},"🤝"), o("Firmaya vergi cezası kes",25000,{"social":1,"businessman_cash":-50000},"🧾")],
  "Vergi Denetimi": [o("Tahsilatı yollara harca",-30000,{"transport":3,"health":1},"🛣️"), o("Kasaya koy",0,{},"🏦"), o("İş insanına af sözü ver",-20000,{"suspicion":8,"businessman_cash":50000},"🤫")],
  "Yeni Aile Sağlığı Merkezi": [o("Merkez gece de açık olsun",-30000,{"health":3},"🌙"), o("Mobil sağlık aracı ekle",-20000,{"health":2,"transport":1},"🚑"), o("Açılışı mitinge çevir",-10000,{"social":2,"suspicion":3},"🎤")],
  "Zincirleme Trafik Kazası": [o("Sis uyarı sistemi kur",-35000,{"transport":3,"security":2},"🌫️"), o("Hız sınırını düşür",0,{"transport":-1,"security":2},"🚸"), o("Yol genişletme ihalesine çık",-60000,{"transport":5,"suspicion":5,"businessman_cash":60000},"🚧")],
}

NEW_CRISES = [
  ("Otopark Krizi","Çarşıda park yeri kalmadı. Esnaf müşterilerin AVM'ye kaçtığını söylüyor, kaldırımlar araçlarla dolu.",
   [o("Katlı otopark yap",-90000,{"transport":5,"social":1},"🅿️"), o("Çarşıyı yayalaştır, aktarma otoparkı kur",-40000,{"transport":2,"health":2,"social":-1},"🚶"), o("Otoparkları özel şirkete devret",50000,{"transport":2,"suspicion":8,"businessman_cash":80000},"💳")]),
  ("Sokak Hayvanları Tartışması","Bir çocuğun ısırılmasının ardından mahalle ikiye bölündü. Hayvanseverler ve veliler belediye önünde.",
   [o("Barınak ve veteriner kliniği kur",-45000,{"health":2,"social":3},"🐕"), o("Kısırlaştırma ve aşı kampanyası",-20000,{"health":1,"social":2},"💉"), o("Hayvanları ilçe dışına bıraktır",-5000,{"social":-5,"security":1},"🚚")]),
  ("Elektrik Zammı Protestosu","Faturalar iki katına çıktı. Dar gelirli mahallelerde kaçak bağlantılar artıyor, gece eylemleri başladı.",
   [o("Dar gelirliye sosyal tarife",-60000,{"social":5},"🧾"), o("Belediye binalarına güneş paneli",-80000,{"social":1,"health":1},"☀️","Uzun vadede fatura yükü azalır."), o("Kaçak bağlantılara göz yum",0,{"social":2,"security":-3,"suspicion":4},"🔌")]),
  ("Siber Saldırı","Belediyenin bütün bilgisayarları fidye yazılımıyla kilitlendi. Ruhsat, su faturası ve otobüs kartı sistemleri çalışmıyor.",
   [o("Fidyeyi gizlice öde",-70000,{"security":1,"suspicion":6},"💸"), o("Sistemi sıfırdan kur",-90000,{"security":4},"🛡️"), o("Yedeklerle idare et, hizmet aksasın",-10000,{"social":-3,"transport":-2},"💾")]),
  ("Kentsel Dönüşüm Teklifi","Bir müteahhit depreme dayanıksız eski mahalleyi yıkıp yeniden yapmayı teklif ediyor. Mahalleli evlerini kaybetmekten korkuyor.",
   [o("Mahalleliyle birlikte, oylamayla yap",-10000,{"social":2,"security":3},"🗳️"), o("Projeyi müteahhide devret",80000,{"security":3,"social":-4,"suspicion":10,"businessman_cash":150000},"🏗️"), o("Teklifi reddet",0,{"security":-2},"✋")]),
  ("Semt Pazarı Taşınıyor","Trafik gerekçesiyle semt pazarının şehir dışına taşınması gündemde. Pazarcılar ve emekliler karşı çıkıyor.",
   [o("Yerinde kapalı pazar yeri yap",-60000,{"social":3,"health":2},"🧺"), o("Pazar eski yerinde kalsın",0,{"transport":-3},"📍"), o("Pazar alanını AVM'ye sat",40000,{"social":-4,"suspicion":6,"businessman_cash":100000},"🏬")]),
  ("Okul Servisi Kazası","Bir okul servisi kırmızı ışıkta geçip kaza yaptı. Kimse ağır yaralanmadı ama veliler ayakta.",
   [o("Belediye okul servisi hattı kur",-55000,{"education":2,"transport":3,"security":2},"🚌"), o("Servis denetimlerini sıkılaştır",-10000,{"security":3},"📋"), o("Bütün servisleri tek firmaya ihale et",-5000,{"transport":1,"suspicion":7,"businessman_cash":60000},"📝")]),
  ("Hava Kirliliği Alarmı","Kış ayında partikül madde ölçümü sınırın üç katına çıktı. Astım hastaları acile koşuyor.",
   [o("Doğalgaza geçişe destek ver",-80000,{"health":6},"🔥"), o("Sanayiye gece üretim yasağı koy",-10000,{"health":4,"businessman_cash":-80000},"🏭"), o("Ölçüm istasyonunu parka taşı",0,{"health":-2,"suspicion":8},"📟","Rakamlar düzelir, hava düzelmez.")]),
]

for c in seed["cards"]:
    if c["type"] == "event" and c["title"] in EVENT_OPTIONS:
        c["options"] = EVENT_OPTIONS[c["title"]]
missing = set(EVENT_OPTIONS) - {c["title"] for c in seed["cards"]}
assert not missing, missing
have = {c["title"] for c in seed["cards"]}
new_rows = []
for t, d, opts in NEW_CRISES:
    if t in have: continue
    row = {"id": str(uuid.uuid5(uuid.NAMESPACE_URL, "toplum-sim/v3/" + t)), "type": "crisis", "title": t, "description": d,
           "options": opts, "effects": None, "budget_effect": 0, "stat_effects": None}
    seed["cards"].append(row); new_rows.append(row)
seed_p.write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")

q = lambda s: "'" + s.replace("'", "''") + "'"
lines = ["-- v3: olay kartı tepkileri, yeni kriz kartları, oda dönem uzunluğu", "alter table public.rooms add column if not exists rounds int;"]
for t, opts in EVENT_OPTIONS.items():
    lines.append(f"update public.cards set options = {q(json.dumps(opts, ensure_ascii=False))}::jsonb where type = 'event' and title = {q(t)};")
for t, d, opts in NEW_CRISES:
    cid = str(uuid.uuid5(uuid.NAMESPACE_URL, "toplum-sim/v3/" + t))
    lines.append(f"insert into public.cards (id, type, title, description, options, budget_effect) values ({q(cid)}, 'crisis', {q(t)}, {q(d)}, {q(json.dumps(opts, ensure_ascii=False))}::jsonb, 0) on conflict (id) do nothing;")
(root / "data/seed_cards_v3.sql").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("seed.json:", len(seed["cards"]), "kart;", len(new_rows), "yeni kriz; SQL yazıldı")
