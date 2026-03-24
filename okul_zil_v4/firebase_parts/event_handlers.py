from .shared import *
from .env_config import FIREBASE_CONFIG, YOLLAR, sifre_hashle

class FirebaseEventHandlersMixin:
        def _komut_geldi(self, mesaj):
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_komut_ts:
                    return  # eski veya tekrar eden komut
                self._son_komut_ts = ts
                kod = veri.get("kod", "")
                if kod == "sustur":
                    self.sinyal_cal.emit("sustur")
                elif kod:
                    self.sinyal_cal.emit(kod)
                    log_yaz("Firebase Kumanda", f"Komut: {kod}", "İnternet")
            except Exception as e:
                print(f"Komut işleme hatası: {e}")

        def _anons_geldi(self, mesaj):
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_anons_ts:
                    return
                self._son_anons_ts = ts
                metin = veri.get("metin", "").strip()
                if metin:
                    self.sinyal_anons.emit(metin)
                    log_yaz("Firebase Kumanda", f"Anons: {metin[:40]}...", "İnternet")
            except Exception as e:
                print(f"Anons işleme hatası: {e}")

        def _ses_geldi(self, mesaj):
            try:
                veri = mesaj.get("data")
                if veri is not None:
                    self.sinyal_ses.emit(int(veri))
            except Exception as e:
                print(f"Ses işleme hatası: {e}")

        def _sarki_geldi(self, mesaj):
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_sarki_ts:
                    return
                self._son_sarki_ts = ts
                ad = veri.get("ad", "").strip()
                if ad:
                    self.sinyal_sarki.emit(ad)
                    log_yaz("Firebase Kumanda", f"Şarkı: {ad}", "İnternet")
            except Exception as e:
                print(f"Şarkı işleme hatası: {e}")

        def _sifre_geldi(self, mesaj):
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_sifre_ts:
                    return
                self._son_sifre_ts = ts
                tip  = veri.get("tip", "")
                hash_ = veri.get("hash", "")
                if tip and hash_:
                    self.sinyal_sifre.emit(tip, hash_)
                    log_yaz("Firebase Kumanda", f"{tip} şifresi değiştirildi", "İnternet")
            except Exception as e:
                print(f"Şifre işleme hatası: {e}")

