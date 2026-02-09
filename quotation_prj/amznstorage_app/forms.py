# amznstorage_app/forms.py (or inside views.py)
from django import forms
from .models import DocProject, Document


# Simple form for file upload
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'upload', 'image']
        

class DocProjectForm(forms.ModelForm):
    class Meta:
        model = DocProject  # Updated model name
        fields = ['title', 'upload', 'image']