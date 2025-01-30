from django.db import models

# Create your models here.


# The class to define airports
class Airport(models.Model):
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"City: {self.city} | Code: {self.code}"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") 
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"Origin: {self.origin} | Destination: {self.destination} | Duration: {self.duration}"


class Passanger(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    gmail = models.EmailField(max_length=255, unique=True)
    
