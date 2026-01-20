# amznstorage_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django import forms
import boto3
from django.conf import settings
from django.http import StreamingHttpResponse, Http404

# Simple form for file upload
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'upload', 'image']

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)# request.FILES handles both FileField and ImageField
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


def pdf_proxy(request, document_id):
    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        raise Http404("Document not found")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    bucket = settings.AWS_STORAGE_BUCKET_NAME
    key = document.upload.name  # IMPORTANT: S3 key, not URL

    obj = s3.get_object(Bucket=bucket, Key=key)

    response = StreamingHttpResponse(
        obj["Body"].iter_chunks(chunk_size=8192),
        content_type="application/pdf",
    )

    # Change "inline" to "attachment" if you want to force download, 
    # or keep "inline" to let the browser 'download' attribute handle it.
    response["Content-Disposition"] = f'inline; filename="{document.title}.pdf"'
    response["Accept-Ranges"] = "bytes"
    return response