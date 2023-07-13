from django.shortcuts import render, redirect
from order_manager.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, ProductCreateForm,DiscountPackageCreateForm, CategoryCreateForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from order_api.controller.assistant.decorator import  store_manager_role_required
from order_api.models import Product, ProductCategory, OrderPlace,  DiscountPackage
from django.db.models import Count
from order_api.controller.order_place_ctr import OrderPlaceViewSet, OrderPlaceSerializer
import json
from django.shortcuts import get_object_or_404

LOGIN_URL="/order-manager/login/"

def getItemsWithPagination (request, items):
  LIMIT = 6
  page_number = request.GET.get("page") or 1
  search = request.GET.get("search") or ''
  paginator = Paginator(items, LIMIT)
  page_objects = paginator.get_page(page_number)
  data = {
    'items': enumerate(page_objects),
    'page_objects': page_objects,
    'total': len(items),
    'params': {'page': page_number, 'search':search },
    'from': (int(page_number) - 1) * LIMIT + 1,
    'to': (int(page_number) - 1) * LIMIT + len(page_objects.object_list),
    'total_page': 1 if len(items) <= LIMIT else (len(items) -1)//LIMIT + 1,
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

def statistic(request):
  context = {
    'segment': 'Thống kê',
  }
  return render(request, 'order-manager/pages/statistic.html', context)

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
def categoryManager(request):
  group  = request.GET.get('group') or ''
  categories = ProductCategory.objects.filter(store_operate=request.user.store_operate).order_by('id').annotate(number_of_product=Count('product'))
  if group: 
    categories = categories.filter(parent__id=group)

  context = {
    'segment': 'Quản lý loại sản phẩm','category_segments' :['Quản lý loại sản phẩm', 'Thêm loại sản phẩm'],
    'parentCategories': ProductCategory.objects.filter(store_operate=request.user.store_operate, parent__isnull = True),
    'data': getItemsWithPagination (request, categories),
    'group': group
  }
  return render(request, 'order-manager/pages/category-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def discountPackageManager(request):
  search  = request.GET.get('search') or ''
  packages = DiscountPackage.objects.filter(store_operate=request.user.store_operate).order_by('id')
  if search: 
    packages = packages.filter(title__contains=search)

  context = {
    'segment': 'Discount package','discount_packages_segments' :['Discount package', 'Thêm discount package'],
    'data': getItemsWithPagination (request, packages),
  }
  return render(request, 'order-manager/pages/discount-package-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required

def productManager(request):
  search  = request.GET.get('search') or ''
  category  = request.GET.get('category') or ''
  categories = ProductCategory.objects.filter(store_operate=request.user.store_operate, parent__isnull=False).order_by('id')
  products = Product.objects.filter(store_operate=request.user.store_operate).order_by('id')
  if search:
    products = products.filter(title__contains=search)
  if category:
    products = products.filter(category=category)
  context = {
    'segment': 'Quản lý sản phẩm','product_segments' :['Quản lý sản phẩm', 'Thêm sản phẩm'],
    'data': getItemsWithPagination (request, products),
    'category': category,
    'categories': categories
  }
  return render(request, 'order-manager/pages/product-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def orderManager(request):
  search  = request.GET.get('search') or ''
  status  = request.GET.get('status') or ''
  order_type  = request.GET.get('order_type') or ''
  is_paid = request.GET.get('is_paid') or ''
  orders = OrderPlace.objects.all()
  if search:
    orders = orders.filter(customer__username__contains=search)
  if status:
    orders = orders.filter(status=status)
  if order_type:
    orders = orders.filter(order_type=order_type)
  if is_paid == '1':
    orders = orders.filter(is_paid=True)
  if is_paid == '0':
    orders = orders.filter(is_paid=False)
  serialize = OrderPlaceSerializer(orders, many=True)
  context = {
    'segment': 'Quản lý đơn hàng','orders_segments' :['Quản lý đơn hàng'],
    'data': getItemsWithPagination (request, serialize.data),
    'status': status,
    'order_type': order_type,
    'is_paid': is_paid,
  }
  return render(request, 'order-manager/pages/order-manager.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def orderDetailManager(request):
  orderId  = request.GET.get('id') or ''
  order = OrderPlace.objects.get(pk=orderId)
  serializer = OrderPlaceSerializer(order)
  context = {
    'segment': 'Thông tin đơn hàng','orders_segments' :['Quản lý đơn hàng', 'Thông tin đơn hàng'],
    'order': serializer.data,
  }
  return render(request, 'order-manager/pages/order-detail.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def addProduct(request):
  form = ProductCreateForm(user = request.user)
  if request.method == 'POST':
    form = ProductCreateForm(user = request.user, data = request.POST,files = request.FILES)
    if form.is_valid():
      form.save()
      form = ProductCreateForm(user = request.user, data=None)
      messages.add_message(request, messages.INFO,'Thêm sản phẩm thành công')
      redirect('/order-manager/product/add')
    else:
      print('error')
  context = { 'form': form, 'segment': 'Thêm sản phẩm', 'product_segments' :['Quản lý sản phẩm', 'Thêm sản phẩm']   
 }
  return render(request, 'order-manager/pages/add-product.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def addDiscountPackage(request):
  form = DiscountPackageCreateForm(user = request.user)
  if request.method == 'POST':
    form = DiscountPackageCreateForm(user = request.user, data = request.POST,files = request.FILES)
    if form.is_valid():
      form.save()
      form = DiscountPackageCreateForm(user = request.user, data=None)
      messages.add_message(request, messages.INFO,'Thêm gói giảm giá thành công')
      redirect('/order-manager/discount-package/add')
    else:
      print('error')
  context = { 'form': form, 'segment': 'Thêm gói giảm giá', 'discount_packages_segments' :['Discount packages', 'Thêm gói giảm giá']   
 }
  return render(request, 'order-manager/pages/add-discount-package.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def addCategory(request):
  form = CategoryCreateForm(user = request.user)
  if request.method == 'POST':
    form = CategoryCreateForm(user = request.user, data = request.POST,files = request.FILES)
    if form.is_valid():
      form.save()
      form = CategoryCreateForm(user = request.user, data=None)
      messages.add_message(request, messages.INFO,'Thêm nhóm sản phẩm thành công')
      redirect('/order-manager/categories')
    else:
      print('error')
  context = { 'form': form, 'segment': 'Thêm nhóm sản phẩm', 'categories_segments' : 'Thêm nhóm sản phẩm'   
 }
  return render(request, 'order-manager/pages/add-category.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def editDiscountPackage(request):
  id = request.GET.get('id')
  packageItem = get_object_or_404(DiscountPackage, pk=id)
  form = DiscountPackageCreateForm(user = request.user, instance= packageItem)
  if request.method == 'POST':
    form = DiscountPackageCreateForm(user = request.user, data = request.POST,files = request.FILES, instance= packageItem)
    if form.is_valid():
      form.save()
      # form = DiscountPackageCreateForm(user = request.user, data=None)
      messages.add_message(request, messages.INFO,' Cập nhật thông tin thành công')
      redirect('/order-manager/discount-packages')
    else:
      print('error')
  context = { 'form': form, 'segment': 'Sửa gói giảm giá', 'discount_packages_segments' :['Discount packages', 'Sửa gói giảm giá']   
 }
  return render(request, 'order-manager/pages/edit-discount-package.html', context)

@login_required(login_url=LOGIN_URL)
@store_manager_role_required
def settings(request):
  context = {
    'segment': 'Thông tin cửa hàng'
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