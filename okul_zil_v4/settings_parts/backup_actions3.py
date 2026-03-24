from .shared import *

class SettingsBackupActionsMixin:
        def yedek_olustur(self):
                """ayarlar.json'ı kullanıcının seçtiği konuma kopyalar."""
                import shutil, datetime as _dt
                tarih = _dt.datetime.now().strftime("%Y%m%d_%H%M")
                varsayilan_ad = f"ozil_yedek_{tarih}.json"
                hedef, _ = QFileDialog.getSaveFileName(
                    self, "Yedek Kaydet", varsayilan_ad, "JSON Dosyası (*.json)")
                if not hedef:
                    return
                try:
                    shutil.copy2(AYARLAR_DOSYASI, hedef)
                    self.lbl_yedek_sonuc.setText(f"✓ Yedek kaydedildi: {hedef}")
                    log_yaz("Yönetici", f"Ayarlar yedeği oluşturuldu: {hedef}")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Yedek oluşturulamadı:\n{e}")

        def yedekten_geri_yukle(self):
                """Seçilen yedek JSON dosyasını ayarlar.json olarak geri yükler."""
                import shutil
                kaynak, _ = QFileDialog.getOpenFileName(
                    self, "Yedek Seç", "", "JSON Dosyası (*.json)")
                if not kaynak:
                    return
                cevap = QMessageBox.question(
                    self, "Emin misiniz?",
                    "Mevcut tüm ayarlarınız yedek dosyasıyla değiştirilecek.\nDevam etmek istiyor musunuz?",
                    QMessageBox.Yes | QMessageBox.No)
                if cevap != QMessageBox.Yes:
                    return
                try:
                    # Doğrulama: geçerli JSON mı?
                    with open(kaynak, "r", encoding="utf-8") as f:
                        import json as _json
                        _json.load(f)
                    shutil.copy2(kaynak, AYARLAR_DOSYASI)
                    self.ana_pencere.verileri_yukle()
                    self.ana_pencere.arayuzu_guncelle()
                    self.gecici_veri = dict(self.ana_pencere.sistem_verisi)
                    self.lbl_geri_sonuc.setText("✓ Geri yükleme başarılı! Ayarlar güncellendi.")
                    log_yaz("Yönetici", f"Ayarlar yedekten geri yüklendi: {kaynak}")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Geri yükleme başarısız:\n{e}")

        def firebase_yedek_yukle(self):
                """Mevcut ayarları Firebase'e yükler (bulut yedek)."""
                import threading, json as _json
                self.pb_fb.setVisible(True)
                self.lbl_fb_sonuc.setText("Yükleniyor...")
                self.lbl_fb_sonuc.setStyleSheet("color:#7f8c8d;")

                ana = self.ana_pencere
                def _yukle():
                    try:
                        fb = ana.fb_dinleyici.db
                        if not fb:
                            raise Exception("Firebase bağlantısı yok")
                        with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as f:
                            ayarlar = _json.load(f)
                        import datetime as _dt
                        ayarlar["_yedek_tarihi"] = _dt.datetime.now().strftime("%d.%m.%Y %H:%M")
                        fb.child("yedek/ayarlar").set(ayarlar)
                        from PyQt5.QtCore import QTimer
                        def _ok():
                            self.pb_fb.setVisible(False)
                            self.lbl_fb_sonuc.setText("✓ Firebase'e yüklendi!")
                            self.lbl_fb_sonuc.setStyleSheet("color:#27ae60; font-weight:bold;")
                        QTimer.singleShot(0, _ok)
                        log_yaz("Yönetici", "Ayarlar Firebase'e yüklendi (bulut yedek)")
                    except Exception as e:
                        from PyQt5.QtCore import QTimer
                        msg = str(e)
                        def _err():
                            self.pb_fb.setVisible(False)
                            self.lbl_fb_sonuc.setText(f"Hata: {msg}")
                            self.lbl_fb_sonuc.setStyleSheet("color:#e74c3c; font-weight:bold;")
                        QTimer.singleShot(0, _err)
                threading.Thread(target=_yukle, daemon=True).start()

        def firebase_yedek_indir(self):
                """Firebase'deki yedek ayarları indirip uygular."""
                import threading, json as _json
                self.pb_fb.setVisible(True)
                self.lbl_fb_sonuc.setText("İndiriliyor...")
                self.lbl_fb_sonuc.setStyleSheet("color:#7f8c8d;")

                ana = self.ana_pencere
                def _indir():
                    try:
                        fb = ana.fb_dinleyici.db
                        if not fb:
                            raise Exception("Firebase bağlantısı yok")
                        veri = fb.child("yedek/ayarlar").get().val()
                        if not veri:
                            raise Exception("Firebase'de kayıtlı yedek bulunamadı")
                        # _yedek_tarihi alanını kaldır
                        veri.pop("_yedek_tarihi", None)
                        from PyQt5.QtCore import QTimer
                        tarih_str = veri.get("_yedek_tarihi", "")
                        def _uygula():
                            cevap = QMessageBox.question(
                                self, "Onay",
                                f"Firebase'deki yedek uygulanacak.\nTarih: {tarih_str}\n\nDevam?",
                                QMessageBox.Yes | QMessageBox.No)
                            if cevap != QMessageBox.Yes:
                                self.pb_fb.setVisible(False)
                                self.lbl_fb_sonuc.setText("İptal edildi.")
                                return
                            try:
                                with open(AYARLAR_DOSYASI, "w", encoding="utf-8") as f:
                                    _json.dump(veri, f, ensure_ascii=False, indent=4)
                                ana.verileri_yukle()
                                ana.arayuzu_guncelle()
                                self.gecici_veri = dict(ana.sistem_verisi)
                                self.pb_fb.setVisible(False)
                                self.lbl_fb_sonuc.setText("✓ Firebase'den indirildi ve uygulandı!")
                                self.lbl_fb_sonuc.setStyleSheet("color:#27ae60; font-weight:bold;")
                                log_yaz("Yönetici", "Ayarlar Firebase'den indirildi")
                            except Exception as ex:
                                self.pb_fb.setVisible(False)
                                self.lbl_fb_sonuc.setText(f"Hata: {ex}")
                        QTimer.singleShot(0, _uygula)
                    except Exception as e:
                        from PyQt5.QtCore import QTimer
                        msg = str(e)
                        def _err():
                            self.pb_fb.setVisible(False)
                            self.lbl_fb_sonuc.setText(f"Hata: {msg}")
                            self.lbl_fb_sonuc.setStyleSheet("color:#e74c3c; font-weight:bold;")
                        QTimer.singleShot(0, _err)
                threading.Thread(target=_indir, daemon=True).start()

