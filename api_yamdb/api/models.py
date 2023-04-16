from django.db import models
from django.contrib.auth.models import AbstractUser

from .permissions import IsUser, IsModerator, IsAdmin

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(null=True, blank=True)
    ROLE_CHOICES = [
        (IsUser, 'user'),
        (IsModerator, 'moderator'),
        ('admin', IsAdmin)
    ]
    role = models.CharField(max_length=150, choices=ROLE_CHOICES, null=True, blank=True)
    password = None
