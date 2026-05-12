from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_product_image_alter_product_categorie_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'En attente'),
                        ('processing', 'En cours'),
                        ('shipped', 'Expédiée'),
                        ('delivered', 'Livrée'),
                        ('cancelled', 'Annulée'),
                    ],
                    default='pending',
                    max_length=20,
                    verbose_name='Statut',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('shipping_address', models.TextField(verbose_name='Adresse de livraison')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='orders',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Utilisateur',
                )),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantité')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix unitaire')),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='orders.order',
                    verbose_name='Commande',
                )),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='order_items',
                    to='products.product',
                    verbose_name='Produit',
                )),
            ],
            options={
                'verbose_name': 'Article de commande',
                'verbose_name_plural': 'Articles de commande',
            },
        ),
    ]
