import os
import sys

# --- KLASÖR VE DOSYA YOLLARI ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Ana Klasörler
ZIL_KLASORU = os.path.join(BASE_DIR, "sesler", "zilmelodileri")
MUZIK_KLASORU = os.path.join(BASE_DIR, "sesler", "muzikyayini")
MARS_KLASORU = os.path.join(BASE_DIR, "sesler", "marslar")
ANONS_KLASORU = os.path.join(BASE_DIR, "sesler", "anons")
DATA_KLASORU = os.path.join(BASE_DIR, "sistem_verileri") # <-- YENİ EKLENDİ

# 2. Veri ve Ayar Dosyaları (Artık hepsi sistem_verileri klasörünün içinde)
LOG_DOSYASI = os.path.join(DATA_KLASORU, "sistem_loglari.json")
AYARLAR_DOSYASI = os.path.join(DATA_KLASORU, "ayarlar.json")
AYARLAR_TEMP = os.path.join(DATA_KLASORU, "ayarlar_temp.json")
IKON_DOSYASI = os.path.join(DATA_KLASORU, "zil_ikon.png")

# --- YOL NORMALİZASYONU ---
# ayarlar.json'daki sabit yolları (F:\...) BASE_DIR'e göre düzeltir
# Böylece klasör nereye taşınırsa taşınsın ses dosyaları bulunur
def yolu_normalize_et(eski_yol):
    """Sabit sürücü yolunu BASE_DIR'e göre göreceli hale getirir."""
    if not eski_yol or eski_yol == "Varsayılan":
        return eski_yol
    eski_yol = eski_yol.replace("/", os.sep)
    # Zaten var mı? Doğrudan dön
    if os.path.exists(eski_yol):
        return eski_yol
    # Dosya adını al, BASE_DIR altında ara
    dosya_adi = os.path.basename(eski_yol)
    # Olası alt klasörler
    aradir = [
        os.path.join(ZIL_KLASORU, dosya_adi),
        os.path.join(MARS_KLASORU, dosya_adi),
        os.path.join(MUZIK_KLASORU, dosya_adi),
        os.path.join(ANONS_KLASORU, dosya_adi),
    ]
    for yol in aradir:
        if os.path.exists(yol):
            return yol
    # Bulunamadıysa orijinali dön
    return eski_yol

# Gerekli klasörlerin otomatik oluşturulması
for k in [ZIL_KLASORU, MUZIK_KLASORU, MARS_KLASORU, ANONS_KLASORU, DATA_KLASORU]:
    if not os.path.exists(k): 
        try:
            os.makedirs(k)
        except:
            pass
# --- ZAMAN VE TAKVİM SABİTLERİ ---
HAFTA_ICI = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
HAFTA_SONU = ["Cumartesi", "Pazar"]
GUNLER = HAFTA_ICI + HAFTA_SONU
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# --- SİSTEM SABİTLERİ ---
KRITIK_SESLER = ["istiklal", "saygi_1", "saygi_1_ist", "saygi_2_ist", "siren"]

