# Importing the necessary libraries
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


# The class to define airports
class Airport(models.Model):
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=3, unique=True)

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"City: {self.city} | Code: {self.code}"


# The class to define flights
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") 
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField(validators=[MinValueValidator(1)])

    # Defining a flight validation function
    def is_valid_flight(self):
        return self.origin != self.destination
    
    # Return an easy-to-read format from the object
    def __str__(self):
        return f"Origin: {self.origin} | Destination: {self.destination} | Duration: {self.duration}"


# The class to define booked flights
class Booked(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    passengers = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"Flight: {self.flight} | Passengers: {self.passengers}"


# The class to define passengers
class Passenger(models.Model):
    gmail = models.EmailField(max_length=255, unique=True)
    booked_flights = models.ManyToManyField(Booked, blank=True, related_name="booked_flights")

    # Return an easy-to-read format from the object
    def __str__(self):
         return f"Gmail: {self.gmail} | Booked_flights: {self.booked_flights}"
    

