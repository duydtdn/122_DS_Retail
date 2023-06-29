
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import DiscountPackage

class DiscountPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPackage
        fields = '__all__'

class DiscountPackageFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='app', lookup_expr='icontains')
    class Meta:
        model = DiscountPackage
        fields = ['id']

class DiscountPackageViewSet(viewsets.ModelViewSet):
    queryset = DiscountPackage.objects.all()
    serializer_class = DiscountPackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DiscountPackageFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]