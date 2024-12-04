from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from titles.models import Category, Genre, Title

from .filters import FilterTitle
from .mixins import ListCreateDeleteViewSet
from .permissions import AdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlePostSerializer,
    TitleSerializer,
)


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    Работа с категориями.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly, )


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Работа с жанрами.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly, )


class TitleViewSet(viewsets.ModelViewSet):
    """
    Работа с произведениями.
    """
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('name')
