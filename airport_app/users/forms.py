# Importing the necessary libraries
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    # Entering a password
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password Confirmation")

    # Entering metadata
    class Meta:
        # Use of user model
        model = User
        # Setting basic fields other than the password
        fields = ["username", "email"]

    # Password identity check
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 != password2:
            raise forms.ValidationError("The Two Passwords Do Not Match")
        return password2