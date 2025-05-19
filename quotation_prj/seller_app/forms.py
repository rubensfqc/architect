from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Seller
from quotation_app.models import Product

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
