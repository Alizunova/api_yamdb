from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Права доступа для разных пользователей.

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
    Права доступа для администратора и суперпользователя.

    Разрешает доступ только аутентифицированным пользователям,
    которые являются администраторами или суперпользователями.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Права доступа для администраторов и анонимных пользователей.

    - Безопасные методы доступны всем.
    - Остальные методы доступны только администраторам
      или суперпользователям.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )
