from rest_framework import permissions


class IsUser(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    or request.method in permissions.SAFE_METHODS)


class IsModerator(IsUser):
    pass


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.role == 'admin'
                    or request.user.is_superuser)
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))
