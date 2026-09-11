from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.chat.models import Conversation


class Contract(models.Model):
    """Bir sohbete (dolayısıyla kabul edilmiş bir teklife) bağlı fason sözleşmesi.
    Platform bu sözleşmeye taraf değildir; sadece taraflara standart bir şablon ve
    karşılıklı onay akışı sunar. Şartlar değiştirilirse (onaylandıktan sonra bile)
    onaylar sıfırlanır, böylece kimse fark ettirmeden şart değiştiremez."""

    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='contract', verbose_name="Sohbet")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_contracts', verbose_name="Oluşturan")

    quantity = models.PositiveIntegerField(verbose_name="Adet")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Birim Fiyat (TL)")
    due_date = models.DateField(verbose_name="Teslim / Vade Tarihi")
    defect_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Kabul Edilebilir Fire Oranı (%)")
    extra_terms = models.TextField(blank=True, verbose_name="Ek Şartlar / Notlar")

    owner_approved = models.BooleanField(default=False, verbose_name="İlan Sahibi Onayı")
    bidder_approved = models.BooleanField(default=False, verbose_name="Teklif Verenin Onayı")
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name="Tam Onay Tarihi")

    # İş bitince her iki taraf da ayrıca "iş tamamlandı" beyan eder; değerlendirme (reviews)
    # ancak bu ikisi de True olduktan sonra açılır.
    owner_completed = models.BooleanField(default=False, verbose_name="İlan Sahibi İş Tamamlandı Beyanı")
    bidder_completed = models.BooleanField(default=False, verbose_name="Teklif Verenin İş Tamamlandı Beyanı")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Tam Tamamlanma Tarihi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Fason Sözleşmesi"
        verbose_name_plural = "Fason Sözleşmeleri"

    def __str__(self):
        return f"Sözleşme: {self.conversation.proposal.advert.title}"

    @property
    def is_fully_approved(self):
        return self.owner_approved and self.bidder_approved

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    @property
    def owner(self):
        return self.conversation.proposal.advert.owner

    @property
    def bidder(self):
        return self.conversation.proposal.bidder

    def reset_approvals(self):
        self.owner_approved = False
        self.bidder_approved = False
        self.approved_at = None

    def approve_for(self, user):
        changed = False
        if user == self.owner and not self.owner_approved:
            self.owner_approved = True
            changed = True
        elif user == self.bidder and not self.bidder_approved:
            self.bidder_approved = True
            changed = True

        if changed:
            if self.owner_approved and self.bidder_approved and not self.approved_at:
                self.approved_at = timezone.now()
            self.save()
        return self.is_fully_approved

    @property
    def is_completed(self):
        return self.owner_completed and self.bidder_completed

    def mark_completed_for(self, user):
        """Bir tarafın 'iş tamamlandı' beyanını kaydeder. Sözleşme henüz tam onaylanmadıysa
        (is_fully_approved değilse) tamamlama beyanı kabul edilmez."""
        if not self.is_fully_approved:
            return self.is_completed

        changed = False
        if user == self.owner and not self.owner_completed:
            self.owner_completed = True
            changed = True
        elif user == self.bidder and not self.bidder_completed:
            self.bidder_completed = True
            changed = True

        if changed:
            if self.owner_completed and self.bidder_completed and not self.completed_at:
                self.completed_at = timezone.now()
            self.save()
        return self.is_completed
