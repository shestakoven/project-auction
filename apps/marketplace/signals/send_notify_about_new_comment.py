from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.marketplace.models import Comment


@receiver(post_save, sender=Comment)
def send_notify(sender, instance, **kwargs):
    """Signal sends notification lot owner and user of parent comment."""
    if instance.parent:
        parent_user = instance.parent.user
        # TODO send message to parent comment user
        pass

    if instance.lot:
        lot_owner = instance.lot.owner
        # TODO send message to lot owner
        pass
