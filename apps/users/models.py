from urllib.parse import urljoin

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models.functions import Lower
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

__all__ = (
    'User',
)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model.

    Attributes:
        first_name (str): First name.
        last_name (str): Last, family name.
        username (str): Unique user's name.
        email (str): E-mail, uses for authentication.
        phone (str): User's phone number.
        is_active (bool): Can user log in to the system.
        is_staff (bool): Can user access to admin interface.
        date_joined (datetime): Date when the account was created.
        avatar (obj: image): User's avatar.

    Nested attributes:
        is_superuser (bool): The user can super access to admin UI.
        groups(Manager): The groups this user belongs to.
        user_permissions(Manager): Specified permissions for this user.
        last_login (datetime): Last date when user login to the system.

    """
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    first_name = models.CharField(
        max_length=255,
        verbose_name=_("First name"),
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name"),
        blank=True,
    )
    username = models.CharField(
        max_length=40,
        unique=True,
        verbose_name=_("Username"),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message=_('Only letters and numbers are allowed')
            ),
        ]
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_("Email"),
    )
    phone = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Phone"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Is staff"),
        help_text=_("The user will have access to admin interface."),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date joined"),
    )
    avatar = ProcessedImageField(
        upload_to='avatars',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
    )

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('email',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name:
            full_name = '{first_name} {last_name}'.format(
                first_name=self.last_name,
                last_name=self.first_name,
            )
            return full_name.strip()
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_admin_change_url(self) -> str:
        """Get admin change URL.

        Build full url (host + path) to standard Django admin page for
        object like:

            https://api.sitename.com/admin/users/user/234/

        """

        assert self.id, "Instance must have an ID"

        return urljoin(
            settings.DJANGO_SITE_BASE_HOST,
            reverse('admin:users_user_change', args=(self.id,)),
        )

    def clean(self):
        same_usernames = (
            User.objects
                .annotate(username_lower=Lower('username'))
                .filter(username_lower=self.username.lower())
                .exclude(pk=self.pk)
        )
        if same_usernames.exists():
            raise ValidationError({'username': _('User with this Username already exists.')})
        super().clean()
