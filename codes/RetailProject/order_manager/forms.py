from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from order_api.models import Product, ProductCategory
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
