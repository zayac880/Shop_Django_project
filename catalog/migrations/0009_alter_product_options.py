# Generated by Django 4.2.3 on 2023-08-19 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('change_product_status', 'Может изменять статус продукта'), ('change_product_description', 'Может изменять описание продукта'), ('change_product_category', 'Может изменять категорию продукта')]},
        ),
    ]