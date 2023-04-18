from rest_framework import permissions


class IsUser(permissions.IsAuthenticated):
    pass


class IsModerator(IsUser):
    pass


class IsAdmin(permissions.IsAdminUser):
    pass
