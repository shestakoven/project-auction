from django.conf import settings
from django.contrib.sites.models import Site

from apps.messenger.models import Dialog, Message
from apps.users.models import User


def create_message(
        sender,
        recipient,
        text,
        msg_type=Message.MessageTypes.NEW_MESSAGE
):
    """
    Create message instance without saving.
    Message won't save in db for future operations, like moderation.

    Args:
        sender (obj): User's instance.
        recipient (obj): User's instance.
        text (str): Message text.
        msg_type (obj): Type of message from MessageTypes
            (NEW_BID, NEW_MESSAGE, etc.)

    Returns:
          obj: Message instance

    """
    dialog = Dialog.objects.get_or_create(sender, recipient)
    return Message(
        dialog=dialog,
        sender=sender,
        type=msg_type,
        message=text
    )


def get_bot():
    """lazy getting a bot from a database."""
    try:
        getattr(get_bot, '_bot')
    except AttributeError:
        get_bot._bot = User.objects.get(username=settings.BOT_USERNAME)
    finally:
        return get_bot._bot


def get_domain():
    """lazy getting a site domain."""
    try:
        getattr(get_domain, '_domain')
    except AttributeError:
        get_domain._domain = Site.objects.get_current().domain
    finally:
        return get_domain._domain


def get_dialog_opponent(dialog, user):
    if dialog.user1 == user:
        return dialog.user2
    return dialog.user1
