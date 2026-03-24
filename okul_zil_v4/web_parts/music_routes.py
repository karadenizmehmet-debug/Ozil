from .shared import *

@flask_app.route("/mobil_sarki_listesi")
def mobil_sarki_listesi():
    if not _auth_kontrol("mobil"):
        return redirect("/")
    try:
        sarkilar = sorted(
            f for f in os.listdir(MUZIK_KLASORU)
            if f.lower().endswith(('.mp3', '.wav', '.ogg'))
        )
    except Exception:
        sarkilar = []
    return render_template_string(MOBIL_SARKI_SABLON, sarkilar=sarkilar,
                                  mevcut_ses=flask_app.mevcut_ses)

@flask_app.route("/mobil_ozel_cal/<path:sarki_adi>")
def mobil_ozel_cal(sarki_adi):
    if _auth_kontrol("mobil") and flask_thread_instance:
        flask_thread_instance.sinyal_sarki_oynat.emit(sarki_adi)
        log_yaz("Mobil", f"Özel Şarkı Başlattı: {sarki_adi}", get_client_info())
    return "OK"

@flask_app.route("/cal/<zil_kodu>")
def uzaktan_cal(zil_kodu):
    if _auth_kontrol("mobil") and flask_thread_instance:
        flask_thread_instance.sinyal_cal.emit(zil_kodu)
        log_yaz("Mobil", f"Zil Çaldırdı: {zil_kodu}", get_client_info())
    return "OK"

@flask_app.route("/sustur")
def uzaktan_sustur():
    if _auth_kontrol("mobil") and flask_thread_instance:
        flask_thread_instance.sinyal_sustur.emit()
        log_yaz("Mobil", "Sistemi Susturdu", get_client_info())
    return "OK"

@flask_app.route("/ses_ayarla/<int:seviye>")
def uzaktan_ses_ayarla(seviye):
    if _auth_kontrol("mobil"):
        flask_app.mevcut_ses = seviye
        if flask_thread_instance:
            flask_thread_instance.sinyal_ses_ayarla.emit(seviye)
    return "OK"

@flask_app.route("/anons_yap", methods=["POST"])
def uzaktan_anons_yap():
    if not _auth_kontrol("mobil"):
        return "HATA", 403
    metin = request.form.get("metin", "").strip()
    if metin and flask_thread_instance:
        flask_thread_instance.sinyal_anons_yap.emit(metin)
        log_yaz("Yönetici (Mobil)", f"Uzaktan Anons Gönderdi: {metin[:30]}...")
    return "OK"

