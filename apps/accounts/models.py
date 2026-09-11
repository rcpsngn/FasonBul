from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Platform kullanıcısı. Rol ayrımı (Müşteri / Atölye / Admin) burada tutulur.
    Firma/atölyeye özgü ek bilgiler (vergi no, açıklama, doğrulama durumu) Profile modelinde tutulur."""

    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'İlan Veren / Müşteri'
        WORKSHOP = 'WORKSHOP', 'Atölye Sahibi / Üretici'
        ADMIN = 'ADMIN', 'Yönetici'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name="Kullanıcı Rolü",
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Şehir")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Profil Fotoğrafı")

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_workshop(self):
        return self.role == self.Role.WORKSHOP

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER


class Profile(models.Model):
    """Kullanıcının firma/atölye bazlı ek bilgileri ve doğrulama (rozet) durumu.
    is_verified alanı elle işaretlenmez; en az bir Vergi Levhası belgesi yüklenince
    signals.py üzerinden otomatik olarak güncellenir (bkz. refresh_verification_status)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Kullanıcı")
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Firma / Atölye Adı")
    tax_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Vergi Numarası (opsiyonel)")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Saha / Atölye Adresi")
    description = models.TextField(blank=True, null=True, verbose_name="Firma / Atölye Açıklaması")
    is_verified = models.BooleanField(default=False, verbose_name="Doğrulanmış (Vergi Levhalı) Rozet")
    verified_at = models.DateTimeField(blank=True, null=True, verbose_name="Doğrulama Tarihi")

    # apps.reviews.Review kaydedildikçe signals.py üzerinden güncellenen önbelleklenmiş ortalamalar.
    # Her sayfa yüklemesinde ortalama hesaplamamak için burada tutulur.
    avg_workmanship = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Ort. İşçilik Kalitesi")
    avg_timeliness = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Ort. Zamanında Teslimat")
    avg_payment_discipline = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Ort. Ödeme Disiplini")
    avg_defect_rate_score = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Ort. Sakat/Fire Memnuniyeti")
    review_count = models.PositiveIntegerField(default=0, verbose_name="Değerlendirme Sayısı")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return self.company_name or self.user.username

    def refresh_review_aggregates(self):
        """apps.reviews.Review'ler üzerinden 4 kriterin ortalamasını yeniden hesaplar.
        Review kaydedildiğinde/silindiğinde apps/reviews/signals.py tarafından çağrılır."""
        from django.db.models import Avg
        aggregates = self.user.reviews_received.aggregate(
            workmanship=Avg('workmanship_score'),
            timeliness=Avg('timeliness_score'),
            payment=Avg('payment_discipline_score'),
            defect_rate=Avg('defect_rate_score'),
        )
        self.review_count = self.user.reviews_received.count()
        self.avg_workmanship = aggregates['workmanship'] or 0
        self.avg_timeliness = aggregates['timeliness'] or 0
        self.avg_payment_discipline = aggregates['payment'] or 0
        self.avg_defect_rate_score = aggregates['defect_rate'] or 0
        self.save(update_fields=[
            'avg_workmanship', 'avg_timeliness', 'avg_payment_discipline',
            'avg_defect_rate_score', 'review_count',
        ])

    @property
    def reputation_badges(self):
        """Yeterli değerlendirme birikince kazanılan itibar etiketleri.
        Eşik: en az 3 değerlendirme + ilgili kriterde 4.5/5 ve üzeri ortalama."""
        badges = []
        if self.review_count >= 3:
            if self.avg_defect_rate_score >= 4.5:
                badges.append('Düşük Fireli Üretici')
            if self.avg_payment_discipline >= 4.5:
                badges.append('Zamanında Ödeyen Firma')
            if self.avg_timeliness >= 4.5:
                badges.append('Zamanında Teslim Eden')
        return badges

    def refresh_verification_status(self):
        """En az bir Vergi Levhası belgesi varsa rozeti otomatik açar, yoksa kapatır.
        Ayrı bir admin onayı gerektirmez (hız için) - bu karar Excel yol haritasında not edilmişti."""
        has_tax_doc = self.user.documents.filter(
            document_type=Document.DocumentType.TAX_CERTIFICATE
        ).exists()
        changed = False
        if has_tax_doc and not self.is_verified:
            self.is_verified = True
            self.verified_at = timezone.now()
            changed = True
        elif not has_tax_doc and self.is_verified:
            self.is_verified = False
            self.verified_at = None
            changed = True
        if changed:
            self.save(update_fields=["is_verified", "verified_at"])
        return self.is_verified


class Document(models.Model):
    """Vergi levhası, kimlik fotokopisi gibi opsiyonel belgeler.
    Platform bu belgeleri hukuki bir arşiv olarak saklama sorumluluğu taşımaz;
    sadece 'yüklendi mi' bilgisi rozet hesaplaması için kullanılır."""

    class DocumentType(models.TextChoices):
        TAX_CERTIFICATE = 'TAX_CERTIFICATE', 'Vergi Levhası'
        ID_COPY = 'ID_COPY', 'Kimlik Fotokopisi'
        OTHER = 'OTHER', 'Diğer'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents", verbose_name="Kullanıcı")
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, verbose_name="Belge Türü")
    file = models.FileField(upload_to="documents/%Y/%m/", verbose_name="Belge Dosyası")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")

    class Meta:
        verbose_name = "Belge"
        verbose_name_plural = "Belgeler"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"


class Machine(models.Model):
    """Atölyenin makine parkuru envanteri (kaç adet ne tür makinesi var)."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="machines", verbose_name="Profil")
    name = models.CharField(max_length=150, verbose_name="Makine Adı")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Adet")
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name="Not")

    class Meta:
        verbose_name = "Makine"
        verbose_name_plural = "Makine Parkuru"

    def __str__(self):
        return f"{self.name} ({self.quantity} adet)"


class DocumentAccessRequest(models.Model):
    """Bir kullanıcının, başka bir kullanıcının belgesini görüntülemek için gönderdiği izin isteği.
    Belge sahibi onaylamadan (APPROVED) karşı taraf belgeyi görüntüleyemez."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Bekliyor'
        APPROVED = 'APPROVED', 'Onaylandı'
        DENIED = 'DENIED', 'Reddedildi'

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='access_requests', verbose_name="Belge")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_document_requests', verbose_name="İsteği Gönderen")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Durum")
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="İstek Tarihi")
    responded_at = models.DateTimeField(blank=True, null=True, verbose_name="Yanıt Tarihi")

    class Meta:
        verbose_name = "Belge Görüntüleme İsteği"
        verbose_name_plural = "Belge Görüntüleme İstekleri"
        unique_together = ('document', 'requester')
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.requester} -> {self.document} ({self.get_status_display()})"
