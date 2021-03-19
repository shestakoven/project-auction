from os.path import join

from django import template
from django.conf import settings

from apps.messenger.models import Message

TEMPLATE_DIR = join(settings.BASE_DIR, 'templates', 'messenger', 'notifies_icons')

register = template.Library()

ICONS_BY_MSG_TYPE = {
    Message.MessageTypes.LOT_SOLD: join(TEMPLATE_DIR, 'icon_sold.xml'),
    Message.MessageTypes.NEW_BID: join(TEMPLATE_DIR, 'icon_new_bid.xml'),
    Message.MessageTypes.BID_BROKE: join(TEMPLATE_DIR, 'icon_bid_broke.xml'),
}


@register.simple_tag()
def get_icon(message_type):
    return ICONS_BY_MSG_TYPE[message_type]
