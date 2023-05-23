
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.http import JsonResponse, HttpResponse

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import OrderPlaceProduct
from orders.models import OrderPlace
from orders.controller.order_place_ctr import OrderPlaceSerializer
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

    @action(detail=False, methods=['get'], url_path ="order-tables")
    def get_tables(self,request) : 
        tableParam = request.GET.get('tableId')
        print(tableParam)
        orders = OrderPlace.objects.filter(table = 3)
        ordersSerializer = OrderPlaceSerializer(orders, many=True)
        print(ordersSerializer.data)
        return Response(ordersSerializer.data, status=status.HTTP_200_OK)