from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from products.data import products


CART_SESSION_KEY = 'cart'


def _get_product(product_id):
    return next((product for product in products if product['id'] == product_id), None)


def _get_cart_items(session_cart):
    cart_items = []
    cart_count = 0
    total = 0

    for product_id, quantity in session_cart.items():
        product = _get_product(product_id)
        if not product:
            continue

        line_total = product['price'] * quantity
        cart_count += quantity
        total += line_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total,
        })

    return cart_items, cart_count, total


def cart_detail(request):
    session_cart = request.session.get(CART_SESSION_KEY, {})
    cart_items, cart_count, total = _get_cart_items(session_cart)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': total,
    })


@require_POST
def add_to_cart(request, product_id):
    product = _get_product(product_id)

    if not product:
        messages.error(request, 'Produit introuvable.')
        return redirect('products_list')

    cart = request.session.get(CART_SESSION_KEY, {})
    current_quantity = int(cart.get(product_id, 0))

    if current_quantity >= product['countInStock']:
        messages.warning(request, 'Le stock disponible est deja dans votre panier.')
        return redirect('cart')

    cart[product_id] = current_quantity + 1
    request.session[CART_SESSION_KEY] = cart
    messages.success(request, f"{product['name']} a ete ajoute au panier.")

    return redirect('cart')
