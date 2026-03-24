from .shared import *

class MainWindowConfigIOMixin:
        def verileri_yukle(self):
                if os.path.exists(AYARLAR_DOSYASI):
                    try:
                        with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as f:
                            v = json.load(f)
                            self.sistem_verisi.update(v)
                        # Sabit yolları (F:\... gibi) BASE_DIR'e göre normalize et
                        self._ses_yollarini_normalize_et()
                    except Exception as e:
                        print(f"Ayar yükleme hatası: {e}")

        def _ses_yollarini_normalize_et(self):
                """ayarlar.json'daki sabit yolları BASE_DIR'e göre düzeltir.
                Klasör farklı bir diske/dizine taşınsa bile ses dosyaları bulunur.
                """
                sesler = self.sistem_verisi.get("sesler", {})
                degisti = False
                for k, v in sesler.items():
                    yeni = yolu_normalize_et(v)
                    if yeni != v:
                        sesler[k] = yeni
                        degisti = True
                        print(f"[Yol] {k}: {v} → {yeni}")
                if degisti:
                    self.sistem_verisi["sesler"] = sesler

                # Müzik klasörü
                muz = self.sistem_verisi.get("muzik_klasoru", "")
                if muz and not os.path.exists(muz):
                    # BASE_DIR altında sesler/muzikyayini ara
                    from config import MUZIK_KLASORU
                    if os.path.exists(MUZIK_KLASORU):
                        self.sistem_verisi["muzik_klasoru"] = MUZIK_KLASORU
                        print(f"[Yol] muzik_klasoru → {MUZIK_KLASORU}")

        def ayarlari_guvenli_kaydet(self):
                """Ayarları JSON dosyasına güvenli (Atomic) şekilde yazar."""
                try:
                    # Önce geçici dosyaya yazıyoruz
                    with open(AYARLAR_TEMP, "w", encoding="utf-8") as f:
                        json.dump(self.sistem_verisi, f, ensure_ascii=False, indent=4)

                    # Yazma hatasız bittiyse, geçici dosyanın adını asıl dosya ile değiştir
                    os.replace(AYARLAR_TEMP, AYARLAR_DOSYASI)
                except Exception as e:
                    log_yaz(
                        "Sistem", f"Kritik Hata: Ayarlar kaydedilemedi! Hata: {e}", "Yerel PC")
