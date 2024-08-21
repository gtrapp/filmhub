from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from .models import *
import requests
import json

# Create your views here.
def index(request):
    return render(request, "movies/index.html")

# @login_required(redirect_field_name='my_redirect_field')
def profile(request, profile):

    return render(request, "movies/profile.html")


def search(request):

        # Default route (e.g. if accessed via a hyperlink)
    if request.method == "GET":
        return render(request, "movies/search.html")

    # If accessed via form submission (POST)
    elif request.method == "POST":

        # Search PQs using Parliament's API and user-provided search term (question ID)
        keyword = request.POST["keyword"]

        url = "https://www.omdbapi.com/?apikey=91050fbc&s=" + keyword

        print(url)

        movies = []

        response = requests.get(url)
        jsonResponse = response.json()
        # movies = jsonResponse["results"]
        movies = jsonResponse["movies"]

# Add dictionary item to list
        # entry.update({'id': questionID, 'subject': questionSubject, 'answered': questionAnswered, 'bookmarked': isBookmarked})
        # results.append(entry)
    print(movies)
    return render(request, "movies/search.html", {
        "movies": movies,
    
        })


# Log user in
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successfull
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "movies/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "movies/login.html")


# Log user out
# @login_required(redirect_field_name='my_redirect_field')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a new user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "movies/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "movies/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "movies/register.html")