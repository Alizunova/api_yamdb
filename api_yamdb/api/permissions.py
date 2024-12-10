from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Ограничение прав доступа для различных пользователей.

    - Безопасные методы (GET, HEAD, OPTIONS) доступны всем.
    - POST доступен только аутентифицированным пользователям.
    - PUT и DELETE доступны автору объекта, модератору или администратору.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated and (
                    request.user == obj.author
                    or request.user.is_moderator
                    or request.user.is_admin
                )
            )
        )


class IsAdminSuperuser(permissions.BasePermission):
    """
    Ограничение прав доступа для администратора и суперпользователя.

    - Доступ разрешен только аутентифицированным пользователям,
      которые являются администраторами или суперпользователями.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Ограничение прав доступа для администраторов и анонимных пользователей.

    - Безопасные методы (GET, HEAD, OPTIONS) доступны всем.
    - Остальные методы доступны только администраторам или суперпользователям.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin)
            )
        )
