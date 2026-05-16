from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Category, Supplier

admin.site.register(Category)
admin.site.register(Supplier)
