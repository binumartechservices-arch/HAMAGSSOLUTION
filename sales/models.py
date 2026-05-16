from django.db import models
from django.conf import settings
from decimal import Decimal
from inventory.models import Medicine, StockTransaction

class Cart(models.Model):
    OPEN = 'OPEN'
    CHECKED_OUT = 'CHECKED_OUT'
    CANCELLED = 'CANCELLED'
    STATUSES = [(OPEN,'Open'),(CHECKED_OUT,'Checked out'),(CANCELLED,'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=16, choices=STATUSES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"Cart#{self.id} {self.user} {self.status}"

    @property
    def items_count(self): return sum(i.quantity for i in self.items.all())
    @property
    def subtotal(self): return sum(i.line_total for i in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart','medicine')

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.medicine} x{self.quantity}"

class Order(models.Model):
    REGULAR = 'REGULAR'
    WALKIN = 'WALKIN'
    TYPES = [(REGULAR,'Regular'),(WALKIN,'Walk-in')]

    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'
    STATUSES = [(PENDING,'Pending'),(PAID,'Paid'),(CANCELLED,'Cancelled')]

    order_type = models.CharField(max_length=16, choices=TYPES)
    customer_profile = models.ForeignKey('accounts.CustomerProfile', on_delete=models.SET_NULL, null=True, blank=True)
    walk_in_name = models.CharField(max_length=255, blank=True)
    walk_in_phone = models.CharField(max_length=32, blank=True)

    gram = models.CharField(max_length=64, blank=True, null = True)
    karate = models.CharField(max_length=64, blank=True, null = True)

    salesman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sales')
    status = models.CharField(max_length=16, choices=STATUSES, default=PENDING)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Order#{self.id} {self.order_type} {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    gram = models.CharField(max_length=64, blank=True)
    karate = models.CharField(max_length=64, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    @property
    def line_total(self): return self.unit_price * self.quantity
    @property
    def profit(self): return (self.unit_price - self.cost_price) * self.quantity

class Payment(models.Model):
    CASH = 'CASH'
    TRANSFER = 'TRANSFER'
    POS = 'POS'
    METHODS = [(CASH,'Cash'),(TRANSFER,'Transfer'),(POS,'POS')]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=16, choices=METHODS, default=CASH)
    reference = models.CharField(max_length=64, blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Payment {self.amount} for Order#{self.order_id}"

class Return(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Return {self.quantity} of {self.order_item}"
