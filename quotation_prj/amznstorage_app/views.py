# amznstorage_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django import forms

# Simple form for file upload
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'upload']

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid, saving document.")
            print(f"Uploaded file name: {request.FILES['upload'].name}")
            print(f"Request: {request}")
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'amznstorage_app/upload.html', {'form': form})

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'amznstorage_app/document_list.html', {'documents': documents})

def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'amznstorage_app/document_detail.html', {'document': document})