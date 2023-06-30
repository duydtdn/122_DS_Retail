
import django_filters.rest_framework as filters
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from order_api.models import CustomUser


from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status

class AuthenticationViewSet(viewsets.ModelViewSet):
     
    @action(methods=['post'], detail=False, url_path='custom-login', url_name='custom_login')
    def custom_login(self, request, pk=None):
        if request.method == 'POST':
        
            phone_number =  request.POST.get('phone_number')
            password = request.POST.get('password')
            user = authenticate(username="customer1", password="customer")
            print(user)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Incorrect phone or password'},status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
