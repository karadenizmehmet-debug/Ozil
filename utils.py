# utils.py
import sys
import os
import json
import traceback
import datetime
import platform
import subprocess
from PyQt5.QtWidgets import QApplication

# config.py dosyasındaki sabiti içeri aktarıyoruz
from config import LOG_DOSYASI


def hata_yakalayici(ex_cls, ex, tb):
    print('{}: {}\n'.format(ex_cls.__name__, ex) + ''.join(traceback.format_tb(tb)))
    sys.exit(1)


from okul_zil_v4.common.security import sifre_hashle

def log_yaz(kullanici, islem, cihaz_bilgisi="Bilinmiyor"):
    try:
        mevcut_loglar = []
        # Dosya varsa ve içeriği boş değilse yükle
        if os.path.exists(LOG_DOSYASI) and os.path.getsize(LOG_DOSYASI) > 0:
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                try:
                    mevcut_loglar = json.load(f)
                except json.JSONDecodeError:
                    # Dosya bozuksa (örn: elektrik kesintisi yarım bıraktıysa) temiz liste oluştur
                    mevcut_loglar = []

        yeni_kayit = {
            "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "kullanici": kullanici,
            "islem": islem,
            "cihaz": cihaz_bilgisi
        }

        # Yeni kaydı listenin başına ekle (en yeni en üstte)
        mevcut_loglar.insert(0, yeni_kayit)

        # Sadece son 500 logu tutacak şekilde güvenli kaydet
        with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(mevcut_loglar[:500], f, ensure_ascii=False, indent=4)

    except Exception as e:
        # Hata varsa konsola yaz ama programı çökertme
        print(f"Log Yazma Hatası: {str(e)}")


def pencere_ortala(pencere):
    try:
        qr = pencere.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        pencere.move(qr.topLeft())
    except Exception:
        pass


def get_wifi_name():
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(
                'netsh wlan show interfaces',
                stderr=subprocess.DEVNULL
            ).decode('cp857', errors='replace')
            for line in out.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(':')[1].strip()
    except Exception:
        pass
    return "Bilinmiyor"


def oto_baslat_ayarla(durum):
    """Windows kayıt defteri aracılığıyla otomatik başlatmayı açar/kapatır."""
    if platform.system() != "Windows":
        print("Otomatik başlatma yalnızca Windows'ta desteklenmektedir.")
        return

    # winreg yalnızca Windows'ta içe aktarılır
    import winreg  # noqa: PLC0415

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "NimetullahNahcivaniZilSistemi"
    try:
        exe_path = (
            f'"{sys.executable}"'
            if getattr(sys, 'frozen', False)
            else f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
        )
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if durum:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Otomatik Başlatma Hatası: {e}")
