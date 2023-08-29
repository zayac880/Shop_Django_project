from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from .apps import CatalogConfig
from .views import contacts, CategoryListView, ProductDetailView, HomeListView, BlogCreateView,\
    BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductCreateView, ProductUpdateView


app_name = CatalogConfig.name


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('category/', cache_page(60 * 15)(CategoryListView.as_view()), name='category'),
    path('contacts/', contacts, name='contacts'),
    path('create-product/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('update-product/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('product_view/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_view'),
    path('create/', never_cache(BlogCreateView.as_view()), name='create'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('view/<int:pk>/', cache_page(60 * 15)(BlogDetailView.as_view()), name='blog_view'),
    path('edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='blog_update'),
    path('delete/<int:pk>/', never_cache(BlogDeleteView.as_view()), name='blog_delete'),
]
