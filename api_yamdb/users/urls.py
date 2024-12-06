from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import get_token, signup, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

auth_urls = [
    path('token/', get_token, name='token'),
    path('signup/', signup, name='signup'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router.urls)),
]
