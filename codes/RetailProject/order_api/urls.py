from rest_framework import routers
from order_api.controller.product_ctr import ProductViewSet
from order_api.controller.category_ctr import ProductCategoryViewSet
from order_api.controller.discount_package_ctr import DiscountPackageViewSet
from order_api.controller.table_ctr import TableViewSet
from order_api.controller.order_place_ctr import OrderPlaceViewSet
from order_api.controller.authentication_ctr import  custom_login, custom_register, custom_add_device_id
from order_api.controller.order_place_ctr import  create_order
from django.urls import path


app_name = 'order-app'
api_router = routers.DefaultRouter()
api_router.register(r'products', ProductViewSet)
api_router.register(r'categories', ProductCategoryViewSet)
api_router.register(r'discount-packages', DiscountPackageViewSet)
api_router.register(r'tables', TableViewSet)
api_router.register(r'orders', OrderPlaceViewSet)

api_urlpatterns = [
    path('auth/custom-login/', custom_login, name='custom_login'),
    path('auth/custom-register/', custom_register, name='custom_register'),
    path('create-order/', create_order, name='create_order'),
    path('add-device/', custom_add_device_id, name='custom_add_device_id'),
]