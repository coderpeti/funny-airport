# Importing the necessary libraries
from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from .models import Airport, Flight, Passenger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import pathlib


# Create your tests here.
class BasicTestCase(TestCase):
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
        url = reverse("users:index")
        response = c.get(url)
        self.assertEqual(response.status_code, 200)


class SearchAirportTestcase(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(city="Budapest", code="BUD")
        
    def test_search_airports_valid(self):
        c = Client()
        url = reverse("users:search_airports")
        response = c.get(url, {"query": "Budapest"})
        self.assertEqual(response.status_code, 200)
    

class FrontendTestCase(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def file_uri(self, file):
        return pathlib.Path(os.path.abspath(file)).as_uri()

    def test_booking_form(self):
        self.driver.get(f"{self.live_server_url}/users/")
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "booking_form"))
            )
            self.assertTrue(element.is_displayed())
        except (TimeoutException, NoSuchElementException):
            self.fail("ERROR: The booking form did not appear!")
    
    def tearDown(self):
        self.driver.quit()

    