from .shared import *

class SettingsSpecialMixin:
    def ozel_ses_arayuzunu_kur(self):
            lay = QVBoxLayout(self.sekme_ozel)
            lay.setContentsMargins(10, 10, 10, 10)
            bilgi = QLabel(
                "Buradan her ders için farklı melodiler seçebilirsiniz. Ses seviyesi ana ekrandaki sürgüden ayarlanır.")
            bilgi.setStyleSheet(
                "color: #0984e3; font-weight: bold; margin-bottom: 5px;")
            lay.addWidget(bilgi)

            ul = QHBoxLayout()
            ul.addWidget(QLabel("Gün Seçin:", font=QFont("Arial", 11, QFont.Bold)))
            self.combo_ozel_gun = QComboBox()
            self.combo_ozel_gun.addItems(GUNLER)
            self.combo_ozel_gun.currentTextChanged.connect(
                self.ozel_ses_gun_degisti)
            ul.addWidget(self.combo_ozel_gun)
            ul.addStretch()
            lay.addLayout(ul)

            self.tablo_ozel_ses = QTableWidget(0, 4)
            self.tablo_ozel_ses.setHorizontalHeaderLabels(
                ["Ders", "Öğrenci Giriş Melodisi", "Öğretmen Giriş Melodisi", "Ders Çıkış Melodisi"])
            self.tablo_ozel_ses.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
            self.tablo_ozel_ses.setColumnWidth(0, 90)
            for i in range(1, 4):
                self.tablo_ozel_ses.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            self.tablo_ozel_ses.verticalHeader().setVisible(False)
            self.tablo_ozel_ses.setSelectionMode(QTableWidget.NoSelection)
            lay.addWidget(self.tablo_ozel_ses)

            self.ozel_ses_eski_gun = self.combo_ozel_gun.currentText()
            self.ozel_ses_tablosunu_doldur(self.ozel_ses_eski_gun)

    def hucre_widget_olustur(self, sd):
            c = QComboBox()
            c.addItems(self.klasordeki_melodiler)
            c.setFixedHeight(35)
            if sd in self.klasordeki_melodiler:
                c.setCurrentText(sd)
            return c

    def ozel_ses_tablosunu_doldur(self, gun):
            self.tablo_ozel_ses.setRowCount(0)
            prg = self.gecici_veri.get(gun, [])
            oz = self.gecici_veri.get("ozel_sesler", {}).get(gun, {})
            for r, v in enumerate(prg):
                if not isinstance(v, dict):
                    continue
                self.tablo_ozel_ses.insertRow(r)
                self.tablo_ozel_ses.setRowHeight(r, 50)
                d_adi = v.get("ders", f"{r+1}. Ders")
                d_no = d_adi.split(".")[0] if "." in d_adi else str(r+1)
                i = QTableWidgetItem(d_adi)
                i.setFont(QFont("Arial", 10, QFont.Bold))
                i.setTextAlignment(Qt.AlignCenter)
                i.setFlags(Qt.ItemIsEnabled)
                self.tablo_ozel_ses.setItem(r, 0, i)
                for col, tip in enumerate(["ogr", "ogrt", "cikis"], 1):
                    ayar = oz.get(f"{d_no}_{tip}", {"dosya": "Varsayılan"})
                    self.tablo_ozel_ses.setCellWidget(
                        r, col, self.hucre_widget_olustur(ayar["dosya"]))

    def ozel_ses_tablosundan_al(self, gun):
            gs = {}
            prg = self.gecici_veri.get(gun, [])
            for r, v in enumerate(prg):
                d_adi = v.get("ders", f"{r+1}. Ders")
                d_no = d_adi.split(".")[0] if "." in d_adi else str(r+1)
                for col, tip in enumerate(["ogr", "ogrt", "cikis"], 1):
                    w = self.tablo_ozel_ses.cellWidget(r, col)
                    if w:
                        gs[f"{d_no}_{tip}"] = {"dosya": w.currentText()}
            return gs

    def ozel_ses_gun_degisti(self, y):
            self.gecici_veri["ozel_sesler"][self.ozel_ses_eski_gun] = self.ozel_ses_tablosundan_al(
                self.ozel_ses_eski_gun)
            self.ozel_ses_eski_gun = y
            self.ozel_ses_tablosunu_doldur(y)
