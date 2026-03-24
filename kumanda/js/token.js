/**
 * token.js - Crypto-secure token yönetimi
 */

// ================================================================
//  OTURUM DEĞİŞKENLERİ
// ================================================================
let girisYapildi = false;
let yoneticiGirildi = false;
let sessionToken = null;
let tokenExpiry = null;
let tokenRefreshTimer = null;

// ================================================================
//  SECURE TOKEN GENERATION
// ================================================================
async function generateSecureToken() {
  const randomBytes = new Uint8Array(CONFIG.TOKEN_LENGTH);
  crypto.getRandomValues(randomBytes);
  return Array.from(randomBytes)
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");
}

// ================================================================
//  TOKEN CREATION & REFRESH
// ================================================================
async function createNewToken() {
  try {
    const token = await generateSecureToken();
    const now = Date.now();
    tokenExpiry = now + CONFIG.TOKEN_EXPIRY_MS;
    sessionToken = token;
    
    // Token'ı Firebase'e yaz
    await db.ref("kumanda/token").set({
      value: token,
      created: now,
      expires: tokenExpiry,
      user_agent: navigator.userAgent.substring(0, 200)
    });
    
    // Token yenileme zamanı (son 5 dakikada)
    const refreshTime = CONFIG.TOKEN_EXPIRY_MS - (5 * 60 * 1000);
    clearTimeout(tokenRefreshTimer);
    tokenRefreshTimer = setTimeout(() => {
      if (girisYapildi) {
        createNewToken().catch(e => {
          if (CONFIG.DEBUG) console.error("Token yenileme hatası:", e);
        });
      }
    }, refreshTime);
    
    return token;
  } catch (e) {
    throw new Error("Token üretim hatası: " + e.message);
  }
}

// ================================================================
//  TOKEN VALIDATION
// ================================================================
function isTokenValid() {
  if (!sessionToken || !tokenExpiry) return false;
  return Date.now() < tokenExpiry;
}

// ================================================================
//  TOKEN ATTACHMENT TO COMMANDS
// ================================================================
function attachTokenToCommand(command) {
  if (!isTokenValid()) {
    toast("⚠️ Oturum süresi doldu. Lütfen tekrar giriş yapın.");
    cikisYap();
    return null;
  }
  return {
    ...command,
    token: sessionToken,
    token_created: tokenExpiry - CONFIG.TOKEN_EXPIRY_MS
  };
}

/**
 * Token temizleme (logout sırasında)
 */
function clearToken() {
  sessionToken = null;
  tokenExpiry = null;
  clearTimeout(tokenRefreshTimer);
  
  // Firebase'deki token'ı sil
  db.ref("kumanda/token").remove().catch(e => {
    if (CONFIG.DEBUG) console.error("Token silme hatası:", e);
  });
}
