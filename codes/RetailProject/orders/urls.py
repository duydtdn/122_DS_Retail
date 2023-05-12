from django.urls import re_path as url
from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home2'),
    path('menu', views.menu, name='menu'),
    path('detail', views.detail, name='detail'),
    path('cart', views.your_cart, name='your-cart'),
    path('signage', views.signage, name='signage'),
]