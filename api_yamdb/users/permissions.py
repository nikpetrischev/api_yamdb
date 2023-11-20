from rest_framework import permissions


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsModer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return "moderator" == request.user.role


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return "admin" == request.user.role
