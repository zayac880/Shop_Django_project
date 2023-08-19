from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}

STATUS_CHOICES = (
        ('Published', 'Опубликован'),
        ('Draft', 'Черновик'),
    )


class Category(models.Model):
    """
    Модель для категорий продуктов.
    """
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель для продуктов.
    """
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='активность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft', verbose_name='статус публикации')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    class Meta:
        """
        Мета-класс модели Product с описанием кастомных прав доступа.
        """

        permissions = [
            ("change_product_status", "Может изменять статус продукта"),
            ("change_product_description", "Может изменять описание продукта"),
            ("change_product_category", "Может изменять категорию продукта"),
        ]

    def __str__(self):
        return f'{self.name} ({self.category}) - {self.price}'


class Blog(models.Model):
    """
    Модель для записей блога.
    """
    title = models.CharField(max_length=100, verbose_name='наименование')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title


class Version(models.Model):
    """
    Модель для версий продуктов.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.CharField(max_length=20, verbose_name='номер версии')
    version_name = models.CharField(max_length=100, verbose_name='название версии')
    is_current_version = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.product.name} - Версия {self.version_number}'
