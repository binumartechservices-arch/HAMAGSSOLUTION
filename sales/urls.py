from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('pos/', views.pos, name='pos'),
    path('pos/add/<int:med_id>/', views.add_to_cart, name='add_to_cart'),
    path('pos/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('pos/update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('receipt/<int:order_id>/', views.receipt, name='receipt'),
    path('return-receipt/<int:order_id>/', views.return_receipt, name='return-receipt'),
    path('orders/', views.orders_list, name='orders_list'),
    path('return-orders/', views.return_orders_list, name='return_orders_list'),
    path('return/<int:order_item_id>/', views.return_item, name='return_item'),
]
