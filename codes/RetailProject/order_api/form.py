from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
# from django.contrib.auth import get_user_model
from order_api.models import CustomUser, OrderPlace, OrderPlaceProduct


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ("username", "phone_number","password","store_operate", "is_active", "is_admin")

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ("username", "phone_number", "password1", "password2","is_admin", "store_operate")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class OrderForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # if user :
        #     self.fields['order_date'].initial = user
    class Meta:
        model = OrderPlace
        fields = ['store_operate', 'order_type', 'pay_type']
