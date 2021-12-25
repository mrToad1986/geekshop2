import json
from datetime import datetime

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def index(request):

    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Магазин',
        'products': products_list,
        'date': datetime.now()
    }
    return render(request, 'mainapp/index.html', context)


with open(f'{settings.BASE_DIR}/mainapp/fixtures/products.json') as file:
    json_product = json.load(file)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/mainapp/fixtures/contacts.json') as f:
        json_contact = json.load(f)
    context = {
        'title': 'Контакты',
        'contacts': json_contact
    }
    return render(request, 'mainapp/contact.html', context)
