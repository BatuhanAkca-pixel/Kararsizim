# Kararsızım — Codex Proje Rehberi (`AGENTS.md`)

> **Belgenin amacı:** Bu dosya, Codex'in **Kararsızım** web uygulamasını doğru kapsamda, tutarlı mimariyle ve **faz faz** geliştirmesi için tek referanstır.
>
> **Son güncelleme:** 25 Ekim 2026  
> **Proje türü:** Türkiye odaklı, Türkçe arayüzlü, halka açık anket / karar verme platformu  
> **Öncelik:** Önce çalışır, test edilebilir bir MVP; ardından iyileştirmeler.

---

## 1. Codex için bağlayıcı çalışma kuralları

1. **Yalnızca kullanıcı tarafından açıkça istenen fazı uygula.** Bu dosyadaki tüm fazları tek komutla tamamlamaya çalışma. Kullanıcı sadece `Faz 1'i uygula` derse Faz 2–5'i yazma.
2. Başlamadan önce repoyu incele. Var olan dosyaları koru; önemli değişiklikleri kısa gerekçeyle açıkla.
3. Çalışan basit çözümü tercih et. Gereksiz soyutlama, servis, paket, mimari katman ve frontend framework'ü ekleme.
4. **Tüm backend ve frontend aynı repoda** bulunacak. Django templates + sade HTML/CSS/JavaScript kullanılacak.
5. Kritik kurallar yalnızca tarayıcıdaki JavaScript ile değil, **Django tarafında** da doğrulanacak.
6. Kimlik doğrulama için **Django'nun yerleşik session/auth sistemi** kullanılacak. Supabase yalnızca yönetilen PostgreSQL veritabanı olarak kullanılacak; Supabase Auth kullanılmayacak.
7. Gizli değerleri `.env`, Vercel environment variables gibi ortamlarda tut; `.env` dosyasını veya şifreleri git'e ekleme. `.env.example` oluştur.
8. Tüm kullanıcıya gösterilen metinler **Türkçe** olsun; kod isimleri ve teknik dokümantasyon İngilizce olabilir. Değişken, sınıf, dosya isimleri tutarlı olsun.
9. Her faz bitiminde testleri çalıştır; çalıştıramadığın test veya harici servis bağlantısı varsa bunu dürüstçe belirt.
10. Her faz sonunda `PROGRESS.md` dosyasında tamamlananları, açık işleri, alınan kararları ve bir sonraki fazın giriş noktasını güncelle.
11. Otomatik olarak dış servislerde hesap açma, ücretli plan başlatma veya canlı veritabanında geri alınamaz işlem yapma.
12. Belirsiz küçük ürün ayrıntılarında bu belgedeki **MVP varsayımlarını** kullan. Yalnızca gerçek bir engel varsa soru sor.
13. Kullanıcının belirttiği teknoloji seçimlerini izinsiz değiştirme; React, Vue, Next.js, DRF, Celery, Redis, Docker, mikroservis veya TypeScript ekleme.
14. **En önemli kontrol:** Anonim kullanıcı hem anket görebilmeli hem oy verebilmeli; **sadece anket oluşturma** giriş gerektirmeli.

## 2. Ürün özeti

**İsim:** Kararsızım  
**Kısa önerme:** “Karar veremiyor musun? Sor, herkes oylasın!”  
**Temel sorun:** İnsanlar iki veya daha fazla seçenek arasında kalıyor; topluluğun hızlı fikrini almak istiyor.  
**Temel çözüm:** Kullanıcı bir soru ve 2–5 seçenekten oluşan anket yayınlar. Diğer kullanıcılar ve ziyaretçiler seçeneklerden birini seçerek oy verir; sonuçlar anlaşılır biçimde görüntülenir.

**Örnek anket:**

- Soru: “Bugün sinemaya mı gitsem, restorana mı gitsem?”
- Seçenek 1: “Sinemaya git 🍿”
- Seçenek 2: “Restorana git 🍝”

**Çekirdek vaat:** Hesap açmadan fikrini belirt; kendi kararsızlığını paylaşmak için kayıt ol.

### 2.1 Hedef kullanıcı

- Özellikle genç kullanıcılar ve sosyal medya alışkanlığı olan kişiler.
- Gündelik kararlarını çevresine danışmak isteyenler.
- Fazla uğraşmadan oy vermek isteyen misafir ziyaretçiler.

### 2.2 Ürünün değişmez kuralları

- **Takip / takipçi sistemi kesinlikle yok.**
- İçerikler yalnızca takip edilen kişilere gösterilmez; **yayındaki tüm anketler herkese açıktır**.
- **Üye olmayan ziyaretçi:** anket listesini ve detayını görür, oy verir, kendi oy verdiği anketin sonuçlarını görür.
- **Üye olan kullanıcı:** misafirin tüm yetkilerine ek olarak anket oluşturur; kendi anketlerini listeleyebilir.
- Anket başına **en az 2, en çok 5 seçenek**.
- Her anketin **tam olarak bir** sorusu vardır. Oy kullanırken **tek bir** seçenek işaretlenir.
- Anket kartında yazara ait **kullanıcı adı** gösterilir; e-posta hiçbir kamusal ekranda veya kamusal HTML/JSON çıktısında görünmez.
- Kayıt ekranında **kullanıcı adı, e-posta, parola, parola tekrarı** istenir.
- Kullanıcı adı ve e-posta birbirinden bağımsız alanlardır; giriş için ilk sürümde **kullanıcı adı + parola** kullanılır.
- Varsayılan akışta tüm ziyaretçiler en yeni yayınlanan anketleri görür.

## 3. MVP kapsamı ve bilinçli sınırlar

### 3.1 MVP'de yapılacaklar

- Mobil uyumlu ana akış (anket kartları, yeni anketler önce, sayfalama).
- Anket detay sayfası.
- Kayıt olma, giriş yapma, çıkış yapma.
- Oturum açmış kullanıcının anket oluşturması.
- Dinamik olarak 2–5 seçenek ekleme / kaldırma.
- Anonim ve oturum açmış kullanıcı için tek seçenekle oy verme.
- Aynı kimlikle aynı ankete tekrar oy verilmesini önleme.
- Oy kullandıktan sonra yüzde / sayı bazlı sonuç ekranı.
- Kullanıcıların kendi oluşturduğu anketleri göreceği “Anketlerim” sayfası.
- Temel Django Admin üzerinden yönetim / uygunsuz anketi yayından kaldırma.
- Hata, boş durum, yükleniyor ve başarılı işlem geri bildirimleri.
- Otomatik testler, yerel geliştirme dokümantasyonu, Vercel'e yayınlama hazırlığı.

### 3.2 İlk MVP'ye dahil edilmeyecekler

