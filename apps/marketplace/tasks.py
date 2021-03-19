from celery import shared_task
from django.core.mail import send_mail

from apps.marketplace.models import Lot, Bid
from apps.marketplace.services.handlers import (
    deactivate_lots_and_send_notifications,
)
from apps.messenger.models import Message, Dialog
from apps.messenger.services import get_bot, get_dialog_opponent, create_message
from apps.users.models import User


@shared_task()
def deactivate_expired_lots():
    """Checks lots which expired but they still active and deactivate them."""
    expired_lots = Lot.objects.expired_by_time()
    deactivate_lots_and_send_notifications(expired_lots)


@shared_task()
def send_email_notifications_celery(msg_pk):
    """Send email notification from signal by celery."""
    message = Message.objects.get(pk=msg_pk)
    send_mail(
        subject=message.type,
        message=message.message,
        from_email=get_bot().email,
        recipient_list=[
            get_dialog_opponent(
                dialog=message.dialog,
                user=get_bot()
            ).email],
        fail_silently=False,
    )
