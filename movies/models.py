from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_user")
    imdb_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    poster = models.CharField(max_length=1000)
    type = models.CharField(max_length=100)
    imdb_rating = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_user")
    followed_by = models.ManyToManyField(User, blank=True, related_name="_following")

    def __str__(self):
        return f"{self.user} is followed by: {self.followed_by}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="_user_comment")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True, related_name="_movie_comment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.movie}"