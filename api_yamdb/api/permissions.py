from rest_framework import permissions
# Аноним- только для чтения
# Аутонтифицированный пользователь, если он автор или модератор или админ
# может все.
# если разрешены безопасные методы- Пост запрос разрешен аутентифицированному
# пользователю, если он не автор
# Доступ на уровне получения объекта
class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):

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


# Доступ на уровне запроса пользователя
class IsAdminSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )

#  разрешены безопасные запросы или это авторизован пользователь или админ
class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)
