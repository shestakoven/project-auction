from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.db.models import Max

from .models import User
from apps.marketplace.models import Lot


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/account.html'

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_lots'] = Lot.objects.filter(
            owner=self.request.user
        ).prefetch_related('images', 'comments')
        context['bidded_lots'] = Lot.objects.filter(
            bids__user=self.request.user
        ).annotate(Max('bids__price'))
        return context


class OtherProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/other_account.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get(self, request, *args, **kwargs):
        if self.request.user.username == kwargs['username']:
            return HttpResponseRedirect(reverse_lazy('account'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_lots'] = Lot.objects.filter(
            owner=kwargs['object'],
            is_private=False,
        ).prefetch_related('images', 'comments')
        context['bidded_lots'] = Lot.objects.filter(
            bids__user=kwargs['object'],
            is_private=False,
        ).annotate(Max('bids__price'))
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'username',
        'avatar',
        'phone',
    ]
    template_name = 'users/account_update_form.html'
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object
