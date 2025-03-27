# Importing the necessary libraries
from django import forms
from django.contrib.auth.models import User


# Creating a registration form
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
        help_texts = {
            "email": None,
            "username": None,
        }

    # Password identity check
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 != password2:
            raise forms.ValidationError("The Two Passwords Do Not Match")
        return password2
    

# Creating a login form
class LoginForm(forms.Form):
    # Entering a password and a username
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



# Creating a booking form
class BookingForm(forms.Form):
    # Origin and destination
    origin = forms.CharField(label="Origin")
    destination = forms.CharField(label="Destination")
    # Number of passengers
    passengers = forms.IntegerField(label="Passengers", min_value=1, max_value=10)