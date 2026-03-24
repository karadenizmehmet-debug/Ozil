from .shared import *
from .env_config import FIREBASE_CONFIG, YOLLAR, sifre_hashle
from .listener_core import FirebaseListenerCoreMixin
from .event_handlers import FirebaseEventHandlersMixin
from .sync_ops import FirebaseSyncOpsMixin

class FirebaseDinleyici(QThread, FirebaseListenerCoreMixin, FirebaseEventHandlersMixin, FirebaseSyncOpsMixin):
    """Firebase dinleyici thread sınıfı."""
    sinyal_cal      = pyqtSignal(str)
    sinyal_anons    = pyqtSignal(str)
    sinyal_ses      = pyqtSignal(int)
    sinyal_sarki    = pyqtSignal(str)
    sinyal_sifre    = pyqtSignal(str, str)
    sinyal_zil_sec      = pyqtSignal(str, str)
    sinyal_zil_ac_kapat  = pyqtSignal(bool)
    sinyal_genel_ayar   = pyqtSignal(bool, int)
    sinyal_durum    = pyqtSignal(bool)
