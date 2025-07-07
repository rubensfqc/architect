from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seller, SellerQuotationSettings

@receiver(post_save, sender=Seller)
def create_quotation_settings(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'quotation_settings'):
        SellerQuotationSettings.objects.create(seller=instance)