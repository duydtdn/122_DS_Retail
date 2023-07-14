from django.shortcuts import render,redirect
# from order_api.controller.assistant.form_ast import CustomUserCreationForm
from django.contrib.auth import authenticate, login
# from order_api.controller.assistant.form_ast import CustomAuthenticationForm
from rest_framework.response import Response
from rest_framework import status
from order_api.models import Store, ProductCategory, Product, DiscountPackage
from django.contrib.auth import logout

def getStoreById(id):
    try:
        store = Store.objects.get(pk=id)
    except Store.DoesNotExist:
        store = None
    return store

def getCategoryByStore(id, isParent=False):
    categories = ProductCategory.objects.filter(store_operate__id=id, parent__isnull=isParent)
    return categories

def getProductByCategory(storeId, categoryId):
    products = []
    if (storeId):
        if (categoryId):
            products = Product.objects.filter(category__id=categoryId, store_operate__id=storeId)
        else :
            products = Product.objects.filter(store_operate__id=storeId)

    return products

def getProductByParentCategory(storeId, categoryId):
    products = []
    if (storeId):
        products = Product.objects.filter(category__parent__id=categoryId, store_operate__id=storeId)
    return products

# Create your views here.
def home(request):
    storeId  = request.GET.get('store') or 0
    category  = request.GET.get('category') or ''
    parentCategories =  getCategoryByStore(storeId, True)
    popularProducts = []
    for  ct in parentCategories:
        popularGroup = {'category': ct, 'products': getProductByParentCategory(storeId, ct.id)[:2]}
        popularProducts.append(popularGroup)
    
    context = {
        'categories': getCategoryByStore(storeId),
        'category': category, 
        'products': 'products',
        'store': getStoreById(storeId),
        'popularProducts': popularProducts,
        'banners': DiscountPackage.objects.filter(store_operate__id=storeId)
    }
    return render(request, 'order-app/home.html', context)

def menu(request):
    storeId  = request.GET.get('store') or 0
    category  = request.GET.get('category') or ''
    context = {
        'category': category, 
        'categories': getCategoryByStore(storeId),
        'products':  getProductByCategory(storeId, category),
        'store': getStoreById(storeId)

    }
    return render(request, 'order-app/menu.html', context)


def detail(request):
    storeId  = request.GET.get('store') or 0
    context = {
        'store': getStoreById(storeId)
    }
    return render(request, 'order-app/detail.html', context)


def your_cart(request):
    storeId  = request.GET.get('store') or 0

    context = {
        'categories': 'categories',
        'products': 'products',
        'store': getStoreById(storeId),

    }
    return render(request, 'order-app/your-cart.html', context)


def signage(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/signage.html', context)

def placeOrders(request):
    storeId  = request.GET.get('store') or 0
    context = {
        'store': getStoreById(storeId)
    }
    return render(request, 'order-app/place-orders.html', context)

def logout_app(request):
    storeId  = request.GET.get('store') or 0
    logout(request)
    return redirect('/order-app/home?store='+storeId)

def signup_success(request):
    return render(request, 'order-app/signup_success.html', context)
