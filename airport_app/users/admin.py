# Importing the necessary libraries
from django.contrib import admin
from .models import Airport, Flight, Booked

# Adding models to the admin interface
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Booked)

