from django_filters.rest_framework import DjangoFilterBackend
from config.permissions import IsSuperUser, IsCurrentUser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from users.api.v1.serializers import UserSerializer, ChangePasswordSerializer, UserCreateSerializer
from users.models import User
from users.security import set_jwt_cookies, set_jwt_access_cookie, unset_jwt_cookies


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']
    filterset_fields = ['is_staff', 'is_superuser', 'is_active', 'role']
    ordering_fields = ['id']

    @action(methods=['get'], detail=False, url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='change-password', url_name='change-password')
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'پسورد با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        creator = self.request.user
        if creator and creator.is_superuser:
            super().perform_create(serializer)
        else:
            serializer.save(is_staff=False, is_superuser=False, is_active=False)

    def perform_update(self, serializer):
        updater = self.request.user
        instance = self.get_object()
        if updater and updater.is_superuser:
            super().perform_update(serializer)
        else:
            serializer.save(is_staff=instance.is_staff, is_superuser=instance.is_superuser,
                            is_active=instance.is_active)

    def get_serializer_class(self):
        if self.action == 'change_password':
            self.serializer_class = ChangePasswordSerializer
        elif self.action == 'create':
            self.serializer_class = UserCreateSerializer
        else:
            self.serializer_class = UserSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated & (IsCurrentUser | IsSuperUser)]
        elif self.action in ['me', 'change_password']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated & IsSuperUser]
        return super().get_permissions()


class TokenObtainPairView(jwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        set_jwt_cookies(response, access_token, refresh_token)
        return response


class TokenRefreshView(jwt_views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data['access']
        set_jwt_access_cookie(response, access_token)
        return response


class TokenBlacklistView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(data={'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        unset_jwt_cookies(response)
        return response
