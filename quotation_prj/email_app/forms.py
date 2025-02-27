from django import forms
from quotation_app.models import Client

class UserMessageForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email']