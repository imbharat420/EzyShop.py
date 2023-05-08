from django.shortcuts import render
from shop.models import Product,Banner


def index(request):
    products = Product.objects.all().filter(is_available=True)
    banners = Banner.objects.filter(is_active=True)
    context = {
        'products':products,
        'banners':banners
    }

    return render(request, 'static_pages/index.html',context)


def welcome(request):
    return render(request, 'static_pages/welcome.html')
