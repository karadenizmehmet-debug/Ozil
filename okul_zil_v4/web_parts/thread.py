from .shared import *

class WebSunucuThread(QThread):
    sinyal_cal = pyqtSignal(str)
    sinyal_sustur = pyqtSignal()
    sinyal_ses_ayarla = pyqtSignal(int)
    sinyal_sifre_degistir = pyqtSignal(str, str)
    sinyal_sarki_oynat = pyqtSignal(str)
    sinyal_genel_ayar = pyqtSignal(bool, int)
    sinyal_anons_yap = pyqtSignal(str)

    def run(self):
        global flask_thread_instance
        flask_thread_instance = self

        import logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

        # Zeroconf / mDNS kaydı
        try:
            from zeroconf import Zeroconf, ServiceInfo
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except Exception:
                IP = '127.0.0.1'
            finally:
                s.close()
            hostname = socket.gethostname()
            info = ServiceInfo(
                "_http._tcp.local.",
                f"ZilSistemi_{hostname}._http._tcp.local.",
                addresses=[socket.inet_aton(IP)],
                port=5000,
                properties={'desc': 'Zil Sistemi'},
                server=f"{hostname}.local."
            )
            self.zc = Zeroconf()
            self.zc.register_service(info)
        except Exception:
            pass

        # Flask'ı başlatıyoruz
        flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
