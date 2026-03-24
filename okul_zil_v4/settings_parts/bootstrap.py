from .shared import *

class SettingsBootstrapMixin:
        def __init__(self, ana_pencere):
                super().__init__(ana_pencere)
                self.ana_pencere = ana_pencere
                self.setWindowTitle("Sistem Ayarları")
                self.resize(950, 650)
                pencere_ortala(self)
                self.setStyleSheet(MODERN_TEMA)
                self.gecici_veri = json.loads(
                    json.dumps(self.ana_pencere.sistem_verisi))
                if "ozel_sesler" not in self.gecici_veri:
                    self.gecici_veri["ozel_sesler"] = {}
                self.melodi_kutulari = {}
                self.klasordeki_melodiler = ["Varsayılan"] + [f for f in os.listdir(
                    ZIL_KLASORU) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
                self.init_ui()

        def init_ui(self):
                layout = QVBoxLayout(self)
                layout.setContentsMargins(10, 10, 10, 10)
                self.sekmeler = QTabWidget()
                self.sekmeler.currentChanged.connect(self.sekme_guvenlik_kontrol)
                self.sekme_saatler = QWidget()
                self.sekme_ozel = QWidget()
                self.sekme_genel = QWidget()
                self.sekme_uzaktan = QWidget()
                self.sekme_loglar = QWidget()
                self.sekme_hakkinda = QWidget()

                self.sekmeler.addTab(self.sekme_saatler, "📅 Saatler")
                self.sekmeler.addTab(self.sekme_ozel, "🎵 Özel Ziller")
                self.sekmeler.addTab(self.sekme_genel, "⚙️ Genel")
                self.sekmeler.addTab(self.sekme_uzaktan, "📱 Uzaktan Kontrol")
                self.sekmeler.addTab(self.sekme_loglar, "📜 Log Kayıtları")
                self.sekme_yedek = QWidget()
                self.sekmeler.addTab(self.sekme_yedek, "💾 Yedek/Güncelle")
                self.sekmeler.addTab(self.sekme_hakkinda, "ℹ️ Hakkında")

                self.ders_saatleri_arayuzunu_kur()
                self.ozel_ses_arayuzunu_kur()
                self.genel_ayarlar_arayuzunu_kur()
                self.uzaktan_kontrol_arayuzunu_kur()
                self.log_arayuzunu_kur()
                self.yedek_guncelle_arayuzunu_kur()
                self.hakkinda_arayuzunu_kur()

                layout.addWidget(self.sekmeler)
                btn_kaydet = QPushButton("💾 TÜM AYARLARI KAYDET VE UYGULA")
                btn_kaydet.setStyleSheet(
                    "background-color: #2ed573; color: white; font-size: 14px; padding: 12px; border: none; border-bottom: 4px solid #27ae60; font-weight: bold; border-radius: 5px;")
                btn_kaydet.clicked.connect(self.ayarlari_kaydet)
                layout.addWidget(btn_kaydet)
                self.eski_sekme_index = 0

                self.uzaktan_kontrol_icerik.setVisible(False)
                self.log_icerik.setVisible(False)

                self.uzaktan_kilit_etiketi = QLabel(
                    "🔒 Bu sekmeyi görüntülemek için Yönetici Şifresini girmelisiniz.")
                self.uzaktan_kilit_etiketi.setAlignment(Qt.AlignCenter)
                self.uzaktan_kilit_etiketi.setStyleSheet(
                    "font-size: 15px; color: #7f8c8d; font-weight: bold; padding: 20px;")
                self.sekme_uzaktan.layout().insertWidget(0, self.uzaktan_kilit_etiketi)

                self.log_kilit_etiketi = QLabel(
                    "🔒 Logları sadece yönetici görüntüleyebilir.")
                self.log_kilit_etiketi.setAlignment(Qt.AlignCenter)
                self.log_kilit_etiketi.setStyleSheet(
                    "font-size: 15px; color: #7f8c8d; font-weight: bold; padding: 20px;")
                self.sekme_loglar.layout().insertWidget(0, self.log_kilit_etiketi)
