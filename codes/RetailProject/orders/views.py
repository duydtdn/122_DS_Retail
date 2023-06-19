from django.shortcuts import render,redirect
from orders.controller.assistant.form_ast import CustomUserCreationForm
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

def placeOrders(request):
    context = {
        'categories': 'categories',
        'products': 'products',
    }
    return render(request, 'order-app/place-orders.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')   # Replace 'home' with the name of your home view
    else:
        form = CustomUserCreationForm()
    return render(request, 'order-app/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home view
    else:
        form = AuthenticationForm()
    return render(request, 'order-app/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view

def signup_success(request):
    return render(request, 'order-app/signup_success.html', context)
