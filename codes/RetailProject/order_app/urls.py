from rest_framework import routers
from django.urls import re_path as url
from django.urls import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home2'),
    path('menu', views.menu, name='menu'),
    path('detail', views.detail, name='detail'),
    path('cart', views.your_cart, name='your-cart'),
    path('signage', views.signage, name='signage'),
    path('place-orders', views.placeOrders, name='place-orders'),
    # path('signup', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    # path('login', views.login, name='login'), 
    path('logout', views.logout, name='logout'),
    # path('custom-login/', views.custom_login, name='custom_login'),
]