from .shared import *

REMOTE_URL = "https://karadenizmehmet-debug.github.io/Ozil/kumanda.html"

class SettingsGeneralRemoteMixin:
        def uzaktan_kontrol_arayuzunu_kur(self):
                self.sekme_uzaktan.setLayout(QVBoxLayout())
                self.uzaktan_kontrol_icerik = QWidget()
                lay = QVBoxLayout(self.uzaktan_kontrol_icerik)
                lay.setContentsMargins(15, 15, 15, 15)
                lay.setSpacing(10)

                g_info = QGroupBox("💻 Cihaz ve Bağlantı Bilgileri")
                l_info = QGridLayout()

                l_info.addWidget(QLabel("Bilgisayar Adı:"), 0, 0)
                self.lbl_pc = QLabel(f"<b>{platform.node()}</b>")
                self.lbl_pc.setTextInteractionFlags(Qt.TextSelectableByMouse)
                l_info.addWidget(self.lbl_pc, 0, 1)

                l_info.addWidget(QLabel("Bağlı Wi-Fi:"), 1, 0)
                self.lbl_wifi = QLabel(f"<b>{get_wifi_name()}</b>")
                l_info.addWidget(self.lbl_wifi, 1, 1)

                self.btn_ag_yenile = QPushButton("🔄 QR Kodu Yenile")
                self.btn_ag_yenile.setObjectName("btn_mavi")
                self.btn_ag_yenile.setFixedSize(220, 35)
                self.btn_ag_yenile.clicked.connect(self.ag_bilgilerini_yenile_islem)
                l_info.addWidget(self.btn_ag_yenile, 2, 0, 1, 2, alignment=Qt.AlignCenter)

                g_info.setLayout(l_info)
                lay.addWidget(g_info)

                g_sifre = QGroupBox("🔐 Merkezi Şifre Yönetimi")
                l_sifre = QGridLayout()
                l_sifre.setSpacing(8)
                self.combo_sifre_tip = QComboBox()
                self.combo_sifre_tip.addItems(["Yönetici Şifresi", "Uygulama Giriş Şifresi", "Mobil Kumanda Şifresi"])
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
                l_sifre.addWidget(btn_sifre_güncelle, 3, 0, 1, 2, alignment=Qt.AlignCenter)
                g_sifre.setLayout(l_sifre)
                lay.addWidget(g_sifre)

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
                self.ag_bilgilerini_yenile_islem()

        def ag_bilgilerini_yenile_islem(self):
                try:
                    wifi = get_wifi_name()
                    self.lbl_wifi.setText(f"<b>{wifi}</b>")
                    self.sol_mobil_etiket.setText(
                        f"<span style='font-size:13px;'>İnternetten erişim bağlantısı:</span><br><br>"
                        f"<b style='color:#0984e3; font-size:15px;'>{REMOTE_URL}</b>"
                    )
                    px = self.ana_pencere.qrcode_olustur(REMOTE_URL)
                    if px:
                        self.sag_qr_etiket.setPixmap(px)
                    log_yaz("Yönetici", "İnternet QR kodu yenilendi", "Ayarlar")
                except Exception as e:
                    print(f"QR güncelleme hatası: {e}")
