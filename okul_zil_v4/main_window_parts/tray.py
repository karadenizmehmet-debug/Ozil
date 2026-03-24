from .shared import *

class MainWindowTrayMixin:
    def tepsi_ikonu_olustur(self):
            self.tray_icon = QSystemTrayIcon(self)

            # --- ÖZEL İKON AYARI ---
            # İkon dosyanızın tam adını buraya yazın (.ico da olabilir)
            ikon_dosyasi = "zil_ikon.png"

            if os.path.exists(IKON_DOSYASI):
                from PyQt5.QtGui import QIcon
                self.tray_icon.setIcon(QIcon(IKON_DOSYASI))
            else:
                self.tray_icon.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaVolume))
            # -----------------------

            m = QMenu()
            ag = QAction("Göster", self)
            ag.triggered.connect(self.showNormal)
            ac = QAction("Kapat", self)
            ac.triggered.connect(self.gercekten_kapat)
            m.addAction(ag)
            m.addAction(ac)
            self.tray_icon.setContextMenu(m)
            self.tray_icon.show()

            # Çift tıklama olayını dinle (Bir önceki adımda eklemiştik)
            self.tray_icon.activated.connect(self.tepsi_ikonu_tiklandi)

    def tepsi_ikonu_tiklandi(self, reason):
            """Sistem tepsisindeki ikona çift tıklandığında pencereyi açar."""
            if reason == QSystemTrayIcon.DoubleClick:
                self.showNormal()          # Pencereyi görünür yap
                self.activateWindow()

    def arka_plana_gizle(self):
            self.hide()

    def closeEvent(self, e):
            e.ignore()
            self.arka_plana_gizle()

    def gercekten_kapat(self):
            """Uygulama tamamen kapatılırken çağrılır (tepsi menüsündeki Kapat butonu)."""
            if hasattr(self, 'fb_dinleyici'):
                self.fb_dinleyici.durdur()
            QApplication.quit()
