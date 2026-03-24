# 🔐 Güvenlik Tokeni Sistemi ve Backend Validasyonu

## Genel Bakış

Kumanda uygulaması artık **token tabanlı oturum yönetimi** kullanıyor. Her başarılı giriş sonrasında:

1. **Token üretilir**: Crypto-secure 256-bit rastgele token
2. **Firebase'e yazılır**: `kumanda/token` yapısında 1 saat geçerlilik ile
3. **Tüm komutlara eklenir**: Komut, anons, ses, şifre değişip vb.
4. **Python backend tarafından doğrulanır**: Token geçerliyse komut çalışır
5. **1 saatte yenilenir**: Son 5 dakikada otomatik yenileme

---

## 🔑 Token Yapısı (Firebase'de)

```json
{
  "kumanda": {
    "token": {
      "value": "a1b2c3d4e5f6...(64 hex char)",
      "created": 1703001234567,
      "expires": 1703004834567,
      "user_agent": "Mozilla/5.0..."
    }
  }
}
```

---

## Komut Yapısı (Token ile)

Tüm komutlar artık bu formatta gönderiliyor:

```json
{
  "kod": "ogr_zil",
  "zaman": 1703001234567,
  "token": "a1b2c3d4e5f6...",
  "token_created": 1703001234567
}
```

---

## 🐍 Python Backend Validasyonu

### 1. Token Doğrulama Fonksiyonu

Firebase Realtime Database'de dinlediğiniz komutları doğrulamadan ÖNCE bu kontrolü yapın:

```python
import firebase_admin
from firebase_admin import db
from datetime import datetime, timedelta
import time

TOKEN_EXPIRY_MS = 3600000  # 1 saat (milisaniye)

def validate_token(token_value, token_created_ms):
    """
    Token'ı doğrula
    
    Args:
        token_value: Token string'i (kumanda/token/value)
        token_created_ms: Token oluşturulma zamanı (milisaniye)
    
    Returns:
        dict: {"valid": True/False, "error": "..."}
    """
    if not token_value:
        return {"valid": False, "error": "Token bulunamadı"}
    
    if not isinstance(token_value, str) or len(token_value) != 64:
        return {"valid": False, "error": "Token formatı geçersiz"}
    
    current_ms = int(time.time() * 1000)
    token_age_ms = current_ms - token_created_ms
    
    if token_age_ms > TOKEN_EXPIRY_MS:
        return {"valid": False, "error": f"Token süresi doldu ({token_age_ms}ms)"}
    
    if token_age_ms < 0:
        return {"valid": False, "error": "Token zamanı gelecekte (saat senkronizasyonu hatası)"}
    
    return {"valid": True}


def execute_command(command_data):
    """
    Gelen komutu token valide ettikten sonra çalıştır
    
    Args:
        command_data: Firebase'den gelen komut nesnesi
    
    Returns:
        dict: {"success": True/False, "reason": "..."}
    """
    # 1. Token'ı komuttan çıkar
    token = command_data.get("token")
    token_created = command_data.get("token_created")
    
    # 2. Token'ı doğrula
    validation = validate_token(token, token_created)
    if not validation["valid"]:
        print(f"❌ Komut reddedildi: {validation['error']}")
        log_security_event("INVALID_TOKEN", command_data, validation["error"])
        return {"success": False, "reason": validation["error"]}
    
    # 3. Firebase'deki aktif token'ı cross-check et (opsiyonel, ekstra güvenlik)
    try:
        firebase_token_data = db.child("kumanda").child("token").get()
        if firebase_token_data.val():
            firebase_token = firebase_token_data.val().get("value")
            if firebase_token != token:
                print("❌ Komut reddedildi: Token uyuşmuyor")
                log_security_event("TOKEN_MISMATCH", command_data, "Firebase token uyuşmadı")
                return {"success": False, "reason": "Token uyuşmuyor"}
    except Exception as e:
        print(f"⚠️ Token cross-check hatası (devam ediliyor): {e}")
    
    # 4. Token geçerliyse komutu çalıştır!
    try:
        kod = command_data.get("kod")
        print(f"✅ Token geçerli, komut çalıştırılıyor: {kod}")
        
        # Komut çalıştırma kodu buraya...
        # return execute_command_by_code(kod)
        
        return {"success": True, "executed_code": kod}
    
    except Exception as e:
        print(f"❌ Komut çalıştırma hatası: {e}")
        return {"success": False, "reason": str(e)}


def log_security_event(event_type, command_data, details):
    """Güvenlik olaylarını kaydet"""
    try:
        log_entry = {
            "timestamp": int(time.time() * 1000),
            "type": event_type,
            "command_kod": command_data.get("kod"),
            "token_age": int(time.time() * 1000) - command_data.get("token_created", 0),
            "details": details
        }
        # Firebase'e güvenlik loglarını yaz
        db.child("logs").child("security").push(log_entry)
    except Exception as e:
        print(f"Log yazma hatası: {e}")
```

