from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательские права администратора, модератора, автора,
    аутонтифицироанного пользователя.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        ))


class IsAdminSuperuser(permissions.BasePermission):
    """
    Пользовательские права администратора, суперпользователя,
    аутонтифицироанного пользователя.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Пользовательские права администратора, суперпользователя,
    анонима, аутонтифицироанного пользователя.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin
                    or request.user.is_superuser
                )
            )
        )
