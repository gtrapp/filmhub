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

    # API routes
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/<str:movie_id>", views.like, name="_like"),
    path("add_mylist", views.add_mylist, name="_add_mylist"),
    path("remove_mylist", views.remove_mylist, name="_remove_mylist"),
    path("add_comment/<int:id>", views.add_comment, name="add-comment"),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like-comment'),
]

