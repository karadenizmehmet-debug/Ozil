from .shared import *

class MainWindowBaseInitMixin:
        def __init__(self):
                super().__init__()

                # --- SES AYGITI KONTROLÜ ---
                self.ses_aygiti_aktif = True
                try:
                    # Windows 10'da daha stabil çalışması için frekans ve buffer ayarla
                    pygame.mixer.pre_init(44100, -16, 2, 4096)
                    pygame.mixer.init()
                    pygame.mixer.music.set_volume(1.0)
                    print(f"[Pygame] Mixer başlatıldı: {pygame.mixer.get_init()}")
                except Exception as e:
                    self.ses_aygiti_aktif = False
                    print(f"Ses aygıtı başlatılamadı: {e}")

                self.sistem_verisi = {"sesler": {}, "ozel_sesler": {
                }, "yonetici_sifre": "1234", "uygulama_sifre": "1234", "mobil_sifre": "1234"}
                for g in GUNLER:
                    self.sistem_verisi[g] = []

                self.zil_aktif = True
                self.calan_ses_anahtari = None
                self.ses_duraklatildi_mi = False
                self.teneffus_yayini_aktif = False
                self.manuel_muzik_modu = False
                self.oynatma_listesi = []
                self.muzik_indeks = 0

                # --- TAKILMA KORUMASI İÇİN YENİ DEĞİŞKEN ---
                self.son_calinan_dakika = ""

                self.verileri_yukle()
                self.init_ui()
                self.tepsi_ikonu_olustur()

                flask_app.mobil_sifre = self.sistem_verisi.get("mobil_sifre", "1234")
                flask_app.uygulama_sifre = self.sistem_verisi.get(
                    "uygulama_sifre", "1234")
                flask_app.yonetici_sifre = self.sistem_verisi.get(
                    "yonetici_sifre", "1234")
                self.web_thread = None

                # --- FİREBASE UZAKTAN KUMANDA (İnternet üzerinden kontrol) ---
                self.fb_dinleyici = FirebaseDinleyici(muzik_klasoru=MUZIK_KLASORU)
                self.fb_dinleyici.sinyal_cal.connect(self._firebase_komut)
                self.fb_dinleyici.sinyal_anons.connect(self.uzaktan_gelen_anons_emri)
                self.fb_dinleyici.sinyal_ses.connect(self.uzaktan_ses_seviyesi_guncelle)
                self.fb_dinleyici.sinyal_sarki.connect(self.ozel_sarki_cal)
                self.fb_dinleyici.sinyal_sifre.connect(self._firebase_sifre_degistir)
                self.fb_dinleyici.sinyal_zil_sec.connect(self._firebase_zil_degistir)
                self.fb_dinleyici.sinyal_zil_ac_kapat.connect(self._firebase_sistem_durum)
                self.fb_dinleyici.sinyal_genel_ayar.connect(self.mobilden_ayar_guncelle)
                self.fb_dinleyici.start()
                # -------------------------------------------------------------

                self.timer = QTimer()
                self.timer.timeout.connect(self.sistem_kontrol)
                self.timer.start(1000)
                self.sistem_kontrol()

        def verileri_yukle(self):
                if os.path.exists(AYARLAR_DOSYASI):
                    try:
                        with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as f:
                            v = json.load(f)
                            self.sistem_verisi.update(v)
                        # Sabit yolları (F:\... gibi) BASE_DIR'e göre normalize et
                        self._ses_yollarini_normalize_et()
                    except Exception as e:
                        print(f"Ayar yükleme hatası: {e}")

