from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Wishlist
from shop.models import Product,Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def _cart_id(request):
    Cart = request.session.session_key
    print("Session Key =",Cart)
    if not Cart:
        Cart = request.session.create()
    return Cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    print("Product =",product)
    if current_user.is_authenticated:
        product_variation = []
        print("User =",current_user)
        if request.method == 'POST': 
            print("POST =",request.POST, "Length =",len(request.POST), "Item =",request.POST.items())
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists =  CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,  user=current_user)

            ex_var_list = [] 
            id = []
            for item in cart_item: #!in cartitem check for existing variations if that product is already in cart
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                print("Item =",item,id)

            print("ex_var_list =",ex_var_list, "id =",id, "product_variation =",product_variation)
            # !MAIN STUFF FOR INCREASING AND DECREASING QUANTITY +=1
            matching_index = next((index for index, existing_variation in enumerate(ex_var_list) if set(existing_variation) == set(product_variation)), None)

            # Check if a matching variation was found
            if matching_index is not None:
                # If found, increase the quantity of the existing cart item
                item_id = id[matching_index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # If not found, add a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
            cart_item.save()
            messages.success(request, "Product added to cart.")
        return redirect('cart')

    else:
        print("else block")
        product_variation = []
        if request.method == 'POST': 
           
            for item in request.POST:
                key = item
                value = request.POST[key]
                print(key + " " + value )
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()


        is_cart_item_exists =  CartItem.objects.filter(product=product, cart=cart).exists()
        print("Cart Item Exists =",is_cart_item_exists) 
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            #existing variations check from database
            # current variation -> product variation 
            #item_id = database

            ex_var_list = [] 
            id = []
            for item in cart_item: #!in cartitem check for existing variations if that product is already in cart
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print("Existing Variation =",ex_var_list,id,product_variation)
            

            # !MAIN STUFF FOR INCREASING AND DECREASING QUANTITY +=1
            # Get the first item in the ex_var_list that matches the product_variation
            matching_index = next((index for index, existing_variation in enumerate(ex_var_list) if set(existing_variation) == set(product_variation)), None)

            # Check if a matching variation was found
            if matching_index is not None:
                # If found, increase the quantity of the existing cart item
                item_id = id[matching_index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # If not found, add a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



def remove_cart(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            print("user authenticated",request.user)
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, "Product has been removed from cart.")
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete() 
    messages.success(request, "Product has been removed from cart.")
    return redirect('cart')


def cart(request,total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            # cart_item.quantity += 1
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html',context)


@login_required(login_url='login')
def wishlist(request):
    wishlist = None
    if request.method == 'POST':
            product_id = request.POST['product_id']
            product = Product.objects.get(id=product_id)
            wishlist = Wishlist.objects.filter(user=request.user, product=product)

            if wishlist.exists():
                pass
            else:
                Wishlist.objects.create(user=request.user, product=product)
                messages.success(request, 'Product added to wishlist')
            return redirect('wishlist')
    else:
        wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'wishlist': wishlist
    }

    return render(request, 'cart/wishlist.html',context)



@login_required(login_url='login')
def remove_wishlist_item(request, product_id):
    wishlist = None
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user, product=product)
    wishlist.delete()
    messages.success(request, 'Product removed from wishlist')
    return redirect('wishlist')
    
