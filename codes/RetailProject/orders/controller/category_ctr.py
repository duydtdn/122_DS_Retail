
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent', 'slug']

class ProductCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='app', lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['id']

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductCategoryFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]