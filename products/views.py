from django.shortcuts import render
from django.views import View
from django.db import DatabaseError

from .data import products as sample_products
from .models import Product

SAMPLE_IMAGE_URL = '/media/products/Perf_pan_shopify.webp'


def _product_image_url(product):
    if getattr(product, 'image', None):
        try:
            return product.image.url
        except ValueError:
            return ''
    return ''


def _database_products():
    queryset = Product.objects.select_related('categorie').all().order_by('name')
    return [
        {
            'name': product.name,
            'description': product.description,
            'price': product.prix,
            'category': product.categorie.name if product.categorie else 'Sans categorie',
            'stock': product.stock,
            'image_url': _product_image_url(product),
        }
        for product in queryset
    ]


def _sample_products():
    return [
        {
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'category': product['category'],
            'stock': product['countInStock'],
            'image_url': SAMPLE_IMAGE_URL,
        }
        for product in sample_products
    ]


class ProductListView(View):
    def get(self, request):
        try:
            products = _database_products()
        except DatabaseError:
            products = []

        if not products:
            products = _sample_products()

        return render(request, 'products/product_list.html', {'products': products})
