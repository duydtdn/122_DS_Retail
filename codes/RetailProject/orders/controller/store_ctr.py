
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'parent', 'slug']

class StoreFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='app', lookup_expr='icontains')

    class Meta:
        model = Store
        fields = ['id']

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StoreFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]