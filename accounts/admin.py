from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, AdminProfile, SalesmanProfile, CustomerProfile
from .models import Company

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_salesman', 'is_customer')
    fieldsets = DjangoUserAdmin.fieldsets + ((
        'Roles', {'fields': ('is_admin', 'is_salesman', 'is_customer')}
    ),)

admin.site.register(AdminProfile)
admin.site.register(SalesmanProfile)
admin.site.register(CustomerProfile)
admin.site.register(Company)