from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Seller(AbstractUser): #models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links Seller to a Django user
    email = models.EmailField(unique=True, default="default@example.com")
    name = models.CharField(max_length=100, default="defaultname")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    #password = "defaultpassword123"  # Set a default password
    #self.set_password(password)  # Hash the password
    #self.save()  # Save the user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

""" class Seller(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a slug from the name if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.name)

        # Call the parent class's save() method
        super().save(*args, **kwargs) """
