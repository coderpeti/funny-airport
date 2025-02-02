# Defining links
# Importing the necessary libraries
from django.urls import path
from . import views

# Defining the name of the app, with which we provide easier access to the links
app_name = "workers"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("making-a-special-offer", views.making_a_special_offer, name="making_a_special_offer")
]