from django.db import migrations


def seed_products(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')

    data = [
        {
            'category': 'Couverts',
            'name': 'Set de couverts inox 24 pièces',
            'image': 'products/set-couverts-inox-24.png',
            'description': 'Un ensemble complet de couverts en acier inoxydable pour 6 personnes.',
            'price': 299,
            'stock': 10,
        },
        {
            'category': 'Couteaux',
            'name': 'Set de couteaux de table 6 pièces',
            'image': 'products/set-couteaux-table-6.png',
            'description': 'Des couteaux élégants et résistants pour les repas quotidiens.',
            'price': 149,
            'stock': 10,
        },
        {
            'category': 'Couverts premium',
            'name': 'Ménagère dorée 16 pièces',
            'image': 'products/menagere-doree-16.png',
            'description': 'Un set de couverts dorés au design moderne pour une table raffinée.',
            'price': 399,
            'stock': 10,
        },
        {
            'category': 'Cuillères',
            'name': 'Set de cuillères à dessert 12 pièces',
            'image': 'products/set-cuilleres-dessert-12.png',
            'description': 'Des cuillères pratiques pour desserts, cafés et goûters.',
            'price': 99,
            'stock': 10,
        },
        {
            'category': 'Fourchettes',
            'name': 'Set de fourchettes inox 12 pièces',
            'image': 'products/set-fourchettes-inox-12.png',
            'description': 'Des fourchettes solides et faciles à nettoyer pour un usage quotidien.',
            'price': 119,
            'stock': 10,
        },
        {
            'category': 'Enfants',
            'name': 'Couverts enfants colorés 4 pièces',
            'image': 'products/couverts-enfants-colores-4.png',
            'description': 'Un petit set sécurisé et coloré adapté aux enfants.',
            'price': 79,
            'stock': 10,
        },
    ]

    for item in data:
        cat, _ = Category.objects.get_or_create(
            name=item['category'],
            defaults={'slug': item['category'].lower().replace(' ', '-')}
        )
        if not Product.objects.filter(name=item['name']).exists():
            Product.objects.create(
                name=item['name'],
                image=item['image'],
                description=item['description'],
                prix=item['price'],
                stock=item['stock'],
                categorie=cat,
            )


def unseed_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_options'),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
