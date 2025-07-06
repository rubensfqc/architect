from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Seller(AbstractUser): #models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links Seller to a Django user
    email = models.EmailField(unique=True, default="default@example.com", verbose_name=_("Email"))
    name = models.CharField(max_length=100, default="defaultname", verbose_name=_("Name"))
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name=_("Profile Picture"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
    slug = models.SlugField(unique=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='seller_set',  # make this unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='seller_user_permissions',  # make this unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    #password = "defaultpassword123"  # Set a default password
    #self.set_password(password)  # Hash the password
    #self.save()  # Save the user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

class SellerQuotationSettings(models.Model):
    CURRENCY_CHOICES = [
        ('BRL', 'Brazilian Real'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('ARS', 'Argentine Peso'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
    ]
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='quotation_settings')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    payment_link = models.URLField(blank=True, null=True)
    pix_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("PIX Key"),
        help_text=_("Enter your PIX key (CPF, CNPJ, email, phone or random)")
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custom_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Quotation Settings for {self.seller.name}"