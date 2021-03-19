from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.html import escape

from apps.messenger import tasks
from apps.marketplace.models import Bid
from apps.messenger.models import Message
from apps.messenger.services import get_bot, get_domain

MESSAGE_TEXTS = {
    'lot_sold': '<a href="{}">{}</a> bought by {}',
    'bid_broken': 'Your bid on <a href="{}">{}</a> broken!',
    'new_bid': '<a href="{}">{}</a> have new bid: {}!'
}


@receiver(post_save, sender=Bid)
def lot_sold(sender, instance, **kwargs):
    """Signal deactivate lot if price of bid equal blitz price of lot,
    send message to lot owner.
    """
    if instance.price == instance.lot.blitz_price:
        tasks.create_message.delay(
            sender_id=get_bot().pk,
            recipient_id=instance.lot.owner.pk,
            msg_type=Message.MessageTypes.LOT_SOLD.LOT_SOLD,
            text=MESSAGE_TEXTS['lot_sold'].format(
                settings.SITE_PROTOCOL +
                get_domain() +
                instance.lot.get_absolute_url(),
                escape(str(instance.lot)),
                instance.user.username
            ),
        )

        instance.lot.deactivate()
        instance.lot.save()


@receiver(pre_save, sender=Bid)
def send_msg_to_old_bid_leader(sender, instance, **kwargs):
    """Signal send message to previous bid leader and send them email."""
    if instance.lot.bids.first():
        tasks.create_message.delay(
            sender_id=get_bot().pk,
            recipient_id=instance.lot.bids.first().user.pk,
            msg_type=Message.MessageTypes.BID_BROKE,
            text=MESSAGE_TEXTS['bid_broken'].format(
                settings.SITE_PROTOCOL +
                get_domain() +
                instance.lot.get_absolute_url(),
                escape(str(instance.lot)),
            ),
        )


@receiver(post_save, sender=Bid)
def new_bid(sender, instance, **kwargs):
    """Signal send message about new bid to lot owner and send them email."""
    if instance.lot.is_active:
        tasks.create_message.delay(
            sender_id=get_bot().pk,
            recipient_id=instance.lot.owner.pk,
            msg_type=Message.MessageTypes.NEW_BID,
            text=MESSAGE_TEXTS['new_bid'].format(
                settings.SITE_PROTOCOL +
                get_domain() +
                instance.lot.get_absolute_url(),
                escape(str(instance.lot)),
                instance.price
            ),
        )
