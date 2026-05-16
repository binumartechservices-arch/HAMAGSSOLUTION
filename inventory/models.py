from django.db import models
from django.conf import settings
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)
    def __str__(self): return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    gram = models.CharField(max_length=64, blank=True)
    karate = models.CharField(max_length=64, blank=True)
    # sku = models.CharField(max_length=64, unique=True)
    # barcode = models.CharField(max_length=64, blank=True)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self): return f"{self.name} ({self.sku})"
    @property
    def low_stock(self): return self.quantity_in_stock <= self.reorder_level

class StockTransaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    RETURN_IN = 'RETURN_IN'
    ADJUST = 'ADJUST'
    TYPES = [(IN,'In'),(OUT,'Out'),(RETURN_IN,'Return In'),(ADJUST,'Adjust')]
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stock_txns')
    type = models.CharField(max_length=16, choices=TYPES)
    quantity = models.IntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self): return f"{self.medicine} {self.type} {self.quantity}"
