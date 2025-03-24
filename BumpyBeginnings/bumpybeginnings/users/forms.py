from django import forms
from .models import SiteUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password',
        min_length=5,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password',
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 1:
            raise ValidationError("Username must be at least 1 character long.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


class SiteUserForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ['isMother', 'dueDate', 'partnerName']
        labels = {
            'isMother': 'Are you the mother?',
            'dueDate': "Due Date/Child's Birthday",
            'partnerName': "Partner's Name",
        }
        widgets = {
            'isMother': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dueDate': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400',
            }),
            'partnerName': forms.TextInput(attrs={
                'placeholder': "Your Partner's Name",
                'class': 'form-control',
                'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
            }),
        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
            }),
        }

# code repurposed from my AWD Final project
class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-400 focus:border-sky-400'
        })
    )

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # if the user provides a new password, ensure that the passwords match
        if password and password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")

        return cleaned_data