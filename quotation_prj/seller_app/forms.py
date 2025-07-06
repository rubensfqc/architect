from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Seller, SellerQuotationSettings
from quotation_app.models import Product
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        labels = {
            'username': _("Username"),
            'email': _("Email"),
            'phone_number': _("Phone Number"),
            'password1': _("Password"),
            'password2': _("Password confirmation"),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        labels = {
            'name': _("Product Name"),
            'description': _("Description"),
            'price': _("Price"),
        }
        widgets = {
        'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
        'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

class SellerUpdateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['email', 'name', 'phone_number', 'profile_picture', 'address']
        labels = {
            'email': _("Email"),
            'name': _("Full Name"),
            'phone_number': _("Phone Number"),
            'profile_picture': _("Profile Picture"),
            'address': _("Address"),
        }

class SellerQuotationSettingsForm(forms.ModelForm):
    class Meta:
        model = SellerQuotationSettings
        fields = ['currency', 'payment_link', 'pix_key', 'base_price', 'custom_message']
        labels = {
            'currency': _("Currency"),
            'payment_link': _("Payment Link"),
            'pix_key': _("PIX Key"),
            'base_price': _("Base Price"),
            'custom_message': _("Custom Message"),
        }
