from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Banner Başlığı")
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name="Alt Başlık / Açıklama")
    image = models.ImageField(upload_to="banners/", blank=True, null=True, verbose_name="Banner Görseli")
    button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Buton Metni")
    button_url = models.CharField(max_length=200, blank=True, null=True, verbose_name="Buton Linki")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"

    def __str__(self):
        return self.title


class Statistic(models.Model):
    title = models.CharField(max_length=100, verbose_name="İstatistik Başlığı (Örn: Tamamlanan İşler)")
    value = models.CharField(max_length=50, verbose_name="Değer (Örn: 1500+)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="FontAwesome/Bootstrap İkon Sınıfı")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        ordering = ['order']
        verbose_name = "İstatistik"
        verbose_name_plural = "İstatistikler"

    def __str__(self):
        return f"{self.title}: {self.value}"