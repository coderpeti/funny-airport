# Importing the necessary libraries
from django.shortcuts import render

# Helper functions
def render_with_results_form(request, results=None, message=None, passengers=None):
    return render(request, "users/results.html", {
        "results": results or [],
        "message": message,
        "passengers": passengers
    })

def render_user_flights(request, results=None, message=None):
    return render(request, "users/tickets.html", {
        "results": results or [],
        "message": message
    })

def is_ajax(request) -> bool:
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
