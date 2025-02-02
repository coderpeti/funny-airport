# Importing the necessary libraries
from django.db import models

# Create your models here.


# The class to define airports
class Airport(models.Model):
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"City: {self.city} | Code: {self.code}"


# The class to define flights
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") 
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    # Defining a flight validation function
    def is_valid_flight(self):
        if self.origin == self.destination or self.duration < 0:
            return False
        else:
            return True
    
    # Return an easy-to-read format from the object
    def __str__(self):
        return f"Origin: {self.origin} | Destination: {self.destination} | Duration: {self.duration}"


# The class to define passengers
class Passenger(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    gmail = models.EmailField(max_length=255, unique=True)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passangers")

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"First Name: {self.first_name} | Second Name: {self.second_name} | Gmail: {self.gmail} | Flights: {self.flights}"