from .shared import *

class SettingsGeneralLayoutMixin:
        def genel_ayarlar_arayuzunu_kur(self):
                lay = QVBoxLayout(self.sekme_genel)
                lay.setContentsMargins(10, 10, 10, 10)
                lay.setSpacing(10)

                ust_satir = QHBoxLayout()
                g_sys = QGroupBox("Sistem")
                l_sys = QVBoxLayout()
                self.check_otobaslat = QCheckBox("PC açıldığında otomatik başlat")
                self.check_otobaslat.setChecked(
                    self.gecici_veri.get("otomatik_baslat", False))
                self.check_teneffus_aktif = QCheckBox("Teneffüs Müzik Yayını Aktif")
                self.check_teneffus_aktif.setChecked(
                    self.gecici_veri.get("teneffus_muzigi_aktif", True))
                self.check_pc_kapat = QCheckBox("Belirlenen saatte bilgisayarı kapat")
                self.check_pc_kapat.setChecked(
                    self.gecici_veri.get("pc_kapat_aktif", False))

                self.time_pc_kapat = QTimeEdit()
                self.time_pc_kapat.setDisplayFormat("HH:mm")
                oto_saat = self.gecici_veri.get("pc_kapat_saat", "17:30")
                self.time_pc_kapat.setTime(QTime.fromString(oto_saat, "HH:mm"))
                self.check_pc_kapat.toggled.connect(self.time_pc_kapat.setEnabled)
                self.time_pc_kapat.setEnabled(self.gecici_veri.get("pc_kapat_aktif", False))
                zaman_lay = QHBoxLayout()
                zaman_lay.addWidget(self.check_pc_kapat)
                zaman_lay.addWidget(QLabel("  Saat:"))
                zaman_lay.addWidget(self.time_pc_kapat)
                zaman_lay.addStretch()
                l_sys.addWidget(self.check_otobaslat)
                l_sys.addWidget(self.check_teneffus_aktif)
                l_sys.addLayout(zaman_lay)
                g_sys.setLayout(l_sys)
                ust_satir.addWidget(g_sys, 1)

                g_muz = QGroupBox("Müzik Yayını")
                l_muz = QGridLayout()
                l_muz.setContentsMargins(5, 5, 5, 5)
                self.txt_muzik_klasoru = QLineEdit()
                self.txt_muzik_klasoru.setReadOnly(True)
                self.txt_muzik_klasoru.setText(
                    self.gecici_veri.get("muzik_klasoru", MUZIK_KLASORU))
                b_sec = QPushButton("📂 Seç")
                b_sec.clicked.connect(lambda: self.txt_muzik_klasoru.setText(
                    QFileDialog.getExistingDirectory(self, "Klasör Seç") or self.txt_muzik_klasoru.text()))
                self.spin_muzik_sesi = QSpinBox()
                self.spin_muzik_sesi.setRange(1, 100)
                self.spin_muzik_sesi.setValue(self.gecici_veri.get("muzik_sesi", 30))

                l_muz.addWidget(QLabel("Klasör:"), 0, 0)
                l_muz.addWidget(self.txt_muzik_klasoru, 0, 1)
                l_muz.addWidget(b_sec, 0, 2)
                l_muz.addWidget(QLabel("Ses:"), 1, 0)
                l_muz.addWidget(self.spin_muzik_sesi, 1, 1)
                g_muz.setLayout(l_muz)
                ust_satir.addWidget(g_muz, 2)
                lay.addLayout(ust_satir)

                ks = self.gecici_veri.get("sesler", {})
                ort = QHBoxLayout()
                g_zil = QGroupBox("Genel Ziller")
                grid_z = QGridLayout()
                grid_z.setSpacing(6)

                ziller = [("toplanma_zil", "Toplanma"), ("ogr_zil", "Öğrenci"),
                          ("ogrt_zil", "Öğretmen"), ("cikis_zil", "Çıkış")]
                for i, (k, e) in enumerate(ziller):
                    t = QLineEdit()
                    t.setReadOnly(True)
                    t.setText(ks.get(k, "Varsayılan"))
                    self.melodi_kutulari[k] = t
                    b1 = QPushButton("📂")
                    b1.clicked.connect(lambda checked=False, a=k: self.dosya_sec(a))
                    b2 = QPushButton("❌")
                    b2.clicked.connect(
                        lambda checked=False, a=k: self.melodi_kutulari[a].setText("Varsayılan"))
                    grid_z.addWidget(QLabel(e), i, 0)
                    grid_z.addWidget(t, i, 1)
                    grid_z.addWidget(b1, i, 2)
                    grid_z.addWidget(b2, i, 3)
                g_zil.setLayout(grid_z)
                ort.addWidget(g_zil)

                g_mar = QGroupBox("Marşlar/Siren")
                grid_m = QGridLayout()
                grid_m.setSpacing(6)

                marslar = [("istiklal", "İstiklal"), ("saygi_1", "1 Dk Saygı"), ("saygi_1_ist",
                                                                                 "1 Dk+Marş"), ("saygi_2_ist", "2 Dk+Marş"), ("siren", "Siren")]
                for i, (k, e) in enumerate(marslar):
                    t = QLineEdit()
                    t.setReadOnly(True)
                    t.setText(ks.get(k, "Varsayılan"))
                    self.melodi_kutulari[k] = t
                    b1 = QPushButton("📂")
                    b1.clicked.connect(lambda checked=False, a=k: self.dosya_sec(a))
                    b2 = QPushButton("❌")
                    b2.clicked.connect(
                        lambda checked=False, a=k: self.melodi_kutulari[a].setText("Varsayılan"))
                    grid_m.addWidget(QLabel(e), i, 0)
                    grid_m.addWidget(t, i, 1)
                    grid_m.addWidget(b1, i, 2)
                    grid_m.addWidget(b2, i, 3)
                g_mar.setLayout(grid_m)
                ort.addWidget(g_mar)
                lay.addLayout(ort)

                # --- HAVA DURUMU ŞEHİR AYARI ---
                g_hava = QGroupBox("🌤️ Hava Durumu")
                l_hava = QHBoxLayout()
                l_hava.addWidget(QLabel("Şehir:"))
                self.txt_hava_sehir = QLineEdit()
                self.txt_hava_sehir.setPlaceholderText("Örn: Konya, İstanbul, Ankara")
                self.txt_hava_sehir.setText(self.gecici_veri.get("hava_sehir", "Konya"))
                l_hava.addWidget(self.txt_hava_sehir)
                g_hava.setLayout(l_hava)
                lay.addWidget(g_hava)

                # --- ANA EKRAN BAŞLIK AYARI ---
                g_baslik = QGroupBox("Ana Ekran Başlığı")
                l_baslik = QVBoxLayout()

                self.txt_ana_baslik = QLineEdit()
                self.txt_ana_baslik.setPlaceholderText("Örn: Ozil - Okulunuzu Seslendirin")
                self.txt_ana_baslik.setText(
                    self.gecici_veri.get("ana_baslik", "Ozil - Okulunuzu Seslendirin")
                )

                l_baslik.addWidget(QLabel("Ana ekranda görünen yazı:"))
                l_baslik.addWidget(self.txt_ana_baslik)
                g_baslik.setLayout(l_baslik)

                lay.addWidget(g_baslik)

                lay.addStretch()
                lay.addStretch()

        def uzaktan_kontrol_arayuzunu_kur(self):
                self.sekme_uzaktan.setLayout(QVBoxLayout())
                self.uzaktan_kontrol_icerik = QWidget()
                lay = QVBoxLayout(self.uzaktan_kontrol_icerik)
                lay.setContentsMargins(15, 15, 15, 15)
                lay.setSpacing(10)

                # --- CİHAZ BİLGİLERİ GRUBU ---
                g_info = QGroupBox("💻 Cihaz ve Bağlantı Bilgileri")
                l_info = QGridLayout()

                l_info.addWidget(QLabel("Bilgisayar Adı:"), 0, 0)
                self.lbl_pc = QLabel(f"<b>{platform.node()}</b>")
                self.lbl_pc.setTextInteractionFlags(Qt.TextSelectableByMouse)
                l_info.addWidget(self.lbl_pc, 0, 1)

                l_info.addWidget(QLabel("Bağlı Wi-Fi:"), 1, 0)
                self.lbl_wifi = QLabel(f"<b>{get_wifi_name()}</b>")
                l_info.addWidget(self.lbl_wifi, 1, 1)

                # --- YENİLEME BUTONU (YENİ) ---
                self.btn_ag_yenile = QPushButton("🔄 Bağlantıyı ve QR Kodu Yenile")
                self.btn_ag_yenile.setObjectName("btn_mavi")  # Stil dosyanıza göre
                self.btn_ag_yenile.setFixedSize(220, 35)
                self.btn_ag_yenile.clicked.connect(self.ag_bilgilerini_yenile_islem)
                l_info.addWidget(self.btn_ag_yenile, 2, 0, 1,
                                 2, alignment=Qt.AlignCenter)

                g_info.setLayout(l_info)
                lay.addWidget(g_info)

                # --- ŞİFRE YÖNETİMİ ---
                g_sifre = QGroupBox("🔐 Merkezi Şifre Yönetimi")
                l_sifre = QGridLayout()
                l_sifre.setSpacing(8)
                self.combo_sifre_tip = QComboBox()
                self.combo_sifre_tip.addItems(
                    ["Yönetici Şifresi", "Uygulama Giriş Şifresi", "Mobil Kumanda Şifresi"])
                self.txt_yeni_sifre1 = QLineEdit()
                self.txt_yeni_sifre1.setPlaceholderText("Yeni Şifre")
                self.txt_yeni_sifre1.setEchoMode(QLineEdit.Password)
                self.txt_yeni_sifre2 = QLineEdit()
                self.txt_yeni_sifre2.setPlaceholderText("Yeni Şifre (Tekrar)")
                self.txt_yeni_sifre2.setEchoMode(QLineEdit.Password)
                btn_sifre_güncelle = QPushButton("ŞİFREYİ GÜNCELLE")
                btn_sifre_güncelle.setObjectName("btn_mavi")
                btn_sifre_güncelle.setFixedSize(160, 35)
                btn_sifre_güncelle.clicked.connect(self.sifre_degistir_islem)

                l_sifre.addWidget(QLabel("Şifre Türü:"), 0, 0)
                l_sifre.addWidget(self.combo_sifre_tip, 0, 1)
                l_sifre.addWidget(QLabel("Yeni Şifre:"), 1, 0)
                l_sifre.addWidget(self.txt_yeni_sifre1, 1, 1)
                l_sifre.addWidget(QLabel("Tekrar:"), 2, 0)
                l_sifre.addWidget(self.txt_yeni_sifre2, 2, 1)
                l_sifre.addWidget(btn_sifre_güncelle, 3, 0, 1,
                                  2, alignment=Qt.AlignCenter)
                g_sifre.setLayout(l_sifre)
                lay.addWidget(g_sifre)

                # --- MOBİL ERİŞİM VE QR KOD (GÜNCELLENEBİLİR ALAN) ---
                self.g_mobil = QGroupBox("📱 Mobil Erişim ve QR Kod")
                self.l_mobil = QHBoxLayout()
                self.l_mobil.setContentsMargins(10, 10, 10, 10)

                self.sol_mobil_etiket = QLabel()
                self.sag_qr_etiket = QLabel()
                self.sag_qr_etiket.setAlignment(Qt.AlignCenter)

                self.l_mobil.addWidget(self.sol_mobil_etiket)
                self.l_mobil.addWidget(self.sag_qr_etiket)
                self.g_mobil.setLayout(self.l_mobil)
                lay.addWidget(self.g_mobil)

                lay.addStretch()
                self.sekme_uzaktan.layout().addWidget(self.uzaktan_kontrol_icerik)

                # İlk açılışta verileri doldur
                self.ag_bilgilerini_yenile_islem()

