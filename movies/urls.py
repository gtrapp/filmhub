from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:profile>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("details/<str:id>", views.details, name="_details"),
    
    # API routes
    path("like/<str:movie_id>", views.like, name="_like"),
    path("add_mylist", views.add_mylist, name="_add_mylist"),
    path("remove_mylist/<str:id>", views.remove_mylist, name="_remove_mylist"),
    path("mylist", views.mylist, name="_mylist"),

]
