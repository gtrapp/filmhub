from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Movie(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    imdb_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    poster = models.CharField(max_length=1000)
    type = models.CharField(max_length=100)
    mylist = models.ManyToManyField(User, blank=True, related_name='_mylist')

    def __str__(self):
        return f"{self.title} ({self.year})"
    

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_user")
    followed_by = models.ManyToManyField(User, blank=True, related_name="_following")

    def __str__(self):
        return f"{self.user} is followed by: {self.followed_by}"