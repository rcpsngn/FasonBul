from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.accounts.models import Profile
from .models import Review


def _refresh_reviewee_profile(review):
    profile, _ = Profile.objects.get_or_create(user=review.reviewee)
    profile.refresh_review_aggregates()


@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    _refresh_reviewee_profile(instance)


@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    _refresh_reviewee_profile(instance)
