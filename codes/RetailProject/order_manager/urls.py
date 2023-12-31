from django.urls import path
from order_manager import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Index
    path('', views.dashboard, name="index"),

    # Pages
    path('dashboard/', views.dashboard, name="dashboard"),
    # path('transaction/', views.transaction, name="transaction"),
    path('customers/', views.customerManager, name="customers"),
    path('products/', views.productManager, name="products"),
    path('product/add', views.addProduct, name="product_add"),
    path('product/edit', views.editProduct, name="product_edit"),
    path('categories/', views.categoryManager, name="categories"),
    path('category/add', views.addCategory, name="category_add"),
    path('category/edit', views.editCategory, name="category_edit"),
    path('orders/', views.orderManager, name="orders"),
    path('order-detail/', views.orderDetailManager, name="order_detail"),
    path('discount-packages/', views.discountPackageManager, name="discount_packages"),
    path('discount-package/add', views.addDiscountPackage, name="discount_package_add"),
    path('discount-package/edit', views.editDiscountPackage, name="discount_package_edit"),
    path('settings/', views.settings, name="settings"),
    path('statistic/', views.statistic, name="statistic"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    # path('register/', views.register_view, name="register"),

    # Components
    path('components/buttons/', views.buttons, name="buttons"),
    path('components/notifications/', views.notifications, name="notifications"),
    path('components/forms/', views.forms, name="forms"),
    path('components/modals/', views.modals, name="modals"),
    path('components/typography/', views.typography, name="typography"),

    # Authentication
    # path('accounts/register/', views.register_view, name="register"),
    path('accounts/login/', views.UserLoginView.as_view(), name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
#     path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
#     path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
#         template_name='accounts/password-change-done.html'
#     ), name="password_change_done"),
#     path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
#     path('accounts/password-reset-confirm/<uidb64>/<token>/',
#         views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"
#     ),
#     path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='accounts/password-reset-done.html'
#     ), name='password_reset_done'),
#     path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
#         template_name='accounts/password-reset-complete.html'
#   ), name='password_reset_complete'),

    path('accounts/lock/', views.lock, name="lock"),

    # Errors
    path('error/403/', views.error_403, name="error_403"),
    path('error/404/', views.error_404, name="error_404"),
    path('error/500/', views.error_500, name="error_500"),
]