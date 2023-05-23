
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import OrderPlace

class OrderPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPlace
        fields = '__all__'

class OrderPlaceFilter(filters.FilterSet):
    class Meta:
        model = OrderPlace
        fields = ['id', 'table']

class OrderPlaceViewSet(viewsets.ModelViewSet):
    queryset = OrderPlace.objects.all()
    serializer_class = OrderPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]