- Takip etmek, arkadaş eklemek, özel akış, mesajlaşma.
- Yorumlar, beğeniler, bildirimler, etiketleme.
- Fotoğraf/video yükleme ve kullanıcı avatarı yükleme.
- Google ile giriş, Supabase Auth, e-posta ile aktivasyon, şifremi unuttum e-posta akışı.
- Yapay zekâ önerileri, öneri motoru, kişiselleştirilmiş algoritmik akış.
- Gerçek zamanlı WebSocket güncellemeleri, push, Redis, kuyruk, mikroservis.
- Anket değiştirme/silme (moderatör müdahalesi dışında), anket süresi/otomatik kapanma, çoklu oy seçimi.
- Gelişmiş spam tespiti, kapsamlı içerik moderasyonu paneli veya gelişmiş arama.

**MVP kararı:** Anketler ilk sürümde süresiz açık kalır. Moderatör gerektiğinde `is_published=False` yaparak yayından kaldırabilir. Bu işlem bir takip mekanizması veya kişiselleştirme oluşturmaz.

### 3.3 Başarı ölçütleri (prototip)

1. Misafir ziyaretçi ana sayfada yayınlanan anketleri görüp oy verebiliyor.
2. Aynı tarayıcıdaki aynı misafir kimliği aynı ankette yeniden oy veremiyor.
3. Üye kişi giriş yapıp 2–5 seçenekli anket yayınlayabiliyor.
4. Başka bir kullanıcı veya misafir yeni anketi görebiliyor.
5. Kayıtlı oylar Supabase PostgreSQL'de kalıcı olarak saklanıyor.
6. Oy sonuçlarının toplamı ve yüzdeleri doğru; toplam oy sayısı seçenek oylarının toplamına eşit.
7. Tüm temel akışlar hem masaüstü hem mobil genişlikte kullanılabiliyor.
8. Üretim ortamı gizli ayarları güvenli; üye e-postaları kamusal yüzeylerden sızmıyor.

---

## 4. Teknik mimari

### 4.1 Teknolojiler

| Katman | Tercih | Not |
| --- | --- | --- |
| Backend | Python **3.12** + **Django 5.2 LTS** | Başlangıç için uzun süre desteklenen seri; güncel güvenlik yaması |
| Frontend | Django Templates, HTML5, CSS3, vanilla JavaScript | Ayrı frontend projesi yok |
| Veritabanı | Supabase **PostgreSQL** | Django ORM üzerinden erişim |
| Kimlik | Django Authentication + sessions | Kendi kullanıcı tablomuz, parola hash'leme Django'da |
| Veritabanı sürücüsü | `psycopg` 3 | PostgreSQL bağlantısı |
| Bağlantı dizesi | `dj-database-url` | `DATABASE_URL` okumak için küçük yardımcı |
| Yayınlama | Vercel | Django otomatik algılama, Python runtime |
| Statik dosyalar | Django `staticfiles` + Vercel CDN | Kullanıcı dosya yüklemesi yok |
| Test | Django `TestCase` / `TransactionTestCase` | Gerektiği kadar test, ekstra test çerçevesi şart değil |
| Sürüm kontrolü | Git | Tek repo |

**Teknik ilkeler:** Server-side rendering, Django forms, ORM, session bazlı yetkilendirme. Gereksiz JSON API veya SPA oluşturma. Kullanıcı deneyimi gerektiren alanları küçük vanilla JS betikleriyle iyileştir.

### 4.2 İstek ve veri akışı

```text
Tarayıcı
  ├─ GET /                          → Django view → template → anket akışı
  ├─ GET /anket/<uuid>/             → Django view → template → anket detay
  ├─ POST /anket/<uuid>/oy-ver/     → Django CSRF + doğrulama → PostgreSQL'e oy
  ├─ GET/POST /kayit-ol/            → Django form / kullanıcı oluşturma
  ├─ GET/POST /giris-yap/           → Django auth session
  └─ GET/POST /anket/olustur/      → login required → poll + seçenekler

Django ORM ↔ Supabase PostgreSQL
Django templates + CSS/JS → Vercel üzerinde aynı uygulama/repo
```

**Önemli:** Tarayıcı doğrudan Supabase PostgreSQL'e bağlanmaz. Supabase bağlantı dizesi veya hassas anahtarlar frontend'e aktarılmaz. Supabase'in anonim/public API anahtarına MVP'de ihtiyaç yoktur.

### 4.3 Önerilen repo yapısı

```text
kararsizim/
├── AGENTS.md
├── PROGRESS.md
├── README.md
├── .gitignore
├── .env.example
├── .python-version              # ör. 3.12
├── requirements.txt
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── tests.py
├── polls/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py              # yalnızca oy mantığı yeterince büyürse
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── tests.py
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── poll_card.html
│   │   └── messages.html
│   ├── accounts/
│   │   ├── register.html
│   │   └── login.html
│   └── polls/
│       ├── feed.html
│       ├── detail.html
│       ├── create.html
│       └── mine.html
└── static/
    ├── css/styles.css
    └── js/
        ├── app.js
        ├── poll-form.js
        └── voting.js
```

**Not:** Sırf ağaçta yazıyor diye içi boş dosyalar yaratma. İlgili fazda gerçekten ihtiyaç duyulanları oluştur. `staticfiles/`, `.venv/`, `.env`, `__pycache__/`, `*.sqlite3` git dışı kalmalıdır.

---

## 5. Veri modeli (önerilen başlangıç tasarımı)

### 5.1 `accounts.User`

Django'nun `AbstractUser` sınıfını **başlangıçtan itibaren** genişleten özel model kullan. `AUTH_USER_MODEL = 'accounts.User'` ayarını **ilk migration öncesi** yap. Bu değişimi sonraya bırakmak migration'ları gereksiz zorlaştırır.

| Alan | Tür | Kural |
| --- | --- | --- |
| `id` | Django standart PK | Kullanıcı kimliği |
| `username` | `CharField` | Benzersiz, 3–24 karakter, baş/son boşluk temizlenir |
| `email` | `EmailField` | Zorunlu, benzersiz, normalleştirilmiş |
| `password` | Django parola hash'i | Düz metin olarak asla saklama |
| `date_joined` | Django standart | Kayıt tarihi |
| `is_active`, `is_staff` | Django standart | Yönetim |

- Kullanıcı adı ve e-posta için **büyük/küçük harf farkını yok sayan benzersizlik** hedefle: Django form doğrulamasının yanında PostgreSQL düzeyinde `Lower(...)` temelli unique constraint gibi uygun bir mekanizma kullan.
- E-postayı hem template'lerde hem yanıt nesnelerinde gizli tut; yalnızca hesap sahibinin kendi özel hesap ekranında gösterilebilir (MVP'de böyle bir ekran gerekmiyor).
- Parolalar için Django'nun varsayılan güçlü parola doğrulayıcılarını kullan.
- Başarısız kayıtta kullanıcının girdiği güvenli alanları koru; parolayı yeniden forma doldurma.

### 5.2 `polls.Poll`

