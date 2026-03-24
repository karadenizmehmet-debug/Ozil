from PyQt5.QtCore import QThread, pyqtSignal

REMOTE_URL = "https://karadenizmehmet-debug.github.io/Ozil/kumanda.html"

class _DummyFlaskApp:
    def __init__(self):
        self.mevcut_ses = 100
        self.mobil_sifre = "1234"
        self.uygulama_sifre = "1234"
        self.yonetici_sifre = "1234"
        self.remote_url = REMOTE_URL

flask_app = _DummyFlaskApp()

class WebSunucuThread(QThread):
    sinyal_cal = pyqtSignal(str)
    sinyal_sustur = pyqtSignal()
    sinyal_ses_ayarla = pyqtSignal(int)
    sinyal_sifre_degistir = pyqtSignal(str, str)
    sinyal_sarki_oynat = pyqtSignal(str)
    sinyal_genel_ayar = pyqtSignal(bool, int)
    sinyal_anons_yap = pyqtSignal(str)

    def run(self):
        return
