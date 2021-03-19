from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.marketplace.models import Lot


@receiver(post_save, sender=Lot)
def set_finished_at(sender, instance, **kwargs):
    """The signal sets the end date for the lot."""
    if not instance.finished_at:
        days = instance.duration
        instance.finished_at = instance.started_at + timedelta(days=days)
        instance.save()
