from django.contrib import admin
from django.urls import path

from .apps import CatalogConfig
from .views import home, contacts, category, product_view


app_name = CatalogConfig.name


urlpatterns = [
    path('', home, name='home'),
    path('category/', category, name='category'),
    path('contacts/', contacts, name='contacts'),
    path('product_view/<int:product_id>/', product_view, name='product_view')
]
