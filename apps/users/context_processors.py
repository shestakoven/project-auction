from apps.messenger.models import Message, Dialog


def unread_messages(request):
    if not request.user.is_authenticated:
        return {}
    dialogs = Dialog.objects.all().prefetch_related('messages').for_user(request.user)
    msgs_count = dialogs.filter(
        messages__is_read=False,
        messages__type=Message.MessageTypes.NEW_MESSAGE
        ).exclude(
        messages__sender=request.user
    ).count()
    notifies_count = dialogs.filter(
        messages__is_read=False
        ).exclude(
        messages__type=Message.MessageTypes.NEW_MESSAGE
    ).count()
    context = {
        'unread_msgs': msgs_count,
        'notifies_count': notifies_count
    }
    return context
