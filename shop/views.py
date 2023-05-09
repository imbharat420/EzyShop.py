from django.shortcuts import render , get_object_or_404, redirect
from .models import Product, ProductGallery,Banner
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.db.models import Q

def shop(request,category_slug=None):
    categories = None
    category = None
    products = None 
    banners = None
    categories = Category.objects.all()
    if category_slug != None:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category,is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    # banner_by_category
    try:
        banners = Banner.objects.filter(category=category,is_active=True)
    except Exception as e:
        pass 

    context = {
        "products":products,
        'categories':categories,
        "total": products_count,
        "banners":banners,
        "category":category,
    }
    return render(request, 'shop/shop.html',context)



def product_details(request,category_slug,product_slug):
    single_product = None
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart =  CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
        
    except Exception as e:
        raise e
    

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
    # print(single_product)
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "product_gallery": product_gallery,
    }
    return render(request, 'shop/single-product.html',context)


def search(request):
    products = None
    products_count = 0
    # cheapest,recommended,recent,most expensive
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
    if 'sort' in request.GET:
        sortItem =  request.GET['sort']
        if sortItem == 'cheapest':
            products = Product.objects.order_by('price')
            products_count = products.count()
        if sortItem == 'recomended': 
            # @TODO: add recommended logic by max sales
            products = Product.objects.order_by('-price')
            products_count = products.count()
        if sortItem == 'recent':
            products = Product.objects.order_by('-created_date')
            products_count = products.count()
        if sortItem == 'expensive':
            products = Product.objects.order_by('-price')
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count
    }
    return render(request, 'shop/shop-category.html',context)


def category(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products
    }

    return render(request, 'shop/shop-category.html',context)


def product(request):
    return redirect('shop')

