from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView

from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def get_cart_queryset(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)

    session_key = request.session.session_key
    if not session_key:
        return Cart.objects.none()
    return Cart.objects.filter(session_key=session_key)


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Veuillez saisir une quantite valide.')
            return redirect('product_detail', pk=product_id)

        if quantity < 1:
            messages.error(request, 'La quantite doit etre positive.')
            return redirect('product_detail', pk=product_id)

        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0},
        )

        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, 'La quantite demandee depasse le stock disponible.')
            if created:
                cart_item.delete()
            return redirect('product_detail', pk=product_id)

        cart_item.quantity = new_quantity
        cart_item.save()
        return redirect('cart_detail')


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart/detail_cart.html'
    context_object_name = 'cart'

    def get_object(self):
        return get_or_create_cart(self.request)


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_delete.html'
    success_url = reverse_lazy('cart_detail')
    context_object_name = 'cartitem'

    def get_queryset(self):
        return CartItem.objects.filter(cart__in=get_cart_queryset(self.request))


class CartItemUpdateView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__in=get_cart_queryset(request),
        )

        try:
            quantity = int(request.POST.get('quantity'))
        except (TypeError, ValueError):
            messages.error(request, 'Veuillez saisir une quantite valide.')
            return redirect('cart_detail')

        if quantity < 1:
            messages.error(request, 'La quantite doit etre positive.')
            return redirect('cart_detail')

        if quantity > cart_item.product.stock:
            messages.error(request, 'La quantite demandee depasse le stock disponible.')
            return redirect('cart_detail')

        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart_detail')
