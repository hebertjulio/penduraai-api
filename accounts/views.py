from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from drf_rw_serializers import generics as rwgenerics
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt import views as simplejwt_views

from .models import User, Profile

from .serializers import (
    UserReadSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileSerializer, ProfileAuthenticateSerializer)


class UserListView(rwgenerics.CreateAPIView):

    read_serializer_class = UserReadSerializer
    write_serializer_class = UserCreateSerializer
    permission_classes = [HasAPIKey]


class UserDetailView(rwgenerics.RetrieveAPIView):

    lookup_field = 'pk'
    queryset = User.objects.filter(is_active=True)
    read_serializer_class = UserReadSerializer


class UserUpdateView(rwgenerics.UpdateAPIView):

    write_serializer_class = UserUpdateSerializer
    read_serializer_class = UserReadSerializer

    def get_object(self):
        user = self.request.user
        return user


class UserDeactivateView(APIView):

    def patch(self, request, *args, **kwargs):
        obj = self.request.user
        obj.is_active = False
        obj.save()
        serializer = UserReadSerializer(obj)
        res = Response(serializer.data, HTTP_200_OK)
        return res


class TokenObtainPairView(simplejwt_views.TokenObtainPairView):

    permission_classes = [HasAPIKey]


class TokenRefreshView(simplejwt_views.TokenRefreshView):

    permission_classes = [HasAPIKey]


class ProfileListView(generics.ListCreateAPIView):

    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs


class ProfileAuthenticateView(APIView):

    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = ProfileAuthenticateSerializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        try:
            pin = request.data['pin']
            user = self.request.user
            profile = user.accountable.get(pin=pin)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, HTTP_200_OK)
        except Profile.DoesNotExist:
            raise PermissionDenied()
