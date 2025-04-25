# Defining links
# Importing the necessary libraries
from django.urls import path
from . import views

# Defining the name of the app, with which we provide easier access to the links
app_name = 'users'

urlpatterns = [
    path("", views.index, name="index"),
    path("search-airports/", views.search_airports, name="search_airports"),
    path("authentication/<str:register_login>/", views.user_authentication, name="authentication"),
    path("profile/", views.user_profile, name="profile"),
    path("logout/", views.user_logout, name="logout"),
    path("special-offers/", views.special_offers, name="special_offers"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("checkout/", views.checkout, name="checkout"),
    path("purchase/", views.purchase, name="purchase"),
    path("cancel_booking/", views.cancel_booking, name="cancel_booking")
]


