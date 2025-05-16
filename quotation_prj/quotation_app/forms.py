from django import forms
from .models import Client, Quotation, Product, QuotationProduct
from seller_app.models import Seller  # Adjust the import based on your app name

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
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

class QuotationProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select a product")

    class Meta:
        model = QuotationProduct
        fields = ['product', 'quantity']


class QuotationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuotationForm, self).__init__(*args, **kwargs)
        products = Product.objects.all()
        for product in products:
            self.fields[f'quantity_{product.id}'] = forms.IntegerField(
                label=f"{product.name}",# ({product.price} $)",
                min_value=0,
                required=False
            )
    #class Meta:
     #   model = Quotation
      #  fields = ['client', 'products', 'total_amount']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Dynamically add fields for each product
    #     products = Product.objects.all()
    #     for product in products:
    #         self.fields[f'product_{product.id}'] = forms.IntegerField(
    #             label=product.name,
    #             required=False,
    #             min_value=0,
    #             initial=0,
    #             widget=forms.NumberInput(attrs={'class': 'form-control'})
    #         )

class QuotatioFormPerSeller(forms.Form):
    def __init__(self, *args, **kwargs):
        seller = kwargs.pop('seller')  # Extract seller from kwargs
        super(QuotatioFormPerSeller , self).__init__(*args, **kwargs)
        print(f"FORM DEBUG seller: {seller}")
        print(f"FORM DEBUG kwargs: {kwargs}")
        print(f"FORM DEBUG products: {Product.objects.filter(seller=seller)}")
        products = Product.objects.filter(seller=seller)
        print(f"FORM DEBUG products: {products}")
        for product in products:
            self.fields[f'quantity_{product.id}'] = forms.IntegerField(
                label=f"{product.name}",  # you can include product.price here too
                min_value=0,
                required=False
            )