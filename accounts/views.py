from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt import views as simplejwt_views

from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import use_transaction

from .permissions import (
    IsAuthenticatedAndProfileIsOwner, IsAuthenticatedAndProfileIsManager
)
from .serializers import (
    SignUpSerializer, UserListSerializer, UserDetailSerializer,
    ProfileRequestSerializer, ProfileListSerializer, ProfileDetailSerializer
)

from .models import Profile


class SignUpView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def post(self, request, version):  # skipcq
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = UserListSerializer(obj)
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class CurrentUserDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserDetailSerializer
    permission_classes = [
        IsAuthenticatedAndProfileIsOwner
    ]

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


class ProfileRequestView(generics.CreateAPIView):

    serializer_class = ProfileRequestSerializer
    permission_classes = [
        IsAuthenticatedAndProfileIsManager
    ]


class ProfileCreateView(generics.CreateAPIView):

    serializer_class = ProfileListSerializer
    permission_classes = [
        HasAPIKey
    ]

    @use_transaction(scope='profile', lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj


class ProfileListView(generics.ListAPIView):

    serializer_class = ProfileListSerializer
    permission_classes = [
        IsAuthenticated
    ]
    filterset_fields = [
        'role'
    ]

    def get_queryset(self):
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProfileDetailSerializer
    lookup_url_kwarg = 'profile_id'

    def get_permissions(self):
        permissions = super().get_permissions()
        profile_id = self.kwargs[self.lookup_field]
        profile = self.request.profile
        if profile and profile.id == profile_id:
            return permissions
        return [IsAuthenticatedAndProfileIsManager()]

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
