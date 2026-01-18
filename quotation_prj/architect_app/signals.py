from django.db.models.signals import post_save
from django.dispatch import receiver
from seller_app.models import Seller
from architect_app.models import Architect, ClientProfile, Operator

@receiver(post_save, sender=Seller)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == Seller.Roles.ARCHITECT:
            Architect.objects.get_or_create(user=instance)
        elif instance.role == Seller.Roles.OPERATOR:
            Operator.objects.get_or_create(user=instance)
        # We skip CLIENT here because it requires an architect_id handled in the view