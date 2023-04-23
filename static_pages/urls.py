
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('welcome/', views.welcome, name='welcome'), 
]