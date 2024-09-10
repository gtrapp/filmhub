from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_user")
    imdb_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    poster = models.CharField(max_length=1000)
    type = models.CharField(max_length=100)
    rated = models.CharField(max_length=10)
    runtime = models.CharField(max_length=10)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    plot = models.CharField(max_length=1000)
    genre = models.CharField(max_length=100)
    awards = models.CharField(max_length=100)
    metascore = models.CharField(max_length=10)
    imdb_rating = models.CharField(max_length=10)
    is_bookmarked = models.BooleanField(default=True)
    my_list = models.ManyToManyField(User, blank=True, null=True, related_name="_movie_mylist")
    
    def __str__(self):
        return f"{self.user} {self.imdb_id} {self.title} {self.year} {self.poster} {self.type} {self.rated} {self.runtime} {self.director} {self.actors} {self.plot} {self.genre} {self.awards} {self.metascore} {self.imdb_rating}"
    

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_user")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_following")

    def __str__(self):
        return f"{self.user} is followed by: {self.followed_by}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True, related_name="_movie_comment")
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return f"{self.author} comment on {self.movie}: {self.message}"