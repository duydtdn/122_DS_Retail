from django.contrib.auth.forms import UserCreationForm
from orders.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number',)
