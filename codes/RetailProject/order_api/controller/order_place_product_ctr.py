
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import OrderPlaceProduct
from order_api.controller.product_ctr import ProductSerializer

class OrderPlaceProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    price = serializers.SerializerMethodField()
    def get_price(self, obj):
        return obj.amount * obj.product.price
    class Meta:
        model = OrderPlaceProduct
        fields = '__all__'
        include=['product', 'price']

class OrderPlaceProductFilter(filters.FilterSet):
    class Meta:
        model = OrderPlaceProduct
        fields = ['id', 'product', 'order_place_id']

class OrderPlaceProductViewSet(viewsets.ModelViewSet):
    queryset = OrderPlaceProduct.objects.all()
    serializer_class = OrderPlaceProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceProductFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]
