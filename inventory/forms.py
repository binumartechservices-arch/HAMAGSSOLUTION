from django import forms
from .models import Medicine

from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name',
            'gram',
            'karate',
            # 'sku',
            # 'barcode',
            # 'category',
            # 'supplier',
            'cost_price',
            'selling_price',
            'quantity_in_stock',
            'reorder_level',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter product name',
                'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            'gram': forms.TextInput(attrs={
                'placeholder': 'Enter gram',
                'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            'karate': forms.TextInput(attrs={
                'placeholder': 'Enter karate',
                'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            # 'sku': forms.TextInput(attrs={
            #     'placeholder': 'Unique SKU',
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            # 'barcode': forms.TextInput(attrs={
            #     'placeholder': 'Optional barcode',
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            # 'category': forms.Select(attrs={
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            # 'supplier': forms.Select(attrs={
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            'cost_price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Cost price (₦)',
                'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            'selling_price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Selling price (₦)',
                'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            # 'quantity_in_stock': forms.NumberInput(attrs={
            #     'placeholder': 'Available quantity',
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            # 'reorder_level': forms.NumberInput(attrs={
            #     'placeholder': 'Reorder level',
            #     'class': 'w-full px-3 py-2 border rounded-xl bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm focus:ring-2 focus:ring-primary focus:border-primary'
            # }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary border-gray-300 rounded focus:ring-primary'
            }),
        }
