from .shared import *

class SettingsBackupOpsMixin:
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

        def yedek_olustur(self):
                """ayarlar.json'ı kullanıcının seçtiği konuma kopyalar."""
                import shutil, datetime as _dt
                tarih = _dt.datetime.now().strftime("%Y%m%d_%H%M")
                varsayilan_ad = f"ozil_yedek_{tarih}.json"
                hedef, _ = QFileDialog.getSaveFileName(
                    self, "Yedek Kaydet", varsayilan_ad, "JSON Dosyası (*.json)")
                if not hedef:
                    return
                try:
                    shutil.copy2(AYARLAR_DOSYASI, hedef)
                    self.lbl_yedek_sonuc.setText(f"✓ Yedek kaydedildi: {hedef}")
                    log_yaz("Yönetici", f"Ayarlar yedeği oluşturuldu: {hedef}")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Yedek oluşturulamadı:\n{e}")

        def yedekten_geri_yukle(self):
                """Seçilen yedek JSON dosyasını ayarlar.json olarak geri yükler."""
                import shutil
                kaynak, _ = QFileDialog.getOpenFileName(
                    self, "Yedek Seç", "", "JSON Dosyası (*.json)")
                if not kaynak:
                    return
                cevap = QMessageBox.question(
                    self, "Emin misiniz?",
                    "Mevcut tüm ayarlarınız yedek dosyasıyla değiştirilecek.\nDevam etmek istiyor musunuz?",
                    QMessageBox.Yes | QMessageBox.No)
                if cevap != QMessageBox.Yes:
                    return
                try:
                    # Doğrulama: geçerli JSON mı?
                    with open(kaynak, "r", encoding="utf-8") as f:
                        import json as _json
                        _json.load(f)
                    shutil.copy2(kaynak, AYARLAR_DOSYASI)
                    self.ana_pencere.verileri_yukle()
                    self.ana_pencere.arayuzu_guncelle()
                    self.gecici_veri = dict(self.ana_pencere.sistem_verisi)
                    self.lbl_geri_sonuc.setText("✓ Geri yükleme başarılı! Ayarlar güncellendi.")
                    log_yaz("Yönetici", f"Ayarlar yedekten geri yüklendi: {kaynak}")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Geri yükleme başarısız:\n{e}")
