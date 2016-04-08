from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^products/$', views.ProductsListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(),
        name='product_detail'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^like/(?P<product_id>[0-9]+)$', views.like_product, name='like')
]