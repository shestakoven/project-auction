from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic.edit import DeleteView

from apps.messenger.forms import MessageForm
from apps.messenger.models import Message, Dialog
from apps.messenger import tasks
from apps.messenger.services import get_bot
from apps.users.models import User


class DialogView(LoginRequiredMixin, FormView):
    template_name = 'messenger/dialog.html'
    form_class = MessageForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user
        self.opponent = get_object_or_404(
            User, username=kwargs['username']
        )
        self.dialog = Dialog.objects.get_or_create(self.user, self.opponent)
        self.dialog.messages.filter(
            sender=self.opponent,
            is_read=False
        ).update(is_read=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['opponent'] = self.opponent
        context['messages_list'] = Message.objects.prefetch_related(
            'sender'
        ).filter(
            dialog=self.dialog)
        context['form'] = self.form_class()
        return context

    # def _send_message(self, text):
    #     msg = services.create_message(
    #         sender=self.user,
    #         recipient=self.opponent,
    #         text=text,
    #         msg_type=Message.MessageTypes.NEW_MESSAGE
    #     )
    #     msg.save()

    def _send_message(self, text):
        tasks.create_message.delay(
            sender_id=self.user.pk,
            recipient_id=self.opponent.pk,
            text=text,
            msg_type=Message.MessageTypes.NEW_MESSAGE
        )

    def form_valid(self, form):
        text = form.cleaned_data['message']
        self._send_message(text)
        return HttpResponseRedirect(
            reverse('dialog-with', args=[self.opponent.username])
        )


class DialogListView(LoginRequiredMixin, ListView):
    model = Dialog
    template_name = 'messenger/dialogs_list.html'

    def get_queryset(self):
        user = self.request.user
        dialogs = Dialog.objects.all().for_user(user).exclude(
            user1=get_bot()
        )

        newest_message = Message.objects.filter(
            dialog=OuterRef('pk')).order_by('-created')

        annotated_dialogs = dialogs.annotate(
            last_msg_created=Subquery(newest_message.values('created')[:1])
        )

        queryset = annotated_dialogs.order_by('-last_msg_created')
        return queryset


class NotificationsListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messenger/notifications.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(
            dialog__user1=get_bot(),
            dialog__user2=user
        ).order_by('-created')
        return queryset


class DeleteNotificationView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('notifications')

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            pk=self.request.POST.get('message_id', None),
            dialog__user2=self.request.user,
        )


class MarkNotificationAsReadView(LoginRequiredMixin, View):
    model = Message
    success_url = reverse_lazy('notifications')
    fields = ['is_read']

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.model,
            pk=self.request.POST.get('message_id', None),
            dialog__user2=request.user,
        )
        obj.is_read = True
        obj.save()
        return HttpResponseRedirect(self.success_url)
