import django_filters.rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework import status
from rest_framework.response import Response
from RetailProject import settings
from urllib.parse import urlencode
import json

import hmac
import hashlib
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from order_api.models import OrderPlace, OrderPlaceProduct, CustomUser
from order_api.form import OrderForm
from order_api.controller.order_place_ctr import OrderPlaceSerializer
from django.views.decorators.csrf import csrf_exempt

from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice

def generatePaymentUrl(returnUrl, order: OrderPlace):
    vnp={}
    vnp['vnp_Amount'] = int(order['total'] * 100)
    vnp['vnp_Command'] = 'pay'
    vnp['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp['vnp_CurrCode'] = 'VND'
    vnp['vnp_IpAddr'] = '192.168.1.1'
    vnp['vnp_Locale'] = 'vn'
    vnp['vnp_OrderInfo'] = 'mua hang'
    vnp['vnp_OrderType'] = 'other'
    vnp['vnp_ReturnUrl'] = returnUrl
    vnp['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
    vnp['vnp_TxnRef'] = order['id']
    vnp['vnp_Version'] = '2.1.0'
    qstr = urlencode(vnp)
    signature = hmac.new(settings.VNPAY_SCRETKEY.encode('utf-8'), qstr.encode('utf-8'), hashlib.sha512).hexdigest()
    paymentUrl = settings.VNPAY_URL + '?' + qstr + '&vnp_SecureHash=' + signature
    return paymentUrl

@csrf_exempt
def get_payment_url(returnUrl,pk=None):
    try:
        order = OrderPlace.objects.get(id=pk)
    except OrderPlace.DoesNotExist:
        return ''
    serializer = OrderPlaceSerializer(order)
    url = generatePaymentUrl(returnUrl,serializer.data)
    return {'paymentUrl':url}

@csrf_exempt
def create_payment(self, request, pk=None):
    data = request.data
    return Response(data, status=status.HTTP_200_OK)

def sendOrderNotification(order):
    storeId = order.store_operate
    list_device = CustomUser.objects.filter(store_operate=storeId, role='store_manager').values_list('device_id', flat=True)
    FCMDevice.objects.send_message(
        Message(data={'message': json.dumps(OrderPlaceSerializer(order).data)}), False, list(list_device)
    )

@login_required
def create_order( request):
    if request.method == 'POST':
        form = OrderForm(data=request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer=request.user
            create_order =  order.save()
            create_order_sr = OrderPlaceSerializer(create_order).data
            items = json.loads(request.POST['items'])
            for item in items:
                productItem = OrderPlaceProduct(order_place=create_order, product_id = int(item['id']), amount=int(item['quantity']), note=item['note'])
                productItem.save()
            try:
              sendOrderNotification(create_order)
            except:
               print('sendOrderNotification error')
            
            if create_order_sr['pay_type'] == 'online_pay':
                return JsonResponse({'message':'success',
                                     'data': get_payment_url(request.META.get('HTTP_REFERER'),pk=create_order_sr['id'])}, status=status.HTTP_200_OK) 
            return JsonResponse({'message':'success', 'data': create_order_sr}, status=status.HTTP_200_OK)
        return JsonResponse({'message':form.errors}, status=status.HTTP_200_OK)
        
    return JsonResponse(status=status.HTTP_404_NOT_FOUND)

def payment_ipn(request):
  inputData = request.GET
  if inputData:
    order_id = inputData['vnp_TxnRef']
    amount = inputData['vnp_Amount']
    order_desc = inputData['vnp_OrderInfo']
    vnp_TransactionNo = inputData['vnp_TransactionNo']
    vnp_ResponseCode = inputData['vnp_ResponseCode']
    vnp_TmnCode = inputData['vnp_TmnCode']
    vnp_PayDate = inputData['vnp_PayDate']
    vnp_BankCode = inputData['vnp_BankCode']
    vnp_CardType = inputData['vnp_CardType']
    # if vnp.validate_response(settings.VNPAY_SCRETKEY):
    if True:
      # Check & Update Order Status in your Database
      # Your code here
      firstTimeUpdate = True
      totalAmount = True
      if totalAmount:
        if firstTimeUpdate:
          if vnp_ResponseCode == '00':
            model = OrderPlace.objects.get(pk=int(order_id))
            serializer = OrderPlaceSerializer(model, data={'is_paid': True}, partial=True)
            if serializer.is_valid():
                serializer.save()
                try:
                  sendOrderNotification(model)
                except: 
                   print('sendOrderNotification error') 
          else:
            print('Payment Error. Your code implement here')

          # Return VNPAY: Merchant update success
          result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
        else:
          # Already Update
          result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
      else:
        # invalid amount
        result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
    else:
      # Invalid Signature
      result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
  else:
    result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

  return result