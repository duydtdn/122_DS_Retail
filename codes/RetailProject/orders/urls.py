from rest_framework import routers
from django.urls import re_path as url
from django.urls import include
from django.urls import path
from . import views
from orders.controller.product_ctr import ProductViewSet
from orders.controller.category_ctr import ProductCategoryViewSet
from orders.controller.discount_package_ctr import DiscountPackageViewSet
from orders.controller.table_ctr import TableViewSet


app_name = 'order'
api_router = routers.DefaultRouter()
api_router.register(r'products', ProductViewSet)
api_router.register(r'categories', ProductCategoryViewSet)
api_router.register(r'discount-packages', DiscountPackageViewSet)
api_router.register(r'tables', TableViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home2'),
    path('menu', views.menu, name='menu'),
    path('detail', views.detail, name='detail'),
    path('cart', views.your_cart, name='your-cart'),
    path('signage', views.signage, name='signage'),
]