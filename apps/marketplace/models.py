import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as tinymce_models

from .querysets import BidQuerySet, CategoryQuerySet, LotQuerySet
from .services import (
    check_bid_to_inactive_lot_not_allowed,
    check_bidder_not_last_same_bidder,
    check_bidder_not_lot_owner,
    check_blitz_price_less_than_start_price,
    check_valid_bid_price,
    get_random_filename,
)

__all__ = (
    'Category',
    'Bid',
    'Lot',
    'Image',
    'Comment',
)


def upload_lot_image_to(_, filename: str) -> str:
    return settings.LOTS_IMAGE_STORING_PATH_TEMPLATE.format(
        filename=get_random_filename(filename),
    )


class Category(MPTTModel):
    """Categories model.

    Each category has name and parent.
    If a category has no parent, it means a first level category.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent"),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
    )

    objects = CategoryQuerySet()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category-detail', args=[self.slug])


class Bid(models.Model):
    """Bids model.

    Store all bids from user to lots.

    """
    user = models.ForeignKey(
        to='users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='bids',
        verbose_name=_("User"),
    )
    lot = models.ForeignKey(
        to='Lot',
        null=True,
        on_delete=models.SET_NULL,
        related_name='bids',
        verbose_name=_("Lot"),
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date"),
    )
    price = models.DecimalField(
        validators=(
            MinValueValidator(0.00),
        ),
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    is_top = models.BooleanField(
        default=True,
        verbose_name=_("Top"),
    )

    objects = BidQuerySet().as_manager()

    class Meta:
        ordering = ('-price',)
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")

    def clean(self):
        """Checks if the bid for the lot is valid.

        Raises:
            ValidationError: If price of bid is invalid
                or user is owner of lot
                or user is last bidder of lot
                or lot is inactive.

        """
        super().clean()

        if not check_valid_bid_price(self.lot, self.price):
            raise ValidationError(
                _(
                    "Bid price can't be less than current price "
                    "or can't be greater than blitz price."
                ),
                code='invalid_price',
            )
        if not check_bidder_not_lot_owner(self.lot, self.user):
            raise ValidationError(
                _("Lot owner can't make bid to his own lots."),
                code='invalid_user',
            )
        if not check_bidder_not_last_same_bidder(self.lot, self.user):
            raise ValidationError(
                _("Last bid of this lot yours."),
                code='invalid_user',
            )
        if check_bid_to_inactive_lot_not_allowed(self.lot):
            raise ValidationError(
                _("Bidding for this lot is over."),
                code='invalid_lot',
            )


class CurrentPrice:
    """Lot current price descriptor."""
    def __get__(self, instance, objtype=None):
        if current_price := instance._current_price:
            return current_price

        if max_bid := instance.bids.get_max_price_bid():
            return max_bid.price

        return instance.start_price

    def __set__(self, instance, value):
        instance._current_price = value


class Lot(models.Model):
    """Lot model.

    Store all lots.

    """

    class AuctionDuration(models.IntegerChoices):
        ONE_DAY = 1, _("1 day")
        THREE_DAYS = 3, _("3 days")
        ONE_WEEK = 7, _("1 week")
        TWO_WEEKS = 14, _("2 weeks")
        THIRTY_DAYS = 30, _("30 days")

    _current_price = None

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    owner = models.ForeignKey(
        to='users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='lots',
        verbose_name=_("Owner"),
    )
    commentators = models.ManyToManyField(
        to='users.User',
        through='Comment',
        related_name='commented_lots',
        verbose_name=_("Commentators"),
    )
    category = models.ForeignKey(
        to='Category',
        null=True,
        on_delete=models.SET_NULL,
        related_name='lots',
        verbose_name=_("Category"),
    )
    duration = models.PositiveSmallIntegerField(
        choices=AuctionDuration.choices,
        default=AuctionDuration.ONE_WEEK,
        verbose_name=_("Duration"),
        help_text=_("Duration of trading."),
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Started at"),
        help_text=_("Date of creation of the lot and the start of trading."),
    )
    finished_at = models.DateTimeField(
        null=True,
        verbose_name=_("Finished at"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Is private"),
        help_text=_("If true, the lot will not be displayed in the lot feed.")
    )
    start_price = models.DecimalField(
        validators=(
            MinValueValidator(0.00),
        ),
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Start price"),
        help_text=_("Bidding will start at this price."),
    )
    blitz_price = models.DecimalField(
        null=True,
        validators=(
            MinValueValidator(0.00),
        ),
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Blitz price"),
        help_text=_("The lot can be redeemed at this price."),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    description = tinymce_models.HTMLField(
        verbose_name=_("Description"),
    )

    current_price = CurrentPrice()

    objects = LotQuerySet().as_manager()

    class Meta:
        ordering = ('-started_at',)
        verbose_name = _("Lot")
        verbose_name_plural = _("Lots")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('lot-detail', args=[self.pk])

    def clean(self):
        """Checks if the lot is valid.

        Raises:
            ValidationError: If price blitz price less than start price.

        """
        super().clean()

        if check_blitz_price_less_than_start_price(
                self.start_price,
                self.blitz_price,
        ):
            raise ValidationError(
                _("Blitz price can't be less than start price."),
                code='invalid_price',
            )

    @property
    def left_time(self):
        """Time until the end of trading without microseconds."""
        delta = self.finished_at - timezone.now()
        return str(delta).split('.')[0]

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False


class Image(models.Model):
    """The "Image" model for lots."""
    image = models.ImageField(
        upload_to=upload_lot_image_to,
        verbose_name=_("Image"),
    )
    number = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        verbose_name=_("Number"),
        help_text=_("Needed for ordering images."),
    )
    lot = models.ForeignKey(
        to='Lot',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Lot"),
    )

    class Meta(object):
        ordering = ('number',)
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f'{self.number} - {self.lot_id}'


class Comment(MPTTModel):
    """Comment model.

    Model stores all comments from lot.

    """
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_("User"),
    )
    lot = models.ForeignKey(
        to='Lot',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_("Lot"),
    )
    text = models.CharField(
        max_length=255,
        verbose_name=_("Text"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    parent = TreeForeignKey(
        to='self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_("Parent"),
    )

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        db_table = 'comments'
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f'{self.text}'
