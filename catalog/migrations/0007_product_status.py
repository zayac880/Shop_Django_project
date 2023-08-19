# Generated by Django 4.2.3 on 2023-08-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Published', 'Опубликован'), ('Draft', 'Черновик')], default='Draft', max_length=20, verbose_name='статус публикации'),
        ),
    ]