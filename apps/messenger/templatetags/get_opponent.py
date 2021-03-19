from django import template

from apps.messenger.services import get_dialog_opponent

register = template.Library()


@register.simple_tag(takes_context=True)
def get_opponent(context, dialog):
    return get_dialog_opponent(dialog=dialog, user=context['user'])
