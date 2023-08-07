from django.contrib import admin
from .models import Category, Product, Version


# Класс для настройки отображения модели Category в административной панели
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')  # Отображение id и наименования категории в списке


# Класс для настройки отображения модели Product в административной панели
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_active')  # Отображение id, названия, цены и категории продукта в списке
    list_filter = ('category',)  # Фильтрация продуктов по категории
    search_fields = ('name', 'description')  # Поиск по названию и описанию продукта


class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_name', 'is_current_version')
    list_filter = ('product',)


# Регистрация моделей с соответствующими классами административных представлений
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Version, VersionAdmin)
