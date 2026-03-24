from .shared import *

@flask_app.route("/")
def index():
    if not _auth_kontrol("mobil"):
        return render_template_string(LOGIN_SABLON, hata=False, pc_adi=platform.node(),
                                      csrf_token=csrf_token_olustur())
    return render_template_string(HTML_SABLON, pc_adi=platform.node(),
                                  mevcut_ses=flask_app.mevcut_ses)

@flask_app.route("/login", methods=["POST"])
def login():
    # CSRF kontrolü
    if not csrf_dogrula():
        return render_template_string(LOGIN_SABLON, hata=True,
                                      pc_adi=platform.node(),
                                      csrf_token=csrf_token_olustur())
    girilen = request.form.get("sifre", "")
    info = get_client_info()
    if girilen == getattr(flask_app, 'mobil_sifre', '1234'):
        log_yaz("Mobil Kullanıcı", "Başarılı Giriş", info)
        session["mobil_giris"] = True
        session.permanent = True
        return redirect("/")
    log_yaz("Mobil Kullanıcı", "Hatalı Giriş Denemesi", info)
    return render_template_string(LOGIN_SABLON, hata=True, pc_adi=platform.node(),
                                  csrf_token=csrf_token_olustur())

@flask_app.route("/sifre_yonetici_giris", methods=["GET", "POST"])
def sifre_yonetici_giris():
    if not _auth_kontrol("mobil"):
        return redirect("/")

    if request.method == "POST":
        if not csrf_dogrula():
            return render_template_string(SIFRE_GIRIS_SABLON, hata=True,
                                          csrf_token=csrf_token_olustur())
        girilen = request.form.get("sifre", "")
        info = get_client_info()
        if girilen == getattr(flask_app, 'yonetici_sifre', '1234'):
            log_yaz("Yönetici (Mobil)", "Şifre Paneline Girdi", info)
            session["yonetici_giris"] = True
            return redirect("/sifre_paneli")
        log_yaz("Yönetici (Mobil)", "Hatalı Şifre Denemesi", info)
        return render_template_string(SIFRE_GIRIS_SABLON, hata=True,
                                      csrf_token=csrf_token_olustur())
    return render_template_string(SIFRE_GIRIS_SABLON, hata=False,
                                  csrf_token=csrf_token_olustur())

@flask_app.route("/sifre_paneli", methods=["GET", "POST"])
def sifre_paneli():
    if not _auth_kontrol("yonetici"):
        return redirect("/sifre_yonetici_giris")

    msg = ""
    if request.method == "POST":
        if not csrf_dogrula():
            msg = "Hata: Güvenlik doğrulaması başarısız!"
        else:
            tip = request.form.get("tip", "")
            y1 = request.form.get("yeni1", "")
            y2 = request.form.get("yeni2", "")

            if y1 != y2:
                msg = "Hata: Yeni şifreler uyuşmuyor!"
            elif len(y1) < 4:
                msg = "Hata: Şifre en az 4 karakter olmalı!"
            else:
                if flask_thread_instance:
                    flask_thread_instance.sinyal_sifre_degistir.emit(tip, y1)
                    log_yaz("Yönetici (Mobil)", f"{tip} şifresini değiştirdi",
                            get_client_info())
                    msg = "Başarılı: Şifre güncellendi."

    return render_template_string(SIFRE_SABLON, msg=msg, csrf_token=csrf_token_olustur())

@flask_app.route("/cikis")
def cikis():
    session.clear()
    return redirect("/")