| Alan | Tür | Kural |
| --- | --- | --- |
| `id` | `UUIDField` primary key | URL'de tahmin edilmesi zor kimlik |
| `author` | `ForeignKey(settings.AUTH_USER_MODEL)` | Zorunlu, üye kullanıcı |
| `question` | `CharField(max_length=180)` | Zorunlu, 12–180 karakter önerisi |
| `description` | `TextField(blank=True)` | İsteğe bağlı, max 500 karakter form doğrulaması |
| `created_at` | `DateTimeField(auto_now_add=True)` | Tarih |
| `is_published` | `BooleanField(default=True)` | Moderasyon; yayında olanlar herkese açık |

- Varsayılan sıralama `-created_at, -id`.
- Yayında olmayan bir anket normal ziyaretçide görüntülenmez / oylanmaz. Moderatör Django Admin'den inceleyebilir.
- İlk sürümde kapanış tarihi/puan algoritması yok.
- Oluşturma sırasında anket ve tüm seçenekler **tek veritabanı transaction'ı** içinde kaydedilmeli; yarım anket oluşmamalı.

### 5.3 `polls.PollOption`

| Alan | Tür | Kural |
| --- | --- | --- |
| `id` | `BigAutoField` | Seçenek kimliği |
| `poll` | `ForeignKey(Poll, related_name='options')` | Sahip anket |
| `text` | `CharField(max_length=80)` | Zorunlu, 2–80 karakter |
| `position` | `PositiveSmallIntegerField` | 1–5 arasında sıra |

- Bir ankette **2–5 seçenek** kuralını oluşturma formunda ve backend işleminde kesin uygula.
- Aynı anketin seçeneklerinde normalize edilmiş **aynı metin iki defa** yer alamaz (örn. `Sinema` ve ` sinema `).
- `(poll, position)` eşsiz olmalı.
- Sıralama `position` ile yapılmalı; oy verme seçeneği sıra numarası değil, gerçek `option_id` üzerinden doğrulanmalı.

### 5.4 `polls.Vote`

| Alan | Tür | Kural |
| --- | --- | --- |
| `id` | `BigAutoField` | Oy kimliği |
| `poll` | `ForeignKey(Poll)` | Oy verilen anket |
| `option` | `ForeignKey(PollOption)` | Oy verilen seçenek |
| `user` | `ForeignKey(User, null=True, blank=True)` | Giriş yapmış oy veren |
| `guest_id` | `UUIDField(null=True, blank=True)` | Üye olmayan tarayıcı kimliği |
| `created_at` | `DateTimeField(auto_now_add=True)` | Oy zamanı |

**Veritabanı bütünlüğü:**

- `user` ve `guest_id` alanlarından **tam olarak biri** dolu olmalı (CHECK constraint).
- Kayıtlı kullanıcılar için `(poll, user)` benzersiz olmalı (`user IS NOT NULL` koşullu unique constraint).
- Misafirler için `(poll, guest_id)` benzersiz olmalı (`guest_id IS NOT NULL` koşullu unique constraint).
- `option.poll_id == vote.poll_id` ilişkisini **her yazma işleminde** sunucu doğrulamalı; salt `option_id` ile rastgele oylamaya izin verme.
- Aynı ankette paralel iki POST yarıştığında constraint son savunma hattı olmalı; `IntegrityError` kullanıcı dostu “Bu ankette zaten oy kullandın.” mesajına çevrilmeli.
- Oy toplamlarını ilk sürümde `COUNT` / aggregation ile hesapla, ayrı sayaç tablosu veya manuel güncellenen sayaç kullanma.
- Silme/koruma (`on_delete`) kararlarını bütünlük ve moderasyon ihtiyacına göre tutarlı uygula; başka kullanıcının verisini etkileyen zincirleme silmeler yaratma.

---

## 6. Anonim oylama: çözüm ve sınırlar

Bu proje için **anonim oylama** zorunlu; fakat hesap açmayan bir insanı farklı cihazlar ve silinen çerezler arasında kusursuz tanımak mümkün değildir. Bu nedenle MVP hedefi **“aynı tarayıcı / misafir kimliği, aynı ankette bir oy”** olmalıdır. “Dünyada her insan kesinlikle bir kez oy verir” gibi yanlış bir güvenlik iddiası kullanma.

### 6.1 Misafir kimliği

1. Misafir ilk oyunu verdiğinde (veya kimlik gerektiren ilk aşamada) güvenli rastgele `UUID4` kimliği oluştur.
2. Kimliği Django `signing` ile imzalanmış, `HttpOnly`, `SameSite=Lax`, HTTPS üretimde `Secure=True` olan uzun ömürlü cookie'de sakla. Önerilen cookie adı `kararsizim_guest`.
3. Sonraki oy isteklerinde **imzayı doğrula**, süre dolması/bozulma halinde yeni kimlik üret.
4. Veritabanında misafir oyu `guest_id` ile eşleştir. E-posta, IP adresi veya cihaz fingerprint'i kullanarak izleme yapma.
5. Ziyaretçi cookie'yi silerse, gizli mod açarsa veya farklı cihaz kullanırsa yeniden oy verebilir: bu **bilinen MVP sınırıdır**.
6. Giriş yapmış kullanıcı oyunda `user_id` kullan; misafir oyunda `guest_id` kullan. Bu ilk sürümde misafir oyunu sonradan hesaba otomatik bağlama. Dolayısıyla misafir oyundan sonra hesapla giriş yapan kişi yeniden oy verebilir; ayrıca bir iyileştirme konusu olarak belgele.
7. Misafir oyunu verdikten sonra cookie'nin gerçekten response ile yazıldığını test et; sonucu görüntülemek için sonraki istekte aynı kimlik kullanılmalı.

### 6.2 Sunucudaki oy verme sırası

1. **Yalnızca `POST`** kabul et ve CSRF doğrulaması uygula.
2. Anketin var ve yayında olduğunu doğrula.
3. Gönderilen `option_id` değerinin **bu ankete ait** olduğunu doğrula.
4. Request kimliğinin kayıtlı kullanıcı mı yoksa misafir mi olduğunu belirle.
5. Aynı kimliğin bu ankette oyu olup olmadığını kontrol et.
6. Atomic veritabanı işlemi içinde oy ekle; benzersiz constraint ile yarış durumlarını yakala.
7. Başarılı oyda `303` benzeri güvenli yönlendirme/POST-Redirect-GET akışıyla detaya dön veya JS ile güncel sonuçları göster. Sayfa yenileme ikinci POST'a dönüşmemeli.
8. Yeni oyları okuyup `total_votes`, `count`, `percentage` hesapla. Sonuçları `0` toplam için sıfıra bölmeden göster.
9. Zaten oylamış kullanıcıya oy formunu yerine sonuçları göster; tekrar oy değiştirmek MVP'de yok.

