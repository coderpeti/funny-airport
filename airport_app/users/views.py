from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    pass


def authentication(request, register_login):
    # If the user wants to register
    if register_login == "registration":
        # If a POST request is received
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # Create a new user
                # We don't save it completely with commit
                user = form.save(commit=False)
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

        return render(request, 'registration.html', {"form": form})
    
    # If the user wants to login
    elif register_login == "login":
        pass


def logout(request):
    pass


def special_offers(request):
    pass


def tickets(request):
    pass


def my_tickets(request):
    pass


def checkout(request):
    pass


def purchase(request):
    pass
