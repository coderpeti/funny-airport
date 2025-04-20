# Importing the necessary libraries
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, BookingForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from .models import Airport, Flight
import re

# Create your views here.
# Helper functions
def render_with_results_form(request, form, results=None):
    return render(request, "users/index.html", {"form": form, "results": results})

# Home Page
def index(request):
    
    # If POST is the request method
    if request.method == "POST":
        form = BookingForm(request.POST)
        
        # If the form is valid
        if form.is_valid():
            # Retrieve data
            origin_name = re.search(r'\((.*?)\)', form.cleaned_data["origin"])
            destination_name = re.search(r'\((.*?)\)', form.cleaned_data["destination"])
            passengers = form.cleaned_data["passengers"]

            try:
                # Find airports by city
                origin_airport = Airport.objects.get(code=origin_name.group(1))
                destination_airport = Airport.objects.get(code=destination_name.group(1))
                # Search in the Flight model
                flights = Flight.objects.filter(origin=origin_airport, destination=destination_airport)
                results =  [f"ORIGIN: {flight.origin.city} ({flight.origin.code}) DESTINATION: {flight.destination.city} ({flight.destination.code}) DURATION: {flight.duration}" for flight in flights]
                
                # Check if there is a match
                if not flights.exists():
                    return render_with_results_form(request, BookingForm(), f"Unfortunately, there are no available flights between {origin_name.group(1)} and {destination_name.group(1)}")
                # If there is a match, return the results
                
                return render_with_results_form(request, BookingForm(), results)
            
            except Airport.DoesNotExist:
                return HttpResponse("Error: One of the airports does not exist.", status=400)
                
    else:
        form = BookingForm()

    # Load form
    return render(request, "users/index.html", {"form":form})


# Search Airports
def search_airports(request):

    # Checking the header of the django request object
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        # Retrieve the query
        query = request.GET.get("query", "") 

        if query == "":
            return JsonResponse([], safe=False) 

        # Selecting airports that contain the query
        airports = Airport.objects.filter(city__icontains=query).values("city", "code")
        airports_list = [f"{airport["city"]} ({airport["code"]})" for airport in airports]
        # Return JSON as a file that allows the list
        return JsonResponse(airports_list, safe=False)
    
    return JsonResponse([], safe=False)  


# Registration and Login Page
def user_authentication(request, register_login):
    
    # If the user's profile is currently available
    #if request.user.is_authenticated:
    #    return HttpResponseRedirect(reverse("users:profile"))

    # If the user wants to register
    if register_login == "registration-login":
        
        # Setting the form
        form = RegistrationForm(request.POST or None)

        # If a POST request is received and form is valid
        if request.method == "POST" and form.is_valid():          
            # Create a new user
            # We don't save it completely with commit
            user = form.save(commit=False)
            # We set the password1 field as a password, which will be automatically encrypted
            user.set_password(form.cleaned_data["password1"])
            # Full save of the user
            user.save()
            # Login to the user
            login(request, user)
            # Return a Json file with the success and the path to which we direct the user
            return JsonResponse({"success": True, "redirect": "/users/"})
        
        # Checking the header of the django request object
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Load a template without returning the entire page, adding the request parameter because of csrf
            html = render_to_string("users/registration.html", {"form": form}, request)
            # Return the html code as a json file
            return JsonResponse({"html": html})

        # Normal loading of page in case of get request
        return render(request, "users/authentication.html", {"form": form, "reg_or_log": "reg"})
    
    # If the user wants to login
    elif register_login == "login-registration": 
        # Setting the form
        form = LoginForm(request.POST or None)

        # If a POST request is received and form is valid
        if request.method == "POST" and form.is_valid():
            # Authentication and Login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # User verification based on the specified username and password
            user = authenticate(username=username, password=password)

            # If the user is authentic
            if user:
                # Login to the user
                login(request, user)
                # Return a Json file with the success and the path to which we direct the user
                return JsonResponse({"success": True, "redirect": "/users/"})

        # Checking the header of the django request object    
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Load a template without returning the entire page, adding the request parameter because of csrf
            html = render_to_string("users/login.html", {"form": form}, request)
            # Return the html code as a json file
            return JsonResponse({"html": html})

        # Normal loading of page in case of get request
        return render(request, "users/authentication.html", {"form": form, "reg_or_log": "log"})


# Profile Page
def user_profile(request):
    return render(request, "users/user_profile.html")


# Logout Page
def user_logout(request):
    pass


# To Browse Special Offers Page
def special_offers(request):
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
