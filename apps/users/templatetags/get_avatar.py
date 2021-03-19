import os

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def users_avatar(user):
    """Set default avatar if user have not."""
    if not user.avatar:
        return os.path.join(settings.STATIC_URL, 'users', 'default_avatar.png')
    return user.avatar.url
