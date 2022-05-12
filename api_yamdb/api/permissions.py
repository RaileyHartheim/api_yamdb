from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """for managing users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """for categories, genres and titles"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class AuthorOrModerOrAdminPermission(permissions.BasePermission):
    """for edit/delete reviews and comments"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_admin
                         or request.user.is_moderator)))
