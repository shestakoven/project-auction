from dal import autocomplete
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from apps.marketplace.models import Bid, Image, Lot


class BidForm(ModelForm):
    """Form to make a bid.

    Placed on the lot page.

    """

    class Meta:
        model = Bid
        fields = ('price',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _("Bid must not be less than current price"),
            }
        )
        self.fields['price'].label = False


class LotCreateForm(ModelForm):
    """Form for creating a lot."""

    class Meta:
        model = Lot
        fields = (
            'category',
            'duration',
            'start_price',
            'blitz_price',
            'is_private',
            'title',
            'description',
        )
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['is_private'].widget.attrs.update({
            'class': 'form-check-input',
        })
        self.fields['duration'].widget.attrs.update({
            'class': 'form-select',
        })


class ImageForm(forms.ModelForm):
    """Form to add images to a lot.

    Placed on the lot create page.

    """

    class Meta:
        model = Image
        fields = ('image',)
        labels = {'image': False}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'type': "file",
            }
        )
