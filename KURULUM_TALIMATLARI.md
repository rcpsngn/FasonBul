# MODÜL 1: Kullanıcı & Profil (accounts) — Kurulum Talimatları

## GÜNCELLEME (v2): Belge Görüntüleme İzin Sistemi Eklendi

Eğer accounts modülünü zaten kurduysan (v1), bu sefer **veritabanını sıfırlamana
gerek yok** — sadece yeni `DocumentAccessRequest` modeli eklendi, bu ek bir migration
ile halledilir. Şu adımları izle:

1. Bu paketteki `apps/accounts/` klasöründeki TÜM dosyaları, projenin
   `apps/accounts/` klasörünün üzerine kopyala (üzerine yaz) — `migrations` klasörüne
   dokunma, onu olduğu gibi bırak.
2. Bu paketteki `templates/accounts/` klasöründeki dosyaları projenin
   `templates/accounts/` üzerine kopyala (üzerine yaz) — yeni eklenen
   `public_profile.html` da otomatik gelecek.
3. Terminalde:
```powershell
python manage.py makemigrations accounts
python manage.py migrate
```
   Bu sefer `db.sqlite3`'ü silmene gerek yok, sadece yeni tabloyu ekleyen küçük
   bir migration (`0002_...py`) oluşacak.
4. `python manage.py test apps.accounts` — artık 7 test olmalı, hepsi geçmeli.
5. Tarayıcıda iki farklı hesapla (bir Atölye, bir Firma hesabı) giriş yapıp,
   Firma hesabından `/hesap/profil/<atölye_kullanıcı_adı>/` adresine giderek
   "Görüntüleme İsteği Gönder"i dene; Atölye hesabıyla kendi profiline dönüp
   "Bekleyen Görüntüleme İstekleri" bölümünden onayla/reddet.

Aşağıdaki "İlk Kurulum" bölümü, modülü hiç kurmamış olanlar veya sıfırdan
kurmak isteyenler içindir.

---

## İLK KURULUM (v1) — Daha Önce Hiç Kurmadıysan

Bu paket, mevcut `apps/account` uygulamasının yerini alacak şekilde tasarlandı ve
Excel yol haritandaki planlanan mimariye (User + Profile + Document + Machine) uygun.

## ÖNEMLİ UYARI — Veritabanı Sıfırlanacak

`account` → `accounts` app ismi değişikliği ve model yapısının değişmesi (User'dan
company_name'in Profile'a taşınması, yeni Document/Machine modelleri) nedeniyle
**mevcut migration geçmişi ve db.sqlite3 ile uyumsuz.** Bu normal bir "app rename"
değil, foundational bir yeniden yapılandırma.

Şu an projede gerçek/canlı kullanıcı verisi olmadığını varsayıyorum (geliştirme
aşamasındasın). Eğer db.sqlite3 içinde korumak istediğin test verisi varsa,
devam etmeden önce dosyayı bir yere kopyala.

## Adımlar (PyCharm terminalinde sırayla)

### 1) Eski account app'ini kaldır, yenisini yerleştir
```powershell
# Proje kökünde:
Remove-Item -Recurse -Force apps\account
Remove-Item db.sqlite3
```
Bu paketteki `apps\accounts` klasörünü projenin `apps\` klasörünün içine kopyala.
Bu paketteki `templates\accounts` klasörünü projenin `templates\` klasörünün içine kopyala
(eski `templates\account` klasörünü silebilirsin).
Bu paketteki `templates\includes\_navbar.html` dosyasını, projenin
`templates\includes\_navbar.html` dosyasının üzerine kopyala (üzerine yaz).

### 2) `fasonbul/settings.py` içinde 3 küçük değişiklik yap

**a) INSTALLED_APPS** — şu satırı:
```python
    'apps.account',
```
şununla değiştir:
```python
    'apps.accounts',
    'rest_framework',
```
(`rest_framework`'ü ekliyoruz çünkü `serializers.py` DRF'e ihtiyaç duyuyor;
`djangorestframework` zaten `requirements.txt`'de kurulu.)

**b) AUTH_USER_MODEL** — şu satırı:
```python
AUTH_USER_MODEL = 'account.User'
```
şununla değiştir:
```python
AUTH_USER_MODEL = 'accounts.User'
```

**c) LOGIN/LOGOUT ayarları** — şu 3 satırı:
```python
LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = 'account:profile'
LOGOUT_REDIRECT_URL = 'account:login'
```
şununla değiştir:
```python
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'accounts:login'
```

### 3) `fasonbul/urls.py` içinde 1 satırı değiştir

Şu satırı:
```python
    path('hesap/', include('apps.account.urls', namespace='account')),
```
şununla değiştir:
```python
    path('hesap/', include('apps.accounts.urls', namespace='accounts')),
```

### 4) Migration oluştur ve veritabanını kur
```powershell
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
```
> Not: Bu sandbox ortamında Django kurulu olmadığı için migration dosyasını
> senin tarafında (`makemigrations`) üretmen gerekiyor — elle yazıp göndermek
> hatalı/eksik bir migration riski taşırdı, bu yüzden bu adımı sana bıraktım.

### 5) Testleri çalıştır
```powershell
python manage.py test apps.accounts
```
3 test de geçmeli: kayıt olunca profil otomatik oluşuyor mu, vergi levhası
yükleyince rozet otomatik açılıyor mu, silince kapanıyor mu.

### 6) Sunucuyu başlat ve kontrol et
```powershell
python manage.py runserver
```
- `/hesap/kayit/` → yeni hesap oluştur (rol: Atölye Sahibi seç)
- `/hesap/profil/` → "Belgelerim" bölümünden "Vergi Levhası" seçip herhangi bir
  dosya yükle → sol paneldeki rozetin "Doğrulanmış" olarak değiştiğini gör
- Belgeyi silince rozetin geri "Henüz Doğrulanmadı" olduğunu gör
- "Makine Parkuru" bölümünden birkaç makine ekleyip sil

## Bu modülde neler var, neler yok

**Var:**
- User: rol ayrımı (Müşteri/Atölye/Admin), telefon, şehir, avatar
- Profile: firma/atölye adı, vergi no (opsiyonel metin alanı — doğrulama
  amacıyla zorunlu tutulmuyor), adres, açıklama, **is_verified** (otomatik)
- Document: vergi levhası / kimlik fotokopisi yükleme — platform bunları
  saklama sorumluluğu taşımıyor, sadece rozet hesaplamak için var
- Machine: atölye makine parkuru (ad, adet, not)
- Rozet mantığı tamamen otomatik: vergi levhası belgesi eklenince/silinince
  admin onayı beklemeden anında güncelleniyor (signals.py)
- serializers.py ileride mobil app/API için hazır, henüz bir API endpoint'i
  (router/viewset) bağlanmadı — sıradaki modüllerde gerek olursa ekleriz

**Yok / bu modülün kapsamı dışında:**
- Kimlik fotokopisi/vergi levhası gerçek doğrulama (insan onayı) — şu an
  sadece "yüklendi mi" kontrolü var, önceki konuşmalarımızdaki "biz taraf
  değiliz, öneride bulunuruz" prensibine uygun
- Firma/Atölye arası mesajlaşma, ilan, sözleşme — bunlar sırada bekleyen
  ayrı modüller (listings, chat, contracts)
