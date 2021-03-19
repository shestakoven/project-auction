from random import choice

import factory

from apps.messenger.models import Message, Dialog
from apps.users.factories.create_users_factory import UsersFactory


class DialogsFactory(factory.django.DjangoModelFactory):
    """Generate dialogs."""
    user1 = factory.SubFactory(UsersFactory)
    user2 = factory.SubFactory(UsersFactory)

    class Meta:
        model = Dialog


class MessagesFactory(factory.django.DjangoModelFactory):
    """Generate messages."""
    dialog = factory.SubFactory(DialogsFactory)
    type = Message.MessageTypes.NEW_MESSAGE
    message = factory.Faker('text')

    @factory.LazyAttribute
    def sender(self):
        return choice([self.dialog.user1, self.dialog.user2])

    class Meta:
        model = Message


class UsersWithMessagesFactory(DialogsFactory):
    """Generate dialogs with 5 messages."""
    dialogs = factory.RelatedFactoryList(
        MessagesFactory,
        factory_related_name='dialog',
        size=5,
    )
