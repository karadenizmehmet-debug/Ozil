from .shared import *

class MainWindowUiWeatherRuntimeMixin:
        def hava_durumu_guncelle(self):
                """Open-Meteo API ile ücretsiz, kayıtsız hava durumu çeker."""
                sehir = self.sistem_verisi.get("hava_sehir", "Konya")
                threading.Thread(target=self._hava_cek, args=(sehir,), daemon=True).start()

        def _hava_cek(self, sehir):
                import urllib.request
                import urllib.parse
                import json as _json
                from functools import partial as _partial

                def _ui(fn, *args):
                    QTimer.singleShot(0, _partial(fn, *args))

                try:
                    geo_url = ("https://nominatim.openstreetmap.org/search"
                               f"?q={urllib.parse.quote(sehir)}&format=json&limit=1")
                    req = urllib.request.Request(
                        geo_url, headers={"User-Agent": "OkulZilSistemi/1.0"})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        geo = _json.loads(r.read())
                except Exception as e:
                    print(f"Hava geocoding hatası: {e}")
                    _ui(self.lbl_hava_acik.setText, "Bağlantı yok")
                    return

                if not geo:
                    _ui(self.lbl_hava_acik.setText, "Şehir bulunamadı")
                    return

                lat = geo[0]["lat"]
                lon = geo[0]["lon"]
                goster_sehir = geo[0].get("display_name", sehir).split(",")[0]

                try:
                    wx_url = (f"https://api.open-meteo.com/v1/forecast"
                              f"?latitude={lat}&longitude={lon}"
                              f"&current=temperature_2m,weathercode,windspeed_10m"
                              f"&timezone=Europe%2FIstanbul")
                    with urllib.request.urlopen(wx_url, timeout=10) as r:
                        wx = _json.loads(r.read())
                except Exception as e:
                    print(f"Hava API hatası: {e}")
                    _ui(self.lbl_hava_acik.setText, "Hava verisi alınamadı")
                    return

                cur = wx["current"]
                sicaklik = round(cur["temperature_2m"])
                kod = cur["weathercode"]

                HAVA_MAP = {
                    0: ("☀️", "Açık"), 1: ("🌤️", "Az Bulutlu"), 2: ("⛅", "Parçalı Bulutlu"),
                    3: ("☁️", "Bulutlu"), 45: ("🌫️", "Sisli"), 48: ("🌫️", "Dondurucu Sis"),
                    51: ("🌦️", "Hafif Çisenti"), 53: ("🌦️", "Çisenti"), 55: ("🌧️", "Yoğun Çisenti"),
                    61: ("🌧️", "Hafif Yağmur"), 63: ("🌧️", "Yağmur"), 65: ("🌧️", "Şiddetli Yağmur"),
                    71: ("🌨️", "Hafif Kar"), 73: ("❄️", "Kar"), 75: ("❄️", "Yoğun Kar"),
                    80: ("🌦️", "Sağanak"), 81: ("🌧️", "Kuvvetli Sağanak"), 82: ("⛈️", "Şiddetli Sağanak"),
                    95: ("⛈️", "Gök Gürültülü Fırtına"), 96: ("⛈️", "Dolu"), 99: ("⛈️", "Şiddetli Fırtına"),
                }
                ikon, aciklama = HAVA_MAP.get(kod, ("🌡️", f"Kod:{kod}"))

                def _guncelle():
                    self.lbl_hava_ikon.setText(ikon)
                    self.lbl_hava_sicak.setText(f"{sicaklik}°C")
                    self.lbl_hava_acik.setText(aciklama)
                    self.lbl_hava_sehir.setText(goster_sehir)
                QTimer.singleShot(0, _guncelle)

