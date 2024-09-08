from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator   # Pagination functionality  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
import requests
import json # JSON functionality
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    return render(request, "movies/index.html")


def top_rated(request):

    # all posts 5 per page
    movies = Movie.objects.all().order_by("imdb_rating").reverse()
    print("Debug - top_rated: ", Movie.objects.all())
    # movies = Movie.objects.all().order_by("imdbRating").reverse()
    paginator = Paginator(movies, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # print("Debug | all posts:",posts)

    return render(request, "movies/top-rated.html", {
        "page_obj": page_obj
    })



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
            title = {}
            title.update({'imdb_id': movie['imdbID'], 'title': movie['Title'], 'year': movie['Year'], 'poster': movie['Poster'], 'type': movie['Type']})
            
            results.append(title)

        if not movies:
            return render(request, "movies/search.html", {
                "message": "No movies found."
            })
        elif movies:
            return render(request, "movies/search.html", {
                "movies": results,
                "keyword": keyword
            })


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
    

def details(request, imdb_id):
    print("Debug - imdb_id: ", imdb_id)
   
    
    # Get movie details 
    url = "https://www.omdbapi.com/?apikey=91050fbc&plot=full&i=" + imdb_id

    result = []

    response = requests.get(url)
    jsonResponse = response.json()
    movie = jsonResponse

    # print("Debug - movie: ", movie)
    
    attributes = {}
    
    if movie: attributes.update({'imdb_id': movie['imdbID'], 'title': movie['Title'], 'year': movie['Year'], 'rated': movie['Rated'], 'released': movie['Released'], 'plot': movie['Plot'], 'poster': movie['Poster'], 'type': movie['Type'], 'runtime': movie['Runtime'], 'genre': movie['Genre'], 'director': movie['Director'], 'actors': movie['Actors'], 'language': movie['Language'], 'awards': movie['Awards'], 'metascore': movie['Metascore'], 'votes': movie['imdbVotes'], 'imdb_rating': movie['imdbRating']}) 
  
    result = result.append(attributes)

    # Movie.objects.filter(imdb_id=imdb_id).update(imdb_rating=movie['imdbRating'])
    # Movie.objects.filter(imdb_id=imdb_id).update(imdb_votes=movie['imdbVotes'])
    # title = Movie.objects.get(imdb_id=imdb_id)
    # print("Debug - title/attributes: ", title.year)

    # exists = check_imdbid_and_user(request.user.id, imdb_id)
    
    # if Movie.objects.filter(imdb_id=imdb_id).exists()
    if Movie.objects.filter(imdb_id=imdb_id).exists():
        print("Debug - title exists")
        
        title = Movie.objects.get(imdb_id=imdb_id)
        movie_pk = Movie.objects.get(pk=title.pk)
        # movie_is_bookmarked = request.user in movie_pk.is_bookmarked.all()
        all_comments = Comment.objects.filter(movie=movie_pk)
        is_owner = request.user.username == movie_pk.user.username
        # print("Debug - local db title: ", title.pk)
        # context = title
        print("Debug - title: ", title)
        return render(request, "movies/details.html", {
            "movie": title,
            "movie_pk": movie_pk,
            # "in_watchlist": in_watchlist,
            "all_comments": all_comments,
            "is_owner": is_owner
    })

    else:
        print("Debug - title not in local db")
        title = attributes
        print("Debug - context: ", title)
    return render(request, "movies/details.html", {
        "movie": title
    })

    


def like(request, movie_id):

    # Debug: print("Debug | Like function")

    # Get user and relevant movie
    user = User.objects.get(id=request.user.id)
    # movie = Movie.objects.get(id=movie_id)
    imdb_id = request.POST.get( movie_id)

    print("Debug | user: ", user)
    print("Debug | movie_id: ", imdb_id)
    
    add_movie = Movie(
        imdb_id = imdb_id,
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

# def add_mylist(request, id):
    # print("Debug - add_mylist: ", id)
    # Movie_data = Movie.objects.get(pk=id)
    # current_user = request.user
    # Movie_data.watchlist.add(current_user)
    # return HttpResponseRedirect(reverse("_details", args=(id, )))
    # return render(request, "movies/add_mylist.html")



def add_comment(request, id):
    current_user = request.user
    movie_data = Movie.objects.get(pk=id)
    message = request.POST['new_comment']
    imdb = movie_data.imdb_id
    print("Debug - imdb: ", imdb)
        
    # save comment to database
    new_comment = Comment(
        author=current_user, 
        movie=movie_data,
        message=message
        )
    new_comment.save()


    # return HttpResponseRedirect(reverse("_details", args=(imdb_id, )))
    return HttpResponseRedirect(reverse("movie._details", args=(id)))


    # if request.method == "POST":


    #     return HttpResponseRedirect(reverse("profile", args=(id, )))

    # else:
    #     return render(request, "movie/details.html")
    
    

    # current_user = request.user
    # movie_data = Movie.objects.get(pk=id)
    # message = request.POST['new_comment']
   
    # print("Debug - current_user: ", current_user)

    # new_comment = Comment(
    #     author=current_user,
    #     listing=movie_data,
    #     message=message
    # )
    # new_comment.save()

    # return HttpResponseRedirect(reverse("listing", args=(id, )))


# def save_title(request):
#     imdb_id = request.POST["imdb_id"]
#     print("Debug: imdb_id: ", imdb_id)
#     if request.method == "GET":
#         return render(request, "movies/details.html", {
#         })
#     elif request.method == "POST":
#         user = request.user
#         imdb_id = request.POST["imdb_id"]
#         title = request.POST["title"]
#         year = request.POST["year"]
#         poster = request.POST["poster"]
#         type = request.POST["type"]
#         rated = request.POST["rated"]
#         runtime = request.POST["runtime"]
#         director = request.POST["director"]
#         actors = request.POST["actors"]
#         plot = request.POST["plot"]
#         genre = request.POST["genre"]
#         awards = request.POST["awards"]
#         metascore = request.POST["metascore"]
#         imdb_rating = request.POST["imdb_rating"]
#         user = Movie(
#             user=user,
#             imdb_id=imdb_id,
#             title=title,
#             year=year,
#             poster=poster,
#             type=type,
#             rated=rated,
#             runtime=runtime,
#             director=director,
#             actors=actors,
#             plot=plot,
#             genre=genre,
#             awards=awards,
#             metascore=metascore,
#             imdb_rating=imdb_rating
#         )

#         title = user.save()
#         print("Debug: title: ", title)
#         return title
        
        # print("Debug: user: ", user)

        # return render(request, "movies/details.html", user{
        # })
    


    
def add_mylist(request):
    imdb_id = request.POST["imdb_id"]
    print("Debug - imdb_id: ", imdb_id)
    if request.method == "GET":
        return render(request, "movies/details.html", {
        })
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
            imdb_rating=imdb_rating
        )
        user.save()

        print("Debug - user: ", user.id)
     # return HttpResponseRedirect(reverse(index))
    # print("Debug - current_usert: ", current_user)
    # movie_id = Movie.objects.get(pk=id)
    # print("Debug - movie_id: ", movie_id)
    # movie_data = Movie.objects.get(pk=id)
    current_user = request.user
    print(current_user )
    # movie_data.mylist.add(current_user)
    return HttpResponseRedirect(reverse("_details", args=(imdb_id, )))



# def add_watchlist(request, id):
#     Movie.objects.get(pk=id)
#     movie_data = Movie.objects.get(pk=id)
#     current_user = request.user
#     movie_data.watchlist.add(current_user)
#     return HttpResponseRedirect(reverse("listing", args=(id, )))


def remove_mylist(request, id):
    print("Debug - remove_mylist: ", id)
    # return render(request, "movies/remove_mylist.html")


def mylist(request, id):
    print("Debug - mylist: ", id)
    # def add_mylist(request):
    #     return render(request, "movies/add_mylist.html")



def profile(request, user_id):
    # Get profile
    profile = User.objects.get(id=user_id)

    # Check if user follows profile
    if Follow.objects.filter(user=user_id, followed_by=request.user).exists():
        # print("Debug | user is following profile")
        following_status = True
    else:
        # print("Debug | user is NOT following profile")
        following_status = False
   
    # Get list of IDs of people the logged in user follows (Follow objects)
    follow_list = []
    following = request.user._following.all()
    for x in following:
        follow_list.append(x.user.id)
    
    # Gets movies from profile in reverse chronological order
    movies = Movie.objects.filter(user=user_id).order_by("id").reverse()
    # print("Debug | profile's movies: ",movies)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "movies/profile.html", {
        "page_obj": page_obj,
        "viewed_profile": profile.username,
        "viewed_profile_id": user_id,
        "movies": movies,
        "following": profile._following.all().count(),
        "followed_by": Follow.objects.filter(user=user_id).count(),
        "following_status": following_status
    })



