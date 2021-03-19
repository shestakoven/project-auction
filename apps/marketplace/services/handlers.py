from django.conf import settings
from django.core.mail import send_mail


def deactivate_lot(lot: 'Lot') -> None:
    """Change lot attribute `is_active` to False.

    Args:
        lot (Lot): Lot object.

    """
    lot.is_active = False
    lot.save()


def deactivate_lots_and_send_notifications(expired_lots):
    """Deactivates expired lots.

    Also sends notifications to lot owner and winner of auction.

    """

    for lot in expired_lots:
        deactivate_lot(lot)
        owner = lot.owner
        won_bid = lot.bids.get_max_price_bid()
        subject = f"The auction for the '{lot.title}' lot has ended"
        message = (
                    "Hello, {user}. "
                    "The auction for the '{lot}' lot has ended."
        )
        if not won_bid:
            # Send email to lot owner if no one made a bet.
            send_mail(
                subject=subject,
                message=(
                    message.format(user=owner.username, lot=lot.title) +
                    "Nobody placed bets on the lot :("
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[owner.email],
                fail_silently=False,
            )
            continue

        # Send email to lot owner.
        send_mail(
            subject=subject,
            message=(
                message.format(user=owner.username, lot=lot.title) +
                f"Contact the winning bidder {won_bid.user.email}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner.email],
            fail_silently=False,
        )

        # Send email to winner of auction.
        send_mail(
            subject=subject,
            message=(
                message.format(user=won_bid.user.username, lot=lot.title) +
                f"Congratulations! You are won!"
                f"Contact the owner of the lots {owner.email}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[won_bid.user.email],
            fail_silently=False,
        )
