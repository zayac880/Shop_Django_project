from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return f'{self.name} ({self.category}) - {self.price}'


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='наименование')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title
