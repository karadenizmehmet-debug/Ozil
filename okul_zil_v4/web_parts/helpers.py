from .shared import *

def csrf_token_olustur():
    """Oturumda yoksa yeni CSRF token üretir, varsa döndürür."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(24)
    return session['csrf_token']

def csrf_dogrula():
    """POST isteklerinde form veya header üzerinden CSRF token'ı doğrular."""
    token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
    return token and token == session.get('csrf_token')

def get_client_info():
    ip = request.remote_addr
    ua = request.user_agent.platform or "Mobil/Tablet"
    return f"{ua} ({ip})"

def _auth_kontrol(seviye="mobil"):
    """
    seviye='mobil'    -> normal kullanıcı girişi
    seviye='yonetici' -> yönetici girişi
    """
    if seviye == "yonetici":
        return session.get("yonetici_giris") is True
    return session.get("mobil_giris") is True

