import os
import sys
from PyQt5.QtWidgets import QApplication
from main_window import OkulZilSistemi
from .login_window import GirisEkrani


def run():
    app = QApplication(sys.argv)
    if os.path.exists("ayar.json"):
        pencere = OkulZilSistemi()
        pencere.show()
    else:
        giris = GirisEkrani()
        giris.show()
    sys.exit(app.exec_())
