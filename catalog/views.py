from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def category(request):
    return render(request, 'catalog/category.html')


def catalog(request):
    return render(request, 'catalog/catalog.html')


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'catalog/contacts.html')
