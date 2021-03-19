import factory

from .bid_factory import BidFactory
from .lot_factory import LotFactory


class LotWithBidsFactory(LotFactory):
    """Generates lot with bids."""
    bids = factory.RelatedFactoryList(
        factory=BidFactory,
        factory_related_name='lot',
        size=5,
    )
