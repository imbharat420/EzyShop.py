
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'), 
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'), 


    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'), 
    path('resetpassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetpassword_validate'), 
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]