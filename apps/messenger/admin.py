from django.contrib import admin

from .models import Message
from .models import Dialog


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user1',
        'user2',
        'created',
        'modified',
    )
    search_fields = (
        'user1',
        'user2',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dialog',
        'message',
        'created',
        'modified',
    )
    search_fields = (
        'message',
        'dialog'
    )
    list_filter = (
        'type',
    )
