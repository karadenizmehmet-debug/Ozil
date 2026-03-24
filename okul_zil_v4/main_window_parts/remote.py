from .shared import *

class MainWindowRemoteMixin:
    def ayarlar_penceresini_ac(self):
            sifre, ok = QInputDialog.getText(
                self, '🔒 Güvenlik', 'Şifre:', QLineEdit.Password)
            if ok and sifre == self.sistem_verisi.get("uygulama_sifre", "1234"):
                log_yaz("Yönetici", "Ayarlar menüsüne giriş yapıldı.")
                try:
                    p = AyarlarPenceresi(self)
                    # Ayarlar penceresi açıldığında log listesini tazelediğinden emin ol
                    p.exec_()
                    self.verileri_yukle()  # Ayarlar değiştiyse geri yükle
                    self.arayuzu_guncelle()
                except:
                    QMessageBox.critical(self, "Hata", traceback.format_exc())

    def uzaktan_gelen_cal_emri(self, k):
            if k == "muzik_toggle":
                self.manuel_muzik_yayini_toggle()
            else:
                self.sesi_cal(k, manuel_basildi=True)

    def uzaktan_ses_seviyesi_guncelle(self, val):
            """Mobil/Firebase'den gelen ses — slider'ı güncelle ama Firebase'e tekrar yazma."""
            self._firebase_ses_guncelleme = True
            self.slider.setValue(val)
            self._firebase_ses_guncelleme = False

    def ses_seviyesi_degisti(self, v):
            self.lbl_ses_yuzde.setText(f"%{v}")
            flask_app.mevcut_ses = v
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.set_volume(v / 100.0)
            except:
                pass
            # Firebase'e yaz — ama Firebase'den gelen güncelleme ise döngüye girme
            if getattr(self, "_firebase_ses_guncelleme", False):
                return
            if hasattr(self, "_ses_firebase_timer"):
                self._ses_firebase_timer.stop()
            else:
                self._ses_firebase_timer = QTimer()
                self._ses_firebase_timer.setSingleShot(True)
                self._ses_firebase_timer.timeout.connect(self._ses_firebase_yaz)
            self._ses_son_deger = v
            self._ses_firebase_timer.start(500)

    def _ses_firebase_yaz(self):
            """Debounce sonrası ses seviyesini Firebase'e yazar."""
            v = getattr(self, "_ses_son_deger", self.slider.value())
            flask_app.mevcut_ses = v  # Flask web arayüzü de güncel olsun
            def _yaz():
                try:
                    if hasattr(self, "fb_dinleyici") and self.fb_dinleyici.db:
                        self.fb_dinleyici.db.child("kumanda/ses").set(v)
                except Exception as e:
                    print(f"Ses Firebase yazma hatası: {e}")
            threading.Thread(target=_yaz, daemon=True).start()

    def mobilden_ayar_guncelle(self, teneffus_aktif, muzik_sesi, firebase_kaynak=False):
            """Mobil veya Firebase'den gelen genel ayarları sisteme işler."""
            self.sistem_verisi["teneffus_muzigi_aktif"] = teneffus_aktif
            self.sistem_verisi["muzik_sesi"] = muzik_sesi
            self.ayarlari_guvenli_kaydet()
            log_yaz("Yönetici (Mobil)",
                    f"Genel Ayarlar Güncellendi: Teneffüs:{teneffus_aktif}, Müzik Sesi:%{muzik_sesi}")
            # Eğer o an teneffüs müziği çalıyorsa sesini anında güncelle
            if self.calan_ses_anahtari == "teneffus_muzigi":
                vol = (muzik_sesi / 100.0) * (self.slider.value() / 100.0)
                try:
                    pygame.mixer.music.set_volume(vol)
                except Exception:
                    pass
            # Firebase'den gelmediyse Firebase'e de yaz (Flask web arayüzünden geldi)
            if not firebase_kaynak and hasattr(self, "fb_dinleyici"):
                self.fb_dinleyici.genel_ayar_guncelle(teneffus_aktif, muzik_sesi)

    def sifre_kaydet_backend(self, tip, yeni):
            """Flask web arayüzünden gelen şifre değişikliği."""
            self.sistem_verisi[f"{tip}_sifre"] = yeni
            if tip == "mobil":
                flask_app.mobil_sifre = yeni
            elif tip == "uygulama":
                flask_app.uygulama_sifre = yeni
            elif tip == "yonetici":
                flask_app.yonetici_sifre = yeni
            # Dosyaya kaydet ve Firebase'e yolla
            self.ayarlari_guvenli_kaydet()
            self._sifreleri_firebase_guncelle()
