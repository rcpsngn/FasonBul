# FasonBul — Modül 3: Sözleşme & İletişim (Sohbet)

Bu pakette **yepyeni bir uygulama** var: `apps/chat`. Önceki paketlerden farkı:
önceki modüllerde (accounts, workshop, fason_advert) uygulamalar zaten
`INSTALLED_APPS`'te kayıtlıydı, sadece dosyalarını güncelledik. Bu sefer
`chat` diye yeni bir app olduğu için, onu **elle** projene tanıtman gerekiyor.
Bu yüzden bu sefer 4 adım var (öncekilerden 1 fazla).

## Ne işe yarıyor

Bir teklif kabul edildiğinde, taraflar arasında otomatik olarak bir sohbet
açılıyor. Orada:
- Serbestçe mesajlaşabiliyorlar
- "Yüz yüze görüştük" diye karşılıklı onay verebiliyorlar — **iki taraf da**
  onaylayınca bu bir rozet/kanıt olarak görünüyor (ileride puanlama
  modülünde kullanılabilir)

## Adım 1 — Dosyaları kopyala

Zip'i aç. İçindeki `apps` klasörünü projenin `apps` klasörünün üzerine,
`templates` klasörünü de projenin `templates` klasörünün üzerine kopyala
(üzerine yazmayı onayla). Bu, hem yeni `apps/chat` klasörünü ekleyecek hem de
`fason_advert`'in teklif sayfalarına "Sohbeti Aç" butonu, navbar'a da
"Mesajlarım" linkini ekleyecek.

## Adım 2 — `fasonbul/settings.py`'de 1 satır ekle

`INSTALLED_APPS` listesine, diğer `apps.xxx` satırlarının yanına şunu ekle:
```python
    'apps.chat',
```

## Adım 3 — `fasonbul/urls.py`'de 1 satır ekle

`urlpatterns` listesine, diğer `path('...', include(...))` satırlarının
yanına şunu ekle:
```python
    path('mesajlar/', include('apps.chat.urls', namespace='chat')),
```

## Adım 4 — Migration ve test

```powershell
python manage.py makemigrations chat
python manage.py migrate
python manage.py test apps.chat
python manage.py runserver
```

7 testin de OK geçmesi lazım.

## Nasıl test edersin (2 hesapla)

1. Firma hesabıyla bir ilan ver (ya da var olanı kullan)
2. Atölye hesabıyla o ilana teklif ver
3. Firma hesabıyla ilanın "Gelen Teklifler" sayfasına git, teklifi **Kabul Et**
4. Otomatik olarak bir sohbet açılmış olmalı — "💬 Sohbeti Aç" butonu görünür
5. Her iki hesaptan da mesaj gönderip alabildiğini kontrol et
6. Her iki hesaptan da "Yüz Yüze Görüştük, Onayla" butonuna bas — ikisi de
   onaylayınca yeşil "✓ Yüz Yüze Görüşüldü" rozetinin çıktığını gör
7. Navbar'daki "Mesajlarım" linkinden sohbetin listede göründüğünü kontrol et

## Kapsam dışı (henüz yapılmadı)

- Dijital fason sözleşmesi şablonu / onay akışı (sıradaki modül: contracts)
- Karşılıklı puanlama / itibar sistemi (ondan sonraki modül: reviews)
