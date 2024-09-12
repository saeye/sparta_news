from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")