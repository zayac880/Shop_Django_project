from django.urls import path

from .apps import CatalogConfig
from .views import contacts, CategoryListView, ProductDetailView, HomeListView, BlogCreateView,\
    BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductCreateView, ProductUpdateView


app_name = CatalogConfig.name


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('contacts/', contacts, name='contacts'),
    path('create-product/', ProductCreateView.as_view(), name='create_product'),
    path('update-product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product_view/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
