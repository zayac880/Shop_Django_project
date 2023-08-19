from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.shortcuts import render

from catalog.forms import ProductForm, VersionForm, VersionFormSet
from catalog.models import Category, Product, Blog, Version
from pytils.translit import slugify


# Домашняя
class HomeListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка продуктов на домашней странице.
    """
    model = Product
    template_name = 'catalog/home.html'

    def get_queryset(self):
        """
        Возвращает список продуктов в зависимости от статуса пользователя (сотрудник или обычный пользователь).
        """
        user = self.request.user
        if user.is_staff:
            return Product.objects.all()  # Показать все продукты для сотрудников
        else:
            return Product.objects.filter(owner=user, status='Published')  # Показать опубликованные продукты пользователя

    def get_context_data(self, *args, **kwargs):
        """
        Добавляет пользователя в контекст для использования в шаблоне.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# Категории
class CategoryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка категорий продуктов.
    """
    model = Category
    template_name = 'catalog/category.html'


# Продукты
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра деталей конкретного продукта.
    """
    model = Product
    template_name = 'catalog/product_view.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    """
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        Обработка формы при успешном валидировании.
        """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования продукта.
    Только владелец продукта или пользователи с правом change_product_status
    или принадлежащие к группе "Модераторы" могут редактировать.
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        """
        Получение объекта продукта.
        В случае, если пользователь не является владельцем продукта, вызывает Http404.
        """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для редактирования продукта.
        Включает форму версий продукта.
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['version'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['version'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Обработка формы при успешном валидировании.
        Сохраняет объект продукта и форму версий продукта.
        """
        formset = self.get_context_data()['version']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)

    def test_func(self, queryset = None):
        """
        Функция проверки наличия права доступа или принадлежности к группе модераторов.
        """
        self.object = super().get_object(queryset)
        return self.object.owner == self.request.user or self.request.user.groups.filter(
            name='managers').exists()


# Контакты
def contacts(request):
    """
    Представление для отображения и обработки контактной формы.
    """
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'catalog/contacts.html')


# БЛОГ
class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой записи в блоге.
    """
    model = Blog
    fields = ['title', 'content']
    success_url = reverse_lazy('catalog:blog')
    template_name = 'blog/blog_create.html'

    def form_valid(self, form):
        """
        Обработка формы при успешном валидировании.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления записи в блоге.
    """
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_create.html'

    def get_object(self, queryset=None):
        """
        Получение объекта Блога.
        В случае, если пользователь не является superuser, вызывает Http404.
        """
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise Http404
        return self.object

    def form_valid(self, form):
        """
        Обработка формы при успешном валидировании.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного обновления записи.
        """
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка записей блога.
    """
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Получение queryset с учетом фильтрации по опубликованным записям.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра деталей конкретной записи блога.
    """
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        """
        Получение объекта записи блога и обновление счетчика просмотров.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи блога.
    """
    model = Blog
    success_url = reverse_lazy('catalog:blog')
    template_name = 'blog/blog_delete.html'

