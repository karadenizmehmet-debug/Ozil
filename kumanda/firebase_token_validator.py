#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔐 Firebase Token Validation Helper
Token doğrulama ve güvenlik işlevleri için yardımcı modül

Kullanım:
    from firebase_token_validator import validate_token, log_security_event
    
    # Komut validasyonu
    validation = validate_token(command_data.get("token"), 
                                command_data.get("token_created"))
    if validation["valid"]:
        # Komutu çalıştır
        pass
"""

import time
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

# Konfigürasyon
TOKEN_EXPIRY_MS = 3600000  # 1 saat (milisaniye)
TOKEN_LENGTH = 64  # 32 byte × 2 hex char = 64 hex string
MAX_COMMANDS_PER_MINUTE = 30
ALLOW_LARGE_TIME_DRIFT_MS = 5000  # 5 saniye tolerans

# Global rate limiting nesnesi
command_history = {}


def validate_token(token_value: Optional[str], token_created_ms: Optional[int]) -> Dict:
    """
    Token'ı kapsamlı şekilde doğrula
    
    Args:
        token_value (str): Token hex string'i (64 karakter)
        token_created_ms (int): Token oluşturma zamanı (epoch milliseconds)
    
    Returns:
        dict: {
            "valid": True/False,
            "error": "Hata mesajı",
            "age_ms": Token yaşı milliseconds cinsinden
        }
    
    Kontroller:
        ✓ Token boş değil
        ✓ Token formatı doğru (64 hex char)
        ✓ Token yaşı hesaplanabilir
        ✓ Token süresi dolmadı
        ✓ Token zamanı gelecekte değil
    """
    
    # Boş kontrol
    if not token_value:
        return {
            "valid": False,
            "error": "Token bulunamadı (None veya boş string)"
        }
    
    # Tür kontrol
    if not isinstance(token_value, str):
        return {
            "valid": False,
            "error": f"Token formatı yanlış. Beklenen: str, Alınan: {type(token_value).__name__}"
        }
    
    # Uzunluk kontrol
    if len(token_value) != TOKEN_LENGTH:
        return {
            "valid": False,
            "error": f"Token uzunluğu yanlış. Beklenen: {TOKEN_LENGTH}, Alınan: {len(token_value)}"
        }
    
    # Hex formatı kontrol
    try:
        int(token_value, 16)  # Hex string mi?
    except ValueError:
        return {
            "valid": False,
            "error": "Token hex formatında değil (0-9, a-f karakterleri olmalı)"
        }
    
    # Zaman bilgisi kontrol
    if token_created_ms is None:
        return {
            "valid": False,
            "error": "Token oluşturma zamanı bulunamadı"
        }
    
    if not isinstance(token_created_ms, (int, float)):
        return {
            "valid": False,
            "error": f"Token zamanı yanlış tür: {type(token_created_ms).__name__}"
        }
    
    # Zamanı hesapla
    current_ms = int(time.time() * 1000)
    token_age_ms = current_ms - token_created_ms
    
    # Gelecekten gelen token (saat sinkronizasyonu hatası)
    if token_age_ms < -ALLOW_LARGE_TIME_DRIFT_MS:
        return {
            "valid": False,
            "error": f"Token zamanı gelecekte ({-token_age_ms}ms). Sunucu saatini kontrol edin.",
            "age_ms": token_age_ms
        }
    
    # Süresi dolmuş token
    if token_age_ms > TOKEN_EXPIRY_MS:
        minutes_expired = (token_age_ms - TOKEN_EXPIRY_MS) // 60000
        return {
            "valid": False,
            "error": f"Token süresi doldu ({minutes_expired} dakika önce)",
            "age_ms": token_age_ms
        }
    
    # Geçerli token
    return {
        "valid": True,
        "age_ms": token_age_ms,
        "error": None
    }


def check_rate_limit(token_value: str, max_commands: int = MAX_COMMANDS_PER_MINUTE) -> Dict:
    """
    Hızlı komut gönderimi (brute-force) tespiti
    
    Args:
        token_value (str): Token (rate limiting için key olarak)
        max_commands (int): 1 dakikada izin verilen maksimum komut
    
    Returns:
        dict: {
            "allowed": True/False,
            "commands_this_minute": Komut sayısı,
            "reset_in_seconds": Kaç saniyede sıfırlanacağı
        }
    """
    now = int(time.time())
    
    if token_value not in command_history:
        command_history[token_value] = []
    
    # 1 dakikadan eski komutları sil
    one_minute_ago = now - 60
    command_history[token_value] = [
        t for t in command_history[token_value]
        if t > one_minute_ago
    ]
    
    # Yeni komut ekle
    command_history[token_value].append(now)
    current_count = len(command_history[token_value])
    
    # Limit kontrol
    allowed = current_count <= max_commands
    
    # Reset zamanı hesapla
    if command_history[token_value]:
        oldest_command = command_history[token_value][0]
        reset_in = 60 - (now - oldest_command)
    else:
        reset_in = 0
    
    return {
        "allowed": allowed,
        "commands_this_minute": current_count,
        "reset_in_seconds": max(0, reset_in),
        "limit": max_commands
    }


def validate_command(command_data: Dict) -> Tuple[bool, str]:
    """
    Komut verisini tam olarak doğrula
    
    Args:
        command_data (dict): Firebase'den gelen komut nesnesi
                           {
                             "kod": "ogr_zil",
                             "token": "abc123...",
                             "token_created": 1234567890,
                             "zaman": 1234567890
                           }
    
    Returns:
        tuple: (valid: bool, reason: str)
    """
    
    # Gerekli alanlar
    required_fields = ["kod", "token", "token_created", "zaman"]
    for field in required_fields:
        if field not in command_data:
            return False, f"Alan eksik: {field}"
    
    # Kod kontrolü
    kod = command_data.get("kod")
    if not kod or not isinstance(kod, str):
        return False, "Komut kodu geçersiz"
    
    # Token doğrulama
    token_validation = validate_token(
        command_data.get("token"),
        command_data.get("token_created")
    )
    
    if not token_validation["valid"]:
        return False, f"Token hatası: {token_validation['error']}"
    
    # Rate limit kontrol
    rate_check = check_rate_limit(command_data.get("token"))
    if not rate_check["allowed"]:
        return False, f"Çok fazla komut gönderimi ({rate_check['commands_this_minute']}/{rate_check['limit']})"
    
    return True, "Komut geçerli"


def log_security_event(event_type: str, command_data: Dict, details: str, firebase_db=None):
    """
    Güvenlik olaylarını kaydet
    
    Args:
        event_type (str): Olay türü (INVALID_TOKEN, RATE_LIMIT, etc.)
        command_data (dict): İlgili komut verisi
        details (str): Detay mesajı
        firebase_db: Firebase database referansı (opsiyonel)
    """
    
    timestamp_ms = int(time.time() * 1000)
    
    log_entry = {
        "timestamp": timestamp_ms,
        "type": event_type,
        "command_kod": command_data.get("kod"),
        "token_age_ms": timestamp_ms - command_data.get("token_created", 0),
        "details": details,
        "logged_at": datetime.now().isoformat()
    }
    
    # Konsola yaz
    print(f"🔐 [{event_type}] {details}")
    print(f"   Komut: {log_entry['command_kod']}")
    print(f"   Token Yaşı: {log_entry['token_age_ms']}ms")
    
    # Firebase'e yaz (opsiyonel)
    if firebase_db:
        try:
            firebase_db.child("logs").child("security").push(log_entry)
        except Exception as e:
            print(f"⚠️  Log yazma hatası: {e}")


def format_time_ms(milliseconds: int) -> str:
    """Millisaniye'yi okunaklı formata çevir"""
    if milliseconds < 1000:
        return f"{milliseconds}ms"
    elif milliseconds < 60000:
        return f"{milliseconds // 1000}s"
    elif milliseconds < 3600000:
        return f"{milliseconds // 60000}m"
    else:
        return f"{milliseconds // 3600000}h"


