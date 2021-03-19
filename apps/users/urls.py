from allauth.account import views
from django.urls import path

from apps.users.views import ProfileView, ProfileEditView, OtherProfileView

urlpatterns = [
    path('account/', ProfileView.as_view(), name='account'),
    path('account/edit', ProfileEditView.as_view(), name='edit-account'),
    path('account/<str:username>/', OtherProfileView.as_view(), name='other-account'),
]
