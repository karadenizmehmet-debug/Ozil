from .shared import *

class MainWindowAudioDialogsMixin:
        def _sablon_sec_dialog(self):
                """Anons şablonları listesini gösterir, seçince metin kutusuna yazar."""
                from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout
                sablonlar = self.sistem_verisi.get("anons_sablonlar", [])
                if not sablonlar:
                    QMessageBox.information(self, "Şablon Yok",
                        "Henüz şablon eklenmemiş.\nAyarlar → Anons Şablonları sekmesinden ekleyebilirsiniz.")
                    return
                dlg = QDialog(self)
                dlg.setWindowTitle("🎤 Anons Şablonu Seç")
                dlg.resize(450, 350)
                dlg.setStyleSheet(MODERN_TEMA)
                lay = QVBoxLayout(dlg)
                liste = QListWidget()
                liste.addItems(sablonlar)
                liste.setFont(QFont("Segoe UI", 11))
                lay.addWidget(liste)
                btn_lay = QHBoxLayout()
                btn_sec = QPushButton("✔️ Seç ve Kapat")
                btn_sec.setObjectName("btn_yesil")
                btn_iptal = QPushButton("İptal")
                btn_lay.addWidget(btn_sec)
                btn_lay.addWidget(btn_iptal)
                lay.addLayout(btn_lay)
                def _sec():
                    item = liste.currentItem()
                    if item:
                        self.txt_anons.setText(item.text())
                    dlg.accept()
                btn_sec.clicked.connect(_sec)
                btn_iptal.clicked.connect(dlg.reject)
                liste.itemDoubleClicked.connect(lambda i: (self.txt_anons.setText(i.text()), dlg.accept()))
                dlg.exec_()

        def sarki_sec_penceresini_ac(self):
                self._sarki_dialog = SarkiSecPenceresi(self)
                self._sarki_dialog.exec_()

