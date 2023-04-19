from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        default='user'
    )
    password = None
