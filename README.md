# Kararsızım

Türkiye odaklı, Türkçe arayüzlü halka açık anket ve karar verme uygulaması. Faz 1–3 tamamlanmıştır: hesaplar, anket oluşturma, kamusal akış ve hem misafir hem üyelikli oylama çalışır.

## Gereksinimler

- Python 3.12
- Supabase PostgreSQL projesi (normal yerel çalışma için)
- Testler için açıkça seçilen `TEST_SQLITE=1` modu

## Yerel kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` içinde güçlü ve benzersiz `DJANGO_SECRET_KEY` ile gerçek bağlantı bilgilerini girin. `DATABASE_URL` içindeki kullanıcı adı/parolada bulunan `@`, `:`, `/`, `#` gibi özel karakterler URL-encode edilmelidir.

Supabase Dashboard → Connect ekranından adresleri birebir kopyalayın:

- Yerel geliştirme ve kontrollü migration için session pooler veya erişilebiliyorsa direct connection.
- Vercel serverless çalışma zamanı için transaction pooler. Transaction pooler ayarları projede prepared statement ve server-side cursor kullanımını kapatır; `CONN_MAX_AGE=0` kullanılır.

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin paneli `http://127.0.0.1:8000/admin/` adresindedir. Yalnızca staff/superuser hesapları erişebilir.

### Yerel demo verisi

Önizlemede farklı kullanıcıların anketlerini ve oy sayılarını görmek için `.env` içinde `TEST_SQLITE=1` kullanarak çalıştırın:

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

`seed_demo` yalnızca SQLite veritabanında çalışır; Supabase/PostgreSQL üzerinde örnek veri oluşturmayı güvenlik nedeniyle reddeder. Komut tekrar çalıştırılabilir ve aynı demo anketlerini çoğaltmaz. Demo kullanıcılarının kullanılabilir parolası yoktur; yalnızca kamusal akışın gerçekçi görünmesi içindir.

## Testler

Supabase bilgisi gerektirmeyen izole testler yalnızca açık SQLite seçimiyle çalıştırılır:

```powershell
$env:DJANGO_SECRET_KEY='test-only-secret-key-not-for-production'
$env:DJANGO_DEBUG='True'
$env:DJANGO_ALLOWED_HOSTS='testserver,localhost,127.0.0.1'
$env:TEST_SQLITE='1'
python manage.py test
python manage.py check
```

`DATABASE_URL` yokken ve `TEST_SQLITE=1` değilken uygulama bilinçli olarak başlamaz. Bu davranış üretimde yanlışlıkla yerel SQLite kullanılmasını engeller. SQLite testleri PostgreSQL'e özgü constraint ve eşzamanlılık davranışlarının kanıtı değildir; gerçek Supabase bağlantısı ayrıca doğrulanmalıdır.

## Mevcut özellikler

- Giriş yapan kullanıcılar 2–5 seçenekli anket oluşturabilir.
- Ana akış herkese açıktır ve anketleri 12 kayıtlık sayfalara böler.
- Anket detayları herkese açıktır; yayından kaldırılan anketler kamusal yüzeylerde görünmez.
- Anketlerim sayfası yalnızca giriş yapan kişinin kendi anketlerini gösterir.
- Misafirler ve üyeler tek seçenekle oy verebilir; sonuçlar yalnızca oy veren kimliğe gösterilir.
- Vercel deploy henüz yapılmadı.

## Anonim oylamanın sınırları

Misafir kimliği rastgele UUID olarak üretilir ve Django tarafından imzalanmış `kararsizim_guest` cookie'sinde saklanır. Cookie `HttpOnly`, `SameSite=Lax` ve üretim HTTPS ortamında `Secure` olarak yazılır. IP adresi, e-posta veya cihaz fingerprint'i kullanılmaz.

Bu koruma “aynı tarayıcıdaki aynı misafir kimliği, aynı ankette bir oy” sağlar. Cookie silinirse, gizli mod kullanılırsa veya başka cihaz/tarayıcıya geçilirse kişi yeniden oy verebilir. Misafir oyu daha sonra açılan hesaba birleştirilmez; misafir oyundan sonra giriş yapan kişi üyelik kimliğiyle tekrar oy verebilir. Bu davranış MVP'nin bilinen sınırıdır.

Veritabanı constraint'leri kayıtlı kullanıcı ve mevcut misafir kimliği için paralel çift oyu engeller. Aynı tarayıcının cookie almadan doğrudan birden fazla paralel ham POST göndermesi farklı misafir kimlikleri oluşturabilir; normal arayüz akışı detay GET isteğinde kimliği önceden cookie'ye yazar. Kamusal yayın öncesinde bu sınır, paylaşımlı rate limit/abuse korumasıyla ayrıca ele alınmalıdır.
