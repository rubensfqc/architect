from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.text import slugify


class Seller(AbstractUser): #models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links Seller to a Django user
    email = models.EmailField(unique=True, default="default@example.com")
    name = models.CharField(max_length=100, default="defaultname")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
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
