from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'produits'


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
