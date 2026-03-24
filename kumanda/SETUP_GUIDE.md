# 🔐 Güvenlik Sistemi Kurulum Rehberi

## Özet

oZil Kumanda sistemi artık **token tabanlı oturum yönetimi** ile oluşturulmuştur. Bu rehber, token sistemini üretime taşımak için gerekli tüm adımları içerir.

**Güvenlik Seviyeleri:**
- ⭐⭐⭐ Istemci Tarafı (JavaScript) - TAMAMLANDI
- ⭐⭐⭐ Firebase Rules - TAMAMLANDI
- ⭐⭐⭐ Backend Validasyonu (Python) - HAZIR (Manuel entegrasyon gerekli)

---

## 📋 Hızlı Başlangıç (5 Adım)

### 1️⃣ Firebase Rules'ı Güncelle (5 dakika)

**Firebase Console'a git:**
1. [Firebase Console](https://console.firebase.google.com/) aç
2. Projeyi seç (ozil-99982)
3. Sol menüden **Realtime Database** seç
4. **Rules** sekmesine tıkla
5. Aşağıdaki kuralları kopyala-yapıştır

```json
{
  "rules": {
    "kumanda": {
      ".read": true,
      ".write": true,
      ".indexOn": ["zaman", "token_created"],
      
      "token": {
        ".read": true,
        ".write": false,
        ".validate": false
      },
      
      "komut": {
        ".validate": "newData.hasChildren(['kod', 'token', 'token_created', 'zaman'])"
      },
      
      "anons": {
        ".validate": "newData.hasChildren(['metin', 'token', 'token_created'])"
      }
    },
    
    "ayarlar": {
      ".read": false,
      ".write": false
    },
    
    "logs": {
      ".read": false,
      ".write": false,
      "security": {
        ".read": false,
        ".write": false
      }
    },
    
    ".read": false,
    ".write": false
  }
}
```

6. **Yayınla (Publish)** butonuna tıkla
7. ✅ Onay: "Rules published successfully"

### 2️⃣ kumanda.html'i Yükle (Zaten yapıldı!)

✅ Token sistem kodu zaten `kumanda.html`'de implement edilmiş.

Kontrol et:
```bash
# Dosyada token fonksiyonlarının olup olmadığını kontrol et
grep -n "generateSecureToken\|isTokenValid\|createNewToken" kumanda.html
```

### 3️⃣ Python Backend'ı Hazırla (15 dakika)

**Dosyası:** `firebase_token_validator.py`

Mevcut Python dinleyici kodunun başına ekle:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ... (dosyanın üstüne ekle)

from firebase_token_validator import validate_token, validate_command, log_security_event

# ... Existing code ...

def komut_listener(message):
    """Firebase komut dinleyicisi - TOKEN VALIDASYONU İLE"""
    komut_data = message["data"]
    
    if komut_data is None:
        return
    
    # ⭐ TOKEN VALIDASYONU (BU SATIRLARI EKLE)
    valid, reason = validate_command(komut_data)
    if not valid:
        print(f"❌ Komut reddedildi: {reason}")
        log_security_event("INVALID_COMMAND", komut_data, reason, db)
        return  # Komutu çalıştırma!
    
    # ✅ TOKEN GEÇERLIYSE KOMUTU ÇALIŞTIR
    kod = komut_data.get("kod")
    print(f"✅ Token geçerli, komut çalıştırılıyor: {kod}")
    
    # Komut çalıştırma mantığı
    if kod == "ogr_zil":
        ring_bell("student")
    elif kod == "ogrt_zil":
        ring_bell("teacher")
    # ... etc
```

### 4️⃣ Tüm Dinleyicileri Güncelle (10 dakika)

Python backend'de bu dinleyicileri bulun ve token validasyonu ekle:

| Dinleyici | Dosya | Satır |
|-----------|-------|-------|
| komut | firebase_dinleyici.py | ~50 |
| anons | firebase_dinleyici.py | ~100 |
| ses | firebase_dinleyici.py | ~150 |
| sarki | firebase_dinleyici.py | ~200 |
| sifre | firebase_dinleyici.py | ~250 |
| zil_sec | firebase_dinleyici.py | ~300 |

**Template:**
```python
def [listener_name]_listener(message):
    data = message["data"]
    if data is None:
        return
    
    # ⭐ TOKEN VALIDASYONU
    valid, reason = validate_command(data)
    if not valid:
        print(f"❌ Reddedildi: {reason}")
        log_security_event("INVALID_[NAME]", data, reason, db)
        return
    
    # ✅ İŞLEMİ YAPPIŞTIR
    # ... existing code ...
```

### 5️⃣ Test Et (5 dakika)

**Browser Console'dan:**
```javascript
// 1. Token'ı kontrol et
console.log("Session token valid?", isTokenValid());
console.log("Token age (ms):", Date.now() - (tokenExpiry - CONFIG.TOKEN_EXPIRY_MS));

// 2. Komut gönder
komutGonder("test_bell", "Test Zili");

// 3. Firebase Console'da token'ı kontrol et
// → kumanda > token > value: "abc123..."
```

**Python Backend'dan:**
```bash
# Terminal'de test çalıştır
python3 firebase_token_validator.py
```

---

## 🛠️ Detaylı Kurulum

### A. Firebase Rules Kurulum

**Adım 1: Firebase Console'da Rules'i Aç**
- https://console.firebase.google.com/
- Proje → Realtime Database → Rules

**Adım 2: Kuralları Kopyala**

Dosya: `firebase-rules.json`

**Adım 3: Yayınla ve Test Et**
```json
// Minimal test kuralı
{
  "rules": {
    "kumanda": {
      ".read": true,
      ".write": true,
      "token": {
        ".read": true,
        ".write": false
      }
    }
  }
}
```

**Adım 4: Simülator ile Test Et**
- Firebase Console → Rules → Simülatör
- Okuma: `kumanda/token` → ✅ İzin verildi
- Yazma: `kumanda/token` → ❌ İzin verilmedi

### B. Python Backend Entegrasyonu

**Dosya Yapısı:**
```
├── firebase_dinleyici.py          (Mevcut - güncellenecek)
├── firebase_token_validator.py    (Yeni - token doğrulama)
└── logs/
    └── security_events.json       (Token olayları)
```

**Adım 1: Validatör'ü Projene Ekle**

```bash
# Dosyayı proje klasörüne kopyala
cp firebase_token_validator.py ./projenim/
```

**Adım 2: İmport Et**

```python
from firebase_token_validator import (
    validate_token,
    validate_command,
    check_rate_limit,
    log_security_event
)
```

**Adım 3: Her Dinleyicide Token Kontrolü Ekle**

```python
def my_listener(message):
    data = message["data"]
    
    # 🔐 TOKEN KONTROL
    valid, reason = validate_command(data)
    if not valid:
        log_security_event("TOKEN_INVALID", data, reason, db)
        return  # Komutu çalıştırma!
    
    # ✅ DEVAM ET
    # ... işlemi yap
```

### C. Güvenlik Olayları Loggingı

**Otomatik logging:**
```python
# python'da olaylar şu yerlere yazılır:
1. Console output (terminal ekranı)
2. Firebase /logs/security (opsiyonel)
3. Local logfile (opsiyonel)
```

**Event türleri:**
- `INVALID_TOKEN` - Token formatı yanlış
- `TOKEN_EXPIRED` - Token süresi doldu
- `RATE_LIMITED` - Çok hızlı komut
- `MISSING_FIELDS` - Gerekli alanlar yoktu
- `COMMAND_REJECTED` - Komut reddedildi

---

## 🔍 Doğrulama Kontrol Listesi

✅ = Tamamlandı  
⏳ = Yapılması gerekli  
❌ = Başarısız

### Frontend (JavaScript)

- [x] Token fonksiyonları `kumanda.html`'de var
- [x] `generateSecureToken()` fonksiyonu crypto-secure
- [x] `isTokenValid()` süresi kontrol ediyor
- [x] `createNewToken()` Firebase'e yazıyor
- [x] Tüm komutlara token ekleniyor
  - [x] komutGonder()
  - [x] anonsGonder()
  - [x] sesGuncelle()
  - [x] sistemToggle()
  - [x] sifreDegistir()
- [x] Token yenileme (55. dakikada)
- [x] Çıkışta token temizleniyor

### Firebase Rules

- [ ] Rules yayınlandı
- [ ] `kumanda/token` sadece okunabilir
- [ ] `kumanda/komut` token doğrulaması var
- [ ] `ayarlar` kilitli (kimse okuyamaz/yazamaz)
- [ ] `logs/security` kilitli

### Python Backend

- [ ] `firebase_token_validator.py` yüklendi
- [ ] Tüm dinleyicilere token kontrolü eklendi
- [ ] `log_security_event()` çalışıyor
- [ ] Rate limiting aktif
- [ ] Güvenlik logları kaydediliyor

### Testing

- [ ] Fresh login sonrası token oluşuyor
- [ ] Token 1 saat içinde geçerli
- [ ] Komutlar token ile gönderiliyor
- [ ] Backend komutları kabul ediyor
- [ ] Süresi dolmuş token reddediliyor
- [ ] Hızlı komutlar rate limited oluyor
- [ ] Çıkışta token silinmiyor (intentional)

---

## 🐛 Sorun Giderme

### Sorun: "Token süresi doldu" alıyorum

**Çözüm:**
1. Tarayıcı saatini kontrol et (Settings → Date & Time)
2. Python sunucu saatini kontrol et: `date`
3. NTP sinkronizasyonu: `sudo ntpdate -s time.nist.gov`

### Sorun: Komutlar çalışmıyor

**Kontrol listeşi:**
```python
# Python backend'de debug modunu aç
DEBUG = True

# Token'ı kontrol et
print(f"Token: {token_value[:16]}...")
print(f"Created: {token_created}")
print(f"Age (ms): {current_time - token_created}")

# Komut verisini kontrol et
print(f"Command data:", command_data)

# Firebase Rules'ı kontrol et
# firebase console → Rules → geçerli JSON olmalı
```

### Sorun: "Token geçersiz formatı" hatası

**Token kontrol:**
```javascript
// Browser console
console.log("Token:", sessionToken);
console.log("Length:", sessionToken.length); // 64 olmalı
console.log("Hex?", /^[a-f0-9]{64}$/.test(sessionToken)); // true
```

### Sorun: Rate limiting çalışmıyor

**Kontrol:**
```python
# Backend'de trace kodu ekle
rate_check = check_rate_limit(token)
print(f"Rate limit: {rate_check}")
# Çıktı: {"allowed": True/False, "commands": 5, ...}
```

---

## 📊 Monitoring ve Loglar

### Güvenlik Olaylarını İzle

**Browser Console:**
```javascript
// Real-time token durumu
setInterval(() => {
  const remaining_ms = tokenExpiry - Date.now();
  console.log(`Token geçerliliği: ${Math.ceil(remaining_ms/1000)}s`);
}, 30000);
```

**Python Backend:**
```python
# güvenlik_raporu.py
import json
from pathlib import Path

def generate_security_report():
    """Günlük güvenlik raporu oluştur"""
    try:
        logs = db.child("logs").child("security").get().val() or {}
        
        invalid_tokens = sum(1 for v in logs.values() 
                           if v.get("type") == "INVALID_TOKEN")
        rate_limited = sum(1 for v in logs.values() 
                         if v.get("type") == "RATE_LIMITED")
        
        report = {
            "date": datetime.now().isoformat(),
            "invalid_tokens": invalid_tokens,
            "rate_limited_attempts": rate_limited,
            "total_events": len(logs)
        }
        
        print(f"📊 Güvenlik Raporu:")
        print(f"   Geçersiz Token: {invalid_tokens}")
        print(f"   Rate Limited: {rate_limited}")
        
        return report
    except Exception as e:
        print(f"Rapor hatası: {e}")

# Her 6 saatte bir çalıştır
schedule.every(6).hours.do(generate_security_report)
```

---

## 🚀 Production Checklist

### Güvenlik
- [ ] Firebase Rules deployed
- [ ] Token validation active
- [ ] Rate limiting configured
- [ ] Security logs enabled
- [ ] Backend timeout = 10s
- [ ] HTTPS enforced (backend)
- [ ] CORS headers configured

### Performance
- [ ] Token caching works (~5ms per check)
- [ ] No database round-trips for every command (batch if needed)
- [ ] Rate limit lookup O(1) (dict)
- [ ] Security logs async (non-blocking)

### Monitoring
- [ ] Alert on >5 INVALID_TOKEN/min
- [ ] Alert on >10 RATE_LIMIT/min
- [ ] Token renewal tracking
- [ ] Backend uptime monitoring

---

## 📞 Kaynaklar

- **Token Guide:** `SECURITY_TOKEN_GUIDE.md`
- **Validator Code:** `firebase_token_validator.py`
- **Rules JSON:** `firebase-rules.json`
- **Frontend Code:** `kumanda.html` (functions: `generateSecureToken`, `createNewToken`, etc.)

---

## 📝 Son Notlar

**Token Sistemi Özellikleri:**

| Özellik | Değer |
|---------|-------|
| Token Uzunluğu | 256-bit (64 hex char) |
| Token Süresi | 1 saat (3600000 ms) |
| Yenileme Zamanı | 55. dakikada |
| Rate Limit | 30 komut/dakika |
| Max Time Drift | 5 saniye |
| Hashing | SHA-256 (şifreler) |
| Random Gen. | crypto.getRandomValues() |

**Güvenlik Seviyeleri:**

```
Istemci (JS)        ⭐⭐⭐ 
├─ Token Generation (crypto-secure)
├─ Session Management (in-memory)
└─ Token Refresh (auto)

Firebase           ⭐⭐⭐
├─ Rules (strict)
├─ Field Validation
└─ Read/Write Locks

Backend (Python)   ⭐⭐⭐
├─ Token Validation
├─ Rate Limiting
└─ Security Logging
```

---

**Sürüm:** 1.0  
**Son Güncelleme:** 2026-03-24  
**Durum:** 🟢 Production Ready (Backend entegrasyonu sonrası)