# ============================================================================
# KULLANIM ÖRNEKLERİ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Firebase Token Validation Test")
    print("=" * 60)
    
    # Test 1: Geçerli token
    print("\n📝 Test 1: Geçerli Token")
    valid_token = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    current_time = int(time.time() * 1000)
    
    result = validate_token(valid_token, current_time)
    print(f"Token: {valid_token[:16]}...")
    print(f"Yaşı: {format_time_ms(result['age_ms'])}")
    print(f"Geçerli: {'✅ Evet' if result['valid'] else '❌ Hayır'}")
    
    # Test 2: Süresi dolmuş token
    print("\n📝 Test 2: Süresi Dolmuş Token")
    old_time = current_time - (TOKEN_EXPIRY_MS + 300000)  # 5 dakika eski
    
    result = validate_token(valid_token, old_time)
    print(f"Yaşı: {format_time_ms(result['age_ms'])}")
    print(f"Geçerli: {'✅ Evet' if result['valid'] else '❌ Hayır'}")
    print(f"Hata: {result['error']}")
    
    # Test 3: Formatı yanlış token
    print("\n📝 Test 3: Formatı Yanlış Token")
    invalid_token = "invalid_token_123"
    
    result = validate_token(invalid_token, current_time)
    print(f"Geçerli: {'✅ Evet' if result['valid'] else '❌ Hayır'}")
    print(f"Hata: {result['error']}")
    
    # Test 4: Komut validasyonu
    print("\n📝 Test 4: Komut Doğrulama")
    command = {
        "kod": "ogr_zil",
        "token": valid_token,
        "token_created": current_time,
        "zaman": current_time
    }
    
    valid, reason = validate_command(command)
    print(f"Komut: {command['kod']}")
    print(f"Geçerli: {'✅ Evet' if valid else '❌ Hayır'}")
    print(f"Sebep: {reason}")
    
    # Test 5: Rate limiting
    print("\n📝 Test 5: Rate Limiting")
    for i in range(5):
        rate_check = check_rate_limit(valid_token)
        if i == 0:
            print(f"Komut #{i+1}: {rate_check['commands_this_minute']}/{rate_check['limit']} " + 
                  f"({'✅ İzin' if rate_check['allowed'] else '❌ Reddedildi'})")
    
    print("\n" + "=" * 60)
