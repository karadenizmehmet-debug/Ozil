from .shared import *

class MainWindowUiRuntimeMixin:
        def arayuzu_guncelle(self):
                g = GUNLER[QDate.currentDate().dayOfWeek() - 1]
                self.tablo_ozet.setRowCount(0)
                p = self.sistem_verisi.get(g, [])
                for r, v in enumerate(p):
                    if not isinstance(v, dict):
                        continue
                    self.tablo_ozet.insertRow(r)
                    i = QTableWidgetItem(v.get("ders", ""))
                    i.setFont(QFont("Arial", 11, QFont.Bold))
                    self.tablo_ozet.setItem(r, 0, i)
                    self.tablo_ozet.setItem(
                        r, 1, QTableWidgetItem(v.get("toplanma", "")))
                    self.tablo_ozet.setItem(
                        r, 2, QTableWidgetItem(v.get("ogrenci", "")))
                    self.tablo_ozet.setItem(
                        r, 3, QTableWidgetItem(v.get("ogretmen", "")))
                    self.tablo_ozet.setItem(r, 4, QTableWidgetItem(v.get("cikis", "")))
                    for c in range(5):
                        if self.tablo_ozet.item(r, c):
                            self.tablo_ozet.item(r, c).setTextAlignment(Qt.AlignCenter)

        def zaman_cizelgesini_guncelle(self, su_an, gun_adi):
                prg = self.sistem_verisi.get(gun_adi, [])
                if not prg:
                    self.lbl_suan_ne.setText("Bugün Ders Yok")
                    self.lbl_geri_sayim.setText("--:--")
                    return

                durum = "Ders Dışı (Mesai Bitti)"
                kalan_saniye = 0

                def str_to_dt(saat_str):
                    if not saat_str or saat_str == "--:--":
                        return None
                    try:
                        t = datetime.datetime.strptime(saat_str, "%H:%M").time()
                        return datetime.datetime.combine(su_an.date(), t)
                    except:
                        return None

                for i, v in enumerate(prg):
                    if not isinstance(v, dict):
                        continue

                    d_adi = v.get("ders", f"{i+1}. Ders")
                    dt_topl = str_to_dt(v.get("toplanma", ""))
                    dt_ogr = str_to_dt(v.get("ogrenci", ""))
                    dt_ogrt = str_to_dt(v.get("ogretmen", ""))
                    dt_cikis = str_to_dt(v.get("cikis", ""))

                    dt_baslangic = dt_topl or dt_ogr or dt_ogrt
                    if not dt_baslangic or not dt_cikis:
                        continue

                    # 1. Mesai başlamamışsa (İlk dersten önceyiz)
                    if i == 0 and su_an < dt_baslangic:
                        durum = "Mesai Başlamadı"
                        kalan_saniye = int((dt_baslangic - su_an).total_seconds())
                        break

                    # 2. Şu an dersteysek veya toplanma/öğretmen zili arasındaysak
                    if dt_baslangic <= su_an < dt_cikis:
                        if dt_ogrt and su_an < dt_ogrt:
                            durum = f"{d_adi} (Zil Çaldı, Derse Geçiliyor)"
                            kalan_saniye = int((dt_ogrt - su_an).total_seconds())
                        else:
                            durum = f"{d_adi} İşleniyor"
                            kalan_saniye = int((dt_cikis - su_an).total_seconds())
                        break

                    # 3. Dersten çıkılmış ama bir sonraki derse girmemişsek (Teneffüs / Öğle Arası)
                    dt_sonraki_bas = None
                    if i + 1 < len(prg):
                        sonraki = prg[i+1]
                        dt_sonraki_bas = str_to_dt(sonraki.get("toplanma", "")) or str_to_dt(
                            sonraki.get("ogrenci", "")) or str_to_dt(sonraki.get("ogretmen", ""))

                    if dt_sonraki_bas and dt_cikis <= su_an < dt_sonraki_bas:
                        fark_dk = (dt_sonraki_bas - dt_cikis).total_seconds() / 60
                        tip = "Öğle Arası" if fark_dk > 30 else "Teneffüs"
                        durum = f"{i+1}. {tip}"
                        kalan_saniye = int((dt_sonraki_bas - su_an).total_seconds())
                        break

                # Arayüze yazdır
                self.lbl_suan_ne.setText(durum)
                if durum == "Ders Dışı (Mesai Bitti)":
                    self.lbl_geri_sayim.setText("--:--")
                elif kalan_saniye > 0:
                    dk, sn = divmod(kalan_saniye, 60)
                    saat, dk = divmod(dk, 60)
                    if saat > 0:
                        self.lbl_geri_sayim.setText(f"{saat:02d}:{dk:02d}:{sn:02d}")
                    else:
                        self.lbl_geri_sayim.setText(f"{dk:02d}:{sn:02d}")
                else:
                    self.lbl_geri_sayim.setText("--:--")

        def sistem_kontrol(self):
                sa = datetime.datetime.now()
                sk = sa.strftime("%H:%M")  # "08:30" formatında
                hg = GUNLER[sa.weekday()]

                self.lbl_saat.setText(sa.strftime("%H:%M:%S"))
                # Tarih etiketi sadece dakikada bir güncellenir
                if sa.second == 0 or not hasattr(self, "_son_tarih_guncelleme") or self._son_tarih_guncelleme != sk:
                    self._son_tarih_guncelleme = sk
                    self.lbl_tarih.setText(f"{sa.day} {AYLAR[sa.month - 1]} {sa.year} {hg}")

                self.zaman_cizelgesini_guncelle(sa, hg)

                if not self.zil_aktif:
                    return

                # --- BİLGİSAYARI OTOMATİK KAPATMA ---
                if self.sistem_verisi.get("pc_kapat_aktif", False) and sk == self.sistem_verisi.get("pc_kapat_saat", ""):
                    if 0 <= sa.second <= 10:
                        # O dakikanın içinde sadece 1 kez tetiklemesi için güvenlik önlemi
                        if self.son_calinan_dakika != sk + "_kapat":
                            self.son_calinan_dakika = sk + "_kapat"
                            log_yaz(
                                "Sistem", f"Otomatik PC Kapatma tetiklendi. Saat: {sk}", "Yerel PC")
                            # Windows'u 60 saniyelik geri sayımla kapat
                            os.system("shutdown /s /t 60")
                # ------------------------------------

                # Müzik devam kontrolü
                if (self.teneffus_yayini_aktif or self.manuel_muzik_modu) and not pygame.mixer.music.get_busy() and not self.ses_duraklatildi_mi:
                    self.siradaki_muzigi_cal()

                # --- TAKILMA KORUMALI ZİL KONTROLÜ (10 Saniyelik Tolerans) ---
                if self.manuel_muzik_modu:
                    return

                # Bu dakikada zaten zil çalındıysa çık (Çift çalmayı engeller)
                if self.son_calinan_dakika == sk:
                    return

                # Dakikanın ilk 10 saniyesi içinde herhangi bir saniyede yakalarsa çalar
                if 0 <= sa.second <= 10:
                    prg = self.sistem_verisi.get(hg, [])
                    for v in prg:
                        if not isinstance(v, dict):
                            continue

                        # Zil vakitlerini kontrol et
                        zs = {
                            "toplanma_zil": (v.get("toplanma", ""), "topl"),
                            "ogr_zil": (v.get("ogrenci", ""), "ogr"),
                            "ogrt_zil": (v.get("ogretmen", ""), "ogrt"),
                            "cikis_zil": (v.get("cikis", ""), "cikis")
                        }

                        for zk, (z_saat, d_suffix) in zs.items():
                            if z_saat and z_saat != "--:--" and z_saat == sk:
                                # KRİTİK: Bu dakikayı her halükarda "işlendi" olarak işaretle ki tekrara düşmesin
                                self.son_calinan_dakika = sk

                                # --- YENİ: ANONS ÇALIYORSA ZİLİ İPTAL ET ---
                                if self.calan_ses_anahtari == "anons" and pygame.mixer.music.get_busy():
                                    log_yaz(
                                        "Sistem", f"Zil İptal Edildi (Anons Devam Ediyor): {zk} ({sk})", "Cihaz")
                                    return
                                # ------------------------------------------

                                if zk in ["toplanma_zil", "ogr_zil", "ogrt_zil"]:
                                    self.teneffus_yayini_aktif = False

                                d_no = v.get("ders", "1").split(".")[0]
                                oz = self.sistem_verisi.get("ozel_sesler", {}).get(
                                    hg, {}).get(f"{d_no}_{d_suffix}", {})

                                self.sesi_cal(zk, False, oz.get("dosya", "Varsayılan"))

                                log_yaz(
                                    "Sistem", f"Otomatik Zil: {zk} ({sk})", "Cihaz")

                                if zk == "cikis_zil" and self.sistem_verisi.get("teneffus_muzigi_aktif", True):
                                    self.teneffus_muziklerini_hazirla()
                                return

        def ses_hatasi_goster(self):
                """Ses aygıtı bulunamazsa ekrana kritik uyarı verir."""
                QMessageBox.critical(self, "🚨 Kritik Ses Hatası",
                                     "Bilgisayara bağlı bir hoparlör veya ses aygıtı bulunamadı!\n\n"
                                     "Lütfen ses bağlantılarını kontrol edin ve programı yeniden başlatın.\n"
                                     "Güvenlik amacıyla zil sistemi şu an devre dışı bırakıldı.")
                log_yaz("Sistem", "Ses aygıtı bulunamadı, sistem durduruldu.", "Yerel PC")

