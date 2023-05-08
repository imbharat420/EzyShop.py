
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'), 
    path('cart/add_cart/<int:product_id>', views.add_cart, name='add_cart'), 
    path('cart/remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='remove_cart'), 
    path('cart/remove_cart_item/<int:product_id>/<int:cart_item_id>', views.remove_cart_item, name='remove_cart_item'), 

    # Remove wishlist
    path('wishlist/', views.wishlist, name='wishlist'), 
    path('remove_wishlist_item/<int:product_id>', views.remove_wishlist_item, name='remove_wishlist_item'), 
]