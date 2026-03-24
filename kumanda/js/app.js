/**
 * app.js - Main initialization ve DOMContentLoaded
 */

// ================================================================
//  FIREBASE INITIALIZATION
// ================================================================
firebase.initializeApp(FIREBASE_CONFIG);
db = firebase.database();

// ================================================================
//  PAGE LOAD - Initialization
// ================================================================
window.addEventListener("DOMContentLoaded", () => {
  // DOM Cache'i doldur
  initDOMCache();
  
  // Giriş ekranını göster
  ekranGoster("giris");
  
  // Debounced event listeners'ı ekle
  const debouncedGenelAyar = debounce(genelAyarGonder, CONFIG.SESSION_DEBOUNCE);
  
  // Checkbox change listener
  const chkTeneffus = document.getElementById("chk_teneffus");
  if (chkTeneffus) chkTeneffus.addEventListener("change", debouncedGenelAyar);
  
  // Müzik ses slider change listener
  const sldrMuzikSesi = document.getElementById("rng_muzik_sesi") || document.getElementById("sldr_muzik_sesi");
  if (sldrMuzikSesi) {
    sldrMuzikSesi.addEventListener("change", debouncedGenelAyar);
  }
});
