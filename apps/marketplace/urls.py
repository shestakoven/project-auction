from django.conf.urls import url
from django.urls import path, include

from apps.marketplace.api.urls import router
from apps.marketplace.views import (
    HomeListView,
    LotCreateView,
    LotDetailView,
    CategoryLotsListView,
    CategoryAutocomplete,
)

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('lot/<uuid:pk>/', LotDetailView.as_view(), name='lot-detail'),
    path('create/lot/', LotCreateView.as_view(), name='lot-create'),
    path('api/v1/marketplace/', include(router.urls)),
    path('create/lot/', LotCreateView.as_view(), name='lot-create'),
    path(
        'category/<slug:slug>',
        CategoryLotsListView.as_view(),
        name='category-detail',
    ),
    url(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete',
    ),
    path('api/v1/marketplace/', include(router.urls)),
    path('qr-code/', include('qr_code.urls', namespace="qr-code")),
    path('tinymce/', include('tinymce.urls')),
]
