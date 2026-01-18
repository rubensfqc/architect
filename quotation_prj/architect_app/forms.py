# forms.py
from django import forms
from .models import Contract
from django.contrib.auth.forms import UserCreationForm
from seller_app.models import Seller

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