from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Architect(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='architect_profile'
    )
    firm_name = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
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
    
class Operator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operator_profile'
    )
    department = models.CharField(max_length=100)
    access_level = models.IntegerField(default=1)

    def __str__(self):
        return f"Operator: {self.user.email}"

class Contract(models.Model):
    # Each contract belongs to ONE architect, only signed contracts before that they are quotes
    class Phases(models.TextChoices):
        ESTUDO = 'EST', _('Schematic design') # Estudo preliminar
        ANTEPROJETO = 'ANT', _('Design development') # Anteprojeto
        EXECUTIVO = 'EXE', _('Construction documents') # Executivo
        FINALIZADO = 'FIN', _('Closure') # Finalizado

    architect = models.ForeignKey('Architect', on_delete=models.CASCADE, related_name="contracts")
    client = models.ForeignKey('ClientProfile', on_delete=models.CASCADE, related_name='contracts')
    title = models.CharField(max_length=255)
    
    # Fase do contrato
    phase = models.CharField(
        max_length=3,
        choices=Phases.choices,
        default=Phases.ESTUDO,
    )
    
    # Progresso numérico para a style="width: X%"
    progress_percentage = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Progress from 0 to 100")
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        # Lógica simples para sugerir progresso baseado na fase caso esteja vindo o padrão
        if self.phase == self.Phases.ESTUDO and self.progress_percentage < 25:
            self.progress_percentage = 25
        elif self.phase == self.Phases.ANTEPROJETO and self.progress_percentage < 50:
            self.progress_percentage = 50
        elif self.phase == self.Phases.EXECUTIVO and self.progress_percentage < 75:
            self.progress_percentage = 75
        elif self.phase == self.Phases.FINALIZADO:
            self.progress_percentage = 100
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.get_phase_display()}"


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        NEW = 'NEW', _('New')
        REVIEWAL = 'REV', _('Reviewal')
        APPROVED = 'APP', _('Approved')

    contract = models.ForeignKey(
        'Contract', 
        on_delete=models.CASCADE, 
        related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    
    # --- Thumbnail & Status ---
    status = models.CharField(
        max_length=10,
        choices=ProjectStatus.choices,
        default=ProjectStatus.NEW,
    )
    thumbnail_file = models.ImageField(upload_to='projects/thumbnails/', null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)

    # --- Limited Comments (Twitter Length: 280 chars) ---
    client_comments = models.CharField(
        max_length=280, 
        blank=True, 
        help_text=_("Client's short feedback (max 280 characters)")
    )
    architect_comments = models.CharField(
        max_length=280, 
        blank=True, 
        help_text=_("Architect's short response (max 280 characters)")
    )

    # --- Full Conversation Log ---
    # Stores data like: [{"user": "client", "msg": "...", "date": "2024-05-01"}, ...]
    conversation_log = models.JSONField(default=list, blank=True)

    expected_completion_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail_file:
            return self.thumbnail_file.url
        return self.thumbnail_url
    

