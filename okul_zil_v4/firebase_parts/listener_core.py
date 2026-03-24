from .shared import *
from .env_config import FIREBASE_CONFIG, YOLLAR, sifre_hashle

class FirebaseListenerCoreMixin:
        def __init__(self, muzik_klasoru=""):
            super().__init__()
            self.muzik_klasoru = muzik_klasoru
            self.db            = None
            # Başlangıçta şimdiki zamanı referans al — eski Firebase verisi tetiklenmesin
            import time as _time
            _simdi = int(_time.time() * 1000)
            self._son_komut_ts = _simdi
            self._son_anons_ts = _simdi
            self._son_sarki_ts = _simdi
            self._son_sifre_ts = _simdi
            self._son_zil_ts        = _simdi
            self._son_sistem_ts     = _simdi
            self._son_genel_ts      = _simdi
            self._calisiyor         = True

        def run(self):
            try:
                fb = pyrebase.initialize_app(FIREBASE_CONFIG)
                self.db = fb.database()

                # Bağlantı durumunu Firebase'e yaz
                self._durum_yaz(True)

                # Dinleyicileri kur
                self.db.child(YOLLAR["komut"]).stream(self._komut_geldi)
                self.db.child(YOLLAR["anons"]).stream(self._anons_geldi)
                self.db.child(YOLLAR["ses"]).stream(self._ses_geldi)
                self.db.child(YOLLAR["sarki"]).stream(self._sarki_geldi)
                self.db.child(YOLLAR["sifre"]).stream(self._sifre_geldi)
                self.db.child(YOLLAR["zil_sec"]).stream(self._zil_sec_geldi)
                self.db.child(YOLLAR["sistem_durum"]).stream(self._sistem_durum_geldi)
                self.db.child(YOLLAR["genel_ayar"]).stream(self._genel_ayar_geldi)

                # Şarkı ve zil listelerini Firebase'e yükle (arka planda)
                threading.Thread(target=self._sarki_listesi_yukle, daemon=True).start()
                threading.Thread(target=self._zil_listesi_yukle, daemon=True).start()
                threading.Thread(target=self._sifreIlkYukle, daemon=True).start()

                self.sinyal_durum.emit(True)
                log_yaz("Firebase", "Uzaktan kumanda bağlandı", "Firebase")

            except Exception as e:
                print(f"Firebase Dinleyici Hatası: {e}")
                self.sinyal_durum.emit(False)

        def durdur(self):
            """Uygulama kapanırken çağrılır — PC çevrimdışı olarak işaretlenir."""
            self._calisiyor = False
            if self.db:
                try:
                    self._durum_yaz(False)
                except Exception:
                    pass

