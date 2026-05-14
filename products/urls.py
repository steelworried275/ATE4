from django.urls import path

from .views import ProductDetailsView, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
]
