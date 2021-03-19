from rest_framework import routers

from apps.marketplace.api.views import (
    CreateCommentViewSet,
    CategoryChildrenViewSet
)

router = routers.DefaultRouter()
router.register(
    r'category-children/(?P<id>[0-9]+)',
    CategoryChildrenViewSet,
    basename='category-children',
)
router.register(
    'create-comment',
    CreateCommentViewSet,
    basename='create-comment',
)
