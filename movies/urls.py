from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("profile/<int:user_id>", views.profile, name="_profile"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("details/<str:imdb_id>", views.details, name="_details"),
  
    path("top_rated", views.top_rated, name="_top_rated"),

    # path('get_video/', views.get_video, name='_get_video'),
    # path("popular", views.popular, name="_popular"),
    # path("movie/<str:imdb_id>", views.movie, name="_movie"),
    # path("upcoming", views.upcoming, name="_upcoming"),
    # path("now_playing", views.now_playing, name="_now_playing"),
    
    # API routes
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),

    path("like/<str:movie_id>", views.like, name="_like"),
    path("add_mylist", views.add_mylist, name="_add_mylist"),
    path("remove_mylist/<str:id>", views.remove_mylist, name="_remove_mylist"),
    path("mylist", views.mylist, name="_mylist"),
    path("add_comment/<int:id>", views.add_comment, name="add-comment"),
    path("watchlist", views.watchlist, name="watchlist")
]

