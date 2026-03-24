import pyrebase
from okul_zil_v4.common.env_loader import get_env_value

FIREBASE_CONFIG = {
    "apiKey": get_env_value("FIREBASE_API_KEY"),
    "authDomain": get_env_value("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": get_env_value("FIREBASE_DATABASE_URL"),
    "projectId": get_env_value("FIREBASE_PROJECT_ID"),
    "storageBucket": get_env_value("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": get_env_value("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": get_env_value("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()
