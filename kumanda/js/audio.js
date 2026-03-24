/**
 * audio.js - Zil melodisi ve şarkı yönetimi
 */

// ================================================================
//  ZİL MELODİSİ SEÇİCİ
// ================================================================
let seciliZilTip = "";
let seciliZilAdi = "";
let zilListesiGuncelleniyorMu = false;

function zilListesiYukle() {
  if (zilListesiGuncelleniyorMu) return; // Race condition önle
  
  const kap = document.getElementById("zil_melodi_liste");
  if (!kap) return;
  
  zilListesiGuncelleniyorMu = true;
  
  db.ref(DB_YOLU.zil_listesi).get().then(snap => {
    if (!snap.exists() || !snap.val() || snap.val().length === 0) {
      kap.innerHTML = "";
      const msg = document.createElement("div");
      msg.className = "sarki-item";
      msg.style.color = "#7f8c8d";
      msg.textContent = "Melodi bulunamadı. PC'nin melodi listesi bekleniyor.";
      kap.appendChild(msg);
      zilListesiGuncelleniyorMu = false;
      return;
    }
    window._zilListesi = snap.val();
    if (seciliZilTip) zilTipSec(seciliZilTip, seciliZilAdi);
    else {
      kap.innerHTML = "";
      const msg = document.createElement("div");
      msg.className = "sarki-item";
      msg.style.color = "#7f8c8d";
      msg.textContent = "Yukarıdan bir zil türü seçin.";
      kap.appendChild(msg);
    }
    zilListesiGuncelleniyorMu = false;
  }).catch(() => {
    kap.innerHTML = "";
    const msg = document.createElement("div");
    msg.className = "sarki-item";
    msg.style.color = "#e74c3c";
    msg.textContent = "Liste yüklenemedi.";
    kap.appendChild(msg);
    zilListesiGuncelleniyorMu = false;
  });
}

function zilTipSec(tip, ad) {
  seciliZilTip = tip;
  seciliZilAdi = ad;
  document.getElementById("zil_secili_tip").textContent = ad + " için melodi seçin:";
  
  const kap = document.getElementById("zil_melodi_liste");
  const liste = window._zilListesi || [];
  if (!liste.length) {
    zilListesiYukle();
    return;
  }
  
  kap.innerHTML = "";
  
  // "Varsayılan" seçeneği her zaman en üstte
  const varsDiv = document.createElement("div");
  varsDiv.className = "sarki-item";
  const varsName = document.createElement("span");
  varsName.className = "sarki-name";
  varsName.textContent = "⭐ Varsayılan";
  const varsBtn = document.createElement("span");
  varsBtn.className = "play-btn";
  varsBtn.textContent = "✓";
  varsDiv.appendChild(varsName);
  varsDiv.appendChild(varsBtn);
  varsDiv.onclick = () => {
    zilSecGonder(tip, "Varsayılan", ad);
  };
  kap.appendChild(varsDiv);
  
  // Diğer melodiler
  liste.forEach(melodi => {
    const div = document.createElement("div");
    div.className = "sarki-item";
    const melodiName = document.createElement("span");
    melodiName.className = "sarki-name";
    melodiName.textContent = melodi;
    const playBtn = document.createElement("span");
    playBtn.className = "play-btn";
    playBtn.textContent = "✓";
    div.appendChild(melodiName);
    div.appendChild(playBtn);
    div.onclick = () => {
      zilSecGonder(tip, melodi, ad);
    };
    kap.appendChild(div);
  });
}

function zilSecGonder(tip, melodi, ad) {
  if (!isTokenValid()) {
    toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
    cikisYap();
    return;
  }
  
  db.ref(DB_YOLU.zil_sec).set({
    tip: tip,
    melodi: melodi,
    zaman: Date.now(),
    token: sessionToken,
    token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
  }).then(() => toast("✓ " + ad + ": " + melodi))
    .catch(e => toast("⚠️ Hata: " + e.message));
}

// ================================================================
//  ŞARKI LİSTESİ
// ================================================================
function sarkiListesiYukle() {
  const kap = document.getElementById("sarki_liste");
  db.ref(DB_YOLU.sarki_liste).get().then(snap => {
    kap.innerHTML = "";
    if (!snap.exists() || !snap.val() || snap.val().length === 0) {
      const msg = document.createElement("div");
      msg.className = "sarki-item";
      msg.style.color = "#7f8c8d";
      msg.textContent = "Şarkı bulunamadı. PC'nin şarkı listesi göndermesi bekleniyor.";
      kap.appendChild(msg);
      return;
    }
    
    snap.val().forEach(sarki => {
      const div = document.createElement("div");
      div.className = "sarki-item";
      const sarkiName = document.createElement("span");
      sarkiName.className = "sarki-name";
      sarkiName.textContent = sarki;
      const playBtn = document.createElement("span");
      playBtn.className = "play-btn";
      playBtn.textContent = "▶️";
      div.appendChild(sarkiName);
      div.appendChild(playBtn);
      div.onclick = () => {
        if (!isTokenValid()) {
          toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
          cikisYap();
          return;
        }
        db.ref(DB_YOLU.sarki).set({
          ad: sarki,
          zaman: Date.now(),
          token: sessionToken,
          token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
        });
        toast("▶️ " + sarki);
      };
      kap.appendChild(div);
    });
  }).catch(() => {
    const msg = document.createElement("div");
    msg.className = "sarki-item";
    msg.style.color = "#e74c3c";
    msg.textContent = "Liste yüklenemedi.";
    kap.innerHTML = "";
    kap.appendChild(msg);
  });
}
