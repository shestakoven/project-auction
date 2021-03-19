import factory
from dateutil.tz import UTC

from apps.marketplace import models
from .lot_factory import LotFactory
from apps.users.factories.create_users_factory import UsersFactory


class BidFactory(factory.django.DjangoModelFactory):
    """Generates bids instances."""
    user = factory.SubFactory(UsersFactory)
    lot = factory.SubFactory(LotFactory)
    date = factory.Faker(
        'date_time_between',
        start_date='-2d',
        end_date='now',
        tzinfo=UTC,
    )
    price = factory.Sequence(lambda n: n + 2)
    is_top = True

    class Meta:
        model = models.Bid
