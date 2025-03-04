from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Seller

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
