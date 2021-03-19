from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.marketplace import tasks
from apps.messenger.models import Message
from apps.messenger.services import get_bot


@receiver(post_save, sender=Message)
def send_email_notification(sender, instance, created, **kwargs):
    """Signal send email about notification from bot to user."""
    if instance.sender != get_bot():
        return
    if not created:
        return
    tasks.send_email_notifications_celery.delay(instance.pk)
