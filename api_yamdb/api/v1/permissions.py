from rest_framework import permissions


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if view.action == 'partial_update' or view.action == 'destroy':
            return (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        return request.user.is_authenticated
