
from rest_framework import status
from order_api.models import  CustomUser
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Đăng nhập thành công'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Sai tài khoản hoặc mật khẩu'},status=status.HTTP_404_NOT_FOUND)

    else:
        return JsonResponse({},status=status.HTTP_404_NOT_FOUND)
@csrf_exempt
def custom_register(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.create_user(username=username, password=password)
            if user is not None:
                return JsonResponse({'message': 'Đăng ký thành công'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Có lỗi xảy ra'},status=status.HTTP_404_NOT_FOUND)

        except Exception :
            return JsonResponse({'error': Exception},status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({},status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def custom_add_device_id(request):
    if request.method == 'POST':
        device_id =  request.POST.get('device_id')
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if user is not None:
                user.device_id = device_id
                user.save()
                return JsonResponse({'message': 'success'}, status=status.HTTP_200_OK)

            else:
                return JsonResponse({'message': 'Có lỗi xảy ra'},status=status.HTTP_404_NOT_FOUND)

        except Exception :
            return JsonResponse({'error': Exception},status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({},status=status.HTTP_404_NOT_FOUND)
