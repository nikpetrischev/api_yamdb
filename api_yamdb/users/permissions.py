from rest_framework import permissions


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (request.user.is_admin or request.user.is_superuser)
        return False
