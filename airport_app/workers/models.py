# Importing the necessary libraries
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


# The class to define workers
class Worker(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    
    # Change the save method to encrypt
    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2', 'argon2', 'bcrypt')):
            self.password = make_password(self.password)
        super(Worker, self).save(*args, **kwargs)

    # Return an easy-to-read format from the object
    def __str__(self):
        return f"Name: {self.name} | Email: {self.email} | Position: {self.position}"
    

# The class to define special offers
class SpecialOffer(models.Model):
    offer_text = models.TextField()
    number_of_passengers = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def __str__(self):
        return f"Offer text: {self.offer_text} | Number of passengers: {self.number_of_passengers} | Worker: {self.worker}"