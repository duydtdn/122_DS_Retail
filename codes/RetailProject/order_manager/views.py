from django.shortcuts import render, redirect
from order_manager.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from order_api.controller.assistant.decorator import  store_manager_role_required
from order_api.models import Product
LOGIN_URL="/order-manager/login/"

def getItemsWithPagination (request, items):
  LIMIT = 4
  page_number = request.GET.get("page") or 1
  search = request.GET.get("search") or ''
  paginator = Paginator(items, LIMIT)
  page_objects = paginator.get_page(page_number)
  data = {
    'items': page_objects,
    'total': items.count(),
    'params': {'page': page_number, 'search':search },
    'from': (int(page_number) - 1) * LIMIT + 1,
    'to': (int(page_number) - 1) * LIMIT + len(page_objects.object_list),
    'total_page': 1 if items.count() <= LIMIT else (items.count() -1)//LIMIT + 1,
    }
  return data

# Dashboard
@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def dashboard(request):
  context = {
    'segment': 'dashboard',
  }
  return render(request, 'order-manager/pages/dashboard/dashboard.html', context)

# Pages
@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def customerManager(request):
  context = {
    'segment': 'customers'
  }
  return render(request, 'order-manager/pages/customer-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def productManager(request):
  search  = request.GET.get('search') or ''
  products = Product.objects.filter(store_operate=request.user.store_operate, title__contains=search).order_by('id')
  context = {
    'segment': 'Quản lý sản phẩm',
    'data': getItemsWithPagination (request, products)
  }
  return render(request, 'order-manager/pages/product-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def transaction(request):
  context = {
    'segment': 'transactions'
  }
  return render(request, 'order-manager/pages/transactions.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def settings(request):
  context = {
    'segment': 'settings'
  }
  return render(request, 'order-manager/pages/settings.html', context)

# Tables
@login_required(login_url=LOGIN_URL)
def bs_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'bs_tables',
  }
  return render(request, 'pages/tables/bootstrap-tables.html', context)

# Components
@login_required(login_url=LOGIN_URL)
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons',
  }
  return render(request, 'order-manager/pages/components/buttons.html', context)

@login_required(login_url=LOGIN_URL)
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications',
  }
  return render(request, 'order-manager/pages/components/notifications.html', context)

@login_required(login_url=LOGIN_URL)
def forms(request):
  context = {
    'parent': 'components',
    'segment': 'forms',
  }
  return render(request, 'order-manager/pages/components/forms.html', context)

@login_required(login_url=LOGIN_URL)
def modals(request):
  context = {
    'parent': 'components',
    'segment': 'modals',
  }
  return render(request, 'order-manager/pages/components/modals.html', context)

@login_required(login_url=LOGIN_URL)
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography',
  }
  return render(request, 'order-manager/pages/components/typography.html', context)


# Authentication
def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      print("Account created successfully!")
      form.save()
      return redirect('/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = { 'form': form }
  return render(request, 'order-manager/accounts/sign-up.html', context)

class UserLoginView(LoginView):
  redirect_field_name="dashboard"
  form_class = LoginForm
  template_name = 'order-manager/accounts/sign-in.html'

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

def logout_view(request):
  logout(request)
  return redirect('/order-manager/login/')

def lock(request):
  return render(request, 'accounts/lock.html')

# Errors
def error_403(request):
  return render(request, 'order-manager/pages/examples/403.html')

def error_404(request):
  return render(request, 'order-manager/pages/examples/404.html')

def error_500(request):
  return render(request, 'order-manager/pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'order-manager/pages/upgrade-to-pro.html')