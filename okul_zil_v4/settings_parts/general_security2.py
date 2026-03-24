from .shared import *

class SettingsGeneralSecurityMixin:
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

