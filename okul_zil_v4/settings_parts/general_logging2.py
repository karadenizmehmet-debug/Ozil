from .shared import *

class SettingsGeneralLoggingMixin:
        def log_arayuzunu_kur(self):
                self.sekme_loglar.setLayout(QVBoxLayout())
                self.log_icerik = QWidget()
                lay = QVBoxLayout(self.log_icerik)
                lay.setContentsMargins(15, 15, 15, 15)

                head_lay = QHBoxLayout()
                head_lay.addWidget(
                    QLabel("📜 Sistem Erişim ve İşlem Kayıtları (Son 500)"))
                btn_yenile = QPushButton("🔄 Yenile")
                btn_yenile.clicked.connect(self.log_tablosunu_guncelle)
                head_lay.addStretch()
                head_lay.addWidget(btn_yenile)
                lay.addLayout(head_lay)

                self.tablo_loglar = QTableWidget(0, 4)
                self.tablo_loglar.setHorizontalHeaderLabels(
                    ["Tarih/Saat", "Kullanıcı", "İşlem", "Cihaz/IP"])
                self.tablo_loglar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tablo_loglar.setEditTriggers(QTableWidget.NoEditTriggers)
                lay.addWidget(self.tablo_loglar)

                self.sekme_loglar.layout().addWidget(self.log_icerik)

        def log_tablosunu_guncelle(self):
                self.tablo_loglar.setRowCount(0)
                if os.path.exists(LOG_DOSYASI):
                    try:
                        with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                            loglar = json.load(f)
                            for r, l in enumerate(loglar):
                                self.tablo_loglar.insertRow(r)
                                self.tablo_loglar.setItem(
                                    r, 0, QTableWidgetItem(l.get("tarih", "")))
                                self.tablo_loglar.setItem(
                                    r, 1, QTableWidgetItem(l.get("kullanici", "")))
                                self.tablo_loglar.setItem(
                                    r, 2, QTableWidgetItem(l.get("islem", "")))
                                self.tablo_loglar.setItem(
                                    r, 3, QTableWidgetItem(l.get("cihaz", "")))
                    except:
                        pass

