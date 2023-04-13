from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=150, null=True, blank=True)
    password = None
