import pytest
from django.utils import timezone
from django.core import mail
from ..users.factories.create_users_factory import UsersFactory
from .factories import BidFactory, LotFactory, LotWithBidsFactory
from .models import Lot
from .services import (
    check_bidder_not_lot_owner,
    check_valid_bid_price,
    deactivate_lot,
    deactivate_lots_and_send_notifications,
)


@pytest.fixture
def user():
    return UsersFactory()


@pytest.fixture
def lot():
    return LotFactory()


@pytest.fixture
def expired_lot():
    lot = LotFactory()
    lot.finished_at = timezone.now()
    lot.save()
    return lot


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Give all tests access to db."""
    return pytest.mark.django_db


def test_active_queryset(lot):
    """Expected lots only with `is_active` equal True."""
    LotFactory.create(is_active=False)
    result = list(Lot.objects.active())
    assert result == [lot]


def test_get_wit_max_price_attribute():
    """Expected attribute `current_price` at lot."""
    LotWithBidsFactory.create_batch(1)
    lot = Lot.objects.get_with_max_bid_price().first()
    assert hasattr(lot, 'current_price')


@pytest.mark.parametrize(
    "bid_price, expected",
    [(200, True), (50, False), (400, False)],
)
def test_check_valid_bid_price_to_lot_without_bids(bid_price, expected):
    """Test checks user bid price to lot without bids."""
    LotFactory.create(start_price=100, blitz_price=300)
    lot = Lot.objects.first()
    result = check_valid_bid_price(lot, bid_price)
    assert result == expected


@pytest.mark.parametrize("bid_price, expected", [(200, True), (149, False)])
def test_check_valid_bid_price_to_lot_with_bids(bid_price, expected):
    """Test checks user bid price to lot with bids."""
    LotFactory.create(start_price=100, blitz_price=300)
    lot = Lot.objects.first()
    BidFactory(lot=lot, price=150)
    result = check_valid_bid_price(lot, bid_price)
    assert result == expected


def test_deactivate_lot(lot):
    """Test `deactivate_lot` func."""
    lot = Lot.objects.first()
    deactivate_lot(lot)
    assert not lot.is_active


def test_check_bidder_is_lot_owner(lot):
    """Expected False if bidder is lot owner."""
    lot = Lot.objects.first()
    user = lot.owner
    result = check_bidder_not_lot_owner(lot, user)
    assert not result


def test_check_if_bidder_not_lot_owner(lot, user):
    """Expected True if bidder isn't lot owner."""
    result = check_bidder_not_lot_owner(lot, user)
    assert result


def test_expired_by_time_queryset(expired_lot):
    """Expected lots with `is_active` equal True
    and `finished_at` less than timezone.now.
    """
    LotFactory()
    result = list(Lot.objects.expired_by_time())
    assert result == [expired_lot]


def test_deactivate_lots_and_send_notifications(lot, expired_lot):
    """Expected that all expired lots will be deactivated.

    And notifications will send to owner and winner of auction.

    """
    expired_lots = Lot.objects.expired_by_time()
    deactivate_lots_and_send_notifications(expired_lots)
    expired_lot.refresh_from_db()
    send_to = mail.outbox[0].to[0]
    assert expired_lot.owner.email == send_to
    assert not expired_lot.is_active
    assert expired_lot not in list(Lot.objects.expired_by_time())
