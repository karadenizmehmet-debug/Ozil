from .shared import *

class MainWindowAudioPlaylistMixin:
        def teneffus_muziklerini_hazirla(self):
                k = self.sistem_verisi.get("muzik_klasoru", MUZIK_KLASORU)
                if not k or not os.path.exists(k):
                    self.oynatma_listesi = []
                    return
                try:
                    self.oynatma_listesi = [os.path.join(k, f) for f in os.listdir(k)
                                            if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
                except Exception:
                    self.oynatma_listesi = []
                if self.oynatma_listesi:
                    random.shuffle(self.oynatma_listesi)
                    self.muzik_indeks = 0
                    if not self.manuel_muzik_modu:
                        self.teneffus_yayini_aktif = True

        def siradaki_muzigi_cal(self):
                if not self.oynatma_listesi:
                    return
                if self.muzik_indeks >= len(self.oynatma_listesi):
                    self.muzik_indeks = 0
                d = self.oynatma_listesi[self.muzik_indeks]
                ms = self.sistem_verisi.get("muzik_sesi", 30)
                gc = self.slider.value() / 100.0
                try:
                    pygame.mixer.music.set_volume((ms / 100.0) * gc)
                    pygame.mixer.music.load(d)
                    pygame.mixer.music.play(fade_ms=2000)
                    self.calan_ses_anahtari = "teneffus_muzigi"
                    self.muzik_indeks += 1
                except:
                    self.muzik_indeks += 1

