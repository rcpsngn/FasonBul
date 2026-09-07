from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User, Profile, Document


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Her yeni kullanıcı için otomatik olarak boş bir Profile oluşturur."""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Document)
def refresh_badge_on_document_save(sender, instance, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=instance.user)
    profile.refresh_verification_status()


@receiver(post_delete, sender=Document)
def refresh_badge_on_document_delete(sender, instance, **kwargs):
    try:
        instance.user.profile.refresh_verification_status()
    except Profile.DoesNotExist:
        pass
