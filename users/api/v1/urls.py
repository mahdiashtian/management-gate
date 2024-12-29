from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from users.api.api_views import UserViewSet, TokenBlacklistView, TokenRefreshView, TokenObtainPairView, RoomViewSet

app_name = 'user'

routers = DefaultRouter()
routers.register(r'users', UserViewSet, basename='user')
routers.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    re_path(r"^auth/jwt/create/?", TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^auth/jwt/refresh/?", TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^auth/jwt/verify/?", TokenVerifyView.as_view(), name="jwt-verify"),
    re_path(r"^auth/jwt/logout/?", TokenBlacklistView.as_view(), name="jwt-logout"),

    path("", include(routers.urls)),
]
