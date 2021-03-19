from django.db import models
from django.db.models import Count, Max
from mptt.managers import TreeManager

from apps.marketplace.raw_sql import (
    CHILDREN_WITH_LOTS_COUNT,
    ROOT_WITH_LOTS_COUNT,
)

__all__ = (
    'BidQuerySet',
    'LotQuerySet',
    'CategoryQuerySet',
)

from django.utils import timezone


class CategoryQuerySet(TreeManager):

    def get_leaf_nodes(self):
        """Returns categories which has no children."""
        return (
            self.annotate(children_count=Count('children'))
            .filter(children_count=0)
        )

    def get_children_with_lots_count(self, category):
        """Returns children of category with lots count."""
        return self.raw(
            CHILDREN_WITH_LOTS_COUNT,
            params={'parent_id': category.id},
        )

    def get_roots_with_lots_count(self):
        """Returns root categories with lots count."""
        return self.raw(ROOT_WITH_LOTS_COUNT)


class BidQuerySet(models.QuerySet):

    def get_max_price_bid(self) -> models.QuerySet:
        """Returns Bid instance with max price."""
        max_price_bid = self.order_by('-price').first()
        return max_price_bid


class LotQuerySet(models.QuerySet):

    def public(self) -> models.QuerySet:
        """Returns Lot instances which is not private."""
        return self.filter(is_private=False)

    def active(self) -> models.QuerySet:
        """Returns Lot instances which is active."""
        return self.filter(is_active=True)

    def get_with_max_bid_price(self):
        """Returns lots with additional field max bid price."""
        return self.annotate(current_price=Max('bids__price'))

    def with_bids_count(self):
        """Returns count of bids from lot."""
        return self.annotate(bids_count=Count('bids'))

    def expired_by_time(self):
        """Returns lots if time expired."""
        finished_but_still_active_lots = self.filter(
            finished_at__lte=timezone.now(),
            is_active=True,
        ).select_related('owner').prefetch_related('bids__user')
        return finished_but_still_active_lots
