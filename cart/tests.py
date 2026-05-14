from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product
from .models import Cart, CartItem


class CartSessionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Tests', slug='tests')
        cls.product = Product.objects.create(
            name='Set de couverts inox 24 pieces',
            description='Un ensemble complet de couverts.',
            prix=299,
            stock=10,
            categorie=category,
        )

    def test_add_to_cart_creates_session_cart_item(self):
        response = self.client.post(
            reverse('add_cart', args=[self.product.id]),
            {'quantity': 1},
        )

        self.assertRedirects(response, reverse('cart_detail'))
        cart = Cart.objects.get(session_key=self.client.session.session_key)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_increments_existing_product(self):
        self.client.post(reverse('add_cart', args=[self.product.id]), {'quantity': 1})
        self.client.post(reverse('add_cart', args=[self.product.id]), {'quantity': 2})

        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_cart_page_renders_session_items(self):
        self.client.post(reverse('add_cart', args=[self.product.id]), {'quantity': 1})

        response = self.client.get(reverse('cart_detail'))

        self.assertContains(response, 'Set de couverts inox')
        self.assertContains(response, '299.00 MAD')
