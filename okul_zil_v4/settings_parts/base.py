from .shared import *

class SettingsBaseMixin:
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

    def sekme_guvenlik_kontrol(self, index):
            tab_name = self.sekmeler.tabText(index)
            if tab_name in ["📱 Uzaktan Kontrol", "📜 Log Kayıtları"]:
                if (tab_name == "📱 Uzaktan Kontrol" and not self.uzaktan_kontrol_icerik.isVisible()) or \
                   (tab_name == "📜 Log Kayıtları" and not self.log_icerik.isVisible()):

                    sifre, ok = QInputDialog.getText(
                        self, '🔑 Yönetici Doğrulaması', 'Yönetici Şifresini Girin:', QLineEdit.Password)
                    if ok and sifre == self.gecici_veri.get("yonetici_sifre", "1234"):
                        self.uzaktan_kontrol_icerik.setVisible(True)
                        self.uzaktan_kilit_etiketi.setVisible(False)
                        self.log_icerik.setVisible(True)
                        self.log_kilit_etiketi.setVisible(False)
                        self.log_tablosunu_guncelle()
                        self.eski_sekme_index = index
                    else:
                        if ok:
                            QMessageBox.warning(
                                self, "Hata", "Yönetici şifresi yanlış!")
                        self.sekmeler.setCurrentIndex(self.eski_sekme_index)
            else:
                self.eski_sekme_index = index

    def dosya_sec(self, a):
            d, _ = QFileDialog.getOpenFileName(
                self, "Ses Seç", "", "Ses (*.mp3 *.wav *.ogg)")
            if d:
                self.melodi_kutulari[a].setText(d)

    def ayarlari_kaydet(self):
            self.gecici_veri[self.tablo_ici_eski_gun] = self.tablodan_veriyi_al(
                self.tablo_ici)
            self.gecici_veri[self.tablo_sonu_eski_gun] = self.tablodan_veriyi_al(
                self.tablo_sonu)
            if self.check_ici.isChecked():
                for g in HAFTA_ICI:
                    self.gecici_veri[g] = json.loads(json.dumps(
                        self.gecici_veri[self.combo_ici.currentText()]))
            if self.check_sonu.isChecked():
                for g in HAFTA_SONU:
                    self.gecici_veri[g] = json.loads(json.dumps(
                        self.gecici_veri[self.combo_sonu.currentText()]))
                    # Ana ekran başlığı kaydı
            if hasattr(self, "txt_ana_baslik"):
                baslik = self.txt_ana_baslik.text().strip()
                if not baslik:
                    baslik = "Ozil - Okulunuzu Seslendirin"
                self.gecici_veri["ana_baslik"] = baslik
            if hasattr(self, "txt_hava_sehir"):
                self.gecici_veri["hava_sehir"] = self.txt_hava_sehir.text().strip() or "Konya"
            self.gecici_veri["ozel_sesler"][self.ozel_ses_eski_gun] = self.ozel_ses_tablosundan_al(
                self.ozel_ses_eski_gun)
            self.gecici_veri["hesap_ayarlari"] = {
                "ilk_ders": self.time_ilk_ders.time().toString("HH:mm"),
                "sabah_ders": self.spin_sabah_ders.value(),
                "ogle_sonra_ders": self.spin_ogle_sonra_ders.value(),
                "ders_sure": self.spin_ders_sure.value(),
                "teneffus": self.spin_teneffus.value(),
                "ogle_sure": self.spin_ogle_sure.value(),
                "fark_ogretmen": self.spin_fark_ogretmen.value(),
                "sabah_toplanma": self.spin_sabah_toplanma.value(),
                "ogle_toplanma": self.spin_ogle_toplanma.value()
            }
            self.gecici_veri["sesler"] = {
                k: v.text() for k, v in self.melodi_kutulari.items() if v.text() != "Varsayılan"}
            self.gecici_veri["teneffus_muzigi_aktif"] = self.check_teneffus_aktif.isChecked(
            )
            self.gecici_veri["muzik_klasoru"] = self.txt_muzik_klasoru.text()
            self.gecici_veri["muzik_sesi"] = self.spin_muzik_sesi.value()

            flask_app.mobil_sifre = self.gecici_veri.get("mobil_sifre", "1234")
            flask_app.uygulama_sifre = self.gecici_veri.get(
                "uygulama_sifre", "1234")
            flask_app.yonetici_sifre = self.gecici_veri.get(
                "yonetici_sifre", "1234")

            oto_baslat = self.check_otobaslat.isChecked()
            self.gecici_veri["otomatik_baslat"] = oto_baslat
            oto_baslat_ayarla(oto_baslat)
            # --- YENİ: PC KAPATMA AYARINI KAYDET ---
            self.gecici_veri["pc_kapat_aktif"] = self.check_pc_kapat.isChecked()
            self.gecici_veri["pc_kapat_saat"] = self.time_pc_kapat.time().toString(
                "HH:mm")
            # ---------------------------------------

            # --- AŞAĞIDAKİ KISMI GÜVENLİ (ATOMIC) YAZMA İLE DEĞİŞTİRDİK ---
            gecici_dosya = "ayarlar_temp.json"
            asil_dosya = "ayarlar.json"
           # --- GÜVENLİ (ATOMIC) YAZMA İŞLEMİ ---
            try:
                with open(AYARLAR_TEMP, "w", encoding="utf-8") as f:
                    json.dump(self.gecici_veri, f, ensure_ascii=False, indent=4)

                os.replace(AYARLAR_TEMP, AYARLAR_DOSYASI)

                self.ana_pencere.verileri_yukle()
                self.ana_pencere.arayuzu_guncelle()
                # Ana ekran başlığını anında güncelle
                yeni_baslik = self.gecici_veri.get("ana_baslik", "")
                if yeni_baslik and hasattr(self.ana_pencere, "lbl_okul"):
                    satirlar = yeni_baslik.split(" - ", 1)
                    if len(satirlar) == 2:
                        self.ana_pencere.lbl_okul.setText(f"{satirlar[0]}\n{satirlar[1]}")
                    else:
                        self.ana_pencere.lbl_okul.setText(yeni_baslik)
                # Firebase'e değişen ayarları yansıt
                ana = self.ana_pencere
                if hasattr(ana, "fb_dinleyici"):
                    # 1. Teneffüs müziği ve müzik sesi
                    ana.fb_dinleyici.genel_ayar_guncelle(
                        self.gecici_veri.get("teneffus_muzigi_aktif", True),
                        self.gecici_veri.get("muzik_sesi", 30)
                    )
                    # 2. Zil melodileri
                    sesler = self.gecici_veri.get("sesler", {})
                    for zil_tip in ("toplanma_zil", "ogr_zil", "ogrt_zil", "cikis_zil"):
                        yol = sesler.get(zil_tip, "Varsayılan")
                        ana.zil_melodisi_firebase_yaz(zil_tip, yol)
                    # 3. Şifreler
                    ana._sifreleri_firebase_guncelle()
                QMessageBox.information(
                    self, "Başarılı", "Ayarlar başarıyla kaydedildi!")
                log_yaz("Yönetici", "Sistem Ayarlarını Kaydetti")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kayıt Hatası:\n{e}")
