from rest_framework import routers
from order_api.controller.product_ctr import ProductViewSet
from order_api.controller.category_ctr import ProductCategoryViewSet
from order_api.controller.discount_package_ctr import DiscountPackageViewSet
from order_api.controller.table_ctr import TableViewSet
from order_api.controller.order_place_ctr import OrderPlaceViewSet
from order_api.controller.authentication_ctr import AuthenticationViewSet


app_name = 'order-app'
api_router = routers.DefaultRouter()
api_router.register(r'products', ProductViewSet)
api_router.register(r'categories', ProductCategoryViewSet)
api_router.register(r'discount-packages', DiscountPackageViewSet)
api_router.register(r'tables', TableViewSet)
api_router.register(r'orders', OrderPlaceViewSet)
api_router.register(r'auth', AuthenticationViewSet, basename="custom_login")