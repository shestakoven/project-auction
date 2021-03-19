import factory.fuzzy
from dateutil.tz import UTC

from apps.marketplace import models
from apps.users.factories.create_users_factory import UsersFactory

DURATIONS = [choice[0] for choice in models.Lot.AuctionDuration.choices]


class LotFactory(factory.django.DjangoModelFactory):
    """Generates lots instances."""
    owner = factory.SubFactory(UsersFactory)
    category = factory.Iterator(models.Category.objects.get_leaf_nodes())
    duration = factory.fuzzy.FuzzyChoice(DURATIONS)
    started_at = factory.Faker(
        'date_time_between',
        start_date='-5d',
        end_date='now',
        tzinfo=UTC,
    )
    is_active = True
    start_price = factory.Sequence(lambda n: n + 1)
    blitz_price = factory.Sequence(lambda n: n + 10)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')

    class Meta:
        model = models.Lot
