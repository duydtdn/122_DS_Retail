from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from order_api.models import Product, ProductCategory, DiscountPackage
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Confirm Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Username'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'example@company.com'
      })
    }

class LoginForm(AuthenticationForm):
  username = UsernameField(label=_("Tài khoản"), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tài khoản"}))
  password = forms.CharField(
      label=_("Mật khẩu"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mật khẩu"}),
  )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")

class ProductCreateForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        if user :
            self.fields['category'].queryset = ProductCategory.objects.filter(store_operate= user.store_operate, parent__isnull=False)
            self.fields['store_operate'].initial = user.store_operate
    class Meta:
        model = Product
        fields = ('title', 'price', 'thumbnail' , 'category', 'store_operate')
        labels = {
            'title': 'Tên sản phẩm',
            'category': 'Chủng loại',
            'price': "Giá sản phẩm"
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên sản phẩm'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'VNĐ'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn loại sản phẩm'
            }),
            'store_operate': forms.HiddenInput(),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn ảnh'
            }),
        }

class DiscountPackageCreateForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(DiscountPackageCreateForm, self).__init__(*args, **kwargs)
        if user :
            self.fields['store_operate'].initial = user.store_operate
    class Meta:
        model = DiscountPackage
        fields ='__all__'
        labels = {
            'title': 'Tên gói giảm giá',
            'gift_code': 'Mã giảm giá',
            'detail': 'Chi tiết',
            'discount': "Discount",
            'thumbnail': "Hình ảnh",
            'amount': 'Số lượng',
            'available': 'Còn lại',
            'is_active': 'Is active'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên gói giảm giá'
            }),
            'gift_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mã giảm giá'
            }),
            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mô tả',
                'rows': '4'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '%'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập số lượng'
            }),
            'available': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập số lượng'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'wrapper-class' : 'form-check form-switch'
            }),
            'store_operate': forms.HiddenInput(),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn ảnh'
            }),
        }

class CategoryCreateForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        if user :
            self.fields['parent'].queryset = ProductCategory.objects.filter(store_operate= user.store_operate, parent__isnull=True)
            self.fields['store_operate'].initial = user.store_operate
    class Meta:
        model = ProductCategory
        fields ='__all__'
        labels = {
            'name': 'Tên nhóm sản phẩm',
            'slug': 'Slug',
            'parent': 'Parent category',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên nhóm sản phẩm'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'slug'
            }),
             'parent': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn parent group'
            }),
            'store_operate': forms.HiddenInput(),
        }
