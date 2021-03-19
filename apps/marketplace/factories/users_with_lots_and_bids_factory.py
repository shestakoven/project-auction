import factory

from .bid_factory import BidFactory
from apps.users.factories.create_users_factory import UsersFactory


class UsersWithLotsAndBidsFactory(UsersFactory):
    """Generates users with lots and bids."""
    bids = factory.RelatedFactoryList(
        factory=BidFactory,
        factory_related_name='user',
        size=5,
    )
