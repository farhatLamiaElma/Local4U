from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
import re


def validate_contact_number(value):
    """
    Validates that the contact number starts with +1 and has exactly 10 digits after the country code.
    """
    if not re.match(r"^\+1\d{10}$", value):
        raise ValidationError("Contact number must start with +1 and contain exactly 10 digits.")


class UserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password],
        help_text="Password must have at least one capital letter, one special character, and be at least 8 characters long."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Re-enter the password to confirm."
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'user_type', 'address', 'contact_number', 'password']

    def clean(self):
        """
        Perform custom validation for password confirmation.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if passwords match
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        # Ensure password meets criteria for at least one capital letter and one special character
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must have at least one uppercase letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:'\",.<>?/" for char in password):
            raise forms.ValidationError("Password must have at least one special character.")

        return cleaned_data

    def clean_email(self):
        """
        Validate that the email is unique and properly formatted.
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_contact_number(self):
        """
        Validate the contact number format.
        """
        contact_number = self.cleaned_data.get('contact_number')
        validate_contact_number(contact_number)
        return contact_number


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'address', 'contact_number', 'profile_picture']
