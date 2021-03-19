from django.core.management import BaseCommand

from apps.marketplace.factories import BidFactory, ImageFactory


class Command(BaseCommand):
    help = 'Add n lots with bids and images in database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            type=int,
            default=5,
            help='How much lots need to add',
        )

    def handle(self, *args, **options):
        """Every lot has one bid and two images."""
        BidFactory.create_batch(size=options['n'])
        ImageFactory.create_batch(size=options['n']*2)
