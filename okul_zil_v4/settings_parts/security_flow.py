from .shared import *

class SettingsSecurityFlowMixin:
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
