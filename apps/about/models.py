from django.db import models


class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name="Alt Başlık")
    content = models.TextField(verbose_name="Hakkımızda İçeriği")
    vision = models.TextField(blank=True, null=True, verbose_name="Vizyonumuz")
    mission = models.TextField(blank=True, null=True, verbose_name="Misyonumuz")
    image = models.ImageField(upload_to="about/", blank=True, null=True, verbose_name="Görsel")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Hakkımızda Sayfası"
        verbose_name_plural = "Hakkımızda Sayfası"

    def __str__(self):
        return self.title


class Statistic(models.Model):
    title = models.CharField(max_length=100, verbose_name="İstatistik Adı (Örn: Aktif Atölye)")
    value = models.CharField(max_length=50, verbose_name="Değer (Örn: 500+)")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['order']
        verbose_name = "İstatistik"
        verbose_name_plural = "İstatistikler"

    def __str__(self):
        return f"{self.title}: {self.value}"