# Importing the necessary libraries
from django.contrib import admin
from .models import Airport, Flight, Passenger

# Register your models here.
# Simplifying the management of the many to many database
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights", )


# Adding models to the admin interface
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger, PassengerAdmin)

