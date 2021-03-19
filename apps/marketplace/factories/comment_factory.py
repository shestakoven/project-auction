import factory

from apps.marketplace import models
from .lot_factory import LotFactory
from apps.users.factories.create_users_factory import UsersFactory


class CommentFactory(factory.django.DjangoModelFactory):
    """Initialization of comment factory."""
    user = factory.SubFactory(UsersFactory)
    lot = factory.SubFactory(LotFactory)
    text = factory.Faker('text')

    class Meta:
        model = models.Comment
