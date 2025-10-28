# Importing the necessary libraries
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Airport, Booked, Flight
from .forms import RegistrationForm, LoginForm, BookingForm, CheckoutForm
from .utils import render_with_results_form, render_user_flights, is_ajax
from workers.models import SpecialOffer
import random
import re

# Create your views here.

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
                flights = [flight for flight in flights if flight.available_seats() >= passengers]
                results =  [
                    {
                        "id": flight.id,
                        "origin": f"{flight.origin.city} ({flight.origin.code})", 
                        "destination": f"{flight.destination.city} ({flight.destination.code})", 
                        "duration": flight.duration, 
                        "capacity": flight.capacity, 
                        "available": flight.available_seats()
                    }
                    for flight in flights
                ]
                
                # Check if there is a match
                if not flights:
                    message = f"Unfortunately, there are no available flights between {origin_name.group(1)} and {destination_name.group(1)}"
                    return render_with_results_form(request, results=[], message=message)
                # If there is a match, return the results
                return render_with_results_form(request, results=results, message=None, passengers=passengers)
            
            except Airport.DoesNotExist:
                return HttpResponse("Error: One of the airports does not exist.", status=400)
                
    else:
        form = BookingForm()

    # Load form
    return render(request, "users/index.html", {"form":form})


# Search Airports
def search_airports(request):
    # Checking the header of the django request object
    if is_ajax(request):
        # Retrieve the query
        query = request.GET.get("query", "") 

        if query == "":
            return JsonResponse([], safe=False) 

        # Selecting airports that contain the query
        airports = Airport.objects.filter(Q(city__icontains=query) | Q(code__icontains=query)).values("city", "code")
        airports_list = [f"{airport['city']} ({airport['code']})" for airport in airports]
        # Return JSON as a file that allows the list
        return JsonResponse(airports_list, safe=False)
    
    return JsonResponse([], safe=False)  


# Registration and Login Page
def user_authentication(request, register_login):
    # If the user's profile is currently available
    if request.user.is_authenticated:
       return HttpResponseRedirect(reverse("users:profile"))

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
        if is_ajax(request):
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
        if is_ajax(request):
            # Load a template without returning the entire page, adding the request parameter because of csrf
            html = render_to_string("users/login.html", {"form": form}, request)
            # Return the html code as a json file
            return JsonResponse({"html": html})

        # Normal loading of page in case of get request
        return render(request, "users/authentication.html", {"form": form, "reg_or_log": "log"})


# Profile Page
def user_profile(request):
    # If the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponse("Error: You are not logged in.", status=401)
    
    return render(request, "users/user_profile.html")


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:authentication", args=["login-registration"]))


# To Browse Special Offers Page
def special_offers(request):
    if is_ajax(request):
        # Get the list of offers
        offers = SpecialOffer.objects.all().order_by("-id")

        # Pass the offers to the first `n` offers
        start_index = int(request.GET.get("start_index", 0))
        # We display 8 offers at once
        batch_size = 8

        # Slicing the offers into the desired block
        offers_batch = offers[start_index:start_index + batch_size]

        offers_data = []
        all_flights = list(Flight.objects.all())

        for offer in offers_batch:
            # Random flight selection
            random_flight = random.choice(all_flights) if all_flights else None
            random_flight_id = random_flight.id if random_flight else None
            available_seats = random_flight.available_seats() if random_flight else None
            offers_data.append({
                "offer_text": offer.offer_text,
                "number_of_passengers": offer.number_of_passengers,
                "worker_name": offer.worker.name,
                "random_flight_id": random_flight_id,
                "available_seats": available_seats
            })

        # We return the offers and the next batch information
        next_start_index = start_index + batch_size if len(offers_batch) == batch_size else None
        return JsonResponse({
            "offers": offers_data,
            "next_start_index": next_start_index
        })
    
    return render(request, "users/special_offers.html")


# My Tickets Page
def my_tickets(request):
    # If the user is not logged in
    if not request.user.is_authenticated:
        return render_user_flights(request, results=[], message="You are not logged in")
    
    # Select the planes belonging to the user
    bookings = Booked.objects.filter(user=request.user)

    # If there are not reservations for the user
    if not bookings.exists():
        return render_user_flights(request, results=[], message="No flights booked yet")

    results =  [
        {
            "id": booking.id,
            "origin": f"{booking.flight.origin.city} ({booking.flight.origin.code})", 
            "destination": f"{booking.flight.destination.city} ({booking.flight.destination.code})", 
            "duration": booking.flight.duration, 
            "passengers": booking.passengers, 
            "carry_on_bags": booking.carry_on_bags,
            "checked_bags": booking.checked_bags
        }
        for booking in bookings
    ]
    
    # If there is a match, return the results
    return render_user_flights(request, results=results, message=None)


# Checkout Page
def checkout(request):
    # If the user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:authentication", args=["registration-login"]))
    
    # If POST is the request method
    if request.method == "POST":
        form = CheckoutForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Retrieve data
            flight_id = request.GET.get("flight_id")
            passengers = request.GET.get("passengers")
            if not flight_id or not passengers:
                return HttpResponse("Error: Missing flight_id or passengers.", status=400)
            carry_on_bags = form.cleaned_data["carry_on_bags"]
            checked_bags = form.cleaned_data["checked_bags"]
            
            # To be safe, we check to see if the flight actually exists
            try:
                flight = Flight.objects.get(pk=flight_id)
                Booked.objects.create(user=request.user, flight=flight, passengers=passengers, carry_on_bags=carry_on_bags, checked_bags=checked_bags)
                
                # If the flight is full, we delete it
                if flight.available_seats() == 0:
                    flight.delete()

                # We create a new reservation
                return HttpResponseRedirect(reverse("users:purchase"))

            except Flight.DoesNotExist:
                return HttpResponse("Error: Flight not found.", status=404)
        
    else:
        form = CheckoutForm()

    # Load form
    return render(request, "users/checkout.html", {"form": form})


# Purchase Page
def purchase(request):
    # If the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponse("Error: You are not logged in.", status=401)
    
    # Select the planes belonging to the user
    bookings = Booked.objects.filter(user=request.user)
    
    # If there are not reservations for the user
    if not bookings.exists():
        return HttpResponse("Error: No flights booked yet.", status=404)
    
    return render(request, "users/purchase.html")


# Cancel Booking
# Only use this function if it was triggered by a POST request
@require_POST
def cancel_booking(request):
    booking_id = request.POST.get("booking_id")
    booking = Booked.objects.get(pk=booking_id, user=request.user)
    booking.delete()
    
    return HttpResponseRedirect(reverse("users:my_tickets"))

# new laptop backup :)