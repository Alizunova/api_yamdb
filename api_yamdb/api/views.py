from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.filters import FilterTitle
from api.mixins import ListCreateDeleteViewSet
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
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):
    """Работа с жанрами."""
    
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Работа с произведениями."""
    
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['GET', 'POST', 'PATCH', 'DELETE']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    """Работа с отзывами на произведения."""
    
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями."""
    
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly
    )
    
    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,review=self.get_review())

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