**Sonuç gösterme kararı:** Kullanıcı (veya misafir) o ankette oy kullanmadan önce sonuç yüzdelerini görmez; **oy verdikten sonra** toplam oy ve seçenek yüzdelerini görür. Bu, kararsız kalanlara bir tercih yaptıran sade MVP davranışıdır.

**Boş ve sınır durumları:** İlk oy, 0 oy, 2 ve 5 seçenek, 100% tek seçenek, yanlış/başka ankete ait seçenek, çift POST, iki eş zamanlı POST, bozuk cookie, cookie kapalı tarayıcı, moderatörce kaldırılmış anket ve anonim → giriş geçişi kapsanmalı.

---

## 7. Sayfalar ve URL sözleşmesi

| URL | Metot | Erişim | Beklenen davranış |
| --- | --- | --- | --- |
| `/` | GET | Herkes | Yayındaki tüm anketlerden en yeniler, 12 kayıt/sayfa |
| `/anket/<uuid:poll_id>/` | GET | Herkes | Soru, seçenekler, kullanıcı adı, tarih ve duruma göre oy / sonuç |
| `/anket/<uuid:poll_id>/oy-ver/` | POST | Herkes | İlgili ankette tek seçenek için oy, CSRF gerekli |
| `/kayit-ol/` | GET/POST | Herkes | Kullanıcı adı + e-posta + parola + parola tekrarı |
| `/giris-yap/` | GET/POST | Herkes | Kullanıcı adı + parola ile giriş |
| `/cikis-yap/` | POST | Giriş yapan | Güvenli çıkış; GET ile logout yapma |
| `/anket/olustur/` | GET/POST | Giriş yapan | 2–5 seçenekli anket oluşturma |
| `/anketlerim/` | GET | Giriş yapan | Kişinin kendi açtığı anketler; sadece kendi kayıtları |
| `/admin/` | GET/POST | Yetkili admin | Django yönetim paneli |

**İstenmeyen yönlendirme davranışından kaçın:** Misafir anket detayına girip oy verebildiği için `oy-ver` endpoint'ine `login_required` koyma. Sadece `olustur` ve `anketlerim` giriş gerektirir. Giriş gerektiren sayfaya misafir giderse giriş sayfasına yönlendir; başarılı girişten sonra güvenli `next` hedefine dön. Açık yönlendirme açığı oluşturma.

### 7.1 Ana sayfa

- Net hero: **“Kararsız mı kaldın?”** / “Sorunu paylaş, topluluk karar versin.”
- Birincil CTA: **“Anket oluştur”**; misafir tıklayınca giriş/kayıt ekranına gider.
- İkincil kısa bilgi: “Oy vermek için hesap gerekmiyor.”
- Masaüstünde kontrollü kart ızgarası, mobilde tek kolon.
- Kart içeriği: soru, opsiyonların kısa gösterimi, `@kullaniciadi`, oluşturulma zamanı, toplam oy sayısı (toplam sayı oy vermeden gösterilebilir, yüzde gösterilmez), **“Oy ver” / “Sonuçları gör”** eylemi.
- Anket yoksa boş durum: “Henüz anket yok. İlk kararsızlığı sen paylaş!” ve CTA.
- İlk sürümde algoritma yok; `-created_at` sırasıyla sayfala.

### 7.2 Anket detay

- Soru hiyerarşide en güçlü metin.
- Her seçenek büyük, dokunulabilir, klavyeyle erişilebilir tek-seçimli radio kontrolü olarak sunulsun.
- Oy işlemi açık CTA ile yapılmalı; seçim olmadan gönderme hata verir.
- Başarılı oy sonrası her seçenekte çubuk + yüzde + oy sayısı; hangi seçenek işaretlendiği vurgulansın.
- Aynı ankete tekrar gelince kullanıcı/misafir geçmiş oyuna göre doğrudan sonuç ekranı görsün.
- Hazırlanan anketin URL'sini kolayca kopyalamaya yarayan, tarayıcı Clipboard API varsa çalışan ve yoksa basit fallback kullanan **“Bağlantıyı kopyala”** eylemi eklenebilir (Faz 4'te).

### 7.3 Anket oluşturma

- Yalnızca oturum açmış kullanıcı.
- Soru zorunlu; açıklama isteğe bağlı.
- Başlangıçta **2 seçenek satırı** açık.
- **“+ Seçenek ekle”** ile en fazla 5'e çıkabilir; 5'te buton devre dışı/gizli.
- Bir seçenek silindiğinde **2'nin altına düşemez**.
- Form hata verince kullanıcının soru/açıklama/seçenek girdileri korunmalı.
- JS devre dışı kalsa da sunucu en az 2, en fazla 5 seçenek denetimini yapmalı.
- Başarılı kayıttan sonra yayınlanan anket detayına yönlendir.

### 7.4 Kayıt / giriş

- Modern, dikkat dağıtmayan form; parola göstermek/gizlemek isteğe bağlı küçük JS davranışı.
- `username`, `email`, `password1`, `password2` sunucuda doğrulanmalı.
- Kullanıcı adı veya e-posta mevcutsa hangi alanın düzeltilmesi gerektiğini açıkça anlat, hassas iç verileri dökme.
- Başarılı kayıt sonrası oturum otomatik açılabilir ve ana akışa/ilgili güvenli sayfaya yönlendirilebilir.
- Özel hesap e-postası haricinde e-posta hiçbir anket ekranında gösterilmez.

---

## 8. Arayüz / tasarım sistemi

### 8.1 Marka kişiliği

**Sıcak, enerjik, genç, kendine güvenen, ferah, kolay kullanılır.** Renkli ama çocuksu değil; modern bir sosyal ürün hissi. Aşırı animasyon, gösterişli gradient yoğunluğu, oyunlaştırma karmaşası ve büyük boş arayüzlerden kaçın.

**Görsel yön:** Açık kırık-beyaz arka plan, yuvarlatılmış ama düzenli kartlar, net tipografi, canlı mor birincil CTA, mercan ve mint küçük vurgu alanları, yumuşak gölgeler. UI içeriği ön planda kalsın.

### 8.2 Önerilen renk token'ları

```css
:root {
  --color-bg: #F8F9FC;
  --color-surface: #FFFFFF;
  --color-ink: #1D2033;
  --color-muted: #646B80;
  --color-border: #E6E8F0;
  --color-primary: #6B4DFF;
  --color-primary-hover: #5737E6;
  --color-primary-soft: #EEE9FF;
  --color-coral: #FF6F7B;
  --color-mint: #32C9AA;
  --color-lemon: #FFE681;
  --color-danger: #C8334B;
  --radius-card: 20px;
  --radius-input: 12px;
  --shadow-card: 0 10px 30px rgba(39, 31, 83, 0.07);
}
```

Bu değerler başlangıçtır. Renk kontrastı erişilebilir değilse **gerekçeli biçimde** düzelt. Parlak pembe, mint veya sarı üzerinde küçük beyaz metin kullanıp okunabilirliği bozma.

