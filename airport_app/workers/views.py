# Importing the necessary libraries
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from .models import Worker
from .forms import LoginForm, SpecialOfferForm


# Create your views here.

# Home Page
def index(request):
    # If POST is the request method
    if request.method == "POST":
        form = LoginForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Retrieve data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                worker = Worker.objects.get(email=email)

                # Check if the password is correc
                if check_password(password, worker.password):
                    # Save the worker id in the session
                    request.session["worker_id"] = worker.id
                    return HttpResponseRedirect(reverse("workers:making_a_special_offer"))

                else:
                    return HttpResponseRedirect(reverse("workers:index"))

            # If the worker does not exist
            except Worker.DoesNotExist:
                return HttpResponseRedirect(reverse("workers:index"))

    else:
        form = LoginForm()

    return render(request, "workers/login.html", {"form": form})


# Special Offer Page
def making_a_special_offer(request):
    if "worker_id" not in request.session:
        return HttpResponseRedirect(reverse("workers:index"))

    # If POST is the request method
    if request.method == "POST":
        form = SpecialOfferForm(request.POST)

        # If the form is valid
        if form.is_valid():
            worker = Worker.objects.get(pk=request.session.get("worker_id"))
            special_offer = form.save(commit=False)
            special_offer.worker = worker
            special_offer.save()

            return HttpResponseRedirect(reverse("workers:making_a_special_offer"))
    
    else:
        form = SpecialOfferForm()

    return render(request, "workers/special_offer.html", {"form": form})
