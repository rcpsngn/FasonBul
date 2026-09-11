from django.conf import settings
from django.db import models

from apps.contracts.models import Contract


class Review(models.Model):
    """Bir sözleşme (iş) tamamlandıktan sonra taraflardan birinin karşı tarafa verdiği
    4 kriterli değerlendirme. Bir kullanıcı aynı sözleşme için yalnızca bir kez
    değerlendirme yapabilir (unique_together)."""

    class Score(models.IntegerChoices):
        ONE = 1, '1 - Çok Kötü'
        TWO = 2, '2 - Kötü'
        THREE = 3, '3 - Orta'
        FOUR = 4, '4 - İyi'
        FIVE = 5, '5 - Çok İyi'

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sözleşme")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given', verbose_name="Değerlendiren")
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received', verbose_name="Değerlendirilen")

    workmanship_score = models.PositiveSmallIntegerField(choices=Score.choices, verbose_name="İşçilik Kalitesi")
    timeliness_score = models.PositiveSmallIntegerField(choices=Score.choices, verbose_name="Zamanında Teslimat")
    payment_discipline_score = models.PositiveSmallIntegerField(choices=Score.choices, verbose_name="Ödeme Disiplini")
    defect_rate_score = models.PositiveSmallIntegerField(choices=Score.choices, verbose_name="Sakat/Fire Oranı Memnuniyeti")

    comment = models.TextField(blank=True, verbose_name="Yorum (opsiyonel)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Değerlendirme"
        verbose_name_plural = "Değerlendirmeler"
        unique_together = ('contract', 'reviewer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewee} ({self.contract_id})"

    @property
    def average_score(self):
        return (
            self.workmanship_score + self.timeliness_score
            + self.payment_discipline_score + self.defect_rate_score
        ) / 4