def following(request):

    # Gets all profiles user follows
    users_followed = request.user._following.all()
  
    # Make list of IDs
    users_followed_ids = []
    for x in users_followed:
        users_followed_ids.append(x.user.id) # add the user id of the user who clicked

    # print("Debug | User follows: ", users_followed_ids)
    
    # Gets posts from profiles in reverse chronological order
    posts = Movie.objects.filter(author__in=users_followed_ids).order_by("id").reverse()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "movie/following.html", {
        "page_obj": page_obj
    })



def follow(request, user_id):
    # Get user 
    user = User.objects.get(pk=request.user.id)
    print("Debug:", user, type(user), user._following.all())
    
    # Get profile being viewed
    profile = User.objects.get(pk=user_id)
    # print("Debug:", profile, type(profile), profile.following.all())

    # Check if user already follows profile. If so, remove
    if Follow.objects.filter(user=profile, followed_by=user).exists():        
      
        # print("Debug: user currently following profile")
        instance = Follow.objects.filter(user=profile, followed_by=user).get()

        user._following.remove(instance)

        # If empty ManyToMany field, delete relationship
        a = Follow.objects.filter(user=profile)
        for x in a:
            if not x.followed_by.exists():
                x.delete()

        # print("Debug: user no longer following profile")

    else:
        
        # print("Debug: user NOT currently following profile")
        instance = Follow(user=profile)
        instance.save()

        instance.followed_by.add(user)
        # print("Debug: user now following profile")

    return JsonResponse({"message": "Profile successfully followed / unfollowed"}, status=201)
    

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
    return JsonResponse({"message": "Movie successfully edited", "new_text": new_content}, status=201)




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