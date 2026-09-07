from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta Adresi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    subject = models.CharField(max_length=200, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactInfo(models.Model):
    address = models.TextField(verbose_name="Adres")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(verbose_name="E-posta")
    map_iframe = models.TextField(blank=True, null=True, verbose_name="Google Map Iframe Kodu")

    class Meta:
        verbose_name = "İletişim Bilgisi"
        verbose_name_plural = "İletişim Bilgileri"

    def __str__(self):
        return "Şirket İletişim Bilgileri"