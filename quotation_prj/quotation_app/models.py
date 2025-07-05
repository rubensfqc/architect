from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from seller_app.models import Seller
from django.utils import timezone

# Validator for numbers in the format "+11 91234-5678" or "11 91234-5678"
brazilian_phone_validator = RegexValidator(
    regex=r'^\+?(\d{2})\s9\d{4}-\d{4}$',
    message="Enter a valid phone number (e.g., '+11 91234-5678' or '11 91234-5678')"
)

class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products", default=1)  # Relate product to a seller

    def __str__(self):
        #return self.name
        return f"{self.name} - ${self.price} (Seller: {self.seller.name})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Custom logic after saving
        print(f"Product '{self.name}' has been saved.")


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=11)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="clients", default=1)  # Relate client to a seller
    created_at = models.DateTimeField(default=timezone.now)  # ⬅️ Timestamp when client is created
    #     max_length=11,  # 2-digit area code + 9-digit number 
    #     validators=[brazilian_phone_validator], 
    #     help_text="Format: +11 91234-5678 or 11 91234-5678"
    # )

    # def save(self, *args, **kwargs):
    #     # Remove all non-numeric characters before saving to the database
    #     self.whatsapp = ''.join(filter(str.isdigit, self.whatsapp))
    #     super().save(*args, **kwargs)

    def __str__(self):
        #return self.name
        return f"{self.name} - {self.whatsapp} (Seller: {self.seller.name})"

class Quotation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='QuotationProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=timezone.now) # Automatically set on creation

class QuotationProduct(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()#default=1)
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.quotation.calculate_total_amount()