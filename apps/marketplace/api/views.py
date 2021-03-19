from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.marketplace.api.serializers import (
    CategorySerializer,
    CreateCommentSerializer,
)
from apps.marketplace.models import Category


class CategoryChildrenViewSet(
        mixins.ListModelMixin,
        GenericViewSet,
):
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        """Returns list of children categories."""
        category_id = self.kwargs['id']
        category = get_object_or_404(Category, pk=category_id)
        queryset = Category.objects.get_children_with_lots_count(category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateCommentViewSet(
        mixins.CreateModelMixin,
        GenericViewSet,
):
    """ViewSet to create comment on lot page."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
