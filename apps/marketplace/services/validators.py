from decimal import Decimal


def check_valid_bid_price(lot: 'Lot', bid_price: Decimal) -> bool:
    """Checks user bid price is valid.

    Args:
        lot (Lot): Lot object.
        bid_price (int): Price which user want to bet.

    Returns:
        bool: True if price of bid is valid, False otherwise.

    """
    if bid_price <= lot.current_price:
        return False
    if bid_price > lot.blitz_price:
        return False
    return True


def check_bidder_not_lot_owner(lot: 'Lot', user: 'User') -> bool:
    """Lot owner can't make bid his own lots.

    Args:
        lot (Lot): Lot object.
        user (User): User which makes bid to lot.

    Returns:
        bool: True if user not owner of current lot, False otherwise.

    """
    return lot.owner.pk != user.pk


def check_bidder_not_last_same_bidder(lot: 'Lot', bidder: 'User') -> bool:
    """Bidder can't make a bid two times a row.

    Args:
        lot(Lot): Lot object.
        bidder (User): User which makes bid to lot.

    Returns:
        bool: True if last bidder nor current bidder, False otherwise.

    """
    last_bid = lot.bids.get_max_price_bid()
    if last_bid:
        return bidder.pk != last_bid.user.pk
    return True


def check_blitz_price_less_than_start_price(
        start_price: Decimal,
        blitz_price: Decimal,
) -> bool:
    """Blitz price must be greater than start price.

    Args:
        start_price (float): Price at which trade starts.
        blitz_price (float): The price at which the lot can be redeemed.

    Returns:
        bool: True if blitz price less than start price, False otherwise.

    """
    return blitz_price <= start_price


def check_bid_to_inactive_lot_not_allowed(lot: 'Lot') -> bool:
    """Make a bid to inactive lot is not allowed.

    Args:
        lot (Lot): Lot instance.

    Returns:
        bool: True if lot is not active, False is lot is active.

    """
    return not lot.is_active
