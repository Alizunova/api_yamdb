from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_jwt_token, signup

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/auth/signup/', signup),
    path('v1/', include(router.urls)),
]
