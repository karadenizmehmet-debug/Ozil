/**
 * ui.js - UI geçişleri, modal'lar, keyboard handler
 */

// ================================================================
//  ACTIVE LISTENERS TRACKING
// ================================================================
let activeListeners = [];
let sistemAcik = true;

// ================================================================
//  SCREEN TRANSITIONS
// ================================================================
function ekranGoster(ekran) {
  ["giris", "kumanda", "sarki", "yonetici", "zil"].forEach(e =>
    document.getElementById("ekran_" + e).style.display = "none");
  document.getElementById("ekran_" + ekran).style.display = "block";
  
  if (ekran === "sarki") sarkiListesiYukle();
  if (ekran === "zil") zilListesiYukle();
  
  // Keyboard event listener ekle/kaldır
  if (ekran !== "giris") {
    document.addEventListener("keydown", handleGlobalKeydown);
  } else {
    document.removeEventListener("keydown", handleGlobalKeydown);
  }
}

// ================================================================
//  GLOBAL KEYBOARD HANDLER (ESC tuşu)
// ================================================================
function handleGlobalKeydown(e) {
  if (e.key === "Escape") {
    const yoneticiPanel = document.getElementById("ekran_yonetici");
    const zilPanel = document.getElementById("ekran_zil");
    const sarkiPanel = document.getElementById("ekran_sarki");
    
    if (yoneticiPanel && yoneticiPanel.style.display !== "none") {
      ekranGoster("kumanda");
      e.preventDefault();
    } else if (zilPanel && zilPanel.style.display !== "none") {
      ekranGoster("kumanda");
      e.preventDefault();
    } else if (sarkiPanel && sarkiPanel.style.display !== "none") {
      ekranGoster("kumanda");
      e.preventDefault();
    }
  }
}

// ================================================================
//  GENEL AYARLAR
// ================================================================
function genelAyarGoster() {
  const card = DOM_CACHE.genel_ayar_card || document.getElementById("genel_ayar_card");
  if (!card) return;
  card.style.display = card.style.display === "none" ? "block" : "none";
}

let _genelAyarTimer = null;

function genelAyarGonder() {
  clearTimeout(_genelAyarTimer);
  _genelAyarTimer = setTimeout(() => {
    if (!isTokenValid()) {
      toast("⚠️ Oturum süresi doldu.");
      return;
    }
    const tenEl = DOM_CACHE.chk_teneffus || document.getElementById("chk_teneffus");
    const sesEl = DOM_CACHE.rng_muzik_sesi || document.getElementById("rng_muzik_sesi");
    if (!tenEl || !sesEl) return;
    
    const ten = tenEl.checked;
    const ses = parseInt(sesEl.value);
    
    db.ref(DB_YOLU.genel_ayar).set({
      teneffus_aktif: ten,
      muzik_sesi: ses,
      zaman: Date.now(),
      token: sessionToken,
      token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
    }).then(() => toast("✓ Ayar güncellendi"))
      .catch(e => toast("⚠️ Hata: " + e.message));
  }, CONFIG.SLIDER_DEBOUNCE);
}

// ================================================================
//  SİSTEM TOGGLE (Açık/Kapalı)
// ================================================================
function sistemToggle() {
  if (!isTokenValid()) {
    toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
    cikisYap();
    return;
  }
  
  const yeniDurum = !sistemAcik;
  db.ref(DB_YOLU.sistem_durum).set({
    aktif: yeniDurum,
    zaman: Date.now(),
    token: sessionToken,
    token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
  }).then(() => {
    _sistemDurumGuncelle(yeniDurum);
    toast(yeniDurum ? "✅ Sistem Açıldı" : "🔴 Sistem Kapatıldı");
  }).catch(e => toast("⚠️ Hata: " + e.message));
}

function _sistemDurumGuncelle(aktif) {
  sistemAcik = aktif;
  const btn = DOM_CACHE.btn_sistem || document.getElementById("btn_sistem");
  const lbl = DOM_CACHE.lbl_sistem || document.getElementById("lbl_sistem");
  if (!btn) return;
  
  if (aktif) {
    btn.style.backgroundColor = "#2ed573";
    btn.style.boxShadow = "0 4px #27ae60";
    if (lbl) lbl.textContent = "SİSTEM: AÇIK";
  } else {
    btn.style.backgroundColor = "#ff4757";
    btn.style.boxShadow = "0 4px #c0392b";
    if (lbl) lbl.textContent = "SİSTEM: KAPALI";
  }
}

// ================================================================
//  QR CODE MODAL
// ================================================================
function qrGoster() {
  const modal = document.getElementById("qr_modal");
  const container = document.getElementById("qr_container");
  const urlEl = document.getElementById("qr_url");
  const url = window.location.href;
  urlEl.textContent = url;
  
  // QR container'ı temizle
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  
  // Yeni QR kodu oluştur
  try {
    new QRCode(container, {
      text: url,
      width: 200,
      height: 200,
      colorDark: "#2c3e50",
      colorLight: "#ffffff"
    });
  } catch (e) {
    container.textContent = "QR kod oluşturulamadı.";
  }
  
  modal.classList.add("active");
  
  // Esc tuşu ile kapatma
  function qrKeyListener(e) {
    if (e.key === "Escape") {
      qrKapat();
      modal.removeEventListener("keydown", qrKeyListener);
    }
  }
  modal.addEventListener("keydown", qrKeyListener);
  
  // Modal dışına tıklanınca kapatma
  function qrClickListener(e) {
    if (e.target === modal) {
      qrKapat();
      modal.removeEventListener("click", qrClickListener);
    }
  }
  modal.addEventListener("click", qrClickListener);
  
  // Focus modal içine
  setTimeout(() => {
    const closeBtn = modal.querySelector(".btn");
    if (closeBtn) closeBtn.focus();
  }, 100);
}

function qrKapat() {
  document.getElementById("qr_modal").classList.remove("active");
}
