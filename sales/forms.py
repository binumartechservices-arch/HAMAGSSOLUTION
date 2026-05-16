from django import forms
from accounts.models import CustomerProfile
from .models import Payment

class CheckoutForm(forms.Form):
    ORDER_TYPES = [
        ('REGULAR', 'Regular Customer'),
        ('WALKIN', 'Walk-in Customer')
    ]

    order_type = forms.ChoiceField(
        choices=ORDER_TYPES,
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none"
        })
    )
    customer = forms.ModelChoiceField(
        queryset=CustomerProfile.objects.filter(is_walk_in=False),
        required=False,
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none"
        })
    )
    gram = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Grams"
        })
    )
    karate = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Karate"
        })
    )
    walk_in_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Walk-in customer name"
        })
    )
    walk_in_phone = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Walk-in customer phone"
        })
    )
    discount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Discount (₦)"
        })
    )
    payment_method = forms.ChoiceField(
        choices=Payment.METHODS,
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none"
        })
    )
    paid_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-indigo-400 focus:outline-none",
            "placeholder": "Amount paid"
        })
    )


class ReturnForm(forms.Form): 
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-pink-400 focus:outline-none",
            "placeholder": "Enter quantity to return"
        })
    )
    reason = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            "class": "w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 focus:ring-2 focus:ring-pink-400 focus:outline-none",
            "rows": 3,
            "placeholder": "Reason for return (optional)"
        })
    )
