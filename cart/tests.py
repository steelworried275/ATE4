from django.test import TestCase
from django.urls import reverse


class CartSessionTests(TestCase):
    def test_add_to_cart_stores_product_in_session(self):
        response = self.client.post(reverse('add_to_cart', args=['1']))

        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(self.client.session['cart'], {'1': 1})

    def test_add_to_cart_increments_existing_product(self):
        self.client.post(reverse('add_to_cart', args=['1']))
        self.client.post(reverse('add_to_cart', args=['1']))

        self.assertEqual(self.client.session['cart'], {'1': 2})

    def test_cart_page_renders_session_items(self):
        self.client.post(reverse('add_to_cart', args=['1']))

        response = self.client.get(reverse('cart'))

        self.assertContains(response, 'Set de couverts inox')
        self.assertContains(response, '299 DH')
