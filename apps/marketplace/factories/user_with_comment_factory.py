import factory

from .comment_factory import CommentFactory
from apps.users.factories.create_users_factory import UsersFactory


class UserWithCommentFactory(UsersFactory):
    """Factory for generating comments from one user to many lots."""
    comments = factory.RelatedFactoryList(
        CommentFactory,
        factory_related_name='user',
        size=10,
    )
