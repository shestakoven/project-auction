from django.core.management import BaseCommand

from apps.users.factories.create_users_factory import UsersFactory


class Command(BaseCommand):
    help = 'Add n users in database.'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='How much users need to add')

    def handle(self, *args, **options):
        UsersFactory.create_batch(size=options['n'])
