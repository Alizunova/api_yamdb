from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from api.permissions import IsAdminUserOrReadOnly


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Базовый вьюсет:

    - Возвращает список объектов (GET).
    - Создает объект (POST).
    - Удаляет объект (DELETE).

    Особенности:
    - Поддерживает пагинацию, фильтрацию и права доступа.
    """

    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    lookup_field = 'id'
    permission_classes = [AllowAny]
