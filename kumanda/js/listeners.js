/**
 * listeners.js - Firebase Realtime Database dinleyicileri
 */

// ================================================================
//  START LISTENERS (Giriş sonrası çalış)
// ================================================================
function dinleyicileriBaslat() {
  // Eski listeners'ları temizle
  activeListeners.forEach(ref => ref.off("value"));
  activeListeners = [];

  // PC bağlantı durumu ve zil aktif durumu
  const durum_ref = db.ref(DB_YOLU.durum);
  durum_ref.on("value", snap => {
    const bar = DOM_CACHE.durum_bar || document.getElementById("durum_bar");
    if (!bar) return;
    const v = snap.val() || {};
    
    // Bağlantı durumu
    if (v.cevrimici) {
      bar.textContent = "🟢 Bağlı — " + (v.pc_adi || "");
      bar.className = "durum-bagli";
      if (v.pc_adi) {
        const pcLbl = DOM_CACHE.lbl_pc || document.getElementById("lbl_pc");
        if (pcLbl) pcLbl.textContent = v.pc_adi + " - Kumanda";
      }
    } else {
      bar.textContent = "🔴 PC Çevrimdışı";
      bar.className = "durum-cevrimdisi";
    }
    
    // Zil aktif durumu
    if (typeof v.zil_aktif === "boolean") {
      _sistemDurumGuncelle(v.zil_aktif);
    }
  });
  activeListeners.push(durum_ref);

  // Genel ayarlar (teneffüs müziği, müzik sesi)
  const ayar_ref = db.ref(DB_YOLU.genel_ayar);
  ayar_ref.on("value", snap => {
    const v = snap.val();
    if (v && typeof v === "object") {
      const chk = DOM_CACHE.chk_teneffus || document.getElementById("chk_teneffus");
      const rng = DOM_CACHE.rng_muzik_sesi || document.getElementById("rng_muzik_sesi");
      const lbl = DOM_CACHE.lbl_muzik_sesi || document.getElementById("lbl_muzik_sesi");
      
      if (chk && typeof v.teneffus_aktif === "boolean") chk.checked = v.teneffus_aktif;
      if (rng && v.muzik_sesi) {
        rng.value = v.muzik_sesi;
        if (lbl) lbl.textContent = "%" + v.muzik_sesi;
      }
    }
  });
  activeListeners.push(ayar_ref);

  // Ses seviyesi senkronizasyonu (PC değiştirirse buraya yansır)
  const ses_ref = db.ref(DB_YOLU.ses);
  ses_ref.on("value", snap => {
    if (snap.val() !== null) {
      mevcutSes = parseInt(snap.val()) || 80;
      _sliderGuncelle(mevcutSes);
    }
  });
  activeListeners.push(ses_ref);
}

// ================================================================
//  PAGE UNLOAD - Listeners temizleme
// ================================================================
window.addEventListener("beforeunload", () => {
  activeListeners.forEach(ref => ref.off("value"));
  activeListeners = [];
});
