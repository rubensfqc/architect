from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify

# Validator for numbers in the format "+11 91234-5678" or "11 91234-5678"
brazilian_phone_validator = RegexValidator(
    regex=r'^\+?(\d{2})\s9\d{4}-\d{4}$',
    message="Enter a valid phone number (e.g., '+11 91234-5678' or '11 91234-5678')"
)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Custom logic after saving
        print(f"Product '{self.name}' has been saved.")


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

class Quotation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='QuotationProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

"""     def calculate_total_amount(self):
        total = self.quotationproduct_set.aggregate(
            total=Sum(models.F('quantity') * models.F('price'))
        )['total'] or 0
        self.total_amount = total
        self.save() """

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




""" class Seller(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a slug from the name if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.name)

        # Call the parent class's save() method
        super().save(*args, **kwargs) """