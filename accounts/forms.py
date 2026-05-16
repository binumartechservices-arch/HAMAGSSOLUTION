from django.forms import ModelForm
from accounts.models import User    
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SalesmanProfile, CustomerProfile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter username'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter email'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help text
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        # Style password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                     'dark:border-gray-600 bg-white dark:bg-gray-800 '
                     'text-gray-700 dark:text-gray-200 '
                     'focus:ring-2 focus:ring-indigo-400 shadow-sm',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                     'dark:border-gray-600 bg-white dark:bg-gray-800 '
                     'text-gray-700 dark:text-gray-200 '
                     'focus:ring-2 focus:ring-indigo-400 shadow-sm',
            'placeholder': 'Confirm password'
        })


class SalesmanForm(ModelForm):
    class Meta:
        model = SalesmanProfile
        fields = ['full_name', 'phone', 'profile_pic']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter username'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-600 bg-white dark:bg-gray-800 '
                         'text-gray-700 dark:text-gray-200 '
                         'focus:ring-2 focus:ring-indigo-400 shadow-sm',
                'placeholder': 'Enter phone number'
            }),
            'profile_pic': forms.ClearableFileInput(attrs={
                'class': 'w-full text-gray-700 dark:text-gray-200'
            }),
        }
        