from .shared import *

@flask_app.route("/mobil_ayarlar")
def mobil_ayarlar():
    if not _auth_kontrol("yonetici"):
        return redirect("/sifre_yonetici_giris")
    return render_template_string(
        MOBIL_AYARLAR_SABLON,
        ten_aktif=getattr(flask_app, 'teneffus_aktif', True),
        muz_ses=getattr(flask_app, 'muzik_sesi', 30)
    )

@flask_app.route("/mobil_ayar_kaydet/<int:ten>/<int:ses>")
def mobil_ayar_kaydet(ten, ses):
    if _auth_kontrol("yonetici"):
        flask_app.teneffus_aktif = bool(ten)
        flask_app.muzik_sesi = ses
        if flask_thread_instance:
            flask_thread_instance.sinyal_genel_ayar.emit(bool(ten), ses)
    return "OK"

