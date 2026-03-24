from .shared import *

class SettingsBackupLayoutMixin:
        def yedek_guncelle_arayuzunu_kur(self):
                """Yedekleme, geri yükleme ve uzak güncelleme sekmesi."""
                import platform as _platform
                lay = QVBoxLayout(self.sekme_yedek)
                lay.setContentsMargins(15, 15, 15, 15)
                lay.setSpacing(12)

                # --- YEDEKLEME ---
                g_yedek = QGroupBox("💾 Ayarları Yedekle")
                l_y = QVBoxLayout()
                l_y.addWidget(QLabel("Tüm ayarlarınızı (zil saatleri, ses dosyaları, şifreler) dışa aktarın."))
                btn_yedek = QPushButton("📤  Yedek Dosyası Oluştur ve Kaydet")
                btn_yedek.setObjectName("btn_mavi")
                btn_yedek.setFixedHeight(40)
                btn_yedek.clicked.connect(self.yedek_olustur)
                l_y.addWidget(btn_yedek)
                self.lbl_yedek_sonuc = QLabel("")
                self.lbl_yedek_sonuc.setStyleSheet("color:#27ae60; font-weight:bold;")
                l_y.addWidget(self.lbl_yedek_sonuc)
                g_yedek.setLayout(l_y)
                lay.addWidget(g_yedek)

                # --- GERİ YÜKLEME ---
                g_geri = QGroupBox("📥 Yedekten Geri Yükle")
                l_g = QVBoxLayout()
                l_g.addWidget(QLabel("Daha önce oluşturduğunuz yedek dosyasını seçin."))
                btn_geri = QPushButton("📂  Yedek Seç ve Geri Yükle")
                btn_geri.setObjectName("btn_turuncu")
                btn_geri.setFixedHeight(40)
                btn_geri.clicked.connect(self.yedekten_geri_yukle)
                l_g.addWidget(btn_geri)
                self.lbl_geri_sonuc = QLabel("")
                self.lbl_geri_sonuc.setStyleSheet("color:#e67e22; font-weight:bold;")
                l_g.addWidget(self.lbl_geri_sonuc)
                g_geri.setLayout(l_g)
                lay.addWidget(g_geri)

                # --- UZAK GÜNCELLEME ---
                g_gunc = QGroupBox("🔄 Uzak Güncelleme (Firebase)")
                l_gunc = QVBoxLayout()
                bilgi = QLabel(
                    "Firebase üzerinden yeni program ayarları veya ders programı gelirse\n"
                    "buradan çekebilirsiniz. Okul ağı dışındayken de çalışır."
                )
                bilgi.setStyleSheet("color:#7f8c8d; font-size:12px;")
                l_gunc.addWidget(bilgi)

                btn_fb_yedek = QPushButton("☁️  Ayarları Firebase'e Yükle (Bulut Yedek)")
                btn_fb_yedek.setObjectName("btn_mavi")
                btn_fb_yedek.setFixedHeight(40)
                btn_fb_yedek.clicked.connect(self.firebase_yedek_yukle)

                btn_fb_geri = QPushButton("⬇️  Firebase'den Ayarları İndir")
                btn_fb_geri.setObjectName("btn_yesil")
                btn_fb_geri.setFixedHeight(40)
                btn_fb_geri.clicked.connect(self.firebase_yedek_indir)

                self.lbl_fb_sonuc = QLabel("")
                self.lbl_fb_sonuc.setStyleSheet("font-weight:bold;")
                self.pb_fb = QProgressBar()
                self.pb_fb.setRange(0, 0)
                self.pb_fb.setVisible(False)
                self.pb_fb.setFixedHeight(8)

                l_gunc.addWidget(btn_fb_yedek)
                l_gunc.addWidget(btn_fb_geri)
                l_gunc.addWidget(self.pb_fb)
                l_gunc.addWidget(self.lbl_fb_sonuc)
                g_gunc.setLayout(l_gunc)
                lay.addWidget(g_gunc)
                lay.addStretch()

        def hakkinda_arayuzunu_kur(self):
                lay = QVBoxLayout(self.sekme_hakkinda)
                lay.setContentsMargins(40, 40, 40, 40)
                from PyQt5.QtWidgets import QFrame  # Import eksikliğini gidermek için
                frame_main = QFrame()
                frame_main.setStyleSheet(
                    "background-color: #2c3e50; border-radius: 15px;")
                v_main = QVBoxLayout(frame_main)
                lbl_star = QLabel("★")
                lbl_star.setStyleSheet("color: #f1c40f; font-size: 40px;")
                lbl_star.setAlignment(Qt.AlignCenter)
                lbl_baslik = QLabel("ZİL SİSTEMİ OTOMASYONU")
                lbl_baslik.setStyleSheet(
                    "color: white; font-size: 22px; font-weight: bold;")
                lbl_baslik.setAlignment(Qt.AlignCenter)
                lbl_versiyon = QLabel("Versiyon 3.0.1 - Güvenli Sürüm")
                lbl_versiyon.setStyleSheet("color: #bdc3c7; font-size: 13px;")
                lbl_versiyon.setAlignment(Qt.AlignCenter)
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet("background-color: #34495e; max-height: 1px;")
                lbl_dev = QLabel("Geliştirici: <b>Mehmet KARADENİZ</b>")
                lbl_dev.setStyleSheet("color: white; font-size: 16px;")
                lbl_dev.setAlignment(Qt.AlignCenter)
                lbl_okul_bilgi = QLabel(
                    "Akşehir / Nimetullah Nahçivani İmam Hatip Ortaokulu\nBilişim Teknolojileri Öğretmeni")
                lbl_okul_bilgi.setStyleSheet("color: #ecf0f1; font-size: 13px;")
                lbl_okul_bilgi.setAlignment(Qt.AlignCenter)

                lbl_contact = QLabel("📧 karadenizmehmet@gmail.com\n📞 0506 494 00 21")
                lbl_contact.setStyleSheet(
                    "color: #f1c40f; font-size: 14px; font-weight: bold; margin-top: 10px;")
                lbl_contact.setAlignment(Qt.AlignCenter)

                lbl_footer = QLabel("© 2026 Tüm Hakları Saklıdır")
                lbl_footer.setStyleSheet("color: #7f8c8d; font-size: 10px;")
                lbl_footer.setAlignment(Qt.AlignCenter)

                v_main.addWidget(lbl_star)
                v_main.addWidget(lbl_baslik)
                v_main.addWidget(lbl_versiyon)
                v_main.addSpacing(10)
                v_main.addWidget(line)
                v_main.addSpacing(10)
                v_main.addWidget(lbl_dev)
                v_main.addWidget(lbl_okul_bilgi)
                v_main.addWidget(lbl_contact)
                v_main.addStretch()
                v_main.addWidget(lbl_footer)
                lay.addWidget(frame_main)

