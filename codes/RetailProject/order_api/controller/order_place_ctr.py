
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from RetailProject import settings
from urllib.parse import urlencode
import json

import hmac
import hashlib
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete, ManagerOfStorePermission
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import OrderPlace, OrderPlaceProduct
from order_api.admin import CustomUserSerializer
from order_api.form import OrderForm
from order_api.controller.order_place_product_ctr import OrderPlaceProductSerializer
from order_api.controller.store_ctr import StoreSerializer
from django.db.models import F,ExpressionWrapper, FloatField, Count,  Value

class OrderPlaceSerializer(serializers.ModelSerializer):
    order_items = OrderPlaceProductSerializer(many=True)
    customer = CustomUserSerializer(many=False)
    store_operate = StoreSerializer(many=False)
    total = serializers.SerializerMethodField()

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

# def generatePaymentUrl(order: OrderPlace):
#     print(order)
#     vnp={}
#     vnp['vnp_Amount'] = int(order['price'] * 100)
#     # vnp['vnp_BankCode'] = ''
#     vnp['vnp_Command'] = 'pay'
#     vnp['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
#     vnp['vnp_CurrCode'] = 'VND'
#     vnp['vnp_IpAddr'] = '192.168.1.1'
#     vnp['vnp_Locale'] = 'vn'
#     vnp['vnp_OrderInfo'] = 'mua hang'
#     vnp['vnp_OrderType'] = 'other'
#     vnp['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
#     vnp['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
#     vnp['vnp_TxnRef'] = order['id']
#     vnp['vnp_Version'] = '2.1.0'
#     qstr = urlencode(vnp)
#     signature = hmac.new(settings.VNPAY_SCRETKEY.encode('utf-8'), qstr.encode('utf-8'), hashlib.sha512).hexdigest()
#     # signature = hashlib.sha256(settings.VNPAY_SCRETKEY.encode('utf-8') + qstr.encode('utf-8')).hexdigest()

#     paymentUrl = settings.VNPAY_URL + '?' + qstr + '&vnp_SecureHash=' + signature
#     return paymentUrl
class OrderPlaceViewSet(viewsets.ModelViewSet):
    queryset = OrderPlace.objects.all()
    serializer_class = OrderPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['get','list','retrieve']:
            permission_classes = [AllowAnyPutDelete]
        else:
            permission_classes = [ManagerOfStorePermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self) :
        qs = OrderPlace.objects.all().order_by('created_at')
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
    # @action(methods=['get'], detail=True, url_path='request-payment', url_name='request_payment')
    # def request_payment(self, request, pk=None):
    #     try:
    #         order = OrderPlace.objects.get(id=pk)
    #     except OrderPlace.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = OrderPlaceSerializer(order)
    #     url = generatePaymentUrl(serializer.data)
    #     return Response({'paymentUrl':url}, status=status.HTTP_200_OK)
    
    # @action(methods=['post'], detail=False, url_path='request-payment', url_name='request_payment')
    # def create_payment(self, request, pk=None):
    #     data = request.data
    #     return Response(data, status=status.HTTP_200_OK)

@login_required
def create_order( request):
    if request.method == 'POST':
        form = OrderForm(data=request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer=request.user
            create_order =  order.save()
            items = json.loads(request.POST['items'])
            for item in items:
                productItem = OrderPlaceProduct(order_place=create_order, product_id = int(item['id']), amount=int(item['quantity']), note=item['note'])
                productItem.save()
            return JsonResponse({'message':'success', 'data':  OrderPlaceSerializer(create_order).data}, status=status.HTTP_200_OK)
        return JsonResponse({'message':form.errors}, status=status.HTTP_200_OK)
        
    return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        
