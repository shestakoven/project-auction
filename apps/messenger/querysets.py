from django.db import models
from django.db.models import Q


class DialogQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(Q(user1=user) | Q(user2=user))
