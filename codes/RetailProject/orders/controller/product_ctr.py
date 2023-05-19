
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import Product
from orders.controller.category_ctr import ProductCategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False)
    class Meta:
        model = Product
        fields = '__all__'

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__id',lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['id']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]