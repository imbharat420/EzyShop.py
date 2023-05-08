from django.db import models
from shop.models import Product
from shop.models import Variation
from user.models import User

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    

    def sub_total(self):
        return self.product.price * self.quantity

    def __str_(self):
        return self.product
    

class Wishlist(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)  
    date_added = models.DateField(auto_now_add=True)
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str_(self):
        return self.product
