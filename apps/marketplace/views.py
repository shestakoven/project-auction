from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin

from apps.marketplace.forms import BidForm, ImageForm, LotCreateForm
from apps.marketplace.models import Category, Image, Lot


class CategoryLotsListView(ListView):
    model = Lot
    template_name = 'marketplace/lot_list.html'
    paginate_by = 10
    context_object_name = 'lots'

    # Such things as category or image will display on main page.
    # That's why here complex queryset.
    queryset = (
        Lot.objects.active()
        .public()
        .with_bids_count()
        .get_with_max_bid_price()
        .select_related('category')
        .prefetch_related('images')
        .order_by('-started_at')
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Returns context with list of root categories and lots count."""
        context = super().get_context_data()
        context['categories'] = Category.objects.get_roots_with_lots_count()
        return context

    def get_queryset(self):
        """Returns lots that belong to a category.

        If category has descendants also returns lots
        that belong to a subcategory.

        """
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        descendants = category.get_descendants(include_self=True)
        return self.queryset.filter(category__in=descendants)


class HomeListView(ListView):
    """View to display content on main page."""
    model = Lot
    template_name = 'marketplace/lot_list.html'
    paginate_by = 10
    context_object_name = 'lots'

    # Such things as category or image will display on main page.
    # That's why here complex queryset.
    queryset = (
        Lot.objects.active()
        .public()
        .with_bids_count()
        .get_with_max_bid_price()
        .select_related('category')
        .prefetch_related('images')
        .order_by('-started_at')
    )

    def get_queryset(self):
        """Filter queryset if request has 'search' parameter."""
        search = self.request.GET.get('search', '')
        lots = self.queryset
        if search:
            lots = lots.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        return lots

    def get_context_data(self, *, object_list=None, **kwargs):
        """Returns context with list of root categories and lots count."""
        context = super().get_context_data()
        context['categories'] = Category.objects.get_roots_with_lots_count()
        return context


class LotDetailView(FormMixin, DetailView):
    """View to display page with one lot.

    Also implements FormMixin to display BidForm.

    """
    model = Lot
    template_name = 'marketplace/lot_detail.html'
    context_object_name = 'lot'
    form_class = BidForm

    # Such things as images and users who made bid to this lot
    # will display on lot detail page. That's why here complex queryset.
    queryset = (
        Lot.objects.prefetch_related('images', 'bids__user', 'comments__user')
        .with_bids_count()
    )

    def get_context_data(self, **kwargs):
        if 'bid_form' not in kwargs:
            kwargs['bid_form'] = self.get_form()

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        """Returns on the same page after user make a successful bid."""
        return reverse('lot-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        """If bid form is valid then redirects at the same page.

        Otherwise redirects at the same page but display errors over bid form

        """
        self.object = self.get_object()
        bid_form = self.get_form()
        bid_form.instance.lot = self.object

        if request.user.is_anonymous:
            return redirect('account_login')

        bid_form.instance.user = request.user

        if bid_form.is_valid():
            bid_form.save()
            return self.form_valid(bid_form)
        return self.render_to_response(
            self.get_context_data(bid_form=bid_form),
        )


class LotCreateView(LoginRequiredMixin, CreateView):
    """View to display a page with a lot creation form.

    Also implements ImageInlineFormSet for adding images to the lot.

    """
    form_class = LotCreateForm
    template_name = 'marketplace/lot_create.html'
    model = Lot
    ImageInlineFormSet = inlineformset_factory(
        Lot,
        Image,
        form=ImageForm,
        min_num=1,
        max_num=6,
        extra=6,
        can_delete=False,
    )

    def get_context_data(self, **kwargs):
        """Lot and images for lot it's separate models.

         That's why here formset use.

         """
        kwargs['formset'] = self.ImageInlineFormSet()
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """Validate and save lot with images.

        If lot form and image formset is valid then redirects at the lot page.
        Otherwise redirects at the same page but display errors over lot form

        """
        lot_form = self.form_class(request.POST)
        lot_form.instance.owner = request.user
        image_formset = self.ImageInlineFormSet(
            request.POST or None,
            request.FILES or None,
        )

        if lot_form.is_valid() and image_formset.is_valid():
            return self.form_valid(lot_form, image_formset)

        return render(
            request,
            'marketplace/lot_create.html',
            context={'form': lot_form, 'formset': image_formset},
        )

    def form_valid(self, lot_form, image_formset):
        """Called if all forms are valid.

        Saves the lot and its images to the base.

        """
        lot = lot_form.save()
        image_formset.instance = lot
        image_formset.save()
        return redirect('lot-detail', pk=lot.id)


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, result):
        return ' / '.join(
            category.name for category in result.get_ancestors(
                include_self=True,
            )
        )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.get_leaf_nodes()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
