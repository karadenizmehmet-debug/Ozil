from .shared import *

class MainWindowAudioPlaybackMixin:
        def ozel_sarki_cal(self, dosya_adi):
                dy = os.path.join(MUZIK_KLASORU, dosya_adi)
                if os.path.exists(dy):
                    try:
                        self.ses_duraklatildi_mi = False
                        self.btn_duraklat.setText("⏸️")
                        pygame.mixer.music.set_volume(
                            float(self.slider.value()) / 100.0)
                        pygame.mixer.music.load(dy)
                        pygame.mixer.music.play()
                        self.calan_ses_anahtari = "ozel_sarki"
                        log_yaz(
                            "Sistem", f"Özel Şarkı Oynatıldı: {dosya_adi}", "Masaüstü")
                    except Exception as e:
                        QMessageBox.warning(self, "Ses Hatası", str(e))

        def manuel_muzik_yayini_toggle(self):
                if self.manuel_muzik_modu:
                    self.manuel_muzik_modu = False
                    self.sesi_kapat()
                else:
                    self.manuel_muzik_modu = True
                    self.teneffus_yayini_aktif = False
                    self.btn_muzik.setText("📻 DURDUR")
                    self.teneffus_muziklerini_hazirla()
                    self.siradaki_muzigi_cal()

        def sesi_duraklat_devam(self):
                if self.ses_duraklatildi_mi:
                    try:
                        pygame.mixer.music.unpause()
                    except:
                        pass
                    self.ses_duraklatildi_mi = False
                    self.btn_duraklat.setText("⏸️")
                else:
                    if pygame.mixer.music.get_busy():
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                        self.ses_duraklatildi_mi = True
                        self.btn_duraklat.setText("▶️")

        def sesi_cal(self, key, manuel_basildi=False, ozel_dosya="Varsayılan"):
                if manuel_basildi and key != "muzik_toggle":
                    self.teneffus_yayini_aktif = False
                    self.manuel_muzik_modu = False
                    self.btn_muzik.setText("📻 Müzik")

                dy = self.sistem_verisi.get("sesler", {}).get(key, "")
                if ozel_dosya != "Varsayılan":
                    dy = os.path.join(ZIL_KLASORU, ozel_dosya)

                if not dy or dy == "Varsayılan" or not os.path.exists(dy):
                    y_mp3 = os.path.join(BASE_DIR, f"{key}.mp3")
                    y_wav = os.path.join(BASE_DIR, f"{key}.wav")
                    if os.path.exists(y_mp3):
                        dy = y_mp3
                    elif os.path.exists(y_wav):
                        dy = y_wav
                    else:
                        return

                if dy and os.path.exists(dy):
                    try:
                        self.ses_duraklatildi_mi = False
                        self.btn_duraklat.setText("⏸️")
                        pygame.mixer.music.set_volume(
                            float(self.slider.value()) / 100.0)
                        pygame.mixer.music.load(dy)
                        pygame.mixer.music.play(fade_ms=2000)
                        self.calan_ses_anahtari = key
                    except:
                        pass

        def sesi_kapat(self):
                try:
                    pygame.mixer.music.fadeout(1500)
                except:
                    pass
                self.calan_ses_anahtari = None
                self.teneffus_yayini_aktif = False
                self.manuel_muzik_modu = False
                self.btn_muzik.setText("📻 Müzik")
                self.ses_duraklatildi_mi = False
                self.btn_duraklat.setText("⏸️")

        def zil_durumu_degistir(self):
                self.zil_aktif = not self.zil_aktif
                if self.zil_aktif:
                    self.btn_durum.setText("SİSTEM: AÇIK")
                    self.btn_durum.setStyleSheet(
                        "background-color:#2ed573; color:white; font-weight:bold; font-size:14px; border-bottom:4px solid #27ae60;")
                else:
                    self.btn_durum.setText("SİSTEM: KAPALI")
                    self.btn_durum.setStyleSheet(
                        "background-color:#ff4757; color:white; font-weight:bold; font-size:14px; border-bottom:4px solid #c0392b;")
                    self.sesi_kapat()
                # Firebase'e güncel durumu bildir
                if hasattr(self, "fb_dinleyici"):
                    self.fb_dinleyici.durum_guncelle(self.zil_aktif)

