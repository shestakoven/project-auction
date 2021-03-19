from django import template

register = template.Library()


@register.simple_tag()
def get_unread_msgs_count(dialog, opponent):
    msgs_count = dialog.messages.filter(is_read=False, sender=opponent).count()
    if msgs_count != 0:
        return msgs_count
    return ''
