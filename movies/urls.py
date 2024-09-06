from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:profile>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("details/<str:imdbID>", views.details, name="_details"),
    path("profile/<int:user_id>", views.profile, name="_profile"),
    path("top_rated", views.top_rated, name="_top_rated"),
    
    # API routes
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<str:movie_id>", views.like, name="_like"),
    path("add_mylist", views.add_mylist, name="_add_mylist"),
    path("remove_mylist/<str:id>", views.remove_mylist, name="_remove_mylist"),
    path("mylist", views.mylist, name="_mylist"),
    path("add_comment/<int:id>", views.add_comment, name="add-comment")
]
