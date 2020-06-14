from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from drf_rw_serializers import generics as rwgenerics
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt import views as simplejwt_views

from .models import User, Profile
from .permissions import IsOwner, IsAdmin

from .serializers import (
    UserReadSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileSerializer)


class UserListView(rwgenerics.CreateAPIView):

    read_serializer_class = UserReadSerializer
    write_serializer_class = UserCreateSerializer
    permission_classes = [
        HasAPIKey
    ]


class UserDetailView(rwgenerics.RetrieveAPIView):

    lookup_field = 'pk'
    queryset = User.objects.filter(is_active=True)
    read_serializer_class = UserReadSerializer


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
        permissions += [IsAdmin()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsAdmin()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs
