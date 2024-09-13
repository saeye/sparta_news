from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    username = models.CharField(max_length=30, unique=True)# unique=True
    email = models.EmailField(unique=True)# unique=True
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    point = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    confirmkey = models.CharField(max_length=50)
    # expired_date = models.DateTimeField()
    # def __init__(self, *args, **kwargs):
    #     expired_date = timezone.now() + timedelta(days=1)