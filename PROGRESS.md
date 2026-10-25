# Kararsızım ilerleme durumu

## Faz 1 — Proje iskeleti, altyapı ve kullanıcı hesapları

Durum: Tamamlandı (gerçek Supabase bağlantısı hariç).

### Tamamlananlar

- Django proje iskeleti ile `accounts` ve `polls` uygulamaları oluşturuldu.
- `AUTH_USER_MODEL = "accounts.User"` ilk migration öncesinde ayarlandı.
- Kullanıcı adı ve e-posta için form ve veritabanı düzeyinde büyük/küçük harf duyarsız benzersizlik kuruldu.
- Kayıt, kullanıcı adı/parola ile giriş ve yalnızca POST ile çıkış akışları eklendi.
- Türkçe, responsive temel sayfa kabuğu; header, mesajlar, formlar ve boş ana sayfa oluşturuldu.
- Supabase PostgreSQL bağlantısı `DATABASE_URL` ile; transaction pooler uyumlu temel seçeneklerle hazırlandı.
- Ortam değişkeni yokken sessiz SQLite geri dönüşü engellendi; yalnızca `TEST_SQLITE=1` test modu tanımlandı.
- Admin paneli ve özel kullanıcı yönetimi eklendi.
- Kurulum, migration, süper kullanıcı ve test adımları README'de belgelendi.
- İlk kullanıcı migration'ı oluşturuldu; Django sistem kontrolü ve 8 otomatik test geçti.
- `runserver` işleminin başlatıldığı doğrulandı; ana sayfa ayrıca Django test istemcisiyle HTTP 200 verdi.

### Açık işler ve doğrulanacaklar

- Gerçek Supabase kimlik bilgileri bulunmadığından PostgreSQL bağlantısı ve migration'lar doğrulanmadı.
- Mevcut makinede Python 3.11.9 kullanıldı. Projenin hedefi Python 3.12 olduğundan yerel/üretim doğrulaması Python 3.12 ile tekrarlanmalı.
- Sandbox yerel HTTP soketine erişimi engellediği için çalışan geliştirme sunucusuna dışarıdan `Invoke-WebRequest` smoke isteği gönderilemedi; aynı ana sayfa davranışı test istemcisiyle doğrulandı.

### Alınan kararlar

- Gizli değerler repoya eklenmedi; `.env` Git dışında tutuldu.
- Ana sayfa Faz 1'de yalnızca boş durum gösterir; anket modelleri ve iş akışları eklenmedi.
- E-posta yalnızca kayıt alanıdır; kamusal header veya ana sayfada gösterilmez.

### Çalıştırılan kontroller

- `TEST_SQLITE=1 python manage.py check`: sorun yok.
- `TEST_SQLITE=1 python manage.py makemigrations --check --dry-run`: bekleyen model değişikliği yok.
- `TEST_SQLITE=1 python manage.py test --verbosity 2`: 8 testin tamamı geçti.
- `TEST_SQLITE=1 python manage.py migrate --noinput`: tüm Faz 1 migration'ları uygulandı.
- Sahte bir PostgreSQL URL'siyle bağlantı kurulmadan settings denetimi: PostgreSQL engine, `CONN_MAX_AGE=0`, `prepare_threshold=None`, server-side cursor kapalı ve güvenli production session cookie ayarı doğrulandı.

### Faz 1 kabul kriterleri

- Django uygulaması ve geliştirme sunucusu başlıyor.
- Kayıt olan kullanıcı otomatik giriş yapıyor; giriş oturumu sonraki istekte korunuyor.
- Çıkış endpoint'i GET isteğini reddediyor ve POST isteğiyle oturumu kapatıyor.
- Kullanıcı adı ve e-posta farklı harf büyüklükleriyle tekrar kaydedilemiyor.
- E-posta kamusal ana sayfa/header çıktısında yer almıyor.
- Admin paneli staff olmayan kullanıcıyı kabul etmiyor.
- Veritabanı ayarı yalnızca açık `TEST_SQLITE=1` seçiminde SQLite kullanıyor; aksi halde `DATABASE_URL` zorunlu.

### Sonraki fazın giriş noktası

Faz 2 tamamlandı. Ayrıntılar aşağıdadır.

## Faz 2 — Anket oluşturma, akış ve detay

Durum: Tamamlandı (gerçek Supabase doğrulaması hariç).

