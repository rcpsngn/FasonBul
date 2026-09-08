from django.db import models
from django.conf import settings


class Workshop(models.Model):
    CATEGORY_CHOICES = (
        ('orme', 'Örme'),
        ('dokuma', 'Dokuma'),
        ('kesim', 'Kesim / Fason Kesim'),
        ('utu_paket', 'Ütü & Paket'),
        ('baski_nakis', 'Baskı & Nakış'),
        ('diger', 'Diğer Fason İşler'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workshops',
        verbose_name="Atölye Sahibi"
    )
    title = models.CharField(max_length=200, verbose_name="Atölye / Firma Adı")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='orme',
        verbose_name="Kategori / Ne Yapıyor?"
    )
    phone = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    city = models.CharField(max_length=100, verbose_name="İl")
    district = models.CharField(max_length=100, verbose_name="İlçe")
    address = models.TextField(blank=True, null=True, verbose_name="Açık Adres")

    # Mesafe Filtreleme İçin Koordinat Alanları
    latitude = models.FloatField(null=True, blank=True, verbose_name="Enlem (Lat)")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Boylam (Lng)")

    capacity = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aylık Kapasite (Parça)")

    email = models.EmailField(blank=True, null=True, verbose_name="E-posta Adresi")
    employee_count = models.PositiveIntegerField(blank=True, null=True, verbose_name="Çalışan Sayısı")
    daily_capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Günlük Üretim Kapasitesi (Adet)")
    description = models.TextField(blank=True, null=True, verbose_name="Atölye Açıklaması / Uzmanlık Alanları")
    logo = models.ImageField(upload_to="workshops/logos/", blank=True, null=True, verbose_name="Atölye Logosu")
    cover_image = models.ImageField(upload_to="workshops/covers/", blank=True, null=True, verbose_name="Kapak Görseli")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        verbose_name = "Atölye"
        verbose_name_plural = "Atölyeler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()} ({self.city})"