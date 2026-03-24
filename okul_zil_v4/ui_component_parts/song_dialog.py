from .shared import *

class SarkiSecPenceresi(QDialog):
    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere

        self.setWindowTitle("🎵 Müzik Kütüphanesi")
        self.resize(500, 600)
        self.setStyleSheet(MODERN_TEMA)

        layout = QVBoxLayout(self)

        info = QLabel("Çalmak istediğiniz şarkıya tıklayın.")
        info.setStyleSheet("color: #0984e3; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(info)

        self.liste = QListWidget()
        self.liste.setFont(QFont("Segoe UI", 11))
        self.liste.itemClicked.connect(self.secili_oynat)
        layout.addWidget(self.liste)

        btn_kapat = QPushButton("❌ PENCEREYİ KAPAT")
        btn_kapat.setObjectName("btn_kirmizi")
        btn_kapat.setFixedSize(300, 45)
        btn_kapat.clicked.connect(self.reject)
        layout.addWidget(btn_kapat, alignment=Qt.AlignCenter)

        self.listeyi_yukle()

    def listeyi_yukle(self):
        self.liste.clear()
        try:
            if not os.path.isdir(MUZIK_KLASORU):
                mesaj = f"Müzik klasörü bulunamadı:\n{MUZIK_KLASORU}"
                QMessageBox.information(self, "Bilgi", mesaj)
                return

            dosyalar = sorted(
                f for f in os.listdir(MUZIK_KLASORU)
                if f.lower().endswith((".mp3", ".wav", ".ogg"))
            )

            if not dosyalar:
                self.liste.addItem("Klasörde şarkı bulunamadı.")
                self.liste.setEnabled(False)
                return

            self.liste.setEnabled(True)
            self.liste.addItems(dosyalar)

        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Klasör okunurken hata:\n{e}")

    def secili_oynat(self):
        item = self.liste.currentItem()
        if not item or not self.liste.isEnabled():
            return

        try:
            self.ana_pencere.ozel_sarki_cal(item.text())
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Şarkı başlatılırken hata:\n{e}")
