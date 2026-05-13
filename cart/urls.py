from django.urls import path

from .views import add_to_cart, cart_detail


urlpatterns = [
    path('', cart_detail, name='cart'),
    path('add/<str:product_id>/', add_to_cart, name='add_to_cart'),
]
