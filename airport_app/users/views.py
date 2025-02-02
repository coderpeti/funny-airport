# Importing the necessary libraries
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.

# Home Page
def index(request):
    pass


# Registration and Login Page
def user_authentication(request, register_login):
    # If the user wants to register
    if register_login == "registration":
        # If a POST request is received
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            # If the form is valid
            if form.is_valid():
                # Create a new user
                # We don't save it completely with commit
                user = form.save(commit=False)
                # We set the password1 field as a password, which will be automatically encrypted
                user.set_password(form.cleaned_data["password1"])
                user.save()

                # Authentication and Login
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:index'))

        else:
            form = RegistrationForm()

        return render(request, 'users/registration.html', {"form": form})
    
    # If the user wants to login
    elif register_login == "login":
        pass


# Logout Page
def user_logout(request):
    pass


# To Browse Special Offers Page
def special_offers(request):
    pass


# Ticket Purchase Page
def tickets(request):
    pass


# My Tickets Page
def my_tickets(request):
    pass


# Checkout Page
def checkout(request):
    pass


# Purchase Page
def purchase(request):
    pass
