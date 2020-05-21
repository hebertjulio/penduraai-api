from rest_framework.status import HTTP_200_OK
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework_api_key.permissions import HasAPIKey

from rest_framework_simplejwt import views as simplejwt_views

from .models import User, Profile
from .serializers import (
    UserSerializer, ProfileSerializer, ProfileAuthenticateSerializer)


class UserListView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = [HasAPIKey]


class UserDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class UserChangeView(generics.UpdateAPIView):

    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user


class UserDeactivateView(APIView):

    def patch(self, request, *args, **kwargs):
        obj = self.request.user
        obj.is_active = False
        obj.save()
        serializer = UserSerializer(obj)
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
        serializer = ProfileAuthenticateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        pin = request.data['pin']
        try:
            obj = self.request.user.profiles_accountable.get(pin=pin)
            serializer = ProfileSerializer(obj)
            res = Response(serializer.data, HTTP_200_OK)
            return res
        except Profile.DoesNotExist:
            pass
        raise exceptions.PermissionDenied()
