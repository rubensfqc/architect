# amznstorage_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DocProject, Document
from django import forms
import boto3
from django.conf import settings
from django.http import StreamingHttpResponse, Http404
from architect_app.models import Project
from .forms import DocumentForm, DocProjectForm 


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
    docProjects = DocProject.objects.all()
    return render(request, 'amznstorage_app/document_list.html', {'documents': documents, 'docProjects':docProjects})

def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'amznstorage_app/document_detail.html', {'document': document})

def pdf_proxy(request, document_id):
    try:
        # CRITICAL: Must use the NEW model name here
        document = DocProject.objects.get(pk=document_id)
    except DocProject.DoesNotExist:
        # This is where your 404 is likely coming from
        raise Http404("Document record not found in database")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    bucket = settings.AWS_STORAGE_BUCKET_NAME
    
    # This must match the 'upload' field in your DocProject model
    # It sends the relative path (e.g., 'projects/2024/05/file.pdf') to S3
    key = document.upload.name 

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
    except s3.exceptions.NoSuchKey:
        raise Http404("File found in database, but missing in S3 bucket")

    response = StreamingHttpResponse(
        obj["Body"].iter_chunks(chunk_size=8192),
        content_type="application/pdf",
    )
    
    # Helps the browser handle the filename correctly
    response["Content-Disposition"] = f'inline; filename="{document.title}.pdf"'
    return response

# New views to handle project-specific document uploads
def upload_project_document(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.project = project  # Assign the project automatically
            doc.save()
            # Redirect back to the project detail page
            return redirect('project_detail', pk=project.id)
    else:
        form = DocumentForm()
        
    return render(request, 'architect_app/project_upload.html', {
        'form': form, 
        'project': project
    })