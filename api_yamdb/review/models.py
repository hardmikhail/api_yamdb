from django.db import models
from django.contrib.auth.models import AbstractUser

from api.permissions import IsUser, IsModerator, IsAdmin


ROLE_CHOICES = [
        ('user', IsUser),
        ('moderator', IsModerator),
        ('admin', IsAdmin)
    ]

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        null=True,
        blank=True,
        default='admin',
    )
    password = None
