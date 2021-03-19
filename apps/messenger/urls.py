from django.urls import path

from apps.messenger.views import (
    DialogView,
    DialogListView,
    NotificationsListView, MarkNotificationAsReadView, DeleteNotificationView,
)

urlpatterns = [
    path('dialogs/', DialogListView.as_view(), name='dialogs'),
    path('dialogs/<str:username>/', DialogView.as_view(), name='dialog-with'),
    path('notifications/', NotificationsListView.as_view(), name='notifications'),
    path('read', MarkNotificationAsReadView.as_view(), name='mark-as-read'),
    path('delete', DeleteNotificationView.as_view(), name='delete-notification'),
]
