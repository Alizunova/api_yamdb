from api.permissions import (IsAdminModeratorAuthorOrReadOnly,
                        IsAdminUserOrReadOnly)
from rest_framework import permissions, viewsets

class TitleViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAdminUserOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly)
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly)