Bu paket, yüklenen project_dump.txt içeriğinden yeniden oluşturuldu.

Yapılan başlıca düzenlemeler:
- Eski hardcoded Firebase API key kaldırıldı.
- Firebase yapılandırması tek noktadan `.env` üzerinden okunacak hale getirildi.
- Tekrarlayan `sifre_hashle` işlevi ortak modüle taşındı.
- Tekrarlayan `.env` okuma mantığı ortak modüle taşındı.
- `.env.example` ve `.gitignore` eklendi.

Kurulum:
1. `.env.example` dosyasını kopyalayıp `.env` yapın.
2. Firebase bilgilerinizi `.env` içine yazın.
3. Uygulamayı çalıştırın.
