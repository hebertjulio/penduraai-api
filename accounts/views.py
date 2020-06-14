from rest_framework import generics

from rest_framework_simplejwt import views as simplejwt_views
from drf_rw_serializers import generics as rwgenerics
from rest_framework_api_key.permissions import HasAPIKey

from .permissions import IsOwner, CanManage

from .serializers import (
    UserReadSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileSerializer)


class UserListView(rwgenerics.CreateAPIView):

    read_serializer_class = UserReadSerializer
    write_serializer_class = UserCreateSerializer
    permission_classes = [
        HasAPIKey
    ]


class CurrentUserDetailView(rwgenerics.RetrieveUpdateDestroyAPIView):

    write_serializer_class = UserUpdateSerializer
    read_serializer_class = UserReadSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsOwner()]
        return permissions

    def get_object(self):
        user = self.request.user
        return user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TokenObtainPairView(simplejwt_views.TokenObtainPairView):

    permission_classes = [
        HasAPIKey
    ]


class TokenRefreshView(simplejwt_views.TokenRefreshView):

    permission_classes = [
        HasAPIKey
    ]


class ProfileListView(generics.ListCreateAPIView):

    serializer_class = ProfileSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanManage()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = user.profiles.filter(is_active=True)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanManage()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = user.profiles.filter(is_active=True)
        return qs
