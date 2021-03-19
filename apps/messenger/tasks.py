from celery import shared_task

from apps.messenger.models import Message, Dialog
from apps.users.models import User


@shared_task()
def create_message(
        sender_id,
        recipient_id,
        text,
        msg_type=Message.MessageTypes.NEW_MESSAGE
):
    """
    Create message instance without saving.
    Message won't save in db for future operations, like moderation.

    Args:
        sender_id (obj): User's pk.
        recipient_id (obj): User's pk.
        text (str): Message text.
        msg_type (obj): Type of message from MessageTypes
            (NEW_BID, NEW_MESSAGE, etc.)

    Returns:
          obj: Message instance

    """
    sender = User.objects.get(pk=sender_id)
    recipient = User.objects.get(pk=recipient_id)
    dialog = Dialog.objects.get_or_create(sender, recipient)
    Message.objects.create(
        dialog=dialog,
        sender=sender,
        type=msg_type,
        message=text
    )
