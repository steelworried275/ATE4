from django.db import models
from users.models import CustomUser
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Utilisateur'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Statut'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créée le')
    shipping_address = models.TextField(verbose_name='Adresse de livraison')

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Commande'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Produit'
    )
    quantity = models.PositiveIntegerField(verbose_name='Quantité')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix unitaire')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Commande #{self.order.id})"

    class Meta:
        verbose_name = 'Article de commande'
        verbose_name_plural = 'Articles de commande'
