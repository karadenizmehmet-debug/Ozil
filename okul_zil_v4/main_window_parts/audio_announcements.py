from .shared import *

class MainWindowAudioAnnouncementMixin:
        def anons_yap_tetikle(self):
                metin = self.txt_anons.text().strip()
                if not metin:
                    return

                # Şifre koruması
                sifre, ok = QInputDialog.getText(
                    self, "🔒 Anons Onayı", "Anons yapmak için şifre girin:", QLineEdit.Password)
                if not ok or sifre != self.sistem_verisi.get("uygulama_sifre", "1234"):
                    if ok:
                        QMessageBox.warning(self, "Hata", "Şifre yanlış!")
                    return

                tekrar = int(self.combo_anons_tekrar.currentText().replace("x", ""))
                self.txt_anons.setText("Anons hazırlanıyor, lütfen bekleyin...")
                self.txt_anons.setEnabled(False)

                # Arayüzün donmaması için işlemi ayrı bir thread (iş parçacığı) içinde başlatıyoruz
                threading.Thread(target=self._anons_arka_plan,
                                 args=(metin, tekrar), daemon=True).start()

        def uzaktan_gelen_anons_emri(self, metin):
                import threading
                # metin "METİN||2" formatında gelebilir (tekrar sayısı dahil)
                tekrar = 1
                if "||" in metin:
                    parcalar = metin.split("||", 1)
                    metin = parcalar[0].strip()
                    try:
                        tekrar = int(parcalar[1])
                    except Exception:
                        tekrar = 1
                threading.Thread(target=self._anons_arka_plan,
                                 args=(metin, tekrar), daemon=True).start()

        def _anons_arka_plan(self, metin, tekrar=1):
                """Arka plan thread'inde çalışır. UI güncellemeleri sinyal ile ana thread'e gönderilir."""
                import time as _time
                import traceback as _tb
                try:
                    tekrar = max(1, min(int(tekrar), 3))

                    # 1. ANONS_KLASORU yoksa oluştur
                    os.makedirs(ANONS_KLASORU, exist_ok=True)

                    # 2. Eski anons dosyalarını temizle
                    for f in os.listdir(ANONS_KLASORU):
                        if f.startswith("temp_anons_") and f.endswith(".mp3"):
                            try:
                                os.remove(os.path.join(ANONS_KLASORU, f))
                            except Exception:
                                pass

                    # 3. Benzersiz dosya adı
                    dsy = os.path.join(ANONS_KLASORU, f"temp_anons_{int(_time.time())}.mp3")

                    # 4. TTS oluştur
                    print(f"[Anons] gTTS başlıyor: {metin[:40]}")
                    tts = gTTS(text=metin, lang='tr')
                    tts.save(dsy)
                    print(f"[Anons] Dosya kaydedildi: {dsy}")

                    if not os.path.exists(dsy) or os.path.getsize(dsy) == 0:
                        raise Exception("TTS dosyası oluşturulamadı veya boş")

                    # 5. Ana thread'e "anons çal" sinyali gönder
                    # lambda yerine functools.partial — Python 3.11'de daha güvenilir
                    from functools import partial as _partial
                    QTimer.singleShot(0, _partial(self._anons_oynat, dsy, tekrar, metin))

                except Exception as e:
                    hata = f"Anons Hatası: {e}\n{_tb.format_exc()}"
                    print(hata)
                    log_yaz("Sistem", f"Anons Hatası: {e}", "Yerel PC")
                    QTimer.singleShot(0, self._anons_temizle)

        def _anons_oynat(self, dsy, tekrar, metin):
                """Ana thread'de çalışır — pygame ve UI güncellemeleri burada yapılır."""
                try:
                    print(f"[Anons] Oynatılıyor: {dsy}, boyut: {os.path.getsize(dsy)} byte")
                    print(f"[Anons] Mixer durumu: {pygame.mixer.get_init()}")
                    print(f"[Anons] Slider: %{self.slider.value()}")
                    pygame.mixer.music.stop()
                    vol = float(self.slider.value()) / 100.0
                    pygame.mixer.music.set_volume(vol)
                    pygame.mixer.music.load(dsy)
                    pygame.mixer.music.play()
                    print(f"[Anons] play() çağrıldı, get_busy: {pygame.mixer.music.get_busy()}")
                    self.calan_ses_anahtari = "anons"
                    self.ses_duraklatildi_mi = False
                    self.btn_duraklat.setText("⏸️")
                    log_yaz("Sistem", f"Sesli Anons ({tekrar}x): {metin[:30]}...", "Yerel PC")

                    # Tekrar > 1 ise tekrar sayacı başlat
                    if tekrar > 1:
                        self._anons_tekrar_kalan = tekrar - 1
                        self._anons_dosya = dsy
                        if not hasattr(self, "_anons_tekrar_timer"):
                            self._anons_tekrar_timer = QTimer()
                            self._anons_tekrar_timer.timeout.connect(self._anons_tekrar_kontrol)
                        self._anons_tekrar_timer.start(500)
                    else:
                        self._anons_temizle()
                except Exception as e:
                    print(f"Anons oynatma hatası: {e}")
                    self._anons_temizle()

        def _anons_tekrar_kontrol(self):
                """QTimer ile her 500ms kontrol eder, ses bittiyse tekrar çalar."""
                try:
                    if not pygame.mixer.music.get_busy():
                        if self._anons_tekrar_kalan > 0:
                            self._anons_tekrar_kalan -= 1
                            pygame.mixer.music.load(self._anons_dosya)
                            pygame.mixer.music.play()
                        else:
                            self._anons_tekrar_timer.stop()
                            self._anons_temizle()
                except Exception:
                    if hasattr(self, "_anons_tekrar_timer"):
                        self._anons_tekrar_timer.stop()
                    self._anons_temizle()

        def _anons_temizle(self):
                """Anons bitince metin kutusunu temizler."""
                self.txt_anons.clear()
                self.txt_anons.setEnabled(True)

