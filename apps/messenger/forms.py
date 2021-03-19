from django.forms import ModelForm

from apps.messenger.models import Message


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = [
            'message',
        ]