### Tamamlananlar

- UUID kimlikli `Poll` ve sıralı `PollOption` modelleri ile ilk migration oluşturuldu.
- Anket sorusu 12–180, açıklama en fazla 500 ve seçenek metni 2–80 karakter olarak sunucuda doğrulanıyor.
- Seçenek sayısı sunucuda 2–5 ile sınırlandı; boş veya Unicode/case normalize edilmiş tekrar seçenekler reddediliyor.
- Anket ve seçenekler tek `transaction.atomic()` işlemi içinde kaydediliyor.
- Anket oluşturma yalnızca giriş yapan kullanıcılara açıldı; başarısız formda güvenli girdiler korunuyor.
- Vanilla JavaScript ile başlangıçta 2 satır, en fazla 5 seçenek ve 2'nin altına düşmeyen ekleme/kaldırma arayüzü eklendi.
- Herkese açık ana akış, 12 kayıtlık sayfalama, kamusal anket detayı ve kullanıcıya özel Anketlerim sayfası eklendi.
- Akış sorgularında yazar `select_related`, seçenekler `prefetch_related` ile yükleniyor.
- Yayından kaldırılmış anketler kamusal akışta görünmüyor ve detay adresi 404 döndürüyor.
- Admin paneline anket, seçenek inline düzenlemesi ve `is_published` moderasyon alanı eklendi.
- Kamusal şablonlarda yalnızca `@username` gösteriliyor; e-posta bulunmuyor ve kullanıcı metinleri auto-escape ediliyor.

### Çalıştırılan kontroller

- `TEST_SQLITE=1 python manage.py makemigrations polls`: `polls/0001_initial.py` oluşturuldu.
- `TEST_SQLITE=1 python manage.py check`: sorun yok.
- `TEST_SQLITE=1 python manage.py makemigrations --check --dry-run`: bekleyen model değişikliği yok.
- `TEST_SQLITE=1 python manage.py test --verbosity 1`: 20 testin tamamı geçti.

### Açık işler ve doğrulanamayanlar

- Gerçek Supabase bilgileri bulunmadığından PostgreSQL migration'ı ve PostgreSQL constraint davranışı doğrulanmadı.
- Testler açıkça `TEST_SQLITE=1` ile çalıştırıldı; SQLite PostgreSQL davranışının eksiksiz kanıtı değildir.
- Mevcut makine Python 3.11.9 kullanıyor; hedef Python 3.12 ile yerel doğrulama tekrarlanmalı.
- Oy sayısı Faz 3'e kadar kartlarda 0 gösterilir; `Vote` modeli ve oylama eklenmedi.

### Faz 2 kabul kriterleri

- Üye 2 veya 5 seçenekli anket yayınlayabiliyor.
- Misafir kullanıcı yayınlanmış anketleri ana akış ve detay sayfasında görebiliyor.
- 1/6 seçenek, boş seçenek ve normalize edilmiş tekrar seçenek içeren POST istekleri reddediliyor.
- Anketlerim yalnızca oturum sahibinin kayıtlarını listeliyor.
- Faz 3 kapsamındaki oy sistemi eklenmedi.

### Sonraki fazın giriş noktası

Faz 3 tamamlandı. Ayrıntılar aşağıdadır.

## Faz 3 — Anonim ve üyelikli oylama, sonuçlar

Durum: Tamamlandı (gerçek PostgreSQL eşzamanlılık doğrulaması hariç).

### Tamamlananlar

- `Vote` modeli; kullanıcı/misafir kimliğinden tam olarak biri dolu CHECK constraint'i ile eklendi.
- `(poll, user)` ve `(poll, guest_id)` için koşullu unique constraint'ler oluşturuldu.
- Seçeneğin ilgili ankete ait olduğu oylama view'ında doğrulanıyor; model doğrulaması da doğrudan/admin yazımları için aynı kuralı kontrol ediyor.
- Misafir UUID'si Django signing ile imzalanıyor; `HttpOnly`, `SameSite=Lax`, bir yıllık ve üretimde `Secure` cookie olarak saklanıyor.
- Misafir kimliği normal akışta detay GET isteğinde hazırlanıyor; bozuk veya süresi geçmiş imza güvenli biçimde yenileniyor.
- Oy endpoint'i herkese açık, yalnızca POST kabul ediyor ve Django CSRF korumasını kullanıyor.
- Oy kaydı atomic transaction içinde yapılıyor; unique constraint kaynaklı `IntegrityError` dostça tekrar-oy mesajına çevriliyor.
- Oy sonrası POST-Redirect-GET uygulanıyor; yenileme yeni POST göndermiyor.
- Oy veren kimlik sonuçları sayı, yüzde, bar ve seçilen seçenek vurgusuyla görüyor; oy vermeyen kişi yüzdeleri görmüyor.
- Ana akış ve Anketlerim kartlarındaki toplam oy sayıları gerçek aggregation ile hesaplanıyor.
- Misafir oyunun hesaba birleştirilmediği ve cookie/cihaz sınırları README'de belgelendi.

