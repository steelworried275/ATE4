from django.urls import path
from .views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('list/', ProductListView.as_view(), name='products_list_legacy'),
]
