/**
 * config.js - Tüm sabitler ve Firebase yaplandırması
 */

// ================================================================
//  CONFIG - Uygulamalarının işleyişini belirleyen sabitler
// ================================================================
const CONFIG = {
  TOAST_DURATION: 3000,
  RATE_LIMIT_WINDOW: 60000,
  RATE_LIMIT_ATTEMPTS: 5,
  FIREBASE_TIMEOUT: 10000,
  SESSION_DEBOUNCE: 300,
  MIN_PASSWORD_LENGTH: 6,
  MAX_PASSWORD_LENGTH: 64,
  MAX_ANONS_BYTES: 1000,
  MAX_REPEAT: 10,
  SLIDER_DEBOUNCE: 300,
  TOKEN_EXPIRY_MS: 3600000, // 1 saat
  TOKEN_LENGTH: 32,  // 32 byte = 256 bit
  DEBUG: false  // Production: false, Development: true
};

// ================================================================
//  FIREBASE YAPILANDIRMASI - Firebase konsolunuzdan güncelleyin
// ================================================================
const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyAJSKfy8otqrah-efNzI0OoLlFETqMsJEM",
  authDomain:        "ozil-99982.firebaseapp.com",
  databaseURL:       "https://ozil-99982-default-rtdb.europe-west1.firebasedatabase.app",
  projectId:         "ozil-99982",
  storageBucket:     "ozil-99982.firebasestorage.app",
  messagingSenderId: "120039746207",
  appId:             "1:120039746207:web:bad5f22a77a4669d1890aa"
};

// ================================================================
//  DATABASE YOLLARI - Python kodu bu yolları dinler
// ================================================================
const DB_YOLU = {
  komut:       "kumanda/komut",
  anons:       "kumanda/anons",
  ses:         "kumanda/ses",
  sarki:       "kumanda/sarki",
  sarki_liste: "kumanda/sarki_liste",
  zil_listesi: "kumanda/zil_listesi",
  zil_sec:     "kumanda/zil_sec",
  durum:         "kumanda/durum",
  sistem_durum:  "kumanda/sistem_durum",
  genel_ayar:    "kumanda/genel_ayar",
  sifre:       "kumanda/sifre",
  ayarlar:     "kumanda/ayarlar"
};

// Firebase Database referansı (app.js'te başlatılır)
let db = null;