### Çalıştırılan kontroller

- `TEST_SQLITE=1 python manage.py makemigrations polls`: `polls/0002_vote.py` oluşturuldu.
- `TEST_SQLITE=1 python manage.py check`: sorun yok.
- `TEST_SQLITE=1 python manage.py makemigrations --check --dry-run`: bekleyen model değişikliği yok.
- `TEST_SQLITE=1 python manage.py test --verbosity 1`: 38 testin tamamı geçti.

### Kapsanan senaryolar

- Misafir ve üyelikli oy, aynı kimlikle ikinci oy, POST-only endpoint ve CSRF reddi.
- Başka ankete ait seçenek, seçim yapılmaması ve yayından kaldırılan ankete oy.
- İmzalı cookie'nin yazılması/okunması ve bozuk cookie'nin güvenli yenilenmesi.
- Tam olarak bir kimlik CHECK constraint'i ve iki koşullu unique constraint.
- `IntegrityError` yarış yolu, 0/1/farklı oy dağılımları ve yüzde hesabı.
- Oy öncesi sonuç gizliliği, kartta toplam sayı ve anonimden üyeliğe geçişte kimlik birleştirilmemesi.

### Gerçek PostgreSQL üzerinde ayrıca doğrulanacaklar

- Koşullu unique ve CHECK constraint'lerin Supabase PostgreSQL migration'ı.
- Aynı mevcut `user_id` veya `guest_id` ile iki gerçek eşzamanlı transaction'ın yalnızca bir Vote oluşturması.
- Transaction pooler altında `IntegrityError` yakalama ve bağlantının sonraki isteklerde sağlıklı kalması.
- SQLite testleri eşzamanlılık kilit davranışını veya PostgreSQL isolation ayrıntılarını kanıtlamaz.
- Cookie almadan doğrudan paralel ham POST gönderen misafir istekleri farklı UUID oluşturabilir; normal UI detay GET'inde cookie önceden atanır. Kamusal yayın öncesi paylaşımlı abuse/rate-limit koruması ayrıca gereklidir.

### Faz 3 kabul kriterleri

- Giriş yapmamış ziyaretçi kayıt olmadan oy verebiliyor.
- Aynı imzalı misafir kimliği veya aynı kullanıcı aynı ankette ikinci oy oluşturamıyor.
- Oy veren kişi doğru toplam, seçenek sayıları ve yüzdeleri görüyor.
- DB constraint yarış hatası kullanıcı dostu sonuçlanıyor.
- Oylama için `login_required` kullanılmıyor.

### Sonraki fazın giriş noktası

Kullanıcı onayıyla Faz 4'te mevcut çalışan akışlar korunarak responsive görsel kalite ve erişilebilirlik iyileştirilebilir. Faz 4 henüz başlatılmadı.

## Yerel önizleme notu

- `.env` yerel önizleme için açıkça `TEST_SQLITE=1` moduna alındı; tanımlı Supabase bağlantısına demo veri yazılmadı.
- Yalnızca SQLite üzerinde çalışmayı kabul eden, tekrar çalıştırılabilir `python manage.py seed_demo` komutu eklendi.
- 6 farklı demo yazarına ait 6 yayınlanmış anket ve toplam 35 örnek oy oluşturuldu.
- Demo komutu iki kez çalıştırılarak kayıtları çoğaltmadığı kontrol edildi.
- Faz 1–3 regresyon testleri tekrar çalıştırıldı: 38 testin tamamı geçti.
- Geliştirme sunucusu `http://127.0.0.1:8000/` adresinde başlatıldı ve Codex önizleme sekmesi istendi.
