from django.shortcuts import render
from catalog.models import Category, Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'catalog/home.html', context)


def category(request):
    category_list = Category.objects.all()
    context = {
        'category_list': category_list
    }
    return render(request, 'catalog/category.html', context)


def product_view(request, product_id):
    product = Product.objects.filter(id=product_id)
    context = {
        'product': product[0]
    }
    print(product[0].image)
    return render(request, 'catalog/product_view.html', context)


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'catalog/contacts.html')
