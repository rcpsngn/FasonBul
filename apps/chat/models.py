from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.fason_advert.models import Proposal


class Conversation(models.Model):
    """Bir teklif kabul edildiğinde otomatik olarak açılan sohbet (bkz. signals.py).
    Karşılıklı 'yüz yüze görüştük' onayı da burada tutulur; iki taraf da onaylayınca
    meeting_confirmed_at doldurulur ve bu bilgi ileride itibar/puanlama modülünde
    bir rozet olarak kullanılabilir."""

    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name='conversation', verbose_name="Teklif")
    owner_confirmed_meeting = models.BooleanField(default=False, verbose_name="İlan Sahibi Yüz Yüze Görüşme Onayı")
    bidder_confirmed_meeting = models.BooleanField(default=False, verbose_name="Teklif Verenin Yüz Yüze Görüşme Onayı")
    meeting_confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name="Görüşme Onay Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Sohbet"
        verbose_name_plural = "Sohbetler"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sohbet: {self.proposal}"

    @property
    def is_meeting_confirmed(self):
        return self.owner_confirmed_meeting and self.bidder_confirmed_meeting

    def is_participant(self, user):
        return user in (self.proposal.advert.owner, self.proposal.bidder)

    def other_participant(self, user):
        if user == self.proposal.advert.owner:
            return self.proposal.bidder
        return self.proposal.advert.owner

    def confirm_meeting_for(self, user):
        """Kullanıcının kendi tarafındaki onayını işaretler. İki taraf da onaylarsa
        meeting_confirmed_at otomatik doldurulur."""
        changed = False
        if user == self.proposal.advert.owner and not self.owner_confirmed_meeting:
            self.owner_confirmed_meeting = True
            changed = True
        elif user == self.proposal.bidder and not self.bidder_confirmed_meeting:
            self.bidder_confirmed_meeting = True
            changed = True

        if changed:
            if self.owner_confirmed_meeting and self.bidder_confirmed_meeting and not self.meeting_confirmed_at:
                self.meeting_confirmed_at = timezone.now()
            self.save()
        return self.is_meeting_confirmed


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Sohbet")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Gönderen")
    content = models.TextField(verbose_name="Mesaj")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"
