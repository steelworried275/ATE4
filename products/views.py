from django.shortcuts import render
from django.views import View

from .data import products as sample_products


def _products():
    return [
        {
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'category': product['category'],
            'stock': product['countInStock'],
            'image_url': product['image'],
        }
        for product in sample_products
    ]


class ProductListView(View):
    def get(self, request):
        return render(request, 'products/product_list.html', {'products': _products()})
