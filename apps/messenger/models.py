from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from apps.messenger.manager import DialogManager


class Dialog(TimeStampedModel):
    """Model for the convenience of finding messages between users."""

    user1 = models.ForeignKey(
        to='users.User',
        related_name='+',
        on_delete=models.CASCADE,
    )
    user2 = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='+'
    )

    objects = DialogManager()

    def __str__(self):
        return f'{self.user1.username} AND {self.user2.username}'

    class Meta:
        db_table = 'dialogs'
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")


class Message(TimeStampedModel):
    """Model for private messages and notifications."""

    class MessageTypes(models.TextChoices):
        NEW_MESSAGE = 'new message', _("New message")
        NEW_BID = 'new bid', _("New bid")
        BID_BROKE = 'bid broken', _("Your bid was broken")
        DEFAULT_NOTIFICATION = 'default_notification', _('Notification')
        LOT_SOLD = 'lot sold', _("Lot sold!")

    dialog = models.ForeignKey(
        to=Dialog,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    date = models.DateTimeField(
        verbose_name=_("Date and time"),
        auto_now=True,
    )
    type = models.CharField(
        verbose_name=_("Message type"),
        max_length=50,
        choices=MessageTypes.choices,
        default=MessageTypes.DEFAULT_NOTIFICATION,
    )
    message = models.CharField(
        verbose_name=_("Message"),
        max_length=1000,
    )
    is_read = models.BooleanField(
        verbose_name=_("Is read?"),
        default=False,
    )

    def __str__(self):
        return f'{self.dialog} {self.message}'

    class Meta:
        db_table = 'messages'
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