### 2. Firebase Listener İçinde Çağırma

```python
def komut_listener(message):
    """Firebase komut dinleyicisi"""
    komut_data = message["data"]
    
    if komut_data is None:
        return
    
    # ⭐ Token validasyonu
    validation_result = execute_command(komut_data)
    
    if not validation_result["success"]:
        # Komut reddedildi
        print(f"Komut reddedildi: {validation_result['reason']}")
        return
    
    # Komut başarıyla çalıştırıldı
    kod = komut_data.get("kod")
    
    if kod == "ogr_zil":
        ring_bell("student")
    elif kod == "ogrt_zil":
        ring_bell("teacher")
    # ... diğer komutlar


# Listener başlat
komut_ref = db.child("kumanda").child("komut")
komut_ref.stream(komut_listener)
```

### 3. Anons Validasyonu (Örnek)

```python
def anons_listener(message):
    """Anons dinleyicisi - token kontrol ile"""
    anons_data = message["data"]
    
    if anons_data is None:
        return
    
    # Token validasyonu MUTLAKA yap
    token = anons_data.get("token")
    token_created = anons_data.get("token_created")
    
    validation = validate_token(token, token_created)
    if not validation["valid"]:
        print(f"❌ Anons reddedildi: {validation['error']}")
        log_security_event("INVALID_TOKEN_ANONS", anons_data, validation["error"])
        return
    
    # Token geçerliyse anons'u oku
    metin_tekrar = anons_data.get("metin", "")
    
    # Text'de "||N" formatı varsa tekrar sayısını ayıkla
    if "||" in metin_tekrar:
        metin, tekrar_str = metin_tekrar.rsplit("||", 1)
        tekrar = int(tekrar_str) if tekrar_str.isdigit() else 1
    else:
        metin = metin_tekrar
        tekrar = 1
    
    print(f"✅ Anons okunuyor: {metin} ({tekrar}x)")
    # speak_announcement(metin, tekrar)
```

---

## 🔒 Firebase Security Rules

Aşağıdaki kuralları Firebase Console → Rules sekmesinden ayarlayın:

```json
{
  "rules": {
    "kumanda": {
      ".read": true,
      ".write": true,
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

### Kuralların Anlamı:

- **kumanda**: Tüm okuma/yazma izni (web tarafı tüm verileri okuyabilmeli)
- **token**: Sadece okunabilir (istemci yazmasın)
- **komut/anons**: Gerekli alanlar olmalı (backend'de PHP/Node validasyonu yapılmalı)
- **ayarlar**: Hassas şifre bilgileri, kimse okuyamaz/yazamaz
- **logs/security**: Sadece backend yazabilir, kimse okuyamaz

---

## ⏰ Token Yenileme Süreci

### Istemci Tarafı (JavaScript) - Otomatik

```javascript
// Oturum süresi: 1 saat = 3600000 ms
// Token yenileme: 55 dakika sonra
// Yüksek kalite: 59. dakikada otomatik yenile

