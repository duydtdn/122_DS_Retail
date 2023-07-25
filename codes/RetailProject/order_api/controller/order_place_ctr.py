
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework import status
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete, ManagerOfStorePermission, IsOwnerOrManager, ModelViewSet
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import OrderPlace
from order_api.admin import CustomUserSerializer
from order_api.controller.order_place_product_ctr import OrderPlaceProductSerializer
from order_api.controller.store_ctr import StoreSerializer

class OrderPlaceSerializer(serializers.ModelSerializer):
    order_items = OrderPlaceProductSerializer(many=True)
    customer = CustomUserSerializer(many=False)
    store_operate = StoreSerializer(many=False)
    total = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
            required=False, allow_null=True,
            format="%Y-%m-%d %H:%M",
    )
    updated_at = serializers.DateTimeField(
            required=False, allow_null=True,
            format="%Y-%m-%d %H:%M",
    )
    def get_total(self, obj):
        return sum(map(lambda item: item.product.price * item.amount, list(obj.order_items.all())))
    class Meta:
        model = OrderPlace
        fields = '__all__'
        include=['order_items', 'customer', 'total']

class OrderPlaceFilter(filters.FilterSet):
    class Meta:
        model = OrderPlace
        fields = ['id', 'store_operate']    
class OrderPlaceViewSet(ModelViewSet):
    queryset = OrderPlace.objects.all()
    serializer_class = OrderPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['get','list','retrieve']:
            self.permission_classes = [AllowAnyPutDelete]
        else:
            self.permission_classes = [ManagerOfStorePermission]
        return super().get_permissions()

    def get_queryset(self) :
        qs = OrderPlace.objects.all().order_by('-created_at')
        user = self.request.user
        if user.role == 'admin':
            return qs
        if user.role == 'store_manager': 
            return qs.filter(store_operate=user.store_operate)
        if user.role == 'customer': 
            return qs.filter(customer=user)
        return []
    
    def patch(self, request, pk):
        model = OrderPlace.objects.get(pk)
        serializer = OrderPlaceSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")    

def cancel_order(request):
    inputData = request.GET
    model = OrderPlace.objects.get(pk=inputData['id'])
    serializer = OrderPlaceSerializer(model, data={'status':'cancelled'}, partial=True)
    if request.user == model.customer and serializer.is_valid():
        serializer.save()
        return JsonResponse({'data':serializer.data}, status=status.HTTP_200_OK)
    return JsonResponse({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
