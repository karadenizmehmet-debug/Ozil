/**
 * commands.js - Komut gönderme (zil, anons, ses)
 */

// ================================================================
//  COMMAND SENDING
// ================================================================
function komutGonder(kod, isim) {
  if (!girisYapildi) {
    toast("⚠️ Lütfen önce giriş yapın!");
    return;
  }
  if (!kod || !isim) {
    toast("⚠️ Komut bilgileri eksik!");
    return;
  }
  
  // Token control
  if (!isTokenValid()) {
    toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
    cikisYap();
    return;
  }
  
  const komut = {
    kod: kod,
    zaman: Date.now(),
    token: sessionToken,
    token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
  };
  
  db.ref(DB_YOLU.komut).set(komut)
    .then(() => toast(isim + " ✓"))
    .catch(e => toast("⚠️ Hata: " + (e.message || "Bilinmeyen hata")));
}

// ================================================================
//  ANNOUNCEMENT SENDING
// ================================================================
function anonsGonder() {
  const txtEl = DOM_CACHE.txt_anons || document.getElementById("txt_anons");
  if (!txtEl) {
    toast("⚠️ Anons alanı bulunamadı!");
    return;
  }
  
  if (!isTokenValid()) {
    toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
    cikisYap();
    return;
  }
  
  const metin = txtEl.value.trim();
  
  // Validasyon
  if (!metin) {
    toast("⚠️ Anons metni boş olamaz!");
    return;
  }
  
  // Uzunluk kontrolü (UTF-8 byte cinsinden)
  const byteLength = new Blob([metin]).size;
  if (byteLength > CONFIG.MAX_ANONS_BYTES) {
    toast(`⚠️ Anons metni çok uzun! (Max: ${CONFIG.MAX_ANONS_BYTES} byte)`);
    return;
  }
  
  const tekrarEl = DOM_CACHE.anons_tekrar || document.getElementById("anons_tekrar");
  if (!tekrarEl) {
    toast("⚠️ Tekrar alanı bulunamadı!");
    return;
  }
  
  const tekrar = parseInt(tekrarEl.value) || 1;
  if (tekrar < 1 || tekrar > CONFIG.MAX_REPEAT) {
    toast(`⚠️ Tekrar sayısı 1-${CONFIG.MAX_REPEAT} arasında olmalı!`);
    return;
  }
  
  // Tekrar sayısını metne "||N" formatında ekle — Python tarafı okur
  const veri = tekrar > 1 ? metin + "||" + tekrar : metin;
  
  db.ref(DB_YOLU.anons).set({
    metin: veri,
    zaman: Date.now(),
    token: sessionToken,
    token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
  }).then(() => {
    toast("Anons İletildi! 🔊 (" + tekrar + "x)");
    txtEl.value = "";
  }).catch(e => toast("⚠️ Hata: " + (e.message || "Bilinmeyen hata")));
}

// ================================================================
//  VOLUME CONTROL
// ================================================================
let mevcutSes = 80;
let sesZamanlayici = null;

function sesGuncelle(val) {
  const numVal = parseInt(val);
  if (isNaN(numVal)) return;
  
  mevcutSes = numVal;
  _sliderGuncelle(mevcutSes);
  
  // ARIA attribute'ları güncelle
  const slider = DOM_CACHE.ses_slider || document.getElementById("ses_slider");
  if (slider) {
    slider.setAttribute("aria-valuenow", mevcutSes);
    slider.setAttribute("aria-label", `Sistem ses seviyesi: %${mevcutSes}`);
  }
  
  // Debounce ile Firebase'e yaz
  clearTimeout(sesZamanlayici);
  sesZamanlayici = setTimeout(() => {
    if (!isTokenValid()) {
      return;
    }
    db.ref(DB_YOLU.ses).set({
      value: mevcutSes,
      token: sessionToken,
      token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
    });
  }, CONFIG.SLIDER_DEBOUNCE);
}

// ================================================================
//  SLIDER SYNCHRONIZATION
// ================================================================
function _sliderGuncelle(deger) {
  if (!deger && deger !== 0) deger = 80;
  deger = parseInt(deger) || 80;
  if (deger < 0) deger = 0;
  if (deger > 100) deger = 100;
  
  const slider1 = DOM_CACHE.ses_slider || document.getElementById("ses_slider");
  const slider2 = document.querySelector("#ekran_sarki input[type=range]");
  const vol1 = DOM_CACHE.vol_val || document.getElementById("vol_val");
  const vol2 = DOM_CACHE.vol_val2 || document.getElementById("vol_val2");
  
  if (slider1) slider1.value = deger;
  if (slider2) slider2.value = deger;
  if (vol1) vol1.textContent = "%" + deger;
  if (vol2) vol2.textContent = "%" + deger;
}
