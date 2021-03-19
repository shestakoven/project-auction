from django.core.management import BaseCommand

from apps.messenger.factories.create_messages_factory import UsersWithMessagesFactory


class Command(BaseCommand):
    help = 'Add n dialogs in database with 5 messages.'

    def add_arguments(self, parser):
        parser.add_argument(
            'n',
            type=int,
            default=5,
            help='How much dialogs need to add',
        )

    def handle(self, *args, **options):
        UsersWithMessagesFactory.create_batch(size=options['n'])
