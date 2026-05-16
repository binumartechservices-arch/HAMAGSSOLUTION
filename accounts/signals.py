from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import AdminProfile, SalesmanProfile, CustomerProfile, User

def ensure_profile(user: User):
    # Create the appropriate profiles if flags are set and profiles don't exist.
    if user.is_admin:
        AdminProfile.objects.get_or_create(user=user)
    
    if user.is_salesman:
        SalesmanProfile.objects.get_or_create(
            user=user,
            defaults={"full_name": user.full_name}
        )
    
    if user.is_customer:
        CustomerProfile.objects.get_or_create(
            user=user,
            defaults={"full_name": user.full_name}
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profiles_for_user(sender, instance: User, created, **kwargs):
    if created:
        ensure_profile(instance)
