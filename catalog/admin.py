from django.contrib import admin
from .models import Category, Product, Version


class CategoryAdmin(admin.ModelAdmin):
    """
    Класс для настройки административного представления модели Category.
    Определяет поля, отображаемые в списке объектов.
    """
    list_display = ('id', 'name', 'is_active')


class ProductAdmin(admin.ModelAdmin):
    """
    Класс для настройки административного представления модели Product.
    Определяет поля, отображаемые в списке объектов, фильтрацию и поиск.
    """
    list_display = ('id', 'name', 'price', 'category', 'is_active')
    list_filter = ('category',)
    search_fields = ('name', 'description')


class VersionAdmin(admin.ModelAdmin):
    """
    Класс для настройки административного представления модели Version.
    Определяет поля, отображаемые в списке объектов и фильтрацию.
    """
    list_display = ('id', 'product', 'version_number', 'version_name', 'is_current_version')
    list_filter = ('product',)


# Регистрация моделей с соответствующими классами административных представлений
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Version, VersionAdmin)
