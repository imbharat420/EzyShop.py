from django.shortcuts import render
from shop.models import Product
def index(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products':products
    }

    return render(request, 'static_pages/index.html',context)


def welcome(request):
    return render(request, 'static_pages/welcome.html')
