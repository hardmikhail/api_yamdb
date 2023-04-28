from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user.is_authenticated
                    and request.user.is_admin)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_admin or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_admin
                    or request.user.is_staff)


class IsModerator(IsUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_moderator)


class IsAdmin(IsUser, IsAdminUser):
    pass


class IsAuthor(IsUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)
