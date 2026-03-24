from .shared import *

class MainWindowFirebaseMixin:
    def _firebase_komut(self, kod):
            """Firebase'den (internet üzerinden) gelen zil/komut kodunu işler."""
            if kod == "sustur":
                self.sesi_kapat()
            elif kod == "muzik_toggle":
                self.manuel_muzik_yayini_toggle()
            else:
                self.sesi_cal(kod, manuel_basildi=True)

    def _sifreleri_firebase_guncelle(self):
            """Şifreleri Firebase'e arka planda yazar — UI bloklamaz."""
            import hashlib
            verisi = dict(self.sistem_verisi)  # snapshot al
            db_ref = getattr(self.fb_dinleyici, "db", None) if hasattr(self, "fb_dinleyici") else None
            if not db_ref:
                return
            def _yukle():
                try:
                    def h(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
                    guncelle = {}
                    for tip in ("mobil_sifre", "yonetici_sifre", "uygulama_sifre"):
                        deger = verisi.get(tip, "")
                        if deger:
                            guncelle[tip + "_hash"] = h(deger)
                    if guncelle:
                        db_ref.child("kumanda/ayarlar").update(guncelle)
                except Exception as e:
                    print(f"Firebase şifre güncelleme hatası: {e}")
            threading.Thread(target=_yukle, daemon=True).start()

    def _firebase_sistem_durum(self, aktif):
            """Firebase'den gelen sistem aç/kapat komutunu işler."""
            if aktif != self.zil_aktif:
                self.zil_durumu_degistir()  # toggle yapar
            # Firebase'e güncel durumu bildir
            if hasattr(self, "fb_dinleyici"):
                self.fb_dinleyici.durum_guncelle(self.zil_aktif)

    def _firebase_zil_degistir(self, zil_tip, melodi_adi):
            """Firebase'den gelen zil melodisi değiştirme komutunu işler."""
            try:
                if "sesler" not in self.sistem_verisi:
                    self.sistem_verisi["sesler"] = {}
                if melodi_adi == "Varsayılan":
                    self.sistem_verisi["sesler"].pop(zil_tip, None)
                else:
                    from config import ZIL_KLASORU
                    tam_yol = os.path.join(ZIL_KLASORU, melodi_adi)
                    self.sistem_verisi["sesler"][zil_tip] = tam_yol
                self.ayarlari_guvenli_kaydet()
                log_yaz("Firebase Kumanda",
                        f"Zil melodisi değiştirildi: {zil_tip} -> {melodi_adi}", "İnternet")
            except Exception as e:
                print(f"Zil değiştirme hatası: {e}")

    def zil_melodisi_firebase_yaz(self, zil_tip, melodi_yolu):
            """Ana programdan zil melodisi değişince Firebase'e yazar."""
            try:
                from config import ZIL_KLASORU
                melodi_adi = os.path.basename(melodi_yolu) if melodi_yolu and melodi_yolu != "Varsayılan" else "Varsayılan"
                def _yaz():
                    try:
                        if hasattr(self, "fb_dinleyici") and self.fb_dinleyici.db:
                            self.fb_dinleyici.db.child("kumanda/zil_sec").set({
                                "tip": zil_tip,
                                "melodi": melodi_adi,
                                "zaman": int(__import__("time").time() * 1000),
                                "kaynak": "ana_program"
                            })
                    except Exception as e:
                        print(f"Zil Firebase yazma hatası: {e}")
                threading.Thread(target=_yaz, daemon=True).start()
            except Exception as e:
                print(f"Zil yol hatası: {e}")

    def _firebase_sifre_degistir(self, tip, yeni_hash):
            """Firebase'den (mobil) gelen şifre değişikliği — hash olarak gelir."""
            try:
                # Hash'i kaydet. Flask web arayüzü de hash ile karşılaştıracak şekilde güncellenir.
                self.sistem_verisi[f"{tip}_sifre_hash"] = yeni_hash
                # Flask'ı da hash ile güncelle (web_server.py karşılaştırma için)
                if tip == "mobil":
                    flask_app.mobil_sifre = yeni_hash  # geçici — hash artık şifre
                elif tip == "yonetici":
                    flask_app.yonetici_sifre = yeni_hash
                elif tip == "uygulama":
                    flask_app.uygulama_sifre = yeni_hash
                self.ayarlari_guvenli_kaydet()
                log_yaz("Firebase Kumanda", f"{tip} şifresi güncellendi (mobil)", "İnternet")
            except Exception as e:
                print(f"Firebase şifre güncelleme hatası: {e}")
