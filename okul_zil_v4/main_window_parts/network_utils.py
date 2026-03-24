from .shared import *

class MainWindowNetworkUtilsMixin:
        def yerel_ip_ogren(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    s.connect(('10.255.255.255', 1))
                    ip = s.getsockname()[0]
                except:
                    ip = '127.0.0.1'
                finally:
                    s.close()
                return ip

        def qrcode_olustur(self, url):
                try:
                    import qrcode
                    from io import BytesIO
                    qr = qrcode.QRCode(version=1, box_size=4, border=1)
                    qr.add_data(url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    qp = QPixmap()
                    qp.loadFromData(buf.getvalue())
                    return qp
                except:
                    return None
