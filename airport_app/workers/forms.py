# Importing the necessary libraries
from django import forms
from .models import SpecialOffer


# Creating a special offers form
class SpecialOfferForm(forms.ModelForm):
    class Meta:
        model = SpecialOffer
        fields = ["offer_text", "number_of_passengers"]

    # We give the offer text an id so that we can style it more easily in CSS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["offer_text"].widget.attrs.update({
            "id": "textarea"
        })
        self.fields["number_of_passengers"].widget.attrs.update({
            "min": "1",
            "max": "10"
        })


# Creating a login form
class LoginForm(forms.Form):
    # Entering a password and a username
    email = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

