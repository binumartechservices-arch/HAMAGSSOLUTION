from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    def role_labels(self):
        roles = []
        if self.is_admin: roles.append("Admin")
        if self.is_salesman: roles.append("Salesman")
        if self.is_customer: roles.append("Customer")
        return ", ".join(roles) or "—"

class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"AdminProfile({self.user.username})"

class SalesmanProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salesman_profile', null=True, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(upload_to='salesman_profiles/', blank=True, null=True)   
    def __str__(self):
        return f"SalesmanProfile({self.user.username})"

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_profile')
    phone = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(upload_to='customer_profiles/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    is_walk_in = models.BooleanField(default=False)

    def __str__(self):
        base = self.full_name or (self.user.username if self.user else "Walk-in")
        return f"{base}"

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    logo = models.FileField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name