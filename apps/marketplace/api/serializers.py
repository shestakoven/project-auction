from django.utils import formats
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.marketplace.models import Category, Comment
from apps.users.models import User


class CategorySerializer(ModelSerializer):
    """Category model serializer.

    Attributes:
        is_leaf_node (bool): True if instance has no children, False otherwise.
        absolute_url (str): Url of the category page.
        lots_count (int): The number of lots that belong to this category.

    """
    absolute_url = serializers.CharField(
        source='get_absolute_url',
        read_only=True,
    )
    lots_count = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'parent',
            'slug',
            'is_leaf_node',
            'absolute_url',
            'lots_count',
        )


class UserSerializer(ModelSerializer):
    """Serializer for user."""
    class Meta:
        model = User
        fields = (
            'username',
        )


class ParentCommentSerializer(ModelSerializer):
    """Serializer for parent comment."""
    user_data = UserSerializer(source='user')

    class Meta:
        model = Comment
        fields = (
            'id',
            'user_data',
        )


class CreateCommentSerializer(ModelSerializer):
    """Serializer to create comment on lot page."""
    created_at_format = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    parent_data = ParentCommentSerializer(source='parent', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'lot',
            'parent',
            'parent_data',
            'text',
            'created_at_format',
        )

    def get_created_at_format(self, obj):
        """Returns format `created_at` field."""
        return formats.date_format(obj.created_at, 'd N Y H:i')
