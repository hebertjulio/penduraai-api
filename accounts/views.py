from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from rest_framework_simplejwt import views as simplejwt_views
from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import use_transaction

from .permissions import IsOwner, IsManager
from .serializers import (
    UserSerializer, SignUpSerializer, ProfileSerializer,
    ProfileRequestSerializer, ProfileCreateSerializer
)


class SignUpView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def post(self, request, version):  # skipcq
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = UserSerializer(obj)
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class CurrentUserDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated, IsOwner
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


class ProfileListView(generics.ListAPIView):

    serializer_class = ProfileSerializer
    filterset_fields = [
        'role'
    ]

    def get_queryset(self):
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated, IsManager
    ]

    def get_queryset(self):
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProfileRequestView(generics.CreateAPIView):

    serializer_class = ProfileRequestSerializer
    permission_classes = [
        IsAuthenticated, IsManager
    ]


class ProfileTransactionView(generics.CreateAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileCreateSerializer
    permission_classes = [
        HasAPIKey
    ]

    @use_transaction(scope='profile')
    def create(self, request, *args, **kwargs):  # skipcq
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj
