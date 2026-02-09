# amznstorage_app/models.py
from django.db import models
from architect_app.models import Project

class Document(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='documents/%Y/%m/%d/')
    # This line for images
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class DocProject(models.Model):
    # Link document to a specific project
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='project_documents',
        null=True, # Set null=True initially if you have existing documents
        blank=True
    )
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='projects/%Y/%m/%d/')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project.name if self.project else 'No Project'})"