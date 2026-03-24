/**
 * auth.js - Authentication (Login, Admin, Password Change)
 */

// ================================================================
//  USER LOGIN
// ================================================================
async function girisYap() {
  const sifre = document.getElementById("inp_sifre").value;
  if (!sifre) {
    toast("⚠️ Şifre boş olamaz!");
    return;
  }

  // Rate limiting kontrol
  const rateCheck = checkRateLimit("giris", CONFIG.RATE_LIMIT_ATTEMPTS, CONFIG.RATE_LIMIT_WINDOW);
  if (!rateCheck.allowed) {
    toast(`⏳ Çok fazla deneme. ${rateCheck.resetTime} saniye bekleyin.`);
    return;
  }

  setLoading(true);
  try {
    const snap = await withTimeout(db.ref(DB_YOLU.ayarlar).get(), CONFIG.FIREBASE_TIMEOUT);
    const ayarlar = snap.exists() ? (snap.val() || {}) : {};

    // 1. Hash karşılaştırma (en güvenli)
    if (ayarlar.mobil_sifre_hash) {
      const hash = await sha256(sifre);
      if (hash === ayarlar.mobil_sifre_hash) {
        girisBasarili(sifre);
        return;
      }
    }

    // 2. Düz metin karşılaştırma (Firebase'e henüz hash yazılmadıysa)
    if (ayarlar.mobil_sifre) {
      if (sifre === ayarlar.mobil_sifre) {
        girisBasarili(sifre);
        return;
      }
    }

    // 3. Firebase'de hiç kayıt yoksa varsayılan şifre "1234"
    if (!ayarlar.mobil_sifre && !ayarlar.mobil_sifre_hash) {
      if (sifre === "1234") {
        girisBasarili(sifre);
        return;
      }
    }

  } catch (e) {
    if (e.message.includes("timeout")) {
      toast("⏱️ Bağlantı zaman aşımı. Lütfen sonra tekrar deneyin.");
    } else if (e.message.includes("PERMISSION_DENIED")) {
      toast("🔒 Erişim reddedildi. Firebase kurallarını kontrol edin.");
    } else {
      toast("⚠️ Hata: " + e.message);
    }
  } finally {
    setLoading(false);
  }
  
  document.getElementById("hata_giris").style.display = "block";
}

function girisBasarili(sifre) {
  girisYapildi = true;
  document.getElementById("hata_giris").style.display = "none";
  ekranGoster("kumanda");
  
  // Token üret ve Firebase'e yaz
  createNewToken()
    .then(() => {
      dinleyicileriBaslat();
      toast("✅ Giriş başarılı!");
    })
    .catch(e => {
      toast("⚠️ Token oluşturulamadı: " + e.message);
      cikisYap();
    });
}

// ================================================================
//  LOGOUT
// ================================================================
function cikisYap() {
  // Listeners'ı kapat
  activeListeners.forEach(ref => ref.off("value"));
  activeListeners = [];
  
  // Token ve timer'ı temizle
  clearToken();
  
  girisYapildi = false;
  yoneticiGirildi = false;
  
  // Şifre input'u temizle
  const inp = document.getElementById("inp_sifre");
  if (inp) inp.value = "";
  
  ekranGoster("giris");
}

