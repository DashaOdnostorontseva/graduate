from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    INN = models.IntegerField(null=True)

