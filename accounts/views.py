from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import views, generics
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response

from drf_rw_serializers import generics as rw_generics
from rest_framework_simplejwt import views as simplejwt_views
from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import use_ticket

from .permissions import IsOwner, IsManager
from .models import User, Profile

from .serializers import (
    UserReadSerializer, UserWriteSerializer, ProfileReadSerializer,
    ProfileWriteSerializer, ProfileUnlockSerializer
)


class UserListView(rw_generics.CreateAPIView):

    write_serializer_class = UserWriteSerializer
    read_serializer_class = UserReadSerializer

    permission_classes = [
        HasAPIKey
    ]


class CurrentUserView(rw_generics.RetrieveUpdateDestroyAPIView):

    write_serializer_class = UserWriteSerializer
    read_serializer_class = UserReadSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions
        return permissions + [IsOwner()]

    def get_object(self):
        return self.request.user

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

    permission_classes = [
        HasAPIKey
    ]

    @use_ticket(discard=True, scope='profile')
    def post(self, request, version, ticket_id):
        request.data.update({
            **{'user': self.ticket.user}, **self.ticket.data
        })
        serializer = ProfileWriteSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = ProfileReadSerializer(obj)
        return Response(serializer.data, HTTP_201_CREATED)


class ProfileListView(generics.ListAPIView):

    serializer_class = ProfileReadSerializer

    permission_classes = [
        IsAuthenticated
    ]

    filterset_fields = [
        'role'
    ]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()
        user = self.request.user
        return user.userprofiles.filter(is_active=True)


class ProfileDetailView(rw_generics.RetrieveUpdateDestroyAPIView):

    write_serializer_class = ProfileWriteSerializer
    read_serializer_class = ProfileReadSerializer

    lookup_url_kwarg = 'profile_id'

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    def get_object(self):
        profile_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        try:
            return user.userprofiles.get(id=profile_id)
        except Profile.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProfileUnlockView(views.APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, version, profile_id):
        request.data.update({'id': profile_id})
        serializer = ProfileUnlockSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class ProfileRolesView(views.APIView):

    def get(self, request, version):
        roles = [{'id': k, 'name': v} for k, v in sorted(Profile.ROLE)]
        return Response(roles, HTTP_200_OK)


class CurrentProfileView(views.APIView):

    def get(self, request, version):
        profile = getattr(self.request.user, 'profile', None)
        serializer = ProfileReadSerializer(profile)
        return Response(serializer.data, status=HTTP_200_OK)
