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

        # Search OMDb API  user-provided search term (keyword)
        keyword = request.POST["keyword"]

        url = "https://www.omdbapi.com/?apikey=91050fbc&s=" + keyword
        
        # OMDb API response
        results = []

        response = requests.get(url)
        jsonResponse = response.json()
        movies = jsonResponse["Search"]

        for movie in movies:

            entry = {}

            entry.update({'id': movie['imdbID'], 'title': movie['Title'], 'year': movie['Year'], 'poster': movie['Poster'], 'type': movie['Type']})

            results.append(entry)


        if not movies:
            return render(request, "movies/search.html", {
                "message": "No movies found."
            })
        elif movies:
            return render(request, "movies/search.html", {
                "movies": results,
                "keyword": keyword
            })


def details(request, id):
    print("Debug - id: ", id)

    # Get movie details
    # url = "https://www.omdbapi.com/?apikey=91050fbc&plot=full&i=" + id

    url = "https://www.omdbapi.com/?apikey=91050fbc&plot=full&i=" + id
    
    print("Debug - url: ", url)

    result = []

    response = requests.get(url)
    jsonResponse = response.json()
    movie = jsonResponse


    print("Debug - movie: ", movie)
    
    attributes = {}
    
    
    if movie: attributes.update({'imdbID': movie['imdbID'], 'title': movie['Title'], 'year': movie['Year'], 'rated': movie['Rated'], 'released': movie['Released'], 'plot': movie['Plot'], 'poster': movie['Poster'], 'type': movie['Type'], 'runtime': movie['Runtime'], 'genre': movie['Genre'], 'director': movie['Director'], 'actors': movie['Actors'], 'language': movie['Language'], 'awards': movie['Awards'], 'metascore': movie['Metascore'], 'votes': movie['imdbVotes']}) 
        # attributes.update({'imdbID': item['imdbID'], 'title': item['Title'], 'year': item['Year'], 'plot': item['Plot'], 'poster': item['Poster'], 'type': item['Type']}) 
        # 
    result = result.append(attributes)

    print("Debug - attributes: ", attributes)   
    print("Debug - result: ", result)

    return render(request, "movies/details.html", {
        "item": attributes
    })


def like(request, movie_id):

    # Debug: print("Debug | Like function")

    # Get user and relevant movie
    user = User.objects.get(id=request.user.id)
    # movie = Movie.objects.get(id=movie_id)
    imdbID = request.POST.get( movie_id)

    print("Debug | user: ", user)
    print("Debug | movie_id: ", imdbID)
    
    add_movie = Movie(
        imdb_id = imdbID,
        like_by = user
     )

    add_movie.save()
    # print("Debug | movie: ", movie)

    # # If user likes movie unlike (and vice versa)
    # if user in movie.like.all():
    #     # print("Debug | User already likes this movie - unliking now")
    #     movie.like.remove(user)

    # else:
    #     # print("Debug: user does not yet like this movie - liking now")
    #     movie.like.add(user)

    return JsonResponse({"message": "Post liked / disliked"})

def add_mylist(request, id):
    print("Debug - add_mylist: ", id)
    Movie_data = Movie.objects.get(pk=id)
    current_user = request.user
    Movie_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("_details", args=(id, )))
    # return render(request, "movies/add_mylist.html")

def remove_mylist(request, id):
    print("Debug - remove_mylist: ", id)
    # return render(request, "movies/remove_mylist.html")

def mylist(request, id):
    print("Debug - mylist: ", id)
    # def add_mylist(request):
    #     return render(request, "movies/add_mylist.html")


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