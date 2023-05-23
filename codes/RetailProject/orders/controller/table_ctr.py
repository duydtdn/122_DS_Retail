
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TableFilter(filters.FilterSet):
    class Meta:
        model = Table
        fields = ['id', 'is_available']

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TableFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]