// ================================================================
//  ADMIN LOGIN
// ================================================================
async function yoneticiGiris() {
  const sifreEl = DOM_CACHE.inp_yon_sifre || document.getElementById("inp_yon_sifre");
  if (!sifreEl) {
    toast("⚠️ Şifre alanı bulunamadı!");
    return;
  }
  
  const sifre = sifreEl.value;
  if (!sifre) {
    toast("⚠️ Şifre boş olamaz!");
    return;
  }

  // Rate limiting
  const rateCheck = checkRateLimit("yonetici_giris", CONFIG.RATE_LIMIT_ATTEMPTS, CONFIG.RATE_LIMIT_WINDOW);
  if (!rateCheck.allowed) {
    toast(`⏳ Çok fazla deneme. ${rateCheck.resetTime} saniye bekleyin.`);
    return;
  }

  setLoading(true);
  try {
    const snap = await withTimeout(db.ref(DB_YOLU.ayarlar).get(), CONFIG.FIREBASE_TIMEOUT);
    const ayarlar = snap.exists() ? (snap.val() || {}) : {};
    
    // ⚠️ SHA-256 HASH İLE KONTROL (düz metin kontrol yok!)
    let eslesme = false;
    if (ayarlar.yonetici_sifre_hash) {
      eslesme = (await sha256(sifre)) === ayarlar.yonetici_sifre_hash;
    } else {
      // Hash yok = sistem kilitli
      toast("⚠️ Sistem şifre ayarlanmadı. Admin ile iletişime geçin.");
      setLoading(false);
      return;
    }
    
    if (eslesme) {
      yoneticiGirildi = true;
      const hataEl = DOM_CACHE.hata_yon || document.getElementById("hata_yon");
      const girisEl = DOM_CACHE.yon_giris_bolum || document.getElementById("yon_giris_bolum");
      const panelEl = DOM_CACHE.yon_panel_bolum || document.getElementById("yon_panel_bolum");
      if (hataEl) hataEl.style.display = "none";
      if (girisEl) girisEl.style.display = "none";
      if (panelEl) panelEl.style.display = "block";
    } else {
      const hataEl = DOM_CACHE.hata_yon || document.getElementById("hata_yon");
      if (hataEl) hataEl.style.display = "block";
    }
  } catch (e) {
    if (e.message.includes("timeout")) {
      toast("⏱️ Bağlantı zaman aşımı.");
    } else {
      toast("⚠️ Bağlantı hatası: " + e.message);
    }
  } finally {
    setLoading(false);
  }
}

// ================================================================
//  PASSWORD CHANGE
// ================================================================
async function sifreDegistir() {
  const tipEl = DOM_CACHE.sifre_tip || document.getElementById("sifre_tip");
  const y1El = DOM_CACHE.inp_yeni1 || document.getElementById("inp_yeni1");
  const y2El = DOM_CACHE.inp_yeni2 || document.getElementById("inp_yeni2");
  const mesajEl = DOM_CACHE.yon_mesaj || document.getElementById("yon_mesaj");
  
  if (!tipEl || !y1El || !y2El || !mesajEl) {
    toast("⚠️ Şifre değişim alanları bulunamadı!");
    return;
  }
  
  const tip = tipEl.value;
  const y1 = y1El.value;
  const y2 = y2El.value;

  if (!y1 || !y2) {
    mesajEl.innerHTML = '<div class="msg-err">Hata: Şifre alanları boş olamaz!</div>';
    return;
  }
  if (y1 !== y2) {
    mesajEl.innerHTML = '<div class="msg-err">Hata: Şifreler uyuşmuyor!</div>';
    return;
  }
  if (y1.length < CONFIG.MIN_PASSWORD_LENGTH) {
    mesajEl.innerHTML = `<div class="msg-err">Hata: En az ${CONFIG.MIN_PASSWORD_LENGTH} karakter olmalı!</div>`;
    return;
  }
  if (y1.length > CONFIG.MAX_PASSWORD_LENGTH) {
    mesajEl.innerHTML = `<div class="msg-err">Hata: Şifre ${CONFIG.MAX_PASSWORD_LENGTH} karakteri geçemez!</div>`;
    return;
  }

  setLoading(true);
  try {
    if (!isTokenValid()) {
      throw new Error("Oturum süresi doldu");
    }
    
    const hash = await sha256(y1);

    // Firebase ayarlar'a hash'i yaz
    const guncelle = {};
    guncelle[tip + "_sifre_hash"] = hash;
    await withTimeout(db.ref(DB_YOLU.ayarlar).update(guncelle), CONFIG.FIREBASE_TIMEOUT);

    // PC'ye şifre değiştirme komutu gönder
    await withTimeout(db.ref(DB_YOLU.sifre).set({
      tip: tip,
      hash: hash,
      zaman: Date.now(),
      token: sessionToken,
      token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
    }), CONFIG.FIREBASE_TIMEOUT);

    // ✅ Başarı mesajı
    mesajEl.innerHTML = '<div class="msg-ok">✓ Şifre güncellendi ve tüm cihazlara yansıtıldı.</div>';
    y1El.value = "";
    y2El.value = "";
  } catch (e) {
    const hataMsg = e.message.includes("timeout")
      ? "Zaman aşımı - lütfen sonra tekrar deneyin."
      : e.message;
    mesajEl.innerHTML = '<div class="msg-err">Hata: ' + hataMsg + '</div>';
  } finally {
    setLoading(false);
  }
}
