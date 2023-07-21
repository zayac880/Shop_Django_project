from django.contrib import admin
from django.urls import path

from .views import home, contacts, category, catalog

urlpatterns = [
    path('', home, name='home/'),
    path('category/', category, name='category/'),
    path('catalog/', catalog, name='catalog/'),
    path('contacts/', contacts, name='contacts/'),
]
