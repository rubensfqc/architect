# amznstorage_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django import forms
import boto3
from django.conf import settings
from django.http import HttpResponseForbidden, StreamingHttpResponse, Http404
from architect_app.models import Project  # Import Project model for ForeignKey relationship

# Simple form for file upload
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        #fields = ['title', 'upload', 'image', 'project']  # Include project field in the form
        fields = ['title', 'upload', 'project']  # Include project field in the form

def upload_document(request, project_id=None):
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        architect = project.contract.architect # Assuming Project has a ForeignKey to Contract, and Contract has a ForeignKey to Architect
        architect_id = architect.user.id
        print("Architect for project %d: %s" % (project_id, architect_id))
        print("Request user: %s" % request.user)
        print("Bollean: %s" % (architect_id == request.user.id))
        if request.method == 'POST' and architect_id != request.user.id:
            return HttpResponseForbidden("You do not have permission to upload documents for this project.")

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)# request.FILES handles both FileField and ImageField
        form.fields['project'].queryset = Project.objects.filter(contract__architect=architect) # 🔒 Restrict projects to architect's contracts
        if form.is_valid():
            print("Form is valid, saving document.")
            print(f"Uploaded file name: {request.FILES['upload'].name}")
            print(f"Request: {request}")
            document = form.save(commit=False)
            if project:
                document.project = project
            document.save()
                        
            # If uploaded from a project page, return there
            if project:
                return redirect('project_detail', pk=project.pk)
            return redirect('document_list')
    else:
        # Pre-fill the project if coming from project_detail
        form = DocumentForm(initial={'project': project}) if project else DocumentForm()
        form.fields['project'].queryset = Project.objects.filter(contract__architect=architect) # 🔒 SAME FILTER on GET
        
    return render(request, 'amznstorage_app/upload.html', {'form': form, 'project': project})

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