### 8.3 Tipografi ve yerleşim

- Başlıklarda karakterli ama temiz sans-serif; uygun ise **Plus Jakarta Sans** veya iyi bir sistem fontu; gövde için **Inter** / sistem sans. Kullanıcı rızası / yükleme gereksinimi için dış font zorunlu değil.
- Okunaklı hiyerarşi: hero yaklaşık 40–56 px masaüstü, 30–36 px mobil; kart başlıkları yaklaşık 18–22 px; temel metin 15–16 px.
- Ana içerik genişliği yaklaşık `1120px`; form genişliği yaklaşık `640px`.
- Masaüstü kartlar için iki sütun, küçük ekranlarda tek sütun; karmaşık masonry gerekmiyor.
- Tıklanabilir alanlar yaklaşık **44x44 px** minimum; belirgin hover/focus durumu.
- Kart içindeki oy verme etkileşimini mümkünse detay sayfasına bırak; çok sayıda kartta kırılgan form karmaşası yaratma.
- CSS değişkenleri ve basit class isimleri kullan. Tailwind / Bootstrap yükleme.

### 8.4 Önerilen küçük metinler

- Logo/marka: **kararsızım.** (nokta ile deneysel bir wordmark yapılabilir)
- Hero: “Kararsız mı kaldın?”
- Alt açıklama: “Seçeneklerini yaz, herkese sor, kararın kolaylaşsın.”
- Ana CTA: “Bir anket oluştur”
- Giriş CTA: “Giriş yap”
- Misafir uyarısı: “Oy vermek serbest, anket açmak için hesap gerekli.”
- Oy eylemi: “Oyumu gönder”
- Tekrar oy: “Bu ankette zaten oy kullandın.”
- Başarılı sonuç: “Oyunu aldık! İşte sonuçlar.”
- Boş akış: “Şimdilik sessiz buralar. İlk anketi sen başlat!”

### 8.5 Erişilebilirlik

- Semantik `header`, `main`, `nav`, `form`, `fieldset`, `legend`, `button` ve doğru heading sıralaması.
- Radio input'ları gerçek input olmalı; yalnızca `div` click handler'ı ile seçenek seçimi yaratma.
- Hataları alan yanında belirt, gerektiğinde `aria-describedby` ve canlı bildirim (`aria-live`).
- Klavye ile gezilebilirlik, görünür focus ring, renk dışında seçim işareti.
- `prefers-reduced-motion` ayarını dikkate al.
- Mobile-first düzen, yatay taşma olmaması.

---

## 9. Güvenlik, gizlilik ve performans kontrolü

### 9.1 Zorunlu güvenlik

- `SECRET_KEY` sadece gizli çevre değişkeninden; üretimde `DEBUG=False`.
- `ALLOWED_HOSTS` ve `CSRF_TRUSTED_ORIGINS` ortama göre açıkça ayarlanmalı.
- `CSRF` middleware etkin; oy verme, kayıt, anket oluşturma ve çıkış için koruma.
- Üretimde güvenli session/CSRF cookie, HTTPS; proxy HTTPS tespiti doğru yapılandırılmalı. `SECURE_PROXY_SSL_HEADER` yalnızca Vercel'in güvenilir proxy header davranışı doğrulandıysa ayarlanmalı.
- Varsayılan Django password hash'leri ve parola doğrulayıcıları.
- Yetki doğrulaması sadece frontend'de değil Django view'larında.
- ORM kullan; string birleştirerek SQL sorgusu yazma.
- Template auto-escape açık kalsın; kullanıcı metnini `|safe` ile basma, DOM'a `innerHTML` ile kontrolsüz ekleme.
- Kullanıcı e-postalarını HTML data-attribute, yorum, JSON veya public endpoint'lere koyma.
- Kullanıcıya ait anket listesinde `author=request.user` filtresi uygula.
- Production log'larına parola, cookie, yetki token'ı, tam `DATABASE_URL` yazma.
- Kamusal yayın öncesi kayıt/giriş/oylama için **gerçek paylaşımlı altyapıya dayanan** rate limit veya Vercel abuse koruması planla. Django `LocMemCache` gibi instance başına bellek tabanlı throttling'i küresel bot koruması diye sunma.
- Admin paneli yalnızca staff/superuser kullanıcılarına açık ve güçlü parolayla korunmalı.

### 9.2 Performans / ölçek

- Akış sayfası **12 anket** ve sayfalama.
- `select_related('author')`, gerektiğinde `prefetch_related('options')` ve `annotate(Count(...))` ile N+1 sorgularını azalt.
- Oy sayıları ilk sürümde sorgularla doğru hesaplanmalı; güncelliği belirsiz elle tutulan counter gerekmez.
- Django Admin ve session kayıtları PostgreSQL üzerinde saklanır.
- Ön yüz JS'si küçük ve framework bağımsız kalsın.
- Vercel geçici dosya sistemi kalıcı veri için kullanılmaz.

---

## 10. Supabase bağlantısı ve Vercel yayınlama kuralları

### 10.1 Temel konfigürasyon

- **Supabase projesi:** PostgreSQL veritabanı kaynağıdır. Django ORM tablolarını migration'larla oluşturur.
- **Yerel geliştirme ve kontrollü migration:** Supabase Dashboard → **Connect → Session pooler** adresi uygun başlangıçtır. Mümkünse migration için doğrudan bağlantı da tercih edilebilir; IPv6 erişimini doğrula.
- **Vercel çalışma zamanı:** Supabase Dashboard → **Connect → Transaction pooler** bağlantısı (genellikle port `6543`) serverless iş yükü için önerilir.
- Adres, host ve kullanıcı adı değerlerini **Supabase panelinden birebir kopyala**; bölge/host adını tahmin etme.
- Transaction pooler kullanırken Psycopg prepared statement'ları devre dışı bırak (`prepare_threshold=None`), Django server-side cursor'larını kapat (`DISABLE_SERVER_SIDE_CURSORS=True`). Bağlantı ayarında `CONN_MAX_AGE=0` ile başla.
- SSL kullan (`sslmode=require`). `sslmode=require` sertifika kimliğini tam doğrulamaz; gerekirse sertifikalı `verify-full` ayrı bir sertleştirme adımıdır.
- İlk sürümde Django tarafında ayrıca uygulama-içi connection pool açma.

