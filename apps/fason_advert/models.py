from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class AdvertCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "İlan Kategorisi"
        verbose_name_plural = "İlan Kategorileri"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Advert(models.Model):
    ADVERT_TYPES = (
        ('capacity', 'Atölye Kapasite İlanı (İş Arıyor)'),
        ('job', 'Fason İşi Veren İlanı (Atölye Arıyor)'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adverts", verbose_name="İlan Sahibi")
    category = models.ForeignKey(AdvertCategory, on_delete=models.CASCADE, related_name="adverts", verbose_name="Kategori")
    title = models.CharField(max_length=200, verbose_name="İlan Başlığı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    advert_type = models.CharField(max_length=20, choices=ADVERT_TYPES, default='job', verbose_name="İlan Tipi")
    description = models.TextField(verbose_name="Açıklama")
    city = models.CharField(max_length=50, verbose_name="Şehir")
    district = models.CharField(max_length=50, verbose_name="İlçe")
    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Adet / Kapasite")
    price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10, blank=True, null=True, verbose_name="Birim Fiyat (TL)")
    image = models.ImageField(upload_to="adverts/", blank=True, null=True, verbose_name="Görsel")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Fason İlanı"
        verbose_name_plural = "Fason İlanları"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id if self.id else ''}".replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title