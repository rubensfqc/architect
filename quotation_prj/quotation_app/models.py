from django.db import models
from django.core.validators import RegexValidator

# Validator for numbers in the format "+11 91234-5678" or "11 91234-5678"
brazilian_phone_validator = RegexValidator(
    regex=r'^\+?(\d{2})\s9\d{4}-\d{4}$',
    message="Enter a valid phone number (e.g., '+11 91234-5678' or '11 91234-5678')"
)

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    # Telephone field (Ensures only digits and + sign)
    whatsapp = models.CharField(max_length=11)
    #     max_length=11,  # 2-digit area code + 9-digit number 
    #     validators=[brazilian_phone_validator], 
    #     help_text="Format: +11 91234-5678 or 11 91234-5678"
    # )

    # def save(self, *args, **kwargs):
    #     # Remove all non-numeric characters before saving to the database
    #     self.whatsapp = ''.join(filter(str.isdigit, self.whatsapp))
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

