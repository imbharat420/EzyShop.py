from django.contrib import admin
from .models import Cart,CartItem,Wishlist


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')



class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date_added')

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Wishlist,WishlistAdmin)