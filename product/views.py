import json
import logging
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import six

from product.forms import SignUpForm
from product.models import Product, Like
from product.forms import CommentForm
from product.utils import is_liked_product, ajax_required

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


class ProductsListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'product_list.html'
    ordering = 'name'

    def get_queryset(self):
        qs = super(ProductsListView, self).get_queryset()
        custom_order = ['like_count', '-like_count']
        self.ordering = self.request.GET.get('order_by', None)
        if self.ordering in custom_order:
            qs = qs.annotate(like_count=Count('like')).order_by(
                self.ordering)

        ordering = self.get_ordering()
        if ordering and ordering not in custom_order:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['ordering'] = self.get_ordering()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        form = CommentForm()
        return render(
            self.request, 'product_detail.html',
            {'form': form, 'product': self.get_object()}
        )

    def post(self, request, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user \
                if self.request.user.is_authenticated() else None
            comment.product = self.get_object()
            comment.save()
            messages.success(self.request, 'Comment successfully added')
            return render(
                self.request, 'product_detail.html',
                {'form': CommentForm(), 'product': self.get_object()})
        else:
            messages.error(self.request, 'Can\'t add you comment')
            return render(
                self.request, 'product_detail.html',
                {'form': form, 'product': self.get_object()})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.cleaned_data['is_staff'] = True
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('product_list'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
@require_POST
@ajax_required
def like_product(request, product_id):
    data = {}
    product = Product.objects.filter(id=product_id).first()
    if product and not is_liked_product(product, request.user):
        try:
            Like.objects.create(product=product, user=request.user)
            messages.success(request, 'like was added', extra_tags='add')
        except Exception as e:
            info = 'Can\'t add like'
            messages.error(request, info)
            logger.info(info)
            logger.error(e)
    elif product and is_liked_product(product, request.user):
        try:
            Like.objects.filter(product=product, user=request.user).delete()
            messages.success(request, 'like was removed', extra_tags='delete')
        except Exception as e:
            info = 'Can\'t remove like'
            messages.error(request, info)
            logger.info(info)
            logger.error(e)
    else:
        messages.error(request, 'Wrong product')
    data['response'] = 'ajaxResponse'
    return HttpResponse(json.dumps(data), content_type='application/json')
