import json

from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()

        with open('data.json', 'r', encoding='utf-8') as json_file:
            catalog_data = json.load(json_file)

        categories_from_create = []
        product_from_create = []
        for catalog_item in catalog_data:
            if catalog_item['model'] == "catalog.category":
                categories_from_create.append(
                    Category(**catalog_item['fields'])
                )
            if catalog_item['model'] == "catalog.product":
                product_from_create.append(
                    Product(**catalog_item['fields'])
                )

        Product.objects.bulk_create(product_from_create)
        Category.objects.bulk_create(categories_from_create)

