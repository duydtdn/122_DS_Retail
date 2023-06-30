from django.shortcuts import render, redirect
from order_manager.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

# Index
def index(request):
  return render(request, 'order-manager/pages/index.html')

# Dashboard
def dashboard(request):
  context = {
    'segment': 'dashboard'
  }
  return render(request, 'order-manager/pages/dashboard/dashboard.html', context)

# Pages
@login_required(login_url="/order-manager/login/")
def customerManager(request):
  context = {
    'segment': 'customers'
  }
  return render(request, 'order-manager/pages/customer-manager.html', context)

@login_required(login_url="/order-manager/login/")
def transaction(request):
  context = {
    'segment': 'transactions'
  }
  return render(request, 'order-manager/pages/transactions.html', context)

@login_required(login_url="/order-manager/login/")
def settings(request):
  context = {
    'segment': 'settings'
  }
  return render(request, 'order-manager/pages/settings.html', context)

# Tables
@login_required(login_url="/order-manager/login/")
def bs_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'bs_tables',
  }
  return render(request, 'pages/tables/bootstrap-tables.html', context)

# Components
@login_required(login_url="/order-manager/login/")
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons',
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url="/order-manager/login/")
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications',
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url="/order-manager/login/")
def forms(request):
  context = {
    'parent': 'components',
    'segment': 'forms',
  }
  return render(request, 'pages/components/forms.html', context)

@login_required(login_url="/order-manager/login/")
def modals(request):
  context = {
    'parent': 'components',
    'segment': 'modals',
  }
  return render(request, 'pages/components/modals.html', context)

@login_required(login_url="/order-manager/login/")
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography',
  }
  return render(request, 'pages/components/typography.html', context)


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
def error_404(request):
  return render(request, 'order-manager/pages/examples/404.html')

def error_500(request):
  return render(request, 'order-manager/pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'order-manager/pages/upgrade-to-pro.html')