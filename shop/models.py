from django.db import models
from category.models import Category
from django.urls import reverse


class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/products', max_length=255)

    def __str__(self):
        return self.product.product_name
        
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


class Banner(models.Model):
    banner_title = models.CharField(max_length=50)
    banner_subtitle = models.CharField(max_length=50)
    banner_image = models.ImageField(upload_to='shop/banner', max_length=255)
    banner_url = models.ForeignKey(Product, on_delete=models.CASCADE,default=1)
    banner_alt = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.banner_title
    
    def get_url(self):
        return reverse('products_by_category', args=[self.category.slug])

    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'