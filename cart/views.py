from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from products.models import Product
from .models import Cart, CartItem


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity < 0:
                messages.error(request, "La quantité doit être positive")
                return redirect('product_detail', pk=product_id)
        except (ValueError, TypeError):
            messages.error(request, "Veuillez saisir une quantité valide")
            return redirect('product_detail', pk=product_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return redirect('cart_detail')


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart/detail_cart.html'
    context_object_name = 'cart'

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_delete.html'
    success_url = reverse_lazy('cart_detail')
    context_object_name = 'cartitem'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                return CartItem.objects.none()
            cart = get_object_or_404(Cart, session_key=session_key)
        return CartItem.objects.filter(cart=cart)


class CartItemUpdateView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity'))
        if quantity > cart_item.product.stock:
            messages.error(request, 'la quantité est excédentaire')
            return redirect('cart_detail')
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart_detail')
