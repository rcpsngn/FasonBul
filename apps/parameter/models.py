from django.db import models


class SiteSetting(models.Model):
    title = models.CharField(max_length=200, verbose_name="Site Başlığı")
    description = models.TextField(blank=True, null=True, verbose_name="Site Açıklaması (SEO)")
    keywords = models.CharField(max_length=300, blank=True, null=True, verbose_name="Anahtar Kelimeler")
    logo = models.ImageField(upload_to="settings/", blank=True, null=True, verbose_name="Site Logosu")
    favicon = models.ImageField(upload_to="settings/", blank=True, null=True, verbose_name="Favicon")
    footer_text = models.TextField(blank=True, null=True, verbose_name="Footer Telif Metni")

    class Meta:
        verbose_name = "Site Genel Ayarı"
        verbose_name_plural = "Site Genel Ayarları"

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Şehir Adı")
    code = models.PositiveIntegerField(unique=True, blank=True, null=True, verbose_name="Plaka Kodu")

    class Meta:
        ordering = ['name']
        verbose_name = "Şehir"
        verbose_name_plural = "Şehirler"

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts", verbose_name="Şehir")
    name = models.CharField(max_length=100, verbose_name="İlçe Adı")

    class Meta:
        ordering = ['name']
        verbose_name = "İlçe"
        verbose_name_plural = "İlçeler"

    def __str__(self):
        return f"{self.city.name} - {self.name}"


class WorkType(models.Model):
    """Tekstil İşçilik Türleri (Örn: Örme, Dokuma, Kesim, Ütü Paket, Nakış vb.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="İşçilik Türü")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "İşçilik / Hizmet Türü"
        verbose_name_plural = "İşçilik / Hizmet Türleri"

    def __str__(self):
        return self.name