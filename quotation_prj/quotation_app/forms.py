from django import forms
from .models import Client, Quotation

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'whatsapp']

    def clean_whatsapp(self):
        phone = self.cleaned_data['whatsapp']
        phone = ''.join(filter(str.isdigit, phone))  # Remove non-numeric characters
        if len(phone) != 11:
            raise forms.ValidationError("Enter a valid Brazilian phone number (e.g., 11 91234-5678)")
        return phone  # Store only digits
    
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['product_name', 'quantity', 'price']
