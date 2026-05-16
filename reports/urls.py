from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('salesman-dashboard/', views.salesman_dashboard, name='salesman-dashboard'),
]
