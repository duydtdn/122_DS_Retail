from django.contrib.auth.forms import UserCreationForm
from order_api.models import CustomUser

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number',)

class CustomAuthenticationForm(AuthenticationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            self.user_cache = authenticate(phone_number=phone_number, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data