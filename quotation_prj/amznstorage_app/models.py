# amznstorage_app/models.py
from django.db import models

class Document(models.Model):
    # Link to Project
    project = models.ForeignKey(
        'architect_app.Project', 
        on_delete=models.CASCADE, 
        related_name='documents',
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='documents/%Y/%m/%d/')
    # This line for images
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title