from django.urls import path

from .views import SimpleLoginView


urlpatterns = [
    path('login/', SimpleLoginView.as_view(), name='login'),
]
