# Defining links
from django.urls import path
from . import views

app_name = "workers"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("making-a-special-offer", views.making_a_special_offer, name="making_a_special_offer")
]