Örnek **yönlendirici** ayar; gerçek `settings.py` içeriğini kullanılacak sürümlere göre Codex oluştursun:

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=0,
        ssl_require=True,
    )
}
DATABASES["default"].setdefault("OPTIONS", {})["prepare_threshold"] = None
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
```

**Güvenli geliştirme notu:** `DATABASE_URL` tanımlı değilse üretim için sessizce SQLite'a geçme. Ayarın eksik olduğunu açıkça bildir. Sadece gizli bilgi olmadan izole birim testi çalıştırabilmek amacıyla **açıkça seçilen** `TEST_SQLITE=1` modunda SQLite kabul edilebilir; gerçek Supabase entegrasyon testleri ayrıca yapılmalı. SQLite testlerinin tüm PostgreSQL constraint / concurrency özelliklerini eksiksiz sınamadığını belgele.

### 10.2 Ortam değişkenleri

`.env.example` aşağıdaki anahtarları **sahte/değiştirilecek değerlerle** açıklamalı biçimde içermeli:

```dotenv
DJANGO_SECRET_KEY=replace-with-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
TEST_SQLITE=0
```

- Local development için `.env` okunacaksa bunu açıkça `python-dotenv` ile uygulamanın başlangıcında yap veya terminal environment değerlerini kullan. Birden fazla dotenv kütüphanesi ekleme.
- Vercel'de `DJANGO_DEBUG=False`, gerçek `DJANGO_SECRET_KEY`, `DATABASE_URL`, domain'e uygun `DJANGO_ALLOWED_HOSTS` ve `DJANGO_CSRF_TRUSTED_ORIGINS` tanımlanmalı.
- `DATABASE_URL` örneğinde şifre içindeki özel karakterlerin URL-encode edilmesi gerektiğini README'de anlat.
- `.env` ve Vercel environment secrets kamusal istemciye gönderilmeyecek.

### 10.3 Vercel yaklaşımı (2026)

- Vercel, Django uygulamalarını artık otomatik algılayabiliyor; **önce standard Django `manage.py` + WSGI/ASGI düzeniyle deploy dene**.
- Sırf eski örneklerde var diye `/api` içine Django kopyalama, özel rewrite'lar veya karmaşık `vercel.json` yazma. Gerçek deploy doğrulaması gerekirse minimal konfigürasyon ekle.
- `STATIC_URL='/static/'` ve `STATIC_ROOT` ayarla. Vercel'in Django statik toplama/CDN desteğini kullan. Build sırasında statik dosyaların gerçekten sunulduğunu doğrula.
- Üretim veritabanında migration'ı **her Vercel build'inde otomatik olarak çalıştırma**: özellikle preview deploy'ların üretim şemasını değiştirme tehlikesi var.
- Migration'ları doğru Supabase projesine ve tercihen session/direct bağlantı üzerinden **kontrollü olarak** çalıştır; sonra Vercel'i deploy et.
- Vercel preview için mümkünse ayrı test/veri kaynağı kullan; preview ve production'ın yanlışlıkla aynı canlı DB'ye yazmasını engelle.
- Canlı ortamda kalıcı lokal SQLite, JSON dosyası veya function dosya sistemi kullanma.
- Harici servis erişimi / Vercel yetkisi yoksa deploy tamamlandı deme; yapılması gereken manuel adımları eksiksiz yaz.

### 10.4 Yerel geliştirme komutları (README'de belgelenmeli)

```bash
python -m venv .venv
# Sanal ortamı işletim sistemine uygun biçimde etkinleştir.
python -m pip install -r requirements.txt
# .env.example -> .env kopyala ve gerçek bağlantı bilgilerini ekle.
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
python manage.py check
```

`requirements.txt` içerisinde güvenlik düzeltmelerini alan **Django 5.2.x** ve uyumlu psycopg sürümü kullanılmalı; bağımlılık sürümleri test edilmiş ve makul biçimde kısıtlanmış olmalı. Rastgele paket ekleme.

---

## 11. Test / kabul senaryoları

Codex, ilgili faz tamamlandıkça aşağıdakileri otomatik test olarak yazmalı veya doğrulayamadığı yerleri işaretlemeli.

| Kimlik | Senaryo | Beklenen sonuç |
| --- | --- | --- |
| A01 | Misafir `/` açar | Yayındaki tüm anketleri görür, giriş zorunluluğu yok |
| A02 | Misafir anket oluşturmayı açar | Girişe yönlendirilir |
| A03 | Üye anket oluşturur; 2 seçenek | Başarılı |
| A04 | Üye 5 seçenekli anket oluşturur | Başarılı |
| A05 | 1 veya 6 seçenek gönderilir | Sunucuda reddedilir |
| A06 | Boş, yalnızca boşluk, tekrar eden seçenekler | Anlaşılır doğrulama hatası |
| A07 | Kayıtta aynı kullanıcı adı (farklı case) | Reddedilir |
| A08 | Kayıtta aynı e-posta (farklı case) | Reddedilir |
| A09 | Anket kartı veya detay incelenir | Yalnızca `@username` görünür; e-posta yok |
| A10 | Misafir geçerli seçenekle oy verir | 1 Vote oluşturulur, giriş istenmez |
| A11 | Aynı misafir cookie'siyle tekrar oy verir | Oy sayısı artmaz; dostça hata/sonuç |
| A12 | Giriş yapan kişi aynı ankette iki kez oy verir | Oy sayısı artmaz |
| A13 | Diğer anketin `option_id` değeri gönderilir | Güvenli şekilde reddedilir |
| A14 | 2 paralel oy isteği | DB benzersizlik kuralı birden fazla oyu engeller |
| A15 | 0 oy, 1 oy, farklı oy dağılımları | Toplam ve yüzdeler doğru, sıfıra bölme yok |
| A16 | 2 kişi farklı anket açar | Herkes ikisini de akışta görür |
| A17 | `/anketlerim/` | Yalnızca kendi anketleri listelenir |
| A18 | `is_published=False` anket | Kamusal akışta yok, oy kabul edilmez |
| A19 | CSRF token olmadan POST | Reddedilir |
| A20 | Cookie bozuk/değiştirilmiş | Hata üretmez; güvenli yeniden kimlik oluşturma |
| A21 | Mobil 375px ve masaüstü 1440px | Yatay taşma, kapanan CTA ve okunamayan yazı yok |
| A22 | Anonim → üyelik/giriş geçişi | Misafir oyları kimlik birleştirmesi yapılmadığı açıkça belgeli |
| A23 | Formda kötü niyetli HTML/JS metni | Metin çalıştırılmaz, güvenli escape edilir |
| A24 | Yayınlama smoke test | Kayıt, giriş, anket yayınlama, misafir oyu, kalıcılık ve CSS/JS doğrulanır |

**Test stratejisi:** Birim testleri için gerekirse kontrollü SQLite kullanılabilir; PostgreSQL'e özgü unique constraint ve eşzamanlılık davranışlarını gerçek Supabase ya da ayrı bir PostgreSQL test veritabanında ayrıca doğrula. Eşzamanlılık testinin SQLite ile kesin kanıt oluşturduğunu iddia etme.

---

## 12. Fazlar ve teslim koşulları

> **ÖNEMLİ:** Aşağıdaki fazların her biri ayrı bir Codex oturumunda/isteğinde uygulanabilir. Bir faz bitmeden diğerine geçme. Her fazın sonunda hangi dosyaların değiştiğini, hangi komutların çalıştığını ve sonraki fazın ihtiyaçlarını özetle.

### FAZ 1 — Proje iskeleti, altyapı, kullanıcı hesapları

**Hedef:** Django uygulaması ayağa kalksın; Supabase bağlantısı yapılandırılsın; özel User modeli, kayıt/giriş/çıkış ve temel görsel kabuk çalışsın.

**Görevler:**

1. Repo yapısını oluştur; Django config, `accounts` ve `polls` uygulamalarını ekle.
2. `AUTH_USER_MODEL` ile özel kullanıcı modelini başlangıçta tanımla; case-insensitive username ve email kuralını kur.
3. `requirements.txt`, `.python-version`, `.gitignore`, `.env.example`, `README.md`, `PROGRESS.md` hazırla.
4. Django settings: templates, static, locale (`tr`), timezone (`Europe/Istanbul`), session, CSRF, gizli ayarlar ve Supabase/PostgreSQL bağlantı yapılandırması.
5. Kayıt / giriş / POST ile çıkış sayfalarını ve view'larını yaz.
6. `base.html`, header, bildirimler ve temel CSS tasarım token'larını oluştur; anket listesi henüz boş durum gösterebilir.
7. Yönetim paneli çalışsın; süper kullanıcı oluşturma adımlarını anlat.
8. Register/login/permission temel testlerini yaz ve çalıştır.

**Faz 1 kabul:** `runserver` çalışır; kayıt olan hesap giriş yapabilir; oturum korunur; e-posta kamusal sayfalarda görünmez; DB ayarı doğru yönetilir; testler yeşildir.

**Faz 1 dışında bırak:** Anket CRUD mantığı, gerçek oy sistemi, gelişmiş UI polish, Vercel deploy.

**Codex'a gönderilecek Faz 1 promptu:**

```text
Bu repodaki AGENTS.md dosyasını baştan sona oku ve bağlayıcı talimat kabul et.
Yalnızca FAZ 1'i uygula: Django iskeleti, Supabase PostgreSQL yapılandırması,
baştan özel User modeli, kayıt/giriş/çıkış, temel responsive layout,
README, .env.example ve testler.
Mevcut dosyaları önce incele. Güvenlik bilgileri yoksa bunları uydurma;
bağlantı adımlarını belgele ve gerekirse açıkça seçilen TEST_SQLITE=1 ile
birim testlerini çalıştır. Test sonuçlarını ve eksik harici kurulumları yaz.
PROGRESS.md dosyasını güncelle. FAZ 2'ye geçme.
```

### FAZ 2 — Anket oluşturma, akış ve detay

**Hedef:** Giriş yapan kişi 2–5 seçenekli anket yayınlasın; misafirler ve tüm kullanıcılar anketleri görebilsin.

**Görevler:**

1. `Poll` ve `PollOption` modellerini, migration'larını ve admin düzenlemesini ekle.
2. Anket + seçeneklerin transaction içinde oluşturulmasını sağla.
3. Sunucuda soru / seçenek sayısı / uzunluk / tekrar doğrulamaları uygula.
4. Vanilla JS ile `+ seçenek ekle` ve `- kaldır` davranışı oluştur; 2–5 sınırını UX'te uygula.
5. Herkese açık `/` akışı (en yeni anketler, 12'li sayfalama); anket detay sayfası oluştur.
6. `@username` göster; e-posta alanını kamusal template'lere koyma.
7. `/anketlerim/` yalnızca oturum açan kişinin anketleriyle dolsun.
8. Sayfa ve model testlerini ekle; sorgu sayısını gereksiz yere artırma.

**Faz 2 kabul:** Bir üye yeni anket yayınlar; üye olmayan kişi anketi görebilir; 1 ve 6 seçenekli, boş veya tekrar eden seçenekli POST reddedilir.

**Faz 2 dışında bırak:** Oyların DB'ye işlenmesi (Faz 3), ileri UI ve deploy.

**Codex'a gönderilecek Faz 2 promptu:**

```text
AGENTS.md ve PROGRESS.md dosyalarını oku. FAZ 1'de yapılmış kodu koru.
Yalnızca FAZ 2'yi uygula: Poll ve PollOption, 2-5 seçenek doğrulamaları,
anket oluşturma formu, herkese açık akış, detay ve Anketlerim.
Django templates + vanilla JS dışına çıkma. Oy sistemi ekleme.
Testleri çalıştır, hataları düzelt, PROGRESS.md'yi güncelle ve dur.
```

### FAZ 3 — Anonim ve üyelikli oylama, sonuçlar

**Hedef:** Hesapsız oy verme gerçeğe dönüşsün; çift oy önlemi, veri bütünlüğü ve sonuçlar çalışsın.

**Görevler:**

1. `Vote` modeli ve DB constraint'lerini kur.
2. Django imzalı misafir cookie kimliğini uygulamaya ekle.
3. Hem misafir hem üyeler için oy verme POST akışını kur; `login_required` **ekleme**.
4. Seçeneğin ilgili ankete ait olması, yayın durumu ve oy kimliği doğrulamalarını uygula.
5. Atomic kayıt + DB unique constraint + olası `IntegrityError` işlemesi.
6. Başarılı oy ve tekrar oylama durumunda sonuç arayüzü: sayı, yüzde, bar, seçilen seçenek.
7. Gerekiyorsa vanilla JS progressive enhancement; JavaScript kapalıyken temel form çalışmalı.
8. 0 oy, 100%, misafir cookie, çift oy, farklı ankete ait seçenek, CSRF, race-condition senaryoları için testler.
9. Anonim oylamanın cookie sınırlarını README'de açıkla.

**Faz 3 kabul:** Giriş yapmamış kişi anketi oylar; yeniden aynı kimlikle oy veremez; sonuçlar doğru görünür; eşzamanlı çift oyu veritabanı engeller.

**Codex'a gönderilecek Faz 3 promptu:**

```text
AGENTS.md ve PROGRESS.md'yi oku. Yalnızca FAZ 3'ü uygula.
Öncelik anonim oy verme, CSRF, imzalı misafir cookie'si, Vote modelinin
DB unique/check constraint'leri, paralel istek güvenliği ve sonuç ekranı.
Oylama için kayıt şartı koyma. Bir ziyaretçinin tüm cihazlarda benzersiz
olduğunu iddia etme. İlgili testleri ve gerçek PostgreSQL üzerinde
ayrıca doğrulanması gereken noktaları raporla. PROGRESS.md'yi güncelle.
FAZ 4'e geçme.
```

### FAZ 4 — Görsel kalite, mobil UX ve erişilebilirlik

**Hedef:** Kararsızım, teknik prototipten gençlere hitap eden derli toplu ürüne dönüşsün.

**Görevler:**

1. Bölüm 8'deki tasarım sistemini tüm sayfalara tutarlı biçimde uygula.
2. Responsive hero, header, anket kartları, form, sonuç çubukları ve footer tamamla.
3. Input / button hover, focus, hata ve loading/success durumlarını toparla.
4. Boş durum, sonuçta 0 oy, anonim uyarısı, girişte `next` dönüşü gibi akışları cilala.
5. Kopyalanabilir anket bağlantısı, minimal bildirim/toast ekle (gerektiği kadar).
6. 375px, 768px, 1440px görünüm ve temel klavye erişilebilirliğini kontrol et.
7. Faz 1–3 davranışlarını koru; mobil/UX regresyon testlerini çalıştır.

**Faz 4 kabul:** Ekranlar modern, açık arka planlı, canlı vurgu renkli, okunabilir ve mobilde rahat kullanılır; temel tüm işlemler sorunsuz sürer.

**Codex'a gönderilecek Faz 4 promptu:**

```text
AGENTS.md ve PROGRESS.md'yi oku. Yalnızca FAZ 4'ü uygula.
Var olan çalışan Django akışlarını bozmadan UI/UX kalitesini artır.
Açık arka plan, canlı mor/mercan/mint vurgu, net tipografi, güçlü
responsive kartlar, erişilebilir formlar ve hoş sonuç barları kullan.
Framework veya gereksiz tasarım kütüphanesi ekleme. Temel akışları
yeniden test et, PROGRESS.md'yi güncelle ve dur.
```

### FAZ 5 — Vercel deployment ve üretim kontrolleri

**Hedef:** Prototipin Vercel üzerinde çalışmasını sağlamak ve temel güvenlik kontrollerini tamamlamak.

**Görevler:**

1. Güncel Vercel Django deployment rehberini doğrula; otomatik framework algılama ile başla.
2. `STATIC_ROOT`, `STATIC_URL`, üretim cookie/host/CSRF/güvenlik ayarlarını kontrol et.
3. Vercel env değişkenleri için açık kurulum tablosu ve adım adım README hazırla.
4. Supabase production runtime için transaction pooler; kontrollü migration için session/direct bağlantı ayrımını kontrol et.
5. Üretim DB migration'larını Vercel build'inde otomatik çalıştırma.
6. `python manage.py check --deploy` ile uyarıları incele; anlamlı olanları gider.
7. `collectstatic` ve CSS/JS servis edilmesini doğrula.
8. Temel abuse/rate-limit önlemleri ve mevcut risklerin bir kontrol listesini çıkar; en azından kamuya açık yayından önce erişilebilir korumayı değerlendir.
9. Erişim ve yetki varsa gerçek Vercel smoke testlerini yap; yoksa eksiksiz manuel yayınlama adımlarını ver, sonuç uydurma.
10. README'ye yayınlama, yapılandırma, geri alma ve sonraki sürüm fikirlerini ekle.

**Faz 5 kabul:** Uygulama gerçek HTTPS adreste (erişim verilmişse) çalışır; kalıcı veri Supabase'dedir; anonim oy, kullanıcı kaydı, anket oluşturma ve stiller smoke testten geçer. Erişim yoksa deploy'un tamamlanmadığı açıkça belirtilir.

**Codex'a gönderilecek Faz 5 promptu:**

```text
AGENTS.md ve PROGRESS.md'yi oku. Yalnızca FAZ 5'i uygula.
Django + Supabase PostgreSQL projesini güncel Vercel yapılandırmasına
göre deploy'a hazırla. Otomatik Django algılamayı tercih et, gereksiz
rewrite kullanma. Güvenli env ayarları, migration süreci,
staticfiles, production kontrolleri ve smoke testleri bitir.
Harici hesap/kimlik bilgileri erişilebilir değilse deploy edilmiş gibi
davranma; kullanıcıya gereken kesin adımları yaz.
PROGRESS.md'yi ve README'yi güncelle; sonucu özetle.
```

---

## 13. İlerleme raporu formatı

Her faz sonunda Codex son mesajında aşağıdaki yapıyı kullan:

```text
Faz: [1/2/3/4/5]
Durum: [Tamamlandı / Kısmen tamamlandı]

