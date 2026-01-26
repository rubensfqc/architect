# quotation_prj/quotation_app/forms.py
from django import forms
from .models import Client, Quotation, Product, QuotationProduct
from seller_app.models import Seller
from django.utils.translation import gettext_lazy as _

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'whatsapp']
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'whatsapp': _('WhatsApp'),
        }

    def clean_whatsapp(self):
        phone = self.cleaned_data['whatsapp']
        phone = ''.join(filter(str.isdigit, phone))  # Remove non-numeric characters
        if len(phone) not in (10, 11):
            raise forms.ValidationError(
                _("Enter a valid Brazilian or European phone number (e.g., BR 11 91234-5678 or EU 0612345678)")
            )
        return phone  # Store only digits
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
        labels = {
            'name': _('Product Name'),
            'price': _('Price'),
            'description': _('Description'),
        }
    
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
    product = forms.ModelChoiceField(queryset=Product.objects.none(), empty_label=_("Select a product"),
        label=_("Product"))
    
    def __init__(self, *args, **kwargs):
        seller = kwargs.pop('seller', None)  # Get the seller_id from kwargs
        super().__init__(*args, **kwargs)
        
        # Filter products by seller_id
        if seller:
            self.fields['product'].queryset = Product.objects.filter(seller=seller)
        else:
            self.fields['product'].queryset = Product.objects.none()  # Default to no products

    

    class Meta:
        model = QuotationProduct
        fields = ['product', 'quantity']
        labels = {
            'product': _('Product'),
            'quantity': _('Quantity'),
        }


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

class QuotationFormPerSeller(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product_map = {}  # Store product info by field name
        seller = kwargs.pop('seller')
        super().__init__(*args, **kwargs)
        
        products = Product.objects.filter(seller=seller)
        for product in products:
            field_name = f'quantity_{product.id}'
            self.fields[field_name] = forms.IntegerField(
                label=_("{name}").format(name=product.name),
                min_value=0,
                required=False
            )
            self.product_map[field_name] = product  # Store full product object