// createNewToken() fonksiyonu:
// 1. Yeni rastgele token üret (crypto.getRandomValues)
// 2. Firebase'de kumanda/token'a yaz
// 3. Timer başlat (55 dakika sonra tekrar çalışması için)
```

### Backend Tarafında (Python) - Önemli!

**Backend token yenilemesini DESTEKLEMEZ!** Backend token'ı doğrular, yeni token *istemci* tarafından üretilir.

---

## 🛡️ Ekstra Güvenlik Önerileri

### 1. Rate Limiting (Backend)

```python
from collections import defaultdict
import time

# Komut gönderme sıklığını limitle
command_rate_limit = defaultdict(list)
MAX_COMMANDS_PER_MINUTE = 30

def check_rate_limit(token_created):
    """Hızlı komut gönderimi tespiti"""
    now = int(time.time() * 1000)
    command_rate_limit[token_created].append(now)
    
    # 1 dakikadan eski komutları sil
    one_minute_ago = now - 60000
    command_rate_limit[token_created] = [
        t for t in command_rate_limit[token_created]
        if t > one_minute_ago
    ]
    
    if len(command_rate_limit[token_created]) > MAX_COMMANDS_PER_MINUTE:
        return False
    return True
```

### 2. IP Adresi Kontrolü (Opsiyonel)

```python
def validate_ip_consistency(new_token_ua, current_ua):
    """User-Agent tutarlılığını kontrol et"""
    if current_ua and new_token_ua != current_ua:
        # Farklı cihazdan giriş yapıldı
        log_security_event("USER_AGENT_CHANGED", {}, 
                          f"Old: {current_ua}, New: {new_token_ua}")
```

### 3. Token Revoke Mekanizması

```python
def revoke_token():
    """Acil durumlarda token'ı geçersiz kıl"""
    try:
        db.child("kumanda").child("token").set({
            "value": None,
            "revoked": int(time.time() * 1000),
            "reason": "Manual revocation"
        })
        print("Token revoke edildi")
    except Exception as e:
        print(f"Revoke hatası: {e}")
```

---

## 📋 Kontrol Listesi

Token sistemini dağıtmadan önce kontrol edin:

- [ ] **kumanda.html** yüklü ve token fonksiyonları çalışıyor mu?
- [ ] **Firebase Rules** ayarlandı mı?
- [ ] **Python backend** `validate_token()` fonksiyonunu çağırıyor mu?
- [ ] **Komut listener** tüm komutları (komut, anons, ses, şifre, zil) kontrol ediyor mu?
- [ ] **Token yenileme** otomatik olarak 55. dakikada çalışıyor mu?
- [ ] **Çıkış sırasında** token Firefox'tan siliniyor mu?
- [ ] **Zaman sinkronizasyonu** kontrol edildi mi (Python ve istemci saati eşit)?
- [ ] **Rate limiting** backend'de ayarlandı mı?
- [ ] **Güvenlik logları** kaydediliyor mu?

---

## 🐛 Hata Ayıklama

### Token geçersiz hatası alıyorum

**Kontrol et:**

```python
# Python'da zamanı kontrol et
import time
print(f"Server time (ms): {int(time.time() * 1000)}")

# Browser console'da zamanı kontrol et
console.log("Browser time (ms):", Date.now())
# Fark 5 saniyeyi geçerse NTP sinkronizasyonu yap
```

### Token yenilenmiyor

```javascript
// Browser console
console.log("Current token:", sessionToken);
console.log("Token expiry:", tokenExpiry);
console.log("Time until expiry:", tokenExpiry - Date.now(), "ms");
```

### Komutlar Firefox'ta çalışmıyor

- `CORSRules` kontrol et
- Facebook Rules `"kumanda": { ".write": true }` olduğundan emin ol
- Browser dev tools → Network tabı → Firebase requestlerini kontrol et

---

## 📞 Kontakt ve Destek

Token sistemi sorununda:

1. Browser console hatalarını kontrol et
2. Firebase Rules kurallarını doğrula
3. Python backend loglarını kontrol et
4. `SECURITY_TOKEN_GUIDE.md` referans al

**Son Güncelleme:** 2026-03-24  
**Token Süresi:** 1 saat  
**Güvenlik Seviyesi:** ⭐⭐⭐⭐ (6/10 - Backend validasyonu eklenir)
