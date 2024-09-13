from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator  # Pagination functionality
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
import requests
import json  # JSON functionality
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):    
    return render(request, "movies/index.html")


def top_rated(request):
    # all posts 5 per page
    movies = Movie.objects.all().order_by("imdb_rating").reverse()
    # print("Debug - top_rated: ", Movie.objects.all())
    print("Debug - top_rated: Movie  <QuerySet")
    # movies = Movie.objects.all().order_by("imdbRating").reverse()
    paginator = Paginator(movies, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print("Debug | all posts:",posts)
    return render(request, "movies/top-rated.html", {"page_obj": page_obj})


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
            title = {}
            title.update(
                {
                    "imdb_id": movie["imdbID"],
                    "title": movie["Title"],
                    "year": movie["Year"],
                    "poster": movie["Poster"],
                    "type": movie["Type"],
                }
            )

            results.append(title)

        if not movies:
            return render(
                request, "movies/search.html", {"message": "No movies found."}
            )
        elif movies:
            return render(
                request, "movies/search.html", {"movies": results, "keyword": keyword}
            )


def watchlist(request, user_id):
    current_user = user_id
    my_list = current_user._movie_mylist.all()
    return render(request, "movies/profile.html", {"movies": my_list})


def check_imdbid_and_user(user_id, imdb_id):
    try:
        # instance = Movie.objects.get(user_id=user_id, imdb_id=imdb_id)
        instance = Movie.objects.get(user_id=user_id, imdb_id=imdb_id)
        print("Debug: check_imdbid_and_user: ", instance)
        if user_id == instance.user_id:
            return False
        return True
    except Movie.DoesNotExist:
        return False

# TODO
def details(request, imdb_id):

    # Get movie details
    url = "https://www.omdbapi.com/?apikey=91050fbc&plot=full&i=" + imdb_id

    result = []

    response = requests.get(url)
    jsonResponse = response.json()
    movie = jsonResponse

    attributes = {}

    if movie:
        attributes.update(
            {
                "imdb_id": movie["imdbID"],
                "title": movie["Title"],
                "year": movie["Year"],
                "rated": movie["Rated"],
                "released": movie["Released"],
                "plot": movie["Plot"],
                "poster": movie["Poster"],
                "type": movie["Type"],
                "runtime": movie["Runtime"],
                "genre": movie["Genre"],
                "director": movie["Director"],
                "actors": movie["Actors"],
                "language": movie["Language"],
                "awards": movie["Awards"],
                "metascore": movie["Metascore"],
                "votes": movie["imdbVotes"],
                "imdb_rating": movie["imdbRating"],
            }
        )

    result = result.append(attributes)

    if Movie.objects.filter(imdb_id=imdb_id).exists():
        print("1) title exists")

        title = Movie.objects.get(imdb_id=imdb_id)
        movie_pk = Movie.objects.get(pk=title.pk)
        # movie_is_bookmarked = request.user in movie_pk.is_bookmarked.all()
        all_comments = Comment.objects.filter(movie=movie_pk)
        is_owner = request.user.username == movie_pk.user.username
   

        # print("2) - movie_instance: ", movie_instance.imdb_id)
        return render(
            request,
            "movies/details.html",
            {
                "movie": title,
                "movie_pk": movie_pk,
                # "in_watchlist": in_watchlist,
                "all_comments": all_comments,
                "is_owner": is_owner,
            },
        )
    else:
        print("3) - title not in local db")
        title = attributes
        print("4) - title: ", title)

    return render(request, "movies/details.html", {"movie": title})


def like(request, movie_id):
    # Get user and relevant movie
    user = User.objects.get(id=request.user.id)
    # movie = Movie.objects.get(id=movie_id)
    imdb_id = request.POST.get(movie_id)

    print("Debug | user: ", user)
    print("Debug | movie_id: ", imdb_id)

    add_movie = Movie(imdb_id=imdb_id, like_by=user)

    add_movie.save()

    return JsonResponse({"message": "Post liked / disliked"})


def add_comment(request, id):
    current_user = request.user
    movie_data = Movie.objects.get(pk=id)
    message = request.POST["new_comment"]
    imdb = movie_data.imdb_id
    print("Debug - imdb: ", imdb)

    # save comment to database
    new_comment = Comment(author=current_user, movie=movie_data, message=message)
    new_comment.save()

    imdb_id = movie_data.imdb_id

    return HttpResponseRedirect(reverse("_details", args=(imdb_id,)))


def my_list(request, id):
    # Listing.objects.get(pk=id)
    movie_instance = Movie.objects.get(pk=id)
    current_user = request.user
    movie_instance.my_list.add(current_user)
    return HttpResponseRedirect(reverse("_details", args=(movie_instance.id,)))


# TODO FIX THIS TO ACCEPT NEW MOVIES to my_list
def add_mylist(request):
    imdb_id = request.POST["imdb_id"] # tt0077889
    print("MR IMDB-imdb_id: ", imdb_id)
    current_user = User.objects.get(pk=request.user.id) # george
    print("CURRENT USER: ", current_user) # alma george

    if request.method == "GET":
        return render(request, "movies/index.html", {})

    elif Movie.objects.filter(imdb_id=imdb_id).exists():
        movie_instance = Movie.objects.filter(imdb_id=imdb_id).first()
        print("add_mylist-movie_instance: ", movie_instance) # id 1 george
        current_user = User.objects.get(pk=request.user.id) # george
        movie_instance.my_list.add(current_user) 
     

    elif request.method == "POST":
        user = request.user
        imdb_id = request.POST["imdb_id"]
        title = request.POST["title"]
        year = request.POST["year"]
        poster = request.POST["poster"]
        type = request.POST["type"]
        rated = request.POST["rated"]
        runtime = request.POST["runtime"]
        director = request.POST["director"]
        actors = request.POST["actors"]
        plot = request.POST["plot"]
        genre = request.POST["genre"]
        awards = request.POST["awards"]
        metascore = request.POST["metascore"]
        imdb_rating = request.POST["imdb_rating"]
        my_list = request.POST["my_list"]
        
        user = Movie(
            user=user,
            imdb_id=imdb_id,
            title=title,
            year=year,
            poster=poster,
            type=type,
            rated=rated,
            runtime=runtime,
            director=director,
            actors=actors,
            plot=plot,
            genre=genre,
            awards=awards,
            metascore=metascore,
            imdb_rating=imdb_rating,
        )
        user.save()

        current_user = User.objects.get(pk=request.user.id) # george
        movie_instance = Movie.objects.get(imdb_id=imdb_id) # whole movie attribute values
        movie_instance.my_list.add(current_user)

    return HttpResponseRedirect(reverse("_details", args=(imdb_id,)))

# TODO fix this logic
def remove_mylist(request):
    print("HELLOOOOOOOOO")
    imdb_id = request.POST["imdb_id"] # tt0077889
    current_user = User.objects.get(pk=request.user.id) # george
    movie_id = Movie.objects.get(imdb_id=imdb_id) # whole movie attribute values

    movie_id.my_list.remove(current_user)

    # return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
    return HttpResponseRedirect(reverse("_details", args=(imdb_id,))) 



def mylist(request, id):
    print("Debug - mylist: ", id)
    # def add_mylist(request):
    #     return render(request, "movies/add_mylist.html")


# TODO
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    print("Debug | user: ", user)
    all_movies = Movie.objects.filter(user=user).order_by("id").reverse()
    my_list = user._movie_mylist.all()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(followed_by=user)
    
    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except: 
        is_following = False

    paginator = Paginator(all_movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "movies/profile.html", {
            "all_movies": all_movies,
            "page_obj": page_obj,
            "username": user.username,
            "following": following, 
            "followers": followers,
            "is_following": is_following,
            "user_profile": user,
            "my_list": my_list
        })


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_people = Follow.objects.filter(user=current_user)
    all_movies = Movie.objects.all().order_by('id').reverse()

    following_posts = []

    for post in all_movies:
        for person in following_people:
            if person.followed_by == post.user:
                following_posts.append(post)

    # Pagination
    paginator = Paginator(following_posts, 3 )
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "movies/following.html", {
        "posts_of_the_page": posts_of_the_page
    })


def follow(request):
    user_follow = request.POST['user_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow(user=current_user, followed_by=user_follow_data)
    f.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


def unfollow(request):
    user_follow = request.POST['user_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow.objects.get(user=current_user, followed_by=user_follow_data)
    f.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id})) 


# @csrf_exempt
def edit(request, post_id):

    print("Debug | Edit function, movie: ", post_id)

    # Get original movie
    movie = Movie.objects.get(pk=post_id)

    # Gets new text (edited) in JSON format
    data = json.loads(request.body)
    new_content = data.get("movie", "t")

    # Update movie to new text
    movie.content = new_content
    movie.save()

    # Return new text for instant display
    return JsonResponse(
        {"message": "Movie successfully edited", "new_text": new_content}, status=201
    )


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
            return render(
                request,
                "movies/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "movies/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "movies/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "movies/register.html")
