from .shared import *
from .env_config import FIREBASE_CONFIG, YOLLAR, sifre_hashle

class FirebaseSyncOpsMixin:
        def _durum_yaz(self, cevrimici, zil_aktif=True):
            try:
                self.db.child(YOLLAR["durum"]).set({
                    "cevrimici":  cevrimici,
                    "pc_adi":     socket.gethostname(),
                    "zil_aktif":  zil_aktif,
                    "guncelleme": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                })
            except Exception:
                pass

        def durum_guncelle(self, zil_aktif):
            """Ana pencereden zil durumu değiştiğinde çağrılır."""
            try:
                self.db.child(YOLLAR["durum"]).update({"zil_aktif": zil_aktif})
            except Exception:
                pass

        def genel_ayar_guncelle(self, teneffus_aktif, muzik_sesi):
            """Ana pencereden genel ayar değiştiğinde Firebase'e yazar."""
            try:
                self.db.child(YOLLAR["genel_ayar"]).set({
                    "teneffus_aktif": teneffus_aktif,
                    "muzik_sesi": muzik_sesi,
                    "zaman": int(__import__("time").time() * 1000)
                })
            except Exception:
                pass

        def _sarki_listesi_yukle(self):
            """Müzik klasöründeki şarkıları Firebase'e yükler (telefon listeden seçer)."""
            if not self.muzik_klasoru or not os.path.isdir(self.muzik_klasoru):
                return
            try:
                sarkilar = sorted(
                    f for f in os.listdir(self.muzik_klasoru)
                    if f.lower().endswith(('.mp3', '.wav', '.ogg'))
                )
                self.db.child(YOLLAR["sarki_liste"]).set(sarkilar)
            except Exception as e:
                print(f"Şarkı listesi yükleme hatası: {e}")

        def _sifreIlkYukle(self):
            """
            ayarlar.json'daki şifreleri ilk kez Firebase'e hash'li olarak yazar.
            Firebase'de zaten hash varsa dokunmaz.
            """
            try:
                if not os.path.exists(AYARLAR_DOSYASI):
                    return
                with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as f:
                    ayarlar = json.load(f)

                # Her başlatmada şifreleri güncelle — şifre değişmiş olabilir
                guncelle = {}
                for tip in ("mobil_sifre", "yonetici_sifre", "uygulama_sifre"):
                    deger = ayarlar.get(tip, "")
                    if deger:
                        guncelle[tip + "_hash"] = sifre_hashle(deger)

                if guncelle:
                    self.db.child(YOLLAR["ayarlar"]).update(guncelle)
            except Exception as e:
                print(f"Şifre ilk yükleme hatası: {e}")

        def _genel_ayar_geldi(self, mesaj):
            """Mobilden gelen teneffüs müziği ve müzik sesi değişikliği."""
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_genel_ts:
                    return
                self._son_genel_ts = ts
                teneffus = bool(veri.get("teneffus_aktif", True))
                muzik_sesi = int(veri.get("muzik_sesi", 30))
                self.sinyal_genel_ayar.emit(teneffus, muzik_sesi)
                log_yaz("Firebase Kumanda",
                        f"Genel ayar güncellendi: Teneffüs={teneffus}, Müzik={muzik_sesi}", "İnternet")
            except Exception as e:
                print(f"Genel ayar işleme hatası: {e}")

        def _sistem_durum_geldi(self, mesaj):
            """Mobilden gelen sistem aç/kapat komutunu işler."""
            try:
                veri = mesaj.get("data")
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_sistem_ts:
                    return
                self._son_sistem_ts = ts
                aktif = veri.get("aktif")
                if aktif is not None:
                    self.sinyal_zil_ac_kapat.emit(bool(aktif))
                    durum_str = "Açıldı" if aktif else "Kapatıldı"
                    log_yaz("Firebase Kumanda", f"Sistem {durum_str}", "İnternet")
            except Exception as e:
                print(f"Sistem durum işleme hatası: {e}")

        def _zil_sec_geldi(self, mesaj):
            try:
                if mesaj is None:
                    return
                veri = mesaj.get("data") if isinstance(mesaj, dict) else None
                if not isinstance(veri, dict):
                    return
                ts = veri.get("zaman", 0)
                if ts <= self._son_zil_ts:
                    return
                self._son_zil_ts = ts
                tip    = veri.get("tip", "")
                melodi = veri.get("melodi", "")
                if tip and melodi:
                    self.sinyal_zil_sec.emit(tip, melodi)
                    log_yaz("Firebase Kumanda", f"Zil melodisi değiştirildi: {tip} -> {melodi}", "İnternet")
            except Exception as e:
                print(f"Zil seç işleme hatası: {e}")

        def _zil_listesi_yukle(self):
            """Zil melodisi klasöründeki dosyaları Firebase'e yükler."""
            try:
                from config import ZIL_KLASORU
                if not os.path.isdir(ZIL_KLASORU):
                    return
                melodiler = sorted(
                    f for f in os.listdir(ZIL_KLASORU)
                    if f.lower().endswith((".mp3", ".wav", ".ogg"))
                )
                self.db.child(YOLLAR["zil_listesi"]).set(melodiler)
            except Exception as e:
                print(f"Zil listesi yükleme hatası: {e}")

