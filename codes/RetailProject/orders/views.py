from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/home.html', context)


def menu(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/menu.html', context)


def detail(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/detail.html', context)


def your_cart(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/your-cart.html', context)


def signage(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/signage.html', context)