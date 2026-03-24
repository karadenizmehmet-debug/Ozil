from .shared import *
from .title_reader import _okul_basligini_oku

class AcilisEkrani:
        def __init__(self):
            super().__init__()
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.resize(600, 300)
            pencere_ortala(self)

            # Okul adını config'den oku
            satir1, satir2 = _okul_basligini_oku()
            okul_metni = satir1
            if satir2:
                okul_metni += f"\n{satir2}"

            layout = QVBoxLayout(self)
            frame = QFrame()
            frame.setStyleSheet(
                "QFrame { background-color: #192a56; border-radius: 20px; border: 4px solid #273c75; }"
            )
            fl = QVBoxLayout(frame)

            lbl_okul = QLabel(okul_metni)
            lbl_okul.setAlignment(Qt.AlignCenter)
            lbl_okul.setStyleSheet(
                "color: white; font-family: 'Arial Black'; font-size: 24px; "
                "background: transparent; border: none; font-weight: 900; letter-spacing: 2px;"
            )

            lbl_alt = QLabel("Profesyonel Zil Otomasyonu Başlatılıyor...\nGeliştirici: Mehmet KARADENİZ")
            lbl_alt.setAlignment(Qt.AlignCenter)
            lbl_alt.setStyleSheet(
                "color: #dcdde1; font-family: 'Segoe UI'; font-size: 13px; "
                "background: transparent; border: none;"
            )

            fl.addStretch()
            fl.addWidget(lbl_okul)
            fl.addWidget(lbl_alt)
            fl.addStretch()
            layout.addWidget(frame)

            self.setWindowOpacity(0.0)
            self.adim = 0
            self.bekleme = 0
            self.timer = QTimer()
            self.timer.timeout.connect(self.animasyon_isle)
            self.timer.start(30)

        def animasyon_isle(self):
            if self.adim == 0:
                self.setWindowOpacity(self.windowOpacity() + 0.05)
                if self.windowOpacity() >= 1.0:
                    self.adim = 1
                    self.bekleme = 0
            elif self.adim == 1:
                self.bekleme += 1
                if self.bekleme > 30:
                    self.adim = 2
            elif self.adim == 2:
                self.setWindowOpacity(self.windowOpacity() - 0.05)
                if self.windowOpacity() <= 0.0:
                    self.timer.stop()
                    self.close()
                    self.on_finish()

        def baslat(self, on_finish):
            self.on_finish = on_finish
            self.show()

