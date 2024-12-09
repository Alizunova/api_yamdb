from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import FilterTitle
from api.viewsets import ListCreateDeleteViewSet
from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminUserOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDeleteViewSet):
    """Работа с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly, ]


class GenreViewSet(ListCreateDeleteViewSet):
    """Работа с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly, ]


class TitleViewSet(viewsets.ModelViewSet):
    """Работа с произведениями."""

    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    permission_classes = [IsAdminUserOrReadOnly, ]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    ordering_fields = ['name', 'year', 'rating']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    """Работа с отзывами на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
