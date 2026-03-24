from .shared import *

class SettingsScheduleOpsMixin:
        def ders_ekle_cikar(self, hedef, islem):
                aktif_gun = self.combo_ici.currentText(
                ) if hedef == "ici" else self.combo_sonu.currentText()
                tablo = self.tablo_ici if hedef == "ici" else self.tablo_sonu
                self.gecici_veri[aktif_gun] = self.tablodan_veriyi_al(tablo)
                prog = self.gecici_veri.get(aktif_gun, [])

                if islem == "ekle":
                    n = len(prog) + 1
                    il = self.time_ilk_ders.time()
                    sd = self.spin_sabah_ders.value()
                    ds = self.spin_ders_sure.value()
                    te = self.spin_teneffus.value()
                    og = self.spin_ogle_sure.value()
                    fk = self.spin_fark_ogretmen.value()
                    st = self.spin_sabah_toplanma.value()
                    ot = self.spin_ogle_toplanma.value()

                    if n == 1:
                        ogr_giris = il.addSecs(-fk * 60)
                        topl = ogr_giris.addSecs(-st * 60).toString("HH:mm")
                        c = il.addSecs(ds * 60)
                    else:
                        on = prog[-1]
                        if on.get("cikis") and on.get("cikis") != "--:--":
                            oc = QTime.fromString(on["cikis"], "HH:mm")
                            if n == sd + 1:
                                il = oc.addSecs(og * 60)
                                ogr_giris = il.addSecs(-fk * 60)
                                topl = ogr_giris.addSecs(-ot * 60).toString("HH:mm")
                            else:
                                il = oc.addSecs(te * 60)
                                ogr_giris = il.addSecs(-fk * 60)
                                topl = ""
                            c = il.addSecs(ds * 60)
                        else:
                            il = QTime()

                    if il.isValid():
                        prog.append({"ders": f"{n}. Ders", "toplanma": topl, "ogrenci": ogr_giris.toString(
                            "HH:mm"), "ogretmen": il.toString("HH:mm"), "cikis": c.toString("HH:mm")})
                    else:
                        prog.append({"ders": f"{n}. Ders", "toplanma": "--:--",
                                    "ogrenci": "--:--", "ogretmen": "--:--", "cikis": "--:--"})

                elif islem == "cikar" and len(prog) > 0:
                    prog.pop()

                self.gecici_veri[aktif_gun] = prog
                self.tabloyu_doldur(tablo, aktif_gun)

        def otomatik_hesapla(self, hedef):
                su_an = self.time_ilk_ders.time()
                sd = self.spin_sabah_ders.value()
                od = self.spin_ogle_sonra_ders.value()
                ds = self.spin_ders_sure.value()
                te = self.spin_teneffus.value()
                og = self.spin_ogle_sure.value()
                fk = self.spin_fark_ogretmen.value()
                st = self.spin_sabah_toplanma.value()
                ot = self.spin_ogle_toplanma.value()

                yeni = []
                for i in range(1, sd + od + 1):
                    ogr = su_an.addSecs(-fk * 60)
                    topl = ogr.addSecs(-st * 60).toString("HH:mm") if i == 1 else (
                        ogr.addSecs(-ot * 60).toString("HH:mm") if i == sd+1 else "")
                    c = su_an.addSecs(ds * 60)
                    yeni.append({"ders": f"{i}. Ders", "toplanma": topl, "ogrenci": ogr.toString(
                        "HH:mm"), "ogretmen": su_an.toString("HH:mm"), "cikis": c.toString("HH:mm")})
                    su_an = c.addSecs(og * 60) if i == sd else c.addSecs(te * 60)

                if hedef == "ici":
                    if self.check_ici.isChecked():
                        for g in HAFTA_ICI:
                            self.gecici_veri[g] = json.loads(json.dumps(yeni))
                    else:
                        self.gecici_veri[self.combo_ici.currentText()] = yeni
                    self.tabloyu_doldur(self.tablo_ici, self.combo_ici.currentText())
                else:
                    if self.check_sonu.isChecked():
                        for g in HAFTA_SONU:
                            self.gecici_veri[g] = json.loads(json.dumps(yeni))
                    else:
                        self.gecici_veri[self.combo_sonu.currentText()] = yeni
                    self.tabloyu_doldur(self.tablo_sonu, self.combo_sonu.currentText())

        def tabloyu_doldur(self, tablo, gun):
                tablo.setRowCount(0)
                prg = self.gecici_veri.get(gun, [])
                for r, v in enumerate(prg):
                    if not isinstance(v, dict):
                        continue
                    tablo.insertRow(r)
                    i = QTableWidgetItem(v.get("ders", ""))
                    i.setFlags(Qt.ItemIsEnabled)
                    tablo.setItem(r, 0, i)
                    tablo.setItem(r, 1, QTableWidgetItem(v.get("toplanma", "")))
                    tablo.setItem(r, 2, QTableWidgetItem(v.get("ogrenci", "")))
                    tablo.setItem(r, 3, QTableWidgetItem(v.get("ogretmen", "")))
                    tablo.setItem(r, 4, QTableWidgetItem(v.get("cikis", "")))

        def tablodan_veriyi_al(self, tablo):
                y = []
                for r in range(tablo.rowCount()):
                    d = tablo.item(r, 0).text() if tablo.item(r, 0) else ""
                    if d:
                        y.append({
                            "ders": d,
                            "toplanma": tablo.item(r, 1).text(),
                            "ogrenci": tablo.item(r, 2).text(),
                            "ogretmen": tablo.item(r, 3).text(),
                            "cikis": tablo.item(r, 4).text()
                        })
                return y

        def hafta_ici_gun_degisti(self, y):
                self.gecici_veri[self.tablo_ici_eski_gun] = self.tablodan_veriyi_al(
                    self.tablo_ici)
                self.tablo_ici_eski_gun = y
                self.tabloyu_doldur(self.tablo_ici, y)

        def hafta_sonu_gun_degisti(self, y):
                self.gecici_veri[self.tablo_sonu_eski_gun] = self.tablodan_veriyi_al(
                    self.tablo_sonu)
                self.tablo_sonu_eski_gun = y
                self.tabloyu_doldur(self.tablo_sonu, y)
