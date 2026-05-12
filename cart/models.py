from django.db import models
from users.models import CustomUser
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Utilisateur'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')

    def __str__(self):
        return f"Panier de {self.user.username}"

    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Panier'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Produit'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantité')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = 'Article du panier'
        verbose_name_plural = 'Articles du panier'
