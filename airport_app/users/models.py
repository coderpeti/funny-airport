# Importing the necessary libraries
from django.db import models
from django.contrib.auth.models import User
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
    capacity = models.IntegerField(validators=[MinValueValidator(1)], default=100)

    # Defining a flight validation function
    def is_valid_flight(self):
        return self.origin != self.destination
    
    def available_seats(self):
        booked_passengers = sum(booking.passengers for booking in self.bookings.all())
        return self.capacity - booked_passengers

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"Origin: {self.origin} | Destination: {self.destination} | Duration: {self.duration} | Capacity: {self.capacity}"


# The class to define booked flights
class Booked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    passengers = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    carry_on_bags = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    checked_bags = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"User: {self.user} | Flight: {self.flight} | Passengers: {self.passengers} | Carry on bags: {self.carry_on_bags} | Checked bags: {self.checked_bags}"
