from .shared import *

class MainWindowUiBuildMixin:
        def init_ui(self):
                self.setWindowTitle(f"Zil Sistemi Otomasyonu - {platform.node()}")

                # --- GÖREV ÇUBUĞU VE PENCERE İKONU EKLENTİSİ ---
                if os.path.exists(IKON_DOSYASI):
                    from PyQt5.QtGui import QIcon
                    self.setWindowIcon(QIcon(IKON_DOSYASI))
                # -----------------------------------------------

                self.resize(1150, 750)
                pencere_ortala(self)
                self.setStyleSheet(MODERN_TEMA)
                ana_lay = QVBoxLayout(self)
                ana_lay.setSpacing(10)
                ana_lay.setContentsMargins(15, 15, 15, 15)

                top_bar = QHBoxLayout()
                lbl_sys = QLabel("ZİL SİSTEMİ OTOMASYONU")
                lbl_sys.setStyleSheet("font-size: 18px; font-weight: bold;")
                lbl_mehmet = QLabel("Geliştirici: Mehmet KARADENİZ")
                lbl_mehmet.setStyleSheet(
                    "font-size: 14px; font-weight: bold; color: #e74c3c;")
                top_bar.addWidget(lbl_sys)
                top_bar.addStretch()
                top_bar.addWidget(lbl_mehmet)
                btn_gizle = QPushButton("⬇️ Arka Plana Gizle")
                btn_gizle.setObjectName("btn_gizle")
                btn_gizle.setFixedSize(140, 35)
                btn_gizle.clicked.connect(self.arka_plana_gizle)
                top_bar.addWidget(btn_gizle)
                ana_lay.addLayout(top_bar)

                icerik_lay = QHBoxLayout()
                icerik_lay.setSpacing(15)

                sol = QVBoxLayout()
                sol.setSpacing(10)
                # ana_baslik ayarından oku, yoksa varsayılanı kullan
                _baslik = self.sistem_verisi.get("ana_baslik", "oZzil - Okulunuzu Seslendirin")
                _satirlar = _baslik.split(" - ", 1)
                _baslik_metin = "\n".join(_satirlar) if len(_satirlar) == 2 else _baslik
                self.lbl_okul = QLabel(_baslik_metin)
                self.lbl_okul.setAlignment(Qt.AlignCenter)
                self.lbl_okul.setStyleSheet(
                    "font-family: 'Segoe UI'; font-size: 20px; font-weight: 900; color: #fff; background-color: #192a56; border-radius: 8px; padding: 15px;")
                sol.addWidget(self.lbl_okul)

                # --- HAVA DURUMU PANELİ ---
                self.g_hava = QGroupBox("🌤️ Hava Durumu")
                self.g_hava.setStyleSheet("QGroupBox { font-size:11px; color:#7f8c8d; border:1px solid #dcdde1; border-radius:6px; margin-top:5px; background:#fff; padding-top:10px; }")
                l_hava = QHBoxLayout()
                l_hava.setContentsMargins(10, 5, 10, 5)
                self.lbl_hava_ikon = QLabel("--")
                self.lbl_hava_ikon.setStyleSheet("font-size:32px; border:none; background:transparent;")
                self.lbl_hava_sicak = QLabel("--°C")
                self.lbl_hava_sicak.setStyleSheet("font-size:22px; font-weight:bold; color:#e74c3c; border:none; background:transparent;")
                self.lbl_hava_acik = QLabel("Yükleniyor...")
                self.lbl_hava_acik.setStyleSheet("font-size:13px; color:#2c3e50; border:none; background:transparent;")
                self.lbl_hava_sehir = QLabel("")
                self.lbl_hava_sehir.setStyleSheet("font-size:11px; color:#7f8c8d; border:none; background:transparent;")
                v_hava = QVBoxLayout()
                v_hava.addWidget(self.lbl_hava_acik)
                v_hava.addWidget(self.lbl_hava_sehir)
                l_hava.addWidget(self.lbl_hava_ikon)
                l_hava.addWidget(self.lbl_hava_sicak)
                l_hava.addLayout(v_hava)
                l_hava.addStretch()
                self.g_hava.setLayout(l_hava)
                sol.addWidget(self.g_hava)
                # Hava durumunu 30 dakikada bir güncelle
                self.hava_timer = QTimer()
                self.hava_timer.timeout.connect(self.hava_durumu_guncelle)
                self.hava_timer.start(30 * 60 * 1000)  # 30 dakika
                QTimer.singleShot(3000, self.hava_durumu_guncelle)  # 3 saniye sonra ilk çekim
                # ---------------------------

                g_ozet = QGroupBox("📌 Bugünün Zil Vakitleri")
                lo = QVBoxLayout()
                lo.setContentsMargins(5, 5, 5, 5)
                self.tablo_ozet = QTableWidget(0, 5)
                self.tablo_ozet.setHorizontalHeaderLabels(
                    ["Ders", "Toplanma", "Öğrenci", "Öğretmen", "Çıkış"])
                self.tablo_ozet.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tablo_ozet.verticalHeader().setVisible(False)
                self.tablo_ozet.setEditTriggers(QTableWidget.NoEditTriggers)
                self.tablo_ozet.setSelectionMode(QTableWidget.NoSelection)
                lo.addWidget(self.tablo_ozet)
                g_ozet.setLayout(lo)
                sol.addWidget(g_ozet)

                # --- YENİ: ZAMAN ÇİZELGESİ / GERİ SAYIM PANELİ ---
                self.g_kalan_sure = QGroupBox("⏳ Durum ve Kalan Süre")
                self.g_kalan_sure.setStyleSheet("""
                    QGroupBox { font-weight: bold; color: #2980b9; border: 2px solid #3498db; border-radius: 8px; margin-top: 10px; background-color: #e8f4f8; }
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
                """)
                l_kalan = QVBoxLayout()
                l_kalan.setContentsMargins(10, 15, 10, 10)

                self.lbl_suan_ne = QLabel("Ders Dışı Zaman")
                self.lbl_suan_ne.setAlignment(Qt.AlignCenter)
                self.lbl_suan_ne.setStyleSheet(
                    "font-size: 16px; font-weight: bold; color: #2c3e50; border: none; background: transparent;")

                self.lbl_geri_sayim = QLabel("--:--")
                self.lbl_geri_sayim.setAlignment(Qt.AlignCenter)
                self.lbl_geri_sayim.setStyleSheet(
                    "font-size: 32px; font-weight: 900; color: #e74c3c; border: none; background: transparent;")

                l_kalan.addWidget(self.lbl_suan_ne)
                l_kalan.addWidget(self.lbl_geri_sayim)
                self.g_kalan_sure.setLayout(l_kalan)
                sol.addWidget(self.g_kalan_sure)
                # --------------------------------------------------

                self.lbl_soz = QLabel(f'{random.choice(SOZLER)}')

                self.lbl_soz.setWordWrap(True)
                self.lbl_soz.setAlignment(Qt.AlignCenter)
                self.lbl_soz.setStyleSheet("""
                    font-family: 'Georgia', serif; 
                    font-size: 20px; 
                    font-style: italic; 
                    color: #2c3e50; 
                    padding: 30px; 
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #f1f2f6);
                    border: 2px solid #0984e3; 
                    border-radius: 15px; 
                    font-weight: 600;
                    line-height: 150%;
                """)
                sol.addWidget(self.lbl_soz)
                icerik_lay.addLayout(sol, 55)

                sag = QVBoxLayout()
                sag.setSpacing(8)
                g_zaman = QGroupBox()
                g_zaman.setStyleSheet(
                    "background-color: #fff; border: 2px solid #0984e3;")
                lz = QVBoxLayout()
                lz.setContentsMargins(5, 5, 5, 5)
                self.lbl_tarih = QLabel("...")
                self.lbl_tarih.setFont(QFont("Segoe UI", 12, QFont.Bold))
                self.lbl_tarih.setStyleSheet("color: #0984e3;")
                self.lbl_tarih.setAlignment(Qt.AlignCenter)
                self.lbl_saat = QLabel("00:00:00")
                self.lbl_saat.setFont(QFont("Segoe UI", 36, QFont.Bold))
                self.lbl_saat.setAlignment(Qt.AlignCenter)
                lz.addWidget(self.lbl_tarih)
                lz.addWidget(self.lbl_saat)
                g_zaman.setLayout(lz)
                sag.addWidget(g_zaman)

                g_mars = QGroupBox("🇹🇷 Marşlar ve Siren")
                gm = QGridLayout()
                gm.setContentsMargins(10, 10, 10, 10)
                gm.setSpacing(10)
                butons_mars = [
                    ("🇹🇷 İstiklal Marşı", "istiklal"),
                    ("⏱️ 1 Dk Saygı", "saygi_1"),
                    ("⏱️ Saygı+İst", "saygi_1_ist"),
                    ("⏱️ 2Dk+İst", "saygi_2_ist"),
                    ("🚨 Siren Sesi", "siren")
                ]
                for i, (isim, k) in enumerate(butons_mars):
                    b = QPushButton(isim)
                    b.setObjectName("btn_kirmizi")
                    b.setFixedSize(140, 45)
                    b.clicked.connect(lambda checked=False,
                                      key=k: self.sesi_cal(key, True))
                    gm.addWidget(b, i//2, i % 2)
                g_mars.setLayout(gm)
                sag.addWidget(g_mars)

                g_zil = QGroupBox("🔔 Genel Ziller")
                gz = QGridLayout()
                gz.setContentsMargins(10, 10, 10, 10)
                gz.setSpacing(10)
                butons_gen = [("🔔 Toplanma", "toplanma_zil", "btn_mavi"), ("🧑‍🎓 Öğrenci", "ogr_zil", "btn_yesil"),
                              ("👨‍🏫 Öğretmen", "ogrt_zil", "btn_mor"), ("🚪 Çıkış", "cikis_zil", "btn_turuncu")]
                for i, (isim, k, cid) in enumerate(butons_gen):
                    b = QPushButton(isim)
                    b.setObjectName(cid)
                    b.setFixedSize(140, 45)
                    b.clicked.connect(lambda checked=False,
                                      key=k: self.sesi_cal(key, True))
                    gz.addWidget(b, i//2, i % 2)
                g_zil.setLayout(gz)
                sag.addWidget(g_zil)

        # --- 🎤 SESLİ ANONS PANELİ ---
                g_anons = QGroupBox("🎤 Hızlı Sesli Anons")
                l_anons = QHBoxLayout()
                l_anons.setContentsMargins(10, 10, 10, 10)
                self.txt_anons = QLineEdit()
                self.txt_anons.setPlaceholderText(
                    "Okunacak anons metnini buraya yazın... (çift tık = şablonlar)")
                self.txt_anons.setStyleSheet(
                    "padding: 8px; font-size: 13px; border-radius: 4px;")
                self.txt_anons.mouseDoubleClickEvent = lambda e: self._sablon_sec_dialog()

                # Tekrar sayısı seçici
                from PyQt5.QtWidgets import QComboBox
                self.combo_anons_tekrar = QComboBox()
                self.combo_anons_tekrar.addItems(["1x", "2x", "3x"])
                self.combo_anons_tekrar.setFixedSize(55, 35)
                self.combo_anons_tekrar.setToolTip("Kaç kez tekrar edilsin?")

                btn_anons = QPushButton("🔊 Oku")
                btn_anons.setObjectName("btn_mavi")
                btn_anons.setFixedSize(80, 35)
                btn_anons.clicked.connect(self.anons_yap_tetikle)

                l_anons.addWidget(self.txt_anons)
                l_anons.addWidget(self.combo_anons_tekrar)
                l_anons.addWidget(btn_anons)
                g_anons.setLayout(l_anons)
                sag.addWidget(g_anons)
                # -----------------------------

                ak = QHBoxLayout()
                g_ses = QGroupBox("Ses Denetimi")
                l_ses = QVBoxLayout()
                sl = QHBoxLayout()
                self.slider = ClickableSlider(Qt.Horizontal)
                self.slider.setRange(0, 100)
                self.slider.setValue(100)
                self.lbl_ses_yuzde = QLabel("%100")
                self.lbl_ses_yuzde.setFont(QFont("Arial", 10, QFont.Bold))
                self.slider.valueChanged.connect(self.ses_seviyesi_degisti)
                sl.addWidget(self.slider)
                sl.addWidget(self.lbl_ses_yuzde)
                l_ses.addLayout(sl)

                bol = QHBoxLayout()
                self.btn_sarki_sec = QPushButton("🎵 Şarkı Seç")
                self.btn_sarki_sec.setObjectName("btn_mor")
                self.btn_sarki_sec.setFixedSize(100, 35)
                self.btn_sarki_sec.clicked.connect(self.sarki_sec_penceresini_ac)

                self.btn_muzik = QPushButton("📻 Müzik")
                self.btn_muzik.setObjectName("btn_mor")
                self.btn_muzik.setFixedSize(80, 35)
                self.btn_muzik.clicked.connect(self.manuel_muzik_yayini_toggle)

                self.btn_duraklat = QPushButton("⏸️")
                self.btn_duraklat.setFixedSize(45, 35)
                self.btn_duraklat.setStyleSheet(
                    "background-color:#ffa502; font-weight:bold; color:white;")
                self.btn_duraklat.clicked.connect(self.sesi_duraklat_devam)

                b_sus = QPushButton("⏹️")
                b_sus.setObjectName("btn_kirmizi")
                b_sus.setFixedSize(45, 35)
                b_sus.clicked.connect(self.sesi_kapat)

                bol.addWidget(self.btn_sarki_sec)
                bol.addWidget(self.btn_muzik)
                bol.addWidget(self.btn_duraklat)
                bol.addWidget(b_sus)
                l_ses.addLayout(bol)
                g_ses.setLayout(l_ses)
                ak.addWidget(g_ses)

                grup_durum = QGroupBox("Sistem Durumu")
                durum_lay = QVBoxLayout()
                self.btn_durum = QPushButton("SİSTEM: AÇIK")
                self.btn_durum.setFixedSize(160, 50)
                self.btn_durum.setStyleSheet(
                    "background-color:#2ed573; color:white; font-weight:bold; font-size:14px; border-bottom:4px solid #27ae60;")
                self.btn_durum.clicked.connect(self.zil_durumu_degistir)
                durum_lay.addWidget(self.btn_durum)
                grup_durum.setLayout(durum_lay)
                ak.addWidget(grup_durum)
                sag.addLayout(ak)

                b_ayar = QPushButton("⚙️ GELİŞMİŞ AYARLARI AÇ")
                b_ayar.setObjectName("btn_ayarlar")
                b_ayar.setFixedSize(300, 50)
                b_ayar.clicked.connect(self.ayarlar_penceresini_ac)
                sag.addWidget(b_ayar, alignment=Qt.AlignCenter)

                icerik_lay.addLayout(sag, 45)
                ana_lay.addLayout(icerik_lay)
                self.arayuzu_guncelle()
                if not self.ses_aygiti_aktif:
                    self.btn_durum.setText("SİSTEM HATA: SES YOK")
                    self.btn_durum.setStyleSheet(
                        "background-color:#e84118; color:white; font-weight:bold; font-size:14px; border-bottom:4px solid #c23616;")
                    self.zil_aktif = False  # Sistemi otomatik kapat
                    # Pencere açıldıktan yarım saniye sonra uyarı mesajını göster
                    QTimer.singleShot(500, self.ses_hatasi_goster)
