from rest_framework import permissions


class IsUser(permissions.IsAuthenticated):
    pass


class IsModerator():
    pass


class IsAdmin(permissions.IsAdminUser):
    pass
