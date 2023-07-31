from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.shortcuts import render
from catalog.models import Category, Product, Blog
from pytils.translit import slugify


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).all()[:5]


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_view.html'


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'catalog/contacts.html')


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content']
    success_url = reverse_lazy('catalog:blog')
    template_name = 'blog/blog_create.html'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content']
    #success_url = reverse_lazy('catalog:blog')
    template_name = 'blog/blog_create.html'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object (self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
    template_name = 'blog/blog_delete.html'
