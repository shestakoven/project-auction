from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Bid, Category, Comment, Image, Lot

__all__ = (
    'CategoryAdmin',
    'BidAdmin',
    'LotAdmin',
    'ImageAdmin',
    'CommentAdmin',
)


class ImagePreviewMixin:
    """Mixin with one function which returns preview of image."""
    def get_preview_image(self, obj):
        """Returns preview of image.

        Args:
            obj (object): Instance which has `image` attribute.

        Returns:
            str: String in html format which contains image url.

        """
        try:
            return format_html('<img src="{}" height="200"/>', obj.image.url)
        except ValueError:
            return _("Place to preview")

    get_preview_image.short_description = _("Preview")


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Category admin.

    Admin class definitions for ``Category`` model.

    """
    mptt_indent_field = 'name'
    list_per_page = 500
    search_fields = (
        'name',
    )
    raw_id_fields = (
        'parent',
    )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Bid admin.

    Admin class definitions for ``Bid`` model.

    """
    fields = (
        'id',
        'user',
        'lot',
        'price',
        'date',
        'is_top',
    )
    list_display = (
        'user',
        'lot',
        'price',
        'date',
        'is_top',
    )
    readonly_fields = (
        'id',
        'date',
    )
    search_fields = (
        'user',
        'lot',
    )


class BidInline(admin.TabularInline):
    """Bid inline.

    Uses in Lot admin.

    """
    model = Bid
    fields = (
        'user',
        'price',
        'date',
    )
    readonly_fields = (
        'date',
    )
    ordering = (
        '-price',
    )
    extra = 0


@admin.register(Image)
class ImageAdmin(ImagePreviewMixin, SortableAdminMixin, admin.ModelAdmin):
    """Image admin.

    Admin class definitions for ``Image`` model.

    """
    fields = (
        'image',
        'lot',
        'get_preview_image',
    )
    raw_id_fields = (
        'lot',
    )
    readonly_fields = (
        'get_preview_image',
    )


class ImageInline(ImagePreviewMixin, SortableInlineAdminMixin, admin.TabularInline):
    """Image inline.

    Uses in Lot admin.

    """
    model = Image
    fields = (
        'image',
        'number',
        'get_preview_image',
    )
    readonly_fields = (
        'get_preview_image',
    )
    extra = 0


class CommentInLine(admin.TabularInline):
    """Comment inline.

    Uses in Lot admin.

    """
    model = Comment
    fields = (
        'user',
        'lot',
        'text',
    )
    extra = 0


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    """Lot admin.

    Admin class definitions for ``Lot`` model.

    """
    fields = (
        'id',
        'owner',
        'category',
        'is_active',
        'duration',
        'started_at',
        'finished_at',
        'start_price',
        'blitz_price',
        'title',
        'description',
    )
    list_display = (
        'title',
        'started_at',
        'finished_at',
        'category',
        'start_price',
        'blitz_price',
        'is_active',
        'is_private',
    )
    list_filter = (
        'is_active',
    )
    search_fields = (
        'title',
    )
    raw_id_fields = (
        'category',
    )
    list_editable = (
        'is_active',
        'is_private',
    )
    readonly_fields = (
        'id',
        'started_at',
    )
    inlines = (
        ImageInline,
        BidInline,
        CommentInLine,
    )


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    """Comment admin.

    Admin class definitions for ``Comment`` model.

    """
    fields = (
        'user',
        'lot',
        'text',
        'parent',
        'created_at',
    )
    list_display = (
        'user',
        'lot',
        'text',
        'created_at',
    )
    readonly_fields = (
        'created_at',
    )
