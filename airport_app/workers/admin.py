# Importing the necessary libraries
from django.contrib import admin
from .models import Worker, SpecialOffer

# Register your models here.
admin.site.register(Worker)
admin.site.register(SpecialOffer)