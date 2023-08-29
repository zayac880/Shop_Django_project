from django.core.cache import cache
from .models import Category


def get_categories():
    categories = cache.get('categories_list')
    if categories is None:
        categories = Category.objects.all()
        cache.set('categories_list', categories)
    return categories
