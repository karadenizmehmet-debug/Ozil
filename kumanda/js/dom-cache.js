/**
 * dom-cache.js - DOM elements'ı cache'le (performance)
 */

// ================================================================
//  DOM CACHE - Tekrar tekrar getElementById çağrısı yapmamak için
// ================================================================
const DOM_CACHE = {
  inp_sifre: null,
  hata_giris: null,
  durum_bar: null,
  lbl_pc: null,
  txt_anons: null,
  anons_tekrar: null,
  ses_slider: null,
  vol_val: null,
  vol_val2: null,
  btn_sistem: null,
  lbl_sistem: null,
  chk_teneffus: null,
  rng_muzik_sesi: null,
  lbl_muzik_sesi: null,
  genel_ayar_card: null,
  inp_yon_sifre: null,
  hata_yon: null,
  sifre_tip: null,
  inp_yeni1: null,
  inp_yeni2: null,
  yon_mesaj: null,
  yon_giris_bolum: null,
  yon_panel_bolum: null,
  qr_modal: null,
  qr_container: null,
  qr_url: null,
  toast: null,
  zil_melodi_liste: null,
  zil_secili_tip: null,
  sarki_liste: null
};

/**
 * DOM Cache'i doldur - Sayfa yüklendiğinde çalış
 */
function initDOMCache() {
  Object.keys(DOM_CACHE).forEach(key => {
    DOM_CACHE[key] = document.getElementById(key);
  });
}
