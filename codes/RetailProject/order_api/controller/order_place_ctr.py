
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

from order_api.controller.assistant.authenticated_ast import AllowAnyPutDelete
from order_api.controller.assistant.pagination_ast import CustomPagination
from order_api.models import OrderPlace, OrderPlaceProduct
from order_api.form import OrderForm
from order_api.controller.order_place_product_ctr import OrderPlaceProductSerializer

class OrderPlaceSerializer(serializers.ModelSerializer):
    order_items = OrderPlaceProductSerializer(many=True)

    class Meta:
        model = OrderPlace
        fields = '__all__'
        include='order_items'

class OrderPlaceFilter(filters.FilterSet):
    class Meta:
        model = OrderPlace
        fields = ['id']    

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
    queryset = OrderPlace.objects.all().order_by('order_date')
    serializer_class = OrderPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]

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
        
