from .shared import *
from okul_zil_v4.common.env_loader import get_env_value
from okul_zil_v4.common.security import sifre_hashle

FIREBASE_CONFIG = {
    "apiKey": get_env_value("FIREBASE_API_KEY"),
    "authDomain": get_env_value("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": get_env_value("FIREBASE_DATABASE_URL"),
    "projectId": get_env_value("FIREBASE_PROJECT_ID"),
    "storageBucket": get_env_value("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": get_env_value("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": get_env_value("FIREBASE_APP_ID"),
}

# Firebase'deki yollar (kumanda.html ile aynı olmalı)
YOLLAR = {
    "komut": "kumanda/komut",
    "anons": "kumanda/anons",
    "ses": "kumanda/ses",
    "sarki": "kumanda/sarki",
    "sarki_liste": "kumanda/sarki_liste",
    "zil_listesi": "kumanda/zil_listesi",
    "zil_sec": "kumanda/zil_sec",
    "durum": "kumanda/durum",
    "sistem_durum": "kumanda/sistem_durum",
    "sifre": "kumanda/sifre",
    "ayarlar": "kumanda/ayarlar",
    "genel_ayar": "kumanda/genel_ayar",
}
