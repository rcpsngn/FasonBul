from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class AdvertCategory(models.Model):
    objects = None
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
    objects = None
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


class Proposal(models.Model):
    """Bir ilan üzerindeki tüm pazarlık sürecinin başlığı (thread).
    Asıl fiyat/adet/mesaj geçmişi artık ProposalOffer'da tutuluyor."""

    objects = None

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Görüşülüyor'
        ACCEPTED = 'ACCEPTED', 'Kabul Edildi'
        REJECTED = 'REJECTED', 'Reddedildi'
        WITHDRAWN = 'WITHDRAWN', 'Geri Çekildi'

    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='proposals', verbose_name="İlan")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals', verbose_name="Teklif Veren (Atölye)")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Durum")

    # Sırada kimin teklif/yanıt vermesi bekleniyor - pazarlığın kimde olduğunu gösterir.
    awaiting_response_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+',
        verbose_name="Sırası Kimde"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Başlama Tarihi")
    responded_at = models.DateTimeField(blank=True, null=True, verbose_name="Sonuçlanma Tarihi")

    class Meta:
        verbose_name = "Teklif"
        verbose_name_plural = "Teklifler"
        unique_together = ('advert', 'bidder')
        ordering = ['-created_at']

    @property
    def latest_offer(self):
        return self.offers.first()  # ProposalOffer Meta.ordering = ['-created_at']

    def __str__(self):
        return f"{self.bidder} -> {self.advert} ({self.get_status_display()})"


class ProposalOffer(models.Model):
    """Pazarlıktaki her bir tur: bir tarafın attığı fiyat/adet/mesaj.
    İlk teklif atölyeden gelir (sender=bidder); firma isterse aynı Proposal
    üzerinde yeni bir ProposalOffer açarak karşı teklif verir (sender=owner), vs."""

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='offers', verbose_name="Teklif")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposal_offers', verbose_name="Gönderen")
    price_offer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Teklif Edilen Birim Fiyat (TL)")
    quantity_offer = models.PositiveIntegerField(blank=True, null=True, verbose_name="Karşılanabilecek Adet")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")

    class Meta:
        verbose_name = "Teklif Turu"
        verbose_name_plural = "Teklif Turları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} - {self.price_offer} TL ({self.proposal_id})"