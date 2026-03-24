import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QMessageBox, QLabel, QTabWidget)
from PyQt5.QtCore import Qt

from main_window import OkulZilSistemi
from .firebase_client import db
from .security import sifre_hashle


class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("oZil | Kurumsal Erişim")
        self.setFixedSize(450, 680)

        self.setStyleSheet("""
            QWidget { background-color: #1a1a26; font-family: 'Segoe UI', Arial; color: #ffffff; }
            QTabWidget::pane { border: 2px solid #32324d; background: #242438; border-radius: 12px; top: -1px; }
            QTabBar::tab { background: #1a1a26; color: #8a8a9d; padding: 15px 30px;
                           border-top-left-radius: 10px; border-top-right-radius: 10px;
                           font-weight: bold; font-size: 14px; min-width: 120px; }
            QTabBar::tab:selected { background: #242438; color: #7c7eff; border-bottom: 4px solid #7c7eff; }
            QLineEdit { background-color: #2d2d44; border: 2px solid #3d3d5c; border-radius: 10px;
                        color: #ffffff; padding: 12px; font-size: 14px; min-height: 25px; margin-bottom: 5px; }
            QLineEdit:focus { border: 2px solid #7c7eff; }
            QPushButton { background-color: #5d5fef; color: #ffffff; border-radius: 10px;
                          padding: 18px; font-size: 16px; font-weight: bold; margin-top: 10px; }
            QPushButton:hover { background-color: #4a4cdb; }
            QLabel#baslik { font-size: 42px; font-weight: bold; color: #7c7eff; margin-top: 10px; }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 30)

        baslik = QLabel("oZil")
        baslik.setObjectName("baslik")
        baslik.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(baslik)
        main_layout.addWidget(QLabel("<center>Akıllı Okul Sistemleri</center>"))

        self.tabs = QTabWidget()
        self.tab_giris = QWidget()
        giris_layout = QVBoxLayout()
        giris_layout.setContentsMargins(20, 40, 20, 40)
        giris_layout.setSpacing(15)
        self.txt_giris_kod = QLineEdit()
        self.txt_giris_kod.setPlaceholderText("6 Haneli Kurum Kodu")
        self.txt_giris_sifre = QLineEdit()
        self.txt_giris_sifre.setPlaceholderText("Şifre")
        self.txt_giris_sifre.setEchoMode(QLineEdit.Password)
        btn_giris = QPushButton("SİSTEME GİRİŞ YAP")
        btn_giris.clicked.connect(self.giris_islem)
        giris_layout.addWidget(self.txt_giris_kod)
        giris_layout.addWidget(self.txt_giris_sifre)
        giris_layout.addWidget(btn_giris)
        giris_layout.addStretch()
        self.tab_giris.setLayout(giris_layout)

        self.tab_kayit = QWidget()
        kayit_layout = QVBoxLayout()
        kayit_layout.setContentsMargins(20, 40, 20, 40)
        kayit_layout.setSpacing(10)
        self.txt_kayit_kod = QLineEdit()
        self.txt_kayit_kod.setPlaceholderText("Kurum Kodu (6 Hane)")
        self.txt_ad_soyad = QLineEdit()
        self.txt_ad_soyad.setPlaceholderText("Sorumlu Ad Soyad")
        self.txt_tel = QLineEdit()
        self.txt_tel.setPlaceholderText("İletişim Telefon No")
        self.txt_kayit_sifre = QLineEdit()
        self.txt_kayit_sifre.setPlaceholderText("Şifre (Min 8 Karakter)")
        self.txt_kayit_sifre.setEchoMode(QLineEdit.Password)
        self.txt_kayit_sifre_tekrar = QLineEdit()
        self.txt_kayit_sifre_tekrar.setPlaceholderText("Şifre Tekrar")
        self.txt_kayit_sifre_tekrar.setEchoMode(QLineEdit.Password)
        btn_kayit = QPushButton("KAYIT BAŞVURUSU YAP")
        btn_kayit.clicked.connect(self.kayit_islem)
        for w in [self.txt_kayit_kod, self.txt_ad_soyad, self.txt_tel,
                  self.txt_kayit_sifre, self.txt_kayit_sifre_tekrar, btn_kayit]:
            kayit_layout.addWidget(w)
        kayit_layout.addStretch()
        self.tab_kayit.setLayout(kayit_layout)

        self.tabs.addTab(self.tab_giris, "GİRİŞ YAP")
        self.tabs.addTab(self.tab_kayit, "YENİ ÜYELİK")
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def kayit_islem(self):
        kod = self.txt_kayit_kod.text().strip()
        ad = self.txt_ad_soyad.text().strip()
        tel = self.txt_tel.text().strip()
        s1 = self.txt_kayit_sifre.text()
        s2 = self.txt_kayit_sifre_tekrar.text()
        if len(kod) != 6 or s1 != s2 or len(s1) < 8 or not ad or not tel:
            QMessageBox.warning(self, "Hata", "Lütfen bilgileri eksiksiz ve doğru girin!")
            return
        try:
            db.child("okullar").child(kod).set({
                "ad_soyad": ad,
                "telefon": tel,
                "sifre_hash": sifre_hashle(s1),
                "aktif": False
            })
            QMessageBox.information(self, "Başarılı",
                                    "Kayıt talebiniz iletildi.\nOnay sonrası giriş yapabilirsiniz.")
            self.tabs.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Hata: {str(e)}")

    def giris_islem(self):
        kod = self.txt_giris_kod.text().strip()
        sifre = self.txt_giris_sifre.text()
        try:
            okul = db.child("okullar").child(kod).get().val()
            if okul:
                sifre_eslesme = (
                    okul.get("sifre_hash") == sifre_hashle(sifre)
                    or okul.get("sifre") == sifre
                )
                if sifre_eslesme:
                    if okul.get("aktif") is True:
                        with open("ayar.json", "w", encoding="utf-8") as f:
                            json.dump({"kurum_kodu": kod}, f)
                        self.ana_pencereyi_ac()
                    else:
                        QMessageBox.warning(self, "Onay Bekleniyor",
                                            "Kurumunuz henüz onaylanmamış.")
                else:
                    QMessageBox.warning(self, "Hata", "Kod veya şifre hatalı!")
            else:
                QMessageBox.warning(self, "Hata", "Kod veya şifre hatalı!")
        except Exception:
            QMessageBox.critical(self, "Bağlantı Hatası",
                                 "İnternet bağlantınızı kontrol edin.")

    def ana_pencereyi_ac(self):
        self.ana_pencere = OkulZilSistemi()
        self.ana_pencere.show()
        self.close()
