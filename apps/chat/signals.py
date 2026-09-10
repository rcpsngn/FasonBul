from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.fason_advert.models import Proposal
from .models import Conversation


@receiver(post_save, sender=Proposal)
def create_conversation_on_accept(sender, instance, **kwargs):
    """Bir teklif kabul edildiğinde, taraflar arasında otomatik olarak bir
    sohbet açar (daha önce açılmamışsa)."""
    if instance.status == Proposal.Status.ACCEPTED:
        Conversation.objects.get_or_create(proposal=instance)
