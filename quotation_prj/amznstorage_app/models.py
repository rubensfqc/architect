# amznstorage_app/models.py
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title