Yapılanlar:
- ...

Oluşturulan / değiştirilen temel dosyalar:
- ...

Çalıştırılan kontroller:
- Komut: ...
- Sonuç: ...

Eksik bilgiler / dış sistem engelleri:
- ... (yoksa "Yok")

Bilinen sınırlar:
- ...

Sonraki adım:
- Kullanıcı onayıyla Faz N'e geçilebilir.
```

**Fazlar arasında otomatik ilerleme yapma.** En kısa yoldan çalışan prototip, açık bir teknik borç listesi ve sağlam testler hedeflenir.

## 14. Daha sonra değerlendirilebilecek özellikler (şimdi yapma)

- Kategori / konu filtreleri ve anket arama.
- Anketin sonlanma tarihi ve kapanınca sonuçların erişilebilirliği.
- Anket linki paylaşımı için Open Graph önizleme.
- Spam azaltmak için paylaşımlı rate limit, CAPTCHA veya abuse tespiti.
- Şifre sıfırlama, e-posta doğrulama.
- Kişinin kendi anketini kapatması / silmesi.
- Ek gizlilik kontrolleri ve hesap silme / veri dışa aktarma.
- Gelişmiş performans ölçümü, sorgu optimizasyonu, gerekirse cache.
- İhtiyaca göre moderasyon, raporlama ve içerik filtreleme.

**Asla eklenmemesi istenen özellik:** Takip/takipçi sistemi. İleride başka fikirler tartışılırsa bile kullanıcı açıkça talep etmeden bu kısıtı kaldırma.

## 15. Resmî doküman başvuru bağlantıları

Uygulamayı geliştirirken, sürüm ve dağıtım davranışı değişmiş olabileceği için gerektiğinde şu güncel kaynakları doğrula:

- Django 5.2 LTS: https://docs.djangoproject.com/en/5.2/
- Django sürüm / destek takvimi: https://www.djangoproject.com/download/
- Vercel Django otomatik destek açıklaması: https://vercel.com/changelog/zero-configuration-django-support
- Vercel Python genel erişim (15 Ekim 2026): https://vercel.com/changelog/python-on-vercel-is-now-generally-available
- Vercel Django örnek proje: https://vercel.com/templates/python/django-notes
- Supabase PostgreSQL bağlantıları: https://supabase.com/docs/guides/database/connecting-to-postgres
- Supabase prepared statements: https://supabase.com/kb/troubleshooting/disabling-prepared-statements-qL8lEL
- Django PostgreSQL ve transaction pooling: https://docs.djangoproject.com/en/5.2/ref/databases/

---

## 16. Codex için ilk hareket

**Bu dosya bir uygulama geliştirme sözleşmesidir; tamamını tek seferde uygulama emri değildir.** İlk çalıştırmada yukarıdaki **Faz 1 promptu** ile başla. Ardından test sonuçları ve `PROGRESS.md` üzerinden kontrollü olarak Faz 2, 3, 4 ve 5'e geç.
