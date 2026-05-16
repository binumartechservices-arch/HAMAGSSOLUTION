from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register-salesman/', views.salesman_register_view, name='register-salesman'),   
    path('<int:pk>/update-salesman/', views.update_salesman, name='update-salesman'), 
    path('customers/', views.customers_list, name='customers'),
    path('salesmen/', views.salesman_list, name='salesmen'),
    path('register-customer/', views.customer_register_view, name='register-customer'),
    path('', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]