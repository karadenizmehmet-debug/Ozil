from .shared import *

class SettingsAboutMixin:
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
