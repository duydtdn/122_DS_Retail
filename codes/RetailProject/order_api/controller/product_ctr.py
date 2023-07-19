
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete, ManagerOfStorePermission
from order_api.controller.assistant.authenticated_ast import ModelViewSet, AdminRoleFilter, ManagerRoleFilter, CustomerRoleFilter
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import Product
from order_api.controller.category_ctr import ProductCategorySerializer
from rest_framework.permissions import IsAdminUser

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False)
    class Meta:
        model = Product
        fields = '__all__'

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__id',lookup_expr='icontains')
    store = filters.CharFilter(field_name='store_operate__id',lookup_expr='exact')
    class Meta:
        model = Product
        fields = ['id']

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['get','list','retrieve']:
            permission_classes = [AllowAnyPutDelete]
        else:
            permission_classes = [ManagerOfStorePermission]
        return [permission() for permission in permission_classes]