SOZLER = [
    "“Eğitimdir ki bir milleti ya özgür, bağımsız, şanlı, yüksek bir topluluk halinde yaşatır; ya da esaret ve sefalete terk eder.”\n— Mustafa Kemal ATATÜRK",
    "“Hayatta en hakiki mürşit ilimdir, fendir.”\n— Mustafa Kemal ATATÜRK",
    "“Okul, genç beyinlere insanlığa saygıyı, millet ve ülkeye sevgiyi, bağımsızlık onurunu öğretir.”\n— Mustafa Kemal ATATÜRK",
    "“Yolculuk, hedefin kendisidir.”\n— Mevlana",
    "“Bilgi güçtür.”\n— Francis Bacon",
    "“Gelecek, hayallerinin güzelliğine inananlarındır.”\n— Eleanor Roosevelt",
    "“Başarı, her gün tekrarlanan küçük çabaların toplamıdır.”\n— Robert Collier",
    "“Zorluklar, yetenekleri geliştirir.”\n— Horatius",
    "“Eğitimin kökleri acı, meyveleri tatlıdır.”\n— Aristoteles",
    "“Bir mermer parçası için heykeltıraş ne ise, ruh için de eğitim odur.”\n— Thomas Edison",
    "“Öğretmen bir kandile benzer, kendini tüketerek başkalarına ışık verir.”\n— Hz. Ali",
    "“Zekâ, bilginin nerede olduğunu bilmektir.”\n— Samuel Johnson",
    "“Öğrenmek akıntıya karşı kürek çekmek gibidir; durduğunuz an geriye gidersiniz.”\n— Benjamin Britten",
    "“Eğitim, meyvenin kendisi değil, ağaç dikmektir.”\n— Anonim",
    "“Dünyayı değiştirmek için kullanabileceğiniz en güçlü silah eğitimdir.”\n— Nelson Mandela"
]

# --- PYQT5 MODERN TEMA ---
MODERN_TEMA = """
QWidget{font-family:'Segoe UI',Arial,sans-serif;color:#2c3e50;background-color:#f1f2f6}
QGroupBox{font-weight:bold;border:1px solid #dcdde1;border-radius:6px;margin-top:5px;background-color:#fff;font-size:12px;padding-top:15px}
QGroupBox::title{subcontrol-origin:margin;subcontrol-position:top left;padding:0 5px;color:#2f3542}
QPushButton{background-color:#dfe4ea;color:#2f3542;border:1px solid #ced6e0;border-bottom:3px solid #a4b0be;border-radius:4px;padding:4px 8px;font-weight:bold;font-size:12px}
QPushButton:hover{background-color:#f1f2f6}
QPushButton:pressed{background-color:#ced6e0;border-bottom:1px solid #a4b0be;margin-top:2px}

/* ÖZEL RENKLİ BUTONLAR */
QPushButton#btn_kirmizi{background-color:#ff4757; color:white; border-bottom:3px solid #c0392b}
QPushButton#btn_mavi{background-color:#0984e3; color:white; border-bottom:3px solid #06528d}
QPushButton#btn_yesil{background-color:#2ecc71; color:white; border-bottom:3px solid #27ae60}
QPushButton#btn_turuncu{background-color:#f39c12; color:white; border-bottom:3px solid #e67e22}
QPushButton#btn_mor{background-color:#8e44ad; color:white; border-bottom:3px solid #732d91}

QPushButton#btn_cal{background-color:#ffffff;border:1px solid #ced6e0;border-bottom:3px solid #b0b0b0;padding:10px;text-align:center}
QPushButton#btn_ayarlar{background-color:#0984e3;color:#fff;font-size:13px;border:none;border-bottom:4px solid #06528d;border-radius:6px}
QPushButton#btn_hesapla{background-color:#0984e3;color:#fff;border:none;border-bottom:3px solid #06528d}
QPushButton#btn_gizle{background-color:#7f8c8d;color:#fff;border:none;border-bottom:3px solid #57606f}
QTableWidget{background-color:#fff;border:1px solid #dce1e6;border-radius:6px}
QHeaderView::section{background-color:#f8f9fa;color:#2f3542;font-weight:bold;padding:6px;border:none;font-size:12px}
QSlider::groove:horizontal{border-radius:4px;height:8px;background:#dfe4ea}
QSlider::handle:horizontal{background:#0984e3;width:18px;height:18px;margin:-5px 0;border-radius:9px}
QTimeEdit,QLineEdit,QSpinBox,QComboBox{border:1px solid #ced6e0;border-radius:3px;padding:4px;background:#fff;font-weight:bold}
QTabWidget::pane{border:1px solid #dcdde1;border-radius:5px;background:#fff;top:-1px}
QTabBar::tab{background:#dfe4ea;border:1px solid #ced6e0;padding:8px 15px;border-top-left-radius:5px;border-top-right-radius:5px;font-weight:bold;margin-right:2px;color:#57606f}
QTabBar::tab:selected{background:#fff;color:#0984e3;border-top:3px solid #0984e3}
"""

