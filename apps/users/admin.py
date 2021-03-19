from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

__all__ = (
    'UserAdmin',
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """User admin.

    Admin class definitions for ``User`` model.

    """
    search_fields = ('first_name', 'last_name', 'email')
    list_display = (
        'id',
        'email',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'avatar',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        'last_login',
        'date_joined',
    )
    ordering = ('id',)
