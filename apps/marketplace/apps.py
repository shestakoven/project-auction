from django.apps import AppConfig


class MarketplaceAppConfig(AppConfig):
    """Configuration for Marketplace app."""
    name = 'apps.marketplace'
    verbose_name = "Marketplace"

    def ready(self):
        from . import signals
