/**
 * utils.js - Yardımcı fonksiyonlar (sha256, toast, debounce, etc.)
 */

// ================================================================
//  DEBOUNCE & THROTTLE UTILITIES
// ================================================================
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

const throttle = (func, limit) => {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// ================================================================
//  LOADING INDICATOR
// ================================================================
let isLoading = false;

function setLoading(show) {
  isLoading = show;
  const buttons = document.querySelectorAll("button[onclick*='Yap'], button[onclick*='Gonder'], button[onclick*='Degistir']");
  buttons.forEach(btn => {
    btn.style.opacity = show ? "0.6" : "1";
    btn.disabled = show;
  });
}

// ================================================================
//  SHA-256 HASHING (Password güvenliği için)
// ================================================================
async function sha256(metin) {
  try {
    const buf = await crypto.subtle.digest("SHA-256",
      new TextEncoder().encode(metin));
    return Array.from(new Uint8Array(buf))
      .map(b => b.toString(16).padStart(2, "0")).join("");
  } catch (e) {
    if (CONFIG.DEBUG) console.error("SHA256 hash hatası:", e);
    throw new Error("Şifre hashleme başarısız");
  }
}

// ================================================================
//  RATE LIMITING (Brute force koruması)
// ================================================================
const rateLimitMap = {};

function checkRateLimit(key, maxAttempts = CONFIG.RATE_LIMIT_ATTEMPTS, windowMs = CONFIG.RATE_LIMIT_WINDOW) {
  const now = Date.now();
  if (!rateLimitMap[key]) rateLimitMap[key] = [];
  
  // Eski deneme'leri temizle
  rateLimitMap[key] = rateLimitMap[key].filter(time => now - time < windowMs);
  
  if (rateLimitMap[key].length >= maxAttempts) {
    return {
      allowed: false,
      resetTime: Math.ceil((rateLimitMap[key][0] + windowMs - now) / 1000)
    };
  }
  
  rateLimitMap[key].push(now);
  return { allowed: true };
}

// ================================================================
//  FIREBASE TIMEOUT WRAPPER
// ================================================================
function withTimeout(promise, timeoutMs = CONFIG.FIREBASE_TIMEOUT) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("İşlem zaman aşımı (timeout)")), timeoutMs)
    )
  ]);
}

// ================================================================
//  TOAST BİLDİRİM
// ================================================================
function toast(mesaj) {
  if (!DOM_CACHE.toast) DOM_CACHE.toast = document.getElementById("toast");
  const el = DOM_CACHE.toast;
  if (!el) return;
  el.textContent = mesaj;
  el.className = "show";
  setTimeout(() => el.className = "", CONFIG.TOAST_DURATION);
}
