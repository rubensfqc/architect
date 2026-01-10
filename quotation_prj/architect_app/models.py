from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Architect(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='architect_profile'
    )
    firm_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='architect_logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.firm_name}"

class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    architect = models.ForeignKey(
        'architect_app.Architect',
        on_delete=models.CASCADE,
        related_name='clients'
    )
    company_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Client: {self.user.email}"

class Contract(models.Model):
    # Each contract belongs to ONE architect, only signed contracts before that they are quotes
    architect = models.ForeignKey(
        Architect,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='contracts'
    )
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.client}"


class Project(models.Model):
    # EachDrawings, design, blueprint. A Project belongs to ONE contract
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    expected_completion_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

