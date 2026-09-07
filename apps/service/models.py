from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="İkon Sınıfı (Örn: fa-scissors)")

    class Meta:
        verbose_name = "Hizmet Kategorisi"
        verbose_name_plural = "Hizmet Kategorileri"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services", verbose_name="Kategori")
    title = models.CharField(max_length=200, verbose_name="Hizmet Başlığı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    short_description = models.CharField(max_length=300, verbose_name="Kısa Açıklama")
    description = models.TextField(verbose_name="Detaylı Açıklama")
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="Hizmet Görseli")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title