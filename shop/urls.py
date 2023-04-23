
from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category, name='category'), 
    path('category/search', views.search, name='search'),
    path('shop/', views.shop, name='shop'), 
    path('shop/<slug:category_slug>/', views.shop, name='products_by_category'), 
    path('shop/<slug:category_slug>/', views.shop, name='products_by_category'), 
    path('shop/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_detail'),
    path('product/', views.product, name='product'), 
] 