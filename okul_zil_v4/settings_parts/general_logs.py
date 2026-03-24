from .shared import *

class SettingsGeneralLogsMixin:
        def log_arayuzunu_kur(self):
                self.sekme_loglar.setLayout(QVBoxLayout())
                self.log_icerik = QWidget()
                lay = QVBoxLayout(self.log_icerik)
                lay.setContentsMargins(15, 15, 15, 15)

                head_lay = QHBoxLayout()
                head_lay.addWidget(
                    QLabel("📜 Sistem Erişim ve İşlem Kayıtları (Son 500)"))
                btn_yenile = QPushButton("🔄 Yenile")
                btn_yenile.clicked.connect(self.log_tablosunu_guncelle)
                head_lay.addStretch()
                head_lay.addWidget(btn_yenile)
                lay.addLayout(head_lay)

                self.tablo_loglar = QTableWidget(0, 4)
                self.tablo_loglar.setHorizontalHeaderLabels(
                    ["Tarih/Saat", "Kullanıcı", "İşlem", "Cihaz/IP"])
                self.tablo_loglar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tablo_loglar.setEditTriggers(QTableWidget.NoEditTriggers)
                lay.addWidget(self.tablo_loglar)

                self.sekme_loglar.layout().addWidget(self.log_icerik)

        def log_tablosunu_guncelle(self):
                self.tablo_loglar.setRowCount(0)
                if os.path.exists(LOG_DOSYASI):
                    try:
                        with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                            loglar = json.load(f)
                            for r, l in enumerate(loglar):
                                self.tablo_loglar.insertRow(r)
                                self.tablo_loglar.setItem(
                                    r, 0, QTableWidgetItem(l.get("tarih", "")))
                                self.tablo_loglar.setItem(
                                    r, 1, QTableWidgetItem(l.get("kullanici", "")))
                                self.tablo_loglar.setItem(
                                    r, 2, QTableWidgetItem(l.get("islem", "")))
                                self.tablo_loglar.setItem(
                                    r, 3, QTableWidgetItem(l.get("cihaz", "")))
                    except:
                        pass

        def sifre_degistir_islem(self):
                tip_idx = self.combo_sifre_tip.currentIndex()
                tip_map = ["yonetici", "uygulama", "mobil"]
                tip = tip_map[tip_idx]

                y1 = self.txt_yeni_sifre1.text()
                y2 = self.txt_yeni_sifre2.text()

                if y1 != y2:
                    QMessageBox.warning(self, "Hata", "Yeni şifreler uyuşmuyor!")
                    return
                if len(y1) < 4:
                    QMessageBox.warning(self, "Hata", "Şifre en az 4 karakter olmalı!")
                    return

                self.gecici_veri[f"{tip}_sifre"] = y1
                if tip == "mobil":
                    flask_app.mobil_sifre = y1
                elif tip == "uygulama":
                    flask_app.uygulama_sifre = y1
                elif tip == "yonetici":
                    flask_app.yonetici_sifre = y1

                # ayarlar.json'a hemen kaydet ve Firebase'i güncelle
                self.ana_pencere.sistem_verisi[f"{tip}_sifre"] = y1
                self.ana_pencere.ayarlari_guvenli_kaydet()
                self.ana_pencere._sifreleri_firebase_guncelle()

                QMessageBox.information(
                    self, "Başarılı", f"{self.combo_sifre_tip.currentText()} güncellendi ve Firebase'e yansıtıldı.")
                log_yaz("Yönetici (PC)", f"{tip} şifresini güncelledi")
                self.txt_yeni_sifre1.clear()
                self.txt_yeni_sifre2.clear()
