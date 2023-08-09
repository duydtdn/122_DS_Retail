from django.urls import path
from . import views

urlpatterns = [
    path('', views.stores, name='stores'),
    path('home', views.home, name='home'),
    path('menu', views.menu, name='menu'),
    path('detail', views.detail, name='detail'),
    path('cart', views.your_cart, name='cart'),
    path('signage', views.signage, name='signage'),
    path('place-orders', views.placeOrders, name='place-orders'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('logout', views.logout_app, name='logout_app'),
]