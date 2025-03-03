from django import forms
from .models import Client, Quotation, Product, QuotationProduct

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
    
    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('seller', None)  # Get seller from view
        super(ProductForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super().save(commit=False)
        product.seller = self.seller  # Assign the seller before saving
        if commit:
            product.save()
        return product

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

