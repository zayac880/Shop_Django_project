import json
from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()

        with open('data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        categories_from_create = []
        product_from_create = []
        category_pk = {}  # Словарь для хранения соответствия идентификаторов категорий объектам категорий

        # Создаем категории и сохраняем их в словаре category_mapping
        for catalog_item in data:
            if catalog_item['model'] == "catalog.category":
                category, created = Category.objects.get_or_create(pk=catalog_item['pk'], defaults=catalog_item['fields'])
                category_pk[catalog_item['pk']] = category

        # Создаем продукты, устанавливая соответствующую категорию через объект категории
        for catalog_item in data:
            if catalog_item['model'] == "catalog.product":
                category_id = catalog_item['fields']['category']
                if category_id in category_pk:
                    catalog_item['fields']['category'] = category_pk[category_id]
                    product_from_create.append(Product(**catalog_item['fields']))

        Product.objects.bulk_create(product_from_create)
        Category.objects.bulk_create(categories_from_create)
