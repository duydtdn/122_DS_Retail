
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import OrderPlaceProduct

class OrderPlaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPlaceProduct
        fields = '__all__'

class OrderPlaceProductFilter(filters.FilterSet):
    class Meta:
        model = OrderPlaceProduct
        fields = ['id', 'product', 'order_place_id']

class OrderPlaceProductProductViewSet(viewsets.ModelViewSet):
    queryset = OrderPlaceProduct.objects.all()
    serializer_class = OrderPlaceProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceProductFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]