# --- FLASK HTML ŞABLONLARI ---
LOGIN_SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sisteme Giriş</title><style>body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:40px 20px;}h2{color:#2f3542;}input{padding:15px;font-size:18px;border-radius:8px;border:1px solid #ced6e0;width:80%;max-width:300px;margin-bottom:20px;text-align:center;}button{padding:15px 30px;font-size:18px;background-color:#0984e3;color:white;border:none;border-radius:8px;font-weight:bold;width:80%;max-width:300px;box-shadow:0 4px #06528d;}.hata{color:#e74c3c;font-weight:bold;margin-top:15px;}.info{color:#7f8c8d;margin-bottom:20px;font-size:14px;}</style></head><body><h2>Nimetullah Nahçivani İHO<br><span style="font-size:16px;color:#7f8c8d;">Mobil Kumanda Girişi</span></h2><div class="info">Bağlı Bilgisayar: <b>{{ pc_adi }}</b></div><form action="/login" method="POST"><input type="hidden" name="csrf_token" value="{{ csrf_token }}"><input type="password" name="sifre" placeholder="Mobil Kumanda Şifresi" required autofocus><br><button type="submit">GİRİŞ YAP</button></form>{% if hata %}<div class="hata">Hatalı Şifre! Lütfen tekrar deneyin.</div>{% endif %}</body></html>"""

SIFRE_GIRIS_SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Yönetici Girişi</title><style>body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:40px 20px;}h2{color:#2c3e50;}input{padding:15px;font-size:18px;border-radius:8px;border:1px solid #ced6e0;width:80%;max-width:300px;margin-bottom:20px;text-align:center;}button{padding:15px 30px;font-size:18px;background-color:#e67e22;color:white;border:none;border-radius:8px;font-weight:bold;width:80%;max-width:300px;}.hata{color:#e74c3c;font-weight:bold;margin-top:15px;}</style></head><body><h2>🔐 Yönetici Girişi</h2><p>Gelişmiş ayarları yönetmek için yönetici şifrenizi girin.</p><form method="POST"><input type="hidden" name="csrf_token" value="{{ csrf_token }}"><input type="password" name="sifre" placeholder="Yönetici Şifresi" required autofocus><br><button type="submit">GİRİŞ YAP</button></form>{% if hata %}<div class="hata">Hatalı Yönetici Şifresi!</div>{% endif %}<br><a href="/" style="color:#0984e3; text-decoration:none;">← Kumandaya Geri Dön</a></body></html>"""

HTML_SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>📱 Uzaktan Kontrol</title><style>body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:10px;margin:0}h2{color:#2f3542;margin-bottom:10px;font-size:20px}.card{background:white;padding:15px;border-radius:15px;box-shadow:0 4px 6px rgba(0,0,0,0.1);margin-bottom:15px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}.btn{padding:15px 5px;font-size:14px;font-weight:bold;color:#fff;background-color:#0984e3;border:none;border-radius:8px;box-shadow:0 4px #06528d;display:flex;flex-direction:column;align-items:center;justify-content:center}.btn:active{box-shadow:0 1px #043e6b;transform:translateY(3px)}.full{grid-column:span 2;padding:15px;font-size:16px}.blue{background-color:#0984e3;box-shadow:0 4px #06528d}.green{background-color:#2ecc71;box-shadow:0 4px #27ae60}.orange{background-color:#f39c12;box-shadow:0 4px #e67e22}.red{background-color:#e74c3c;box-shadow:0 4px #c0392b}.dark{background-color:#2c3e50;box-shadow:0 4px #1a252f}.purple{background-color:#8e44ad;box-shadow:0 4px #732d91}.icon{font-size:22px;margin-bottom:5px}.footer{margin-top:20px;display:flex;justify-content:space-around;padding-bottom:20px}.footer a{text-decoration:none;color:#0984e3;font-weight:bold}#toast{visibility:hidden;background-color:#333;color:#fff;text-align:center;padding:10px;position:fixed;bottom:20px;left:50%;transform:translateX(-50%);border-radius:5px;z-index:1}.show{visibility:visible;animation:fadein .5s,fadeout .5s 2.5s}.slider-cont{margin-top:10px;padding:10px}input[type=range]{width:100%;height:15px;border-radius:5px;background:#dfe4ea;outline:none}@keyframes fadein{from{opacity:0}to{opacity:1}}@keyframes fadeout{from{opacity:1}to{opacity:0}}</style></head><body><h2>Nimetullah Nahçivani İHO<br><span style="font-size:14px;color:#7f8c8d">{{ pc_adi }} - Kumanda</span></h2><div class="card"><strong>🎤 Canlı Sesli Anons</strong><div style="display:flex; margin-top:10px; gap:8px;"><input type="text" id="txt_anons" placeholder="Duyuru metnini yazın..." style="flex:1; padding:10px; border:1px solid #ced6e0; border-radius:5px; outline:none;"><button class="btn blue" style="padding:10px 15px; flex-direction:row; box-shadow:none;" onclick="anonsGonder()"><span class="icon" style="margin:0 5px 0 0; font-size:18px;">🔊</span>Oku</button></div></div><div class="card"><strong>🔊 Sistem Ses Seviyesi</strong><div class="slider-cont"><input type="range" id="ses_slider" min="0" max="100" value="{{ mevcut_ses }}" oninput="v(this.value)"></div><div id="vol_val">%{{ mevcut_ses }}</div></div><div class="grid"><button class="btn dark" onclick="c('toplanma_zil','Toplanma Zili')"><span class="icon">🔔</span>Toplanma</button><button class="btn blue" onclick="c('ogr_zil','Öğrenci Zili')"><span class="icon">🧑‍🎓</span>Öğrenci</button><button class="btn green" onclick="c('ogrt_zil','Öğretmen Zili')"><span class="icon">👨‍🏫</span>Öğretmen</button><button class="btn orange" onclick="c('cikis_zil','Çıkış Zili')"><span class="icon">🚪</span>Çıkış</button></div><div class="grid"><button class="btn red" onclick="c('istiklal','İstiklal Marşı')"><span class="icon">🇹🇷</span>İstiklal Marşı</button><button class="btn red" onclick="c('siren','Siren')"><span class="icon">🚨</span>Siren Sesi</button><button class="btn red" onclick="c('saygi_1','1 Dk Saygı')"><span class="icon">⏱️</span>1 Dakika Saygı Duruşu</button><button class="btn red" onclick="c('saygi_1_ist','1 Dk+İstiklal')"><span class="icon">⏱️</span>1 Dk Saygı + İstiklal</button><button class="btn red full" onclick="c('saygi_2_ist','2 Dk+İstiklal')"><span class="icon">⏱️</span>2 Dakika Saygı Duruşu + İstiklal Marşı</button></div><div class="grid"><button class="btn purple full" onclick="window.location.href='/mobil_sarki_listesi'"><span class="icon">🎵</span>ŞARKI LİSTESİ</button><button class="btn purple full" onclick="c('muzik_toggle','Müzik Yayını')"><span class="icon">📻</span>Müzik Yayını (Aç/Kapat)</button><button class="btn dark full" style="background-color:#57606f" onclick="s()"><span class="icon">⏹️</span>SİSTEMİ SUSTUR</button></div><div class="footer"><a href="/sifre_yonetici_giris">🔐 Şifre Yönetimi</a><a href="/cikis">🚪 Çıkış</a></div><div id="toast"></div><script>function t(m){let x=document.getElementById("toast");x.innerHTML=m;x.className="show";setTimeout(()=>x.className="",3000)}function c(k,m){fetch('/cal/'+k);t(m+" Çalışıyor")}function s(){fetch('/sustur');t("Susturuldu")}function v(val){document.getElementById("vol_val").innerHTML="%"+val;fetch('/ses_ayarla/'+val)}function anonsGonder(){let m=document.getElementById("txt_anons").value;if(!m)return;fetch('/anons_yap',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'metin='+encodeURIComponent(m)}).then(r=>t("Anons İletildi!"));document.getElementById("txt_anons").value='';}</script></body></html>"""

MOBIL_SARKI_SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🎵 Şarkı Listesi</title><style>body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:10px;margin:0}.header-fix{position:fixed;top:0;left:0;right:0;background:white;padding:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1);z-index:100}.sarki-list{margin-top:120px;padding:10px;background:white;border-radius:15px;max-width:500px;margin-left:auto;margin-right:auto;text-align:left;overflow:hidden}.sarki-item{padding:15px;border-bottom:1px solid #f1f2f6;cursor:pointer;display:flex;justify-content:space-between;align-items:center}.sarki-item:active{background-color:#dfe4ea}.name{font-weight:bold;color:#2c3e50}.play-btn{color:#0984e3;font-size:20px}input[type=range]{width:100%;height:15px;border-radius:5px;background:#dfe4ea;outline:none;margin-top:10px}a{display:block;margin:20px;color:#0984e3;text-decoration:none;font-weight:bold}</style></head><body><div class="header-fix"><strong>🔊 Ses Ayarı: <span id="vol_val">%{{ mevcut_ses }}</span></strong><br><input type="range" min="0" max="100" value="{{ mevcut_ses }}" oninput="v(this.value)"></div><div class="sarki-list">{% for sarki in sarkilar %}<div class="sarki-item" onclick="cal('{{ sarki }}')"><span class="name">{{ sarki }}</span><span class="play-btn">▶️</span></div>{% else %}<div class="sarki-item">Şarkı bulunamadı.</div>{% endfor %}</div><a href="/">← Geri Dön</a><script>function cal(s){fetch('/mobil_ozel_cal/'+encodeURIComponent(s));}function v(val){document.getElementById("vol_val").innerHTML="%"+val;fetch('/ses_ayarla/'+val);}</script></body></html>"""

SIFRE_SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Şifre Yönetimi</title><style>body{font-family:'Segoe UI',sans-serif;background-color:#f1f2f6;text-align:center;padding:20px;}h3{color:#2c3e50;}.card{background:white;padding:20px;border-radius:12px;box-shadow:0 4px 8px rgba(0,0,0,0.1);max-width:400px;margin:0 auto 20px;}input, select{width:100%;padding:12px;margin:10px 0;border-radius:8px;border:1px solid #ddd;box-sizing:border-box;}button{width:100%;padding:12px;background:#2ed573;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer;}.msg{padding:10px;border-radius:5px;margin-bottom:10px;font-size:14px;}.err{background:#ff4757;color:white;}.ok{background:#2ed573;color:white;}</style></head><body><h3>🔐 Merkezi Şifre Yönetimi</h3>{% if msg %}<div class="msg {{ 'ok' if 'Başarılı' in msg else 'err' }}">{{ msg }}</div>{% endif %}<div class="card"><form method="POST"><input type="hidden" name="csrf_token" value="{{ csrf_token }}"><label>Değiştirilecek Şifre:</label><select name="tip"><option value="yonetici">🔑 Yönetici Şifresi</option><option value="uygulama">⚙️ Uygulama Giriş Şifresi</option><option value="mobil">📱 Mobil Kumanda Şifresi</option></select><input type="password" name="yeni1" placeholder="Yeni Şifre" required><input type="password" name="yeni2" placeholder="Yeni Şifre (Tekrar)" required><button type="submit">ŞİFREYİ GÜNCELLE</button></form></div><a href="/" style="color:#0984e3; font-weight:bold; text-decoration:none;">← Kumandaya Geri Dön</a></body></html>"""