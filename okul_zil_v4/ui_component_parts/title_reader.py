from .shared import *

def _okul_basligini_oku():
    """
    ayarlar.json'dan 'ana_baslik' alanını okur.
    İki satırlık gösterim için ' - ' veya '\\n' ile ayrılmış metni böler.
    Döndürür: (satir1, satir2)
    """
    try:
        if os.path.exists(AYARLAR_DOSYASI):
            with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as f:
                ayarlar = json.load(f)
            baslik = ayarlar.get("ana_baslik", "")
            if baslik:
                # '\n' ile ayrılmış ise böl
                if "\n" in baslik:
                    parcalar = baslik.split("\n", 1)
                    return parcalar[0].strip(), parcalar[1].strip()
                # ' - ' ile ayrılmış ise böl
                if " - " in baslik:
                    parcalar = baslik.split(" - ", 1)
                    return parcalar[0].strip(), parcalar[1].strip()
                return baslik.strip(), ""
    except Exception:
        pass
    # Varsayılan fallback
    return "Okul Zil Sistemi", "Profesyonel Zil Otomasyonu"
