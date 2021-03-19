from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from apps.messenger.querysets import DialogQuerySet


class DialogManager(models.Manager):

    def get_queryset(self):
        queryset = DialogQuerySet(self.model)
        return queryset

    def get_or_create(self, sender, recipient):
        """Classic get_or_create don't work in this case."""
        try:
            return self.get(
                Q(user1=sender, user2=recipient) |
                Q(user1=recipient, user2=sender)
            )
        except ObjectDoesNotExist:
            return self.create(
                user1=sender,
                user2=recipient
            )

    def for_user(self, user):
        return self.get_queryset().for_user(user)
