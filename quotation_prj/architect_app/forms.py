# forms.py
from django import forms
from .models import Contract, Project, ClientProfile, Architect
from django.contrib.auth.forms import UserCreationForm
from seller_app.models import Seller, SellerQuotationSettings

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['title', 'client', 'budget', 'is_active', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SellerSignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Seller.Roles.choices)
    name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = Seller
        fields = ("email", "username", "name", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role')
        user.name = self.cleaned_data.get('name')
        if commit:
            user.save()
        return user
    
# forms.py
class ClientSignUpForm(UserCreationForm):
    # This allows us to pass the architect ID into the form
    architect_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta(UserCreationForm.Meta):
        model = Seller
        fields = ("email", "username", "name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Seller.Roles.CLIENT  # Force role to CLIENT
        if commit:
            user.save()
        return user


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'location', 'status', 
            'thumbnail_file', 'thumbnail_url', 
            'architect_comments',
            'contract',
            'expected_completion_date'
        ]
        widgets = {
            'expected_completion_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'architect_comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Max 280 chars'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
        }


class ClientEditForm(forms.ModelForm):
    # We can bring in fields from the User/Seller model directly into this form
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = ClientProfile
        fields = ['company_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate first/last name from the user object
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update the linked user object
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile
    

class ArchitectSettingsForm(forms.ModelForm):
    # Manually add fields from the Seller (User) model
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Architect
        fields = ['firm_name', 'license_number', 'phone_number', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the Seller fields with current values if an instance exists
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            # The email field should probably be read-only to prevent auth issues
            self.fields['email'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        architect = super().save(commit=False)
        user = architect.user
        
        # Update the Seller model fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # email is usually kept read-only, but you can update it here if needed
        
        if commit:
            user.save()
            architect.save()
        return architect
    

class ArchitectUnifiedSettingsForm(forms.ModelForm):
    # Seller Fields
    name = forms.CharField(max_length=150, required=True)
    #last_name = forms.CharField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=15, required=False) # Maps to Seller.phone_number
    
    # Quotation Settings Fields
    currency = forms.ChoiceField(choices=SellerQuotationSettings.CURRENCY_CHOICES)
    payment_link = forms.URLField(required=False)
    pix_key = forms.CharField(required=False)
    #base_price = forms.DecimalField(max_digits=10, decimal_places=2)
    redirect_url = forms.URLField(required=False, label="Customer Redirect Link")
    product_catalog_url = forms.URLField(required=False, label="Product Catalog Link")
    custom_message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Architect
        fields = ['firm_name', 'license_number', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            user = self.instance.user
            # Populate Seller data
            self.fields['name'].initial = user.name
            #self.fields['last_name'].initial = user.last_name
            self.fields['phone_number'].initial = user.phone_number
            
            # Populate Quotation data
            q_settings, created = SellerQuotationSettings.objects.get_or_create(seller=user)
            self.fields['currency'].initial = q_settings.currency
            self.fields['payment_link'].initial = q_settings.payment_link
            self.fields['pix_key'].initial = q_settings.pix_key
            #self.fields['base_price'].initial = q_settings.base_price
            self.fields['redirect_url'].initial = q_settings.redirect_url
            self.fields['product_catalog_url'].initial = q_settings.product_catalog_url
            self.fields['custom_message'].initial = q_settings.custom_message

    def save(self, commit=True):
        architect = super().save(commit=False)
        user = architect.user
        
        # 1. Save Seller Data
        user.first_name = self.cleaned_data['name']
        #user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        
        # 2. Save Quotation Settings
        q_settings = user.quotation_settings
        q_settings.currency = self.cleaned_data['currency']
        q_settings.payment_link = self.cleaned_data['payment_link']
        q_settings.pix_key = self.cleaned_data['pix_key']
        #q_settings.base_price = self.cleaned_data['base_price']
        q_settings.redirect_url = self.cleaned_data['redirect_url']
        q_settings.product_catalog_url = self.cleaned_data['product_catalog_url']
        q_settings.custom_message = self.cleaned_data['custom_message']
        
        if commit:
            user.save()
            q_settings.save()
            architect.save()
        return architect