
import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from RetailProject import settings
from urllib.parse import urlencode
import hmac
import hashlib
from datetime import datetime

from orders.controller.assistant.authenticated_ast import AllowAnyPutDelete
from orders.controller.assistant.pagination_ast import CustomPagination
from orders.models import OrderPlace
from orders.controller.order_place_product_ctr import OrderPlaceProductSerializer

class OrderPlaceSerializer(serializers.ModelSerializer):
    # order_places = OrderPlaceProductSerializer(many=True)

    class Meta:
        model = OrderPlace
        fields = '__all__'

class OrderPlaceFilter(filters.FilterSet):
    class Meta:
        model = OrderPlace
        fields = ['id', 'table']    

def generatePaymentUrl(order: OrderPlace):
    print(order)
    vnp={}
    vnp['vnp_Amount'] = int(order['price'] * 100)
    # vnp['vnp_BankCode'] = ''
    vnp['vnp_Command'] = 'pay'
    vnp['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp['vnp_CurrCode'] = 'VND'
    vnp['vnp_IpAddr'] = '192.168.1.1'
    vnp['vnp_Locale'] = 'vn'
    vnp['vnp_OrderInfo'] = 'mua hang'
    vnp['vnp_OrderType'] = 'other'
    vnp['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
    vnp['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
    vnp['vnp_TxnRef'] = order['id']
    vnp['vnp_Version'] = '2.1.0'
    qstr = urlencode(vnp)
    signature = hmac.new(settings.VNPAY_SCRETKEY.encode('utf-8'), qstr.encode('utf-8'), hashlib.sha512).hexdigest()
    # signature = hashlib.sha256(settings.VNPAY_SCRETKEY.encode('utf-8') + qstr.encode('utf-8')).hexdigest()

    paymentUrl = settings.VNPAY_URL + '?' + qstr + '&vnp_SecureHash=' + signature
    return paymentUrl


class OrderPlaceViewSet(viewsets.ModelViewSet):
    queryset = OrderPlace.objects.all()
    serializer_class = OrderPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderPlaceFilter
    pagination_class = CustomPagination
    permission_classes = [AllowAnyPutDelete]
    
    @action(methods=['get'], detail=True, url_path='request-payment', url_name='request_payment')
    def request_payment(self, request, pk=None):
        try:
            order = OrderPlace.objects.get(id=pk)
        except OrderPlace.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderPlaceSerializer(order)
        url = generatePaymentUrl(serializer.data)
        return Response({'paymentUrl':url}, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, url_path='request-payment', url_name='request_payment')
    def create_payment(self, request, pk=None):
        data = request.data
        return Response(data, status=status.HTTP_200_OK)
        
