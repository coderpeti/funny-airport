# Importing the necessary libraries
from django.test import TestCase, Client
from selenium import webdriver
import os
import pathlib
from .models import Airport, Flight, Passenger

# Get the file's uniform resource identifier
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Setting the default browser for testing
driver = webdriver.Chrome

# Create your tests here.
class UserTestCase(TestCase):
    # Create test data
    def setUp(self):
        a1 = Airport.objects.create(city="City A", code="AAA")
        a2 = Airport.objects.create(city="City B", code="BBB")
        
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=100)

    # Testing the authenticity of flights
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        f2 = Flight.objects.get(origin=a1, destination=a1, duration=100)
        self.assertTrue(f.is_valid_flight())
        self.assertFalse(f2.is_valid_flight())
    
    # Home page testing
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    