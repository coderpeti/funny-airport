# Defining links
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("", views.index, name="index"),
    path("authentication/<str:register_login>/", views.authentication, name="authentication"),
    path("logout/", views.logout, name="logout"),
    path("special-offers/", views.special_offers, name="special_offers"),
    path("tickets/", views.tickets, name="tickets"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("checkout/", views.checkout, name="checkout"),
    path("purchase/", views.purchase, name="purchase")
]