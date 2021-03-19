import factory.fuzzy

from apps.marketplace import models


class ImageFactory(factory.django.DjangoModelFactory):
    """Generates images for lots."""
    image = factory.django.ImageField(
        color=factory.fuzzy.FuzzyChoice(['magenta', 'blue', 'green'])
    )
    lot = factory.Iterator(models.Lot.objects.all())

    class Meta:
        model = models.Image
