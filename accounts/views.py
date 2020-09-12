from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import views, generics
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from drf_rw_serializers import generics as rw_generics

from rest_framework_simplejwt import views as simplejwt_views

from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import use_ticket

from .serializers import (
    UserReadSerializer, UserWriteSerializer, ProfileReadSerializer,
    ProfileWriteSerializer
)

from .models import User, Profile
from .permissions import IsOwner, IsManager


class UserListView(rw_generics.CreateAPIView):

    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer

    permission_classes = [
        HasAPIKey
    ]


class CurrentUserDetailView(rw_generics.RetrieveUpdateDestroyAPIView):

    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsOwner()]

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


class ProfileConfirmView(views.APIView):

    @use_ticket(discard=True, scope='profile')
    def post(self, request, version, token):
        data = request.data
        data.update({**{'user': self.ticket.user}, **self.ticket.data})
        context = {'request': request}
        serializer = ProfileWriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = ProfileReadSerializer(obj)
        return Response(serializer.data, HTTP_201_CREATED)


class ProfileListView(generics.ListAPIView):

    read_serializer_class = ProfileReadSerializer
    write_serializer_class = ProfileWriteSerializer

    permission_classes = [
        IsAuthenticated
    ]

    filterset_fields = [
        'role'
    ]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'POST':
            return [HasAPIKey()]
        return permissions

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs


class ProfileDetailView(rw_generics.RetrieveUpdateDestroyAPIView):

    read_serializer_class = ProfileReadSerializer
    write_serializer_class = ProfileWriteSerializer

    lookup_url_kwarg = 'profile_id'

    def get_permissions(self):
        permissions = super().get_permissions()
        profile_id = self.kwargs[self.lookup_url_kwarg]
        profile = self.request.profile
        if profile and profile.id == profile_id:
            return permissions
        permissions += [IsManager()]
        return permissions

    def get_object(self):
        profile_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        try:
            obj = user.userprofiles.get(id=profile_id)
            return obj
        except Profile.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
