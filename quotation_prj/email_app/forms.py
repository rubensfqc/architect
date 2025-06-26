from django import forms
from django.utils.translation import gettext_lazy as _
from quotation_app.models import Client

class UserMessageForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email']
        labels = {
            'name': _('Name'),
            'email': _('Email'),
        }