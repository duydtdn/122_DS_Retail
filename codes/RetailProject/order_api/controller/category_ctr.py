
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete, ModelViewSet, ManagerOfStorePermission
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent', 'slug']

class ProductCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='app', lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['id']

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductCategoryFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['get','list','retrieve']:
            permission_classes = [AllowAnyPutDelete]
        else:
            permission_classes = [ManagerOfStorePermission]
        return [permission() for permission in permission